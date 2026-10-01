"""Strict S2 identity, routing, confidentiality and weighted inert traces."""
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
from notebook_contract import (ContractError, WRONG_VERSION, S2_QUESTION_COUNTS,
                               resolve_notebook, strict_contract_identity)
from s2_revision import check_s2
from s1_revision import collect


def fixture(evaluator='td3-S2'):
    identity = {'cell_type': 'code', 'metadata': {'tal': {
        'question': 'identity', 'role': 'identification'}}, 'outputs': [],
        'source': 'nom="Essai"\nprenom="Alex"\nclasse="G2"\nnumero_etudiant="SYN-01"'}
    answers = [{'cell_type': 'code', 'metadata': {'tal': {
        'question': f'Q{q}', 'role': 'answer'}}, 'source': '', 'outputs': []}
        for q in range(1, S2_QUESTION_COUNTS[evaluator] + 1)]
    return {'metadata': {'tal': {'id': evaluator, 'evaluator': evaluator, 'version': 2}},
            'cells': [identity] + answers}


class S2Contracts(unittest.TestCase):
    def test_all_six_complete_contracts_and_literal_identity(self):
        for evaluator in S2_QUESTION_COUNTS:
            nb = fixture(evaluator)
            self.assertEqual(strict_contract_identity(nb)['numero_etudiant'], 'SYN-01')
            nb['cells'].reverse()
            self.assertEqual(resolve_notebook(nb)['evaluator'], evaluator)
            for mutate in ('missing', 'duplicate', 'wrong_question', 'markdown'):
                broken = fixture(evaluator)
                if mutate == 'missing': broken['cells'].pop()
                elif mutate == 'duplicate': broken['cells'].append(copy.deepcopy(broken['cells'][1]))
                elif mutate == 'wrong_question': broken['cells'][1]['metadata']['tal']['question'] = 'Q999'
                else: broken['cells'][1]['cell_type'] = 'markdown'
                with self.subTest(evaluator=evaluator, mutate=mutate), self.assertRaisesRegex(ContractError, '^' + WRONG_VERSION + '$'):
                    strict_contract_identity(broken)
        nb = fixture()
        for source in ('nom="A"\nprenom="B"\nclasse="G2"',
                       'nom="A"\nprenom="B"\nclasse="G2"\nnumero_etudiant=guess()',
                       nb['cells'][0]['source'] + '\nnumero_etudiant="AUTRE"'):
            nb['cells'][0]['source'] = source
            with self.assertRaises(ContractError): strict_contract_identity(nb)

    def test_weighted_saved_values_are_typed_and_inert(self):
        nb = fixture()
        nb['cells'][1].update(source='raise RuntimeError("NEVER_EXECUTE")\nprint("Résultat Q1 :", 3)',
            outputs=[{'output_type': 'stream', 'name': 'stdout', 'text': 'Résultat Q1 : 3\n'}])
        # We intentionally do not ask for a syntax objective here: recorded
        # values are not certified executions, and no statement is run.
        checks = [{'label': 'Valeur', 'traces': {'Q1': (3,)}, 'points': 2.5,
                   'feedback': 'Valeur entière.'}]
        result = check_s2(json.dumps(nb), 'copy.ipynb', 'td3-S2', checks)
        self.assertEqual((result[0], result[2], result[4]), (2.5, 2.5, None))
        self.assertEqual(result[1][0]['max_points'], 2.5)
        nb['cells'][1]['outputs'][0]['text'] = 'Résultat Q1 : True\n'
        self.assertEqual(check_s2(json.dumps(nb), 'copy.ipynb', 'td3-S2', checks)[0], 0)
        nb['metadata']['tal']['version'] = 1
        rejected = check_s2(json.dumps(nb), 'copy.ipynb', 'td3-S2', checks)
        self.assertEqual((rejected[1], rejected[3], rejected[4]), ([], {}, WRONG_VERSION))

    def test_file_proof_follows_nominal_try_and_not_except_decoys(self):
        nb = fixture()
        answer = nb['cells'][1]
        answer['source'] = ('try:\n with open("never-open-this.txt", encoding="utf-8") as fichier:\n'
                            '  resultat=fichier.read()\nexcept OSError:\n resultat=""\n'
                            'print("Résultat Q1 :", resultat)')
        sources, _ = collect(nb)
        proof = sources['Q1'][0][1]
        self.assertTrue(proof.calls('open'))
        self.assertTrue(proof.calls('read'))
        answer['source'] = ('try:\n resultat="inventé"\nexcept OSError:\n'
                            ' with open("never-open-this.txt", encoding="utf-8") as fichier:\n'
                            '  resultat=fichier.read()\nprint("Résultat Q1 :", resultat)')
        sources, _ = collect(nb)
        self.assertFalse(sources['Q1'][0][1].calls('open'))
        self.assertFalse(sources['Q1'][0][1].calls('read'))


