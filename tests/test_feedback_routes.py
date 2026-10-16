"""Real formative reports preserve observed work on screen and in saved HTML."""
import copy
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
from notebook_contract import load_catalog
import outils
from routes import EVALUATOR_MODES


class StudentFeedbackRoutes(unittest.TestCase):
    def test_all_active_s1_s3_formative_reports_show_actual_work_and_save_it(self):
        entries = [e for e in load_catalog() if e['active']
                   and e['semester'] in ('S1', 'S3')
                   and EVALUATOR_MODES.get(e['evaluator']) == 'td']
        self.assertGreaterEqual(len(entries), 19)
        sentinel_source = 'raise RuntimeError("SOURCE_OBSERVEE_JAMAIS_EXECUTEE")'
        sentinel_output = 'SORTIE_OBSERVEE <script>copie()</script>\n'
        for entry in entries:
            evaluator = entry['evaluator']
            original = json.loads((ROOT / entry['notebook']).read_text())
            for endpoint in ('/submit', '/eval/' + evaluator):
                with self.subTest(evaluator=evaluator, endpoint=endpoint), tempfile.TemporaryDirectory() as directory:
                    notebook = copy.deepcopy(original)
                    identity = next(c for c in notebook['cells'] if c.get('metadata', {}).get('tal', {}).get('role') == 'identification')
                    identity['source'] = 'nom="Modele"\nprenom="Test"\nclasse="Validation"\nnumero_etudiant="TEST001"'
                    answer = next(c for c in notebook['cells'] if c.get('metadata', {}).get('tal', {}) == {'question': 'Q1', 'role': 'answer'})
                    answer['source'] = sentinel_source
                    answer['outputs'] = [
                        {'output_type': 'stream', 'name': 'stdout', 'text': sentinel_output},
                        {'output_type': 'error', 'ename': 'RuntimeError', 'evalue': 'ERREUR_OBSERVEE', 'traceback': []},
                    ]
                    with patch.object(outils, 'BASE_DIR', directory):
                        app = create_app()
                        app.config.update(TESTING=True)
                        response = app.test_client().post(endpoint, headers={'X-Forwarded-Prefix': '/universite/tal'},
                            data={'file': (io.BytesIO(json.dumps(notebook).encode()), 'validation.ipynb')},
                            content_type='multipart/form-data')
                    self.assertEqual(response.status_code, 200)
                    reports = list(Path(directory).rglob('*.html'))
                    self.assertEqual(len(reports), 1)
                    for html in (response.get_data(as_text=True), reports[0].read_text()):
                        self.assertIn('SOURCE_OBSERVEE_JAMAIS_EXECUTEE', html)
                        self.assertIn('SORTIE_OBSERVEE &lt;script&gt;copie()&lt;/script&gt;', html)
                        self.assertIn('ERREUR_OBSERVEE', html)
                        self.assertNotIn('<script>copie()</script>', html)
                        self.assertIn('toggle-solutions', html)
                        self.assertIn('/universite/tal/', html)
                    self.assertEqual(len(list(Path(directory).rglob('*.ipynb'))), 1)
                    self.assertEqual(len(list(Path(directory).rglob('*.csv'))), 1)


if __name__ == '__main__':
    unittest.main()
