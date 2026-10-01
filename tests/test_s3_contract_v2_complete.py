"""All S3 contracts refuse incompatible or unidentified copies before grading."""
import copy
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from app import create_app
import outils
import routes
from notebook_contract import (ContractError, WRONG_VERSION, S3_QUESTION_COUNTS,
                               load_catalog, resolve_notebook, s3_contract_identity)


def fixture(evaluator):
    identity = {'cell_type': 'code', 'metadata': {'tal': {
        'question': 'identity', 'role': 'identification'}}, 'outputs': [],
        'source': '# nom="Commentaire"\nprenom="Alice"\nnom="Dupont"\nclasse="G1"\nnumero_etudiant="E1"'}
    answers = [{'cell_type': 'code', 'metadata': {'tal': {
        'question': f'Q{q}', 'role': 'answer'}}, 'source': '', 'outputs': []}
        for q in range(1, S3_QUESTION_COUNTS[evaluator] + 1)]
    return {'metadata': {'tal': {'id': evaluator, 'evaluator': evaluator, 'version': 2}},
            'cells': [identity] + answers}


class StrictS3Contracts(unittest.TestCase):
    def test_catalog_and_complete_contracts(self):
        entries = [e for e in load_catalog() if e['semester'] == 'S3' and e['active']]
        self.assertEqual({e['evaluator'] for e in entries}, set(S3_QUESTION_COUNTS))
        self.assertEqual(len(entries), 18)
        for entry in entries:
            self.assertEqual(entry['version'], 2)
            nb = fixture(entry['evaluator'])
            nb['cells'].reverse()
            nb['cells'].append({'cell_type': 'code', 'source': 'raise RuntimeError("NEVER_RUN")', 'metadata': {}})
            self.assertEqual(s3_contract_identity(nb)['nom'], 'Dupont')

    def test_bad_cell_contracts_are_wrong_version(self):
        for evaluator in S3_QUESTION_COUNTS:
            variants = []
            nb = fixture(evaluator); nb['cells'].pop(); variants.append(nb)
            nb = fixture(evaluator); nb['cells'].pop(0); variants.append(nb)
            nb = fixture(evaluator)
            for cell in nb['cells']: cell['metadata'] = {}
            variants.append(nb)
            nb = fixture(evaluator); nb['cells'].append(copy.deepcopy(nb['cells'][1])); variants.append(nb)
            nb = fixture(evaluator); nb['cells'][1]['cell_type'] = 'markdown'; variants.append(nb)
            nb = fixture(evaluator); nb['cells'][1]['metadata']['tal']['question'] = 'Q999'; variants.append(nb)
            for nb in variants:
                with self.subTest(evaluator=evaluator, nb=nb), self.assertRaisesRegex(ContractError, '^' + WRONG_VERSION + '$'):
                    resolve_notebook(nb)

    def test_identity_is_exact_literal_and_unambiguous(self):
        nb = fixture('td0-s3')
        identity = s3_contract_identity(nb)
        self.assertEqual(identity, {'nom': 'Dupont', 'prenom': 'Alice', 'classe': 'G1', 'numero_etudiant': 'E1'})
        self.assertEqual(outils.extract_identification_info(nb['cells'])['nom'], 'Dupont')
        base = nb['cells'][0]['source']
        for suffix in ['\nnom="Autre"', '\nnom=build_name()', '\nnumero_etudiant="../E1"', '\nnumero_etudiant=""']:
            nb['cells'][0]['source'] = base + suffix
            with self.assertRaises(ContractError): s3_contract_identity(nb)
        for field in ['nom', 'prenom', 'classe', 'numero_etudiant']:
            nb = fixture('td0-s3')
            nb['cells'][0]['source'] = '\n'.join(line for line in nb['cells'][0]['source'].splitlines() if not line.startswith(field + '='))
            with self.assertRaises(ContractError): s3_contract_identity(nb)
        self.assertFalse(outils.check_identification({'nom': '', 'prenom': 'Alice', 'classe': 'G1'}))

    def test_revision_direct_api_uses_same_identity_gate(self):
        from revision_s3 import check_revision
        for evaluator in ('td-r0-s3', 'td-r1-s3', 'td-r2-s3'):
            nb = fixture(evaluator)
            nb['cells'][0]['source'] += '\nnom="Duplicate"'
            result = check_revision(json.dumps(nb), evaluator)
            self.assertEqual(result[1], [])
            self.assertIn('seule affectation', result[4])