class S2Routes(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        patcher = patch.object(outils, 'BASE_DIR', self.temp.name)
        patcher.start(); self.addCleanup(patcher.stop)
        self.client = create_app().test_client()
        self.checker = Mock(return_value=(2, [{'check': 'PRIVATE_CRITERION',
            'student_answer': '<script>PRIVATE_TRACE</script>', 'correct_answer': 'PRIVATE_EXPECTED',
            'status': 'ok', 'points': 2, 'max_points': 2}], 20,
            {'nom': 'WRONG', 'prenom': 'WRONG', 'classe': 'WRONG',
             'score_nature': 'technique_provisoire', 'score_max': 20,
             'relecture_humaine': 'requise'}, None))
        module = SimpleNamespace(check_notebook=self.checker, HUMAN_REVIEW='PRIVATE_REVIEW',
                                 HUMAN_REVIEW_DIMENSIONS=['Raisonnement algorithmique'])
        importer = patch.object(routes, 'import_module', return_value=module)
        importer.start(); self.addCleanup(importer.stop)

    def post(self, nb, path='/submit'):
        return self.client.post(path, data={'file': (io.BytesIO(json.dumps(nb).encode()), 'copy.ipynb')})

    def test_bad_versions_and_missing_identity_never_grade_or_persist(self):
        for evaluator in S2_QUESTION_COUNTS:
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

    def test_versioned_storage_unique_numbers_private_control_reports(self):
        for evaluator in S2_QUESTION_COUNTS:
            historical = Path(self.temp.name) / evaluator / 'G2' / 'historical.csv'
            historical.parent.mkdir(parents=True); historical.write_text('old header\nold grade\n')
            for number in ('SYN-01', '_SYN-01'):
                nb = fixture(evaluator)
                nb['cells'][0]['source'] = nb['cells'][0]['source'].replace('"SYN-01"', repr(number))
                body = self.post(nb).get_data(as_text=True)
                if routes.EVALUATOR_MODES[evaluator] == 'controle':
                    self.assertIn('Copie reçue et enregistrée', body)
                    for private in ('PRIVATE_CRITERION', 'PRIVATE_TRACE', 'PRIVATE_EXPECTED', 'PRIVATE_REVIEW', 'Score technique provisoire'):
                        self.assertNotIn(private, body)
            folder = Path(self.temp.name) / (evaluator + '-v2') / 'G2'
            self.assertEqual(len(list(folder.rglob('*.ipynb'))), 2)
            self.assertEqual(len(list(folder.rglob('*.html'))), 2)
            for report in folder.rglob('*.html'):
                text = report.read_text()
                self.assertNotIn('<script>PRIVATE_TRACE</script>', text)
                self.assertIn('PRIVATE_CRITERION', text)
            with next(folder.glob('*.csv')).open() as handle:
                rows = list(csv.reader(handle, delimiter=';'))
            self.assertEqual(len(rows), 3)
            self.assertTrue(all(len(row) == len(rows[0]) for row in rows))
            self.assertEqual([row[-1] for row in rows[1:]], ['SYN-01', '_SYN-01'])
            self.assertEqual(historical.read_text(), 'old header\nold grade\n')


if __name__ == '__main__': unittest.main()
