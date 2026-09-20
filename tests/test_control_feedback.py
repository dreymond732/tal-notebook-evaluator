"""Public control receipts must never become a correction oracle."""
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from app import create_app
import outils
import routes


class ControlFeedbackTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.base_patch = patch.object(outils, 'BASE_DIR', self.directory.name)
        self.base_patch.start()
        self.addCleanup(self.base_patch.stop)
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()
        self.details = [{
            'check': 'PRIVATE_CHECK', 'student_answer': '<script>PRIVATE_ANSWER</script>',
            'correct_answer': 'PRIVATE_SOLUTION', 'status': '✅',
            'points': 13.37, 'max_points': 17.89,
        }]
        self.checker = Mock(return_value=(13.37, self.details, 17.89,
                                          {'nom': 'Exemple', 'prenom': 'Test', 'classe': 'S1'}, None))
        self.import_patch = patch.object(routes, 'import_module',
                                         return_value=SimpleNamespace(check_notebook=self.checker))
        self.import_patch.start()
        self.addCleanup(self.import_patch.stop)

    def submit(self, name='Controletilt-s1', filename='copie.ipynb', **kwargs):
        # Arbitrary submitted source is data only; the fake evaluator never executes it.
        content = json.dumps({'cells': [{'cell_type': 'code', 'source': ['raise RuntimeError()']}]}).encode()
        return self.client.post('/eval/' + name,
                                data={'file': (io.BytesIO(content), filename)},
                                content_type='multipart/form-data', **kwargs)

    def assert_no_results(self, response):
        html = response.get_data(as_text=True)
        for secret in ('PRIVATE_CHECK', 'PRIVATE_ANSWER', 'PRIVATE_SOLUTION', '13.37', '17.89', '✅', '❌'):
            self.assertNotIn(secret, html)
        return html

    def test_modes_cover_registry_and_ambiguous_td_urls_are_controls(self):
        self.assertEqual(set(routes.EVALUATORS), set(routes.EVALUATOR_MODES))
        self.assertLessEqual(set(routes.EVALUATOR_MODES.values()), {'td', 'controle'})
        for name in ('td2-S2', 'td4-S2'):
            self.assertEqual(routes.EVALUATOR_MODES[name], 'controle')
            self.assertIn('Copie reçue et enregistrée', self.assert_no_results(self.submit(name)))

    def test_control_get_and_proxy_form_do_not_publish_results(self):
        response = self.client.get('/eval/Controletilt-s1', headers={'X-Forwarded-Prefix': '/universite/tal'})
        self.assertEqual(response.status_code, 200)
        html = self.assert_no_results(response)
        self.assertIn('action="/universite/tal/eval/Controletilt-s1"', html)
        self.assertNotIn('Copie reçue et enregistrée', html)
        self.checker.assert_not_called()

    def test_control_receipt_persists_private_report_not_receipt(self):
        response = self.submit()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Copie reçue et enregistrée', self.assert_no_results(response))
        root = Path(self.directory.name)
        reports = list(root.rglob('*.html'))
        self.assertEqual(len(reports), 1)
        report = reports[0].read_text()
        self.assertIn('PRIVATE_CHECK', report)
        self.assertIn('13.37', report)
        self.assertNotIn('<script>PRIVATE_ANSWER</script>', report)
        self.assertIn('&lt;script&gt;PRIVATE_ANSWER&lt;/script&gt;', report)
        self.assertEqual(len(list(root.rglob('*.ipynb'))), 1)
        self.assertIn('13,37', next(root.rglob('*.csv')).read_text())
        self.assertEqual(self.client.get('/soumissions/' + str(reports[0].relative_to(root))).status_code, 404)

    def test_td_feedback_stays_available(self):
        response = self.submit('td1-s1')
        html = response.get_data(as_text=True)
        self.assertIn('PRIVATE_CHECK', html)
        self.assertIn('PRIVATE_SOLUTION', html)
        self.assertIn('13.37', html)
        self.assertNotIn('Copie reçue et enregistrée', html)

    def test_checker_returned_errors_and_exceptions_do_not_leak(self):
        for error_kind in ('returned', 'raised'):
            with self.subTest(error_kind=error_kind):
                self.checker.side_effect = None
                if error_kind == 'returned':
                    self.checker.return_value = (0, [], 1, {}, 'PRIVATE_SOLUTION')
                else:
                    self.checker.side_effect = ValueError('PRIVATE_SOLUTION')
                with self.assertLogs(self.app.logger, level='ERROR'):
                    response = self.submit()
                html = self.assert_no_results(response)
                self.assertIn("Le dépôt n&#39;a pas pu être confirmé", html)
                self.assertNotIn('Copie reçue et enregistrée', html)
        self.assertEqual(list(Path(self.directory.name).rglob('*.html')), [])

    def test_persistence_failure_never_returns_success(self):
        for target in ('log_grade_to_csv', 'get_rapport_path'):
            with self.subTest(target=target):
                with patch.object(outils, target, side_effect=OSError('PRIVATE_SOLUTION')):
                    with self.assertLogs(self.app.logger, level='ERROR'):
                        response = self.submit()
                html = self.assert_no_results(response)
                self.assertNotIn('Copie reçue et enregistrée', html)
                self.assertIn("Le dépôt n&#39;a pas pu être confirmé", html)

    def test_invalid_upload_does_not_invoke_checker_or_claim_receipt(self):
        for response in (self.submit(filename='copie.txt'), self.client.post('/eval/Controletilt-s1')):
            self.assertNotIn('Copie reçue et enregistrée', self.assert_no_results(response))
        self.checker.assert_not_called()

    def test_missing_mode_fails_closed(self):
        with patch.dict(routes.EVALUATOR_MODES, {'Controletilt-s1': None}):
            with self.assertLogs(self.app.logger, level='ERROR'):
                response = self.submit()
        self.assertEqual(response.status_code, 503)
        self.assert_no_results(response)
        self.checker.assert_not_called()

    def test_import_error_is_generic(self):
        with patch.object(routes, 'import_module', side_effect=ImportError('PRIVATE_SOLUTION')):
            with self.assertLogs(self.app.logger, level='ERROR'):
                response = self.client.get('/eval/Controletilt-s1')
        self.assertEqual(response.status_code, 503)
        self.assert_no_results(response)


if __name__ == '__main__':
    unittest.main()