class StrictS3Routes(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        patcher = patch.object(outils, 'BASE_DIR', self.temp.name)
        patcher.start(); self.addCleanup(patcher.stop)
        self.client = create_app().test_client()
        # The route must trust gated identity, not a legacy checker's incomplete data.
        self.checker = Mock(return_value=(0, [], 7, {'nom': 'WRONG', 'prenom': 'WRONG',
            'classe': 'WRONG', 'score_nature': 'technique_provisoire', 'score_max': 7,
            'relecture_humaine': 'À relire'}, None))
        importer = patch.object(routes, 'import_module', return_value=SimpleNamespace(check_notebook=self.checker))
        importer.start(); self.addCleanup(importer.stop)

    def post(self, nb, path):
        return self.client.post(path, data={'file': (io.BytesIO(json.dumps(nb).encode()), 'copy.ipynb')})

    def test_all_versions_metadata_and_empty_identities_reject_before_grading(self):
        for evaluator in S3_QUESTION_COUNTS:
            variants = []
            for version in (None, 1, True, '2', 3):
                nb = fixture(evaluator)
                if version is None: nb['metadata'] = {}
                else: nb['metadata']['tal']['version'] = version
                variants.append((nb, WRONG_VERSION))
            nb = fixture(evaluator); nb['cells'][1]['metadata'] = {}; variants.append((nb, WRONG_VERSION))
            nb = fixture(evaluator); nb['cells'][0]['source'] = 'nom=""'; variants.append((nb, 'Complétez'))
            for nb, message in variants:
                for path in ('/submit', '/eval/' + evaluator):
                    with self.subTest(evaluator=evaluator, path=path, message=message):
                        self.assertIn(message, self.post(nb, path).get_data(as_text=True))
        self.checker.assert_not_called()
        self.assertEqual(list(Path(self.temp.name).rglob('*')), [])

    def test_all_homonyms_have_distinct_copies_reports_and_versioned_csv(self):
        for evaluator in S3_QUESTION_COUNTS:
            historical = Path(self.temp.name) / evaluator / 'G1' / 'historical.csv'
            historical.parent.mkdir(parents=True)
            historical.write_text('old header\nold grade\n')
            for number in ('E1', '_E1'):
                nb = fixture(evaluator)
                nb['cells'][0]['source'] = nb['cells'][0]['source'].replace('"E1"', repr(number))
                body = self.post(nb, '/submit').get_data(as_text=True)
                if evaluator.startswith('controle-'):
                    self.assertIn('Copie reçue et enregistrée', body)
                    self.assertNotIn('Score technique provisoire', body)
            folder = Path(self.temp.name) / (evaluator + '-v2') / 'G1'
            self.assertEqual(len(list(folder.rglob('*.ipynb'))), 2)
            self.assertEqual(len(list(folder.rglob('*.html'))), 2)
            for path in folder.rglob('*.ipynb'):
                self.assertTrue(path.name.startswith('DUPONT_Alice_'))
            with next(folder.glob('*.csv')).open() as handle:
                rows = list(csv.reader(handle, delimiter=';'))
            self.assertEqual(len(rows), 3)
            self.assertTrue(all(len(row) == len(rows[0]) for row in rows))
            self.assertEqual([row[-1] for row in rows[1:]], ['E1', '_E1'])
            self.assertEqual(historical.read_text(), 'old header\nold grade\n')


if __name__ == '__main__': unittest.main()
