"""An explicitly registered ungraded subject can be submitted without a fake score."""
import copy
import csv
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from app import create_app
import human_review_submission as human
import outils
import prepare_student_notebooks as prep
import routes
from notebook_contract import ContractError, load_catalog, resolve_notebook, human_review_identity
from test_notebook_contract import notebook as automatic_notebook


def notebook():
    identity = {'cell_type': 'code', 'metadata': {'tal': {'question': 'identity', 'role': 'identification'}},
                'source': 'nom="Exemple"\nprenom="Test"\nclasse="S3"\nnumero_etudiant="E1"', 'outputs': []}
    answers = [{'cell_type': 'code', 'id': f'answer-q{q}',
                'metadata': {'tal': {'question': f'Q{q}', 'role': 'answer'}},
                'source': 'raise RuntimeError("NEVER_EXECUTE")\n# <script>alert(1)</script>',
                'outputs': [{'output_type': 'display_data', 'data': {
                    'text/plain': '<img src=x onerror=alert(1)>',
                    'text/html': '<script>UNTRUSTED_HTML</script>'}}]} for q in range(1, 5)]
    return {'nbformat': 4, 'nbformat_minor': 5, 'metadata': {'tal': {
        'id': 'td1b-s3', 'evaluator': None, 'version': 2}}, 'cells': [identity, *answers]}


class HumanReviewContractTests(unittest.TestCase):
    def test_catalog_strictly_separates_manual_and_automatic_assessment(self):
        catalog = load_catalog()
        manual = [entry for entry in catalog if entry.get('assessment') == 'human_review']
        self.assertEqual([entry['id'] for entry in manual], ['td1b-s3'])
        self.assertIsNone(manual[0]['evaluator'])
        self.assertTrue(manual[0]['active'])
        routes.validate_evaluator_semesters()
        self.assertEqual(len(routes.EVALUATORS), 33)
        self.assertEqual(resolve_notebook(notebook())['assessment'], 'human_review')
        self.assertEqual(human_review_identity(notebook())['numero_etudiant'], 'E1')

    def test_catalog_refuses_manual_flag_on_an_existing_corrector(self):
        original = {'schema_version': 1, 'notebooks': load_catalog()}
        for edits in ({'assessment': 'human_review'}, {'assessment': 'unknown'}):
            data = copy.deepcopy(original)
            data['notebooks'][0].update(edits)
            with patch('notebook_contract.Path.read_text', return_value=json.dumps(data)):
                with self.assertRaises(ValueError):
                    load_catalog()
        for edits in ({'evaluator': 'td1b-s3'}, {'version': 1}, {'active': False}, {'assessment': 'automatic'}):
            data = copy.deepcopy(original)
            next(entry for entry in data['notebooks'] if entry['id'] == 'td1b-s3').update(edits)
            with patch('notebook_contract.Path.read_text', return_value=json.dumps(data)):
                with self.assertRaises(ValueError):
                    load_catalog()

    def test_old_or_malformed_cell_contracts_refused(self):
        variants = [{'cells': []}]
        for change in ('old', 'missing_identity', 'missing_answer', 'duplicate', 'extra', 'markdown', 'invalid_metadata'):
            nb = notebook()
            if change == 'old': nb['metadata']['tal']['version'] = 1
            elif change == 'missing_identity': nb['cells'].pop(0)
            elif change == 'missing_answer': nb['cells'].pop()
            elif change == 'duplicate': nb['cells'].append(copy.deepcopy(nb['cells'][1]))
            elif change == 'extra': nb['cells'][1]['metadata']['tal']['question'] = 'Q9'
            elif change == 'markdown': nb['cells'][1]['cell_type'] = 'markdown'
            else: nb['cells'][1]['metadata'] = []
            variants.append(nb)
        for nb in variants:
            with self.subTest(nb=nb), self.assertRaisesRegex(ContractError, '^mauvaise version du notebook$'):
                resolve_notebook(nb)
        with self.assertRaises(ContractError):
            resolve_notebook(notebook(), expected_evaluator='td1-s3')
        nb = notebook(); nb['cells'][0]['source'] += '\nnumero_etudiant="../../oops"'
        with self.assertRaises(ContractError): human_review_identity(nb)

    def test_upload_cannot_choose_manual_assessment(self):
        nb = automatic_notebook()
        nb['metadata']['tal']['assessment'] = 'human_review'
        self.assertNotEqual(resolve_notebook(nb).get('assessment'), 'human_review')
        nb['metadata']['tal']['evaluator'] = None
        with self.assertRaises(ContractError): resolve_notebook(nb)

    def test_companion_distribution_retains_metadata_tutor_and_only_injects_url(self):
        entry = next(entry for entry in load_catalog() if entry['id'] == 'td1b-s3')
        source = ROOT / entry['notebook']
        original = json.loads(source.read_text())
        self.assertEqual(resolve_notebook(original)['id'], entry['id'])
        self.assertEqual(original['cells'][-1], prep.submission_cell())
        with tempfile.TemporaryDirectory() as temporary, patch.object(prep, 'load_catalog', return_value=[entry]):
            output = Path(temporary) / 'dist'
            self.assertEqual(prep.render(output, 'https://example.test/course'), 1)
            self.assertEqual(prep.verify_rendered(output, 'https://example.test/course'), 1)
            rendered = json.loads((output / entry['notebook']).read_text())
        self.assertEqual(json.loads(source.read_text()), original)
        self.assertEqual(rendered['cells'][:-1], original['cells'][:-1])
        self.assertEqual(rendered['metadata'], original['metadata'])
        self.assertNotIn(prep.URL_PLACEHOLDER, json.dumps(rendered))


class HumanReviewRoutesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(); self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        base = patch.object(outils, 'BASE_DIR', str(self.root)); base.start(); self.addCleanup(base.stop)
        self.app = create_app(); self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def post(self, nb):
        return self.client.post('/submit', data={'file': (io.BytesIO(json.dumps(nb).encode()), '../../copy.ipynb')})

    def test_manual_receipt_saves_original_escaped_report_and_ungraded_log(self):
        nb = notebook()
        nb['cells'].append({'cell_type': 'markdown', 'id': 'bilan', 'metadata': {
            'tal': {'question': 'practice-bilan', 'role': 'practice'},
            'tal_review': {'question': 'bilan'}}, 'source': 'BILAN_PERSONNEL <script>'})
        nb['cells'][0]['source'] = 'nom="=2+2"\nprenom="<script>"\nclasse="../../S3"\nnumero_etudiant="E1"'
        with patch.object(routes, 'import_module') as importer, patch.object(outils, 'log_grade_to_csv') as grades:
            response = self.post(nb)
        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn('reçu pour relecture enseignante ; aucune note automatique', body)
        self.assertNotIn('NEVER_EXECUTE', body)
        importer.assert_not_called(); grades.assert_not_called()
        saved = list(self.root.rglob('*.ipynb')); reports = list(self.root.rglob('*.html'))
        self.assertEqual(len(saved), 1); self.assertEqual(json.loads(saved[0].read_text()), nb)
        report = reports[0].read_text()
        self.assertIn('NEVER_EXECUTE', report)
        self.assertIn('BILAN_PERSONNEL &lt;script&gt;', report)
        self.assertIn('&lt;script&gt;', report)
        self.assertIn('&lt;img src=x onerror=alert(1)&gt;', report)
        self.assertNotIn('<script>', report); self.assertNotIn('UNTRUSTED_HTML', report)
        with next(self.root.rglob('*.csv')).open() as stream: rows = list(csv.reader(stream, delimiter=';'))
        self.assertEqual(len(rows), 2)
        self.assertNotIn('Note', rows[0]); self.assertNotIn('Bonus', rows[0])
        self.assertIn("'=2+2", rows[1])
        self.assertEqual(self.client.get('/health').json['evaluators'], 33)
        self.post(nb)
        self.assertEqual(len(list(self.root.rglob('*.ipynb'))), 2)

    def test_storage_failure_never_confirms_receipt(self):
        for owner, target in ((human.Path, 'write_bytes'), (human.Path, 'write_text'), (human.csv, 'writer')):
            with self.subTest(target=target), patch.object(owner, target, side_effect=OSError('PRIVATE_FAILURE')):
                with self.assertLogs(self.app.logger, level='ERROR'):
                    response = self.post(notebook())
            self.assertEqual(response.status_code, 503)
            body = response.get_data(as_text=True)
            self.assertNotIn('reçu pour relecture', body)
            self.assertNotIn('PRIVATE_FAILURE', body)

    def test_invalid_identity_and_old_copy_are_not_saved(self):
        nb = notebook(); nb['metadata']['tal']['version'] = 1
        self.assertEqual(self.post(nb).status_code, 400)
        nb = notebook(); nb['cells'][0]['source'] = 'nom=run_code()'
        self.assertEqual(self.post(nb).status_code, 400)
        self.assertEqual(list(self.root.rglob('*')), [])
