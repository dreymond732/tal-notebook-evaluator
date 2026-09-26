"""Contract is trusted routing, never a student-controlled module loader."""
import copy
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
from notebook_contract import (ContractError, evaluation_cells, load_catalog,
                               resolve_cells, resolve_notebook, validate_cell_metadata)


def notebook(evaluator='td2-s1'):
    return {'nbformat': 4, 'nbformat_minor': 5, 'metadata': {
        'tal': {'id': evaluator, 'version': 1, 'evaluator': evaluator}}, 'cells': []}


def cell(question='Q1', role='answer'):
    return {'cell_type': 'code', 'source': ['raise RuntimeError("NEVER_EXECUTE")'],
            'metadata': {'tal': {'question': question, 'role': role}}, 'outputs': []}


class NotebookContractTests(unittest.TestCase):
    def test_catalog_matches_registry_and_inactive_subject_is_explicit(self):
        catalog = load_catalog()
        self.assertEqual(len(catalog), 33)
        self.assertEqual({e['evaluator'] for e in catalog if e['active']}, set(routes.EVALUATORS))
        inactive = [entry for entry in catalog if not entry['active']]
        self.assertEqual([e['id'] for e in inactive], ['controle-final-s2'])
        self.assertIsNone(inactive[0]['evaluator'])
        for entry in catalog:
            self.assertTrue((Path(__file__).resolve().parents[1] / entry['notebook']).is_file())

    def test_unknown_inactive_malformed_and_version_mismatch_are_rejected(self):
        bad_contracts = [None, [], {}, {'id': []},
                         {'id': 'td2-s1', 'evaluator': 'td2-s1', 'version': True},
                         {'id': 'td2-s1', 'evaluator': 'td2-s1', 'version': 2},
                         {'id': 'td2-s1', 'evaluator': 'os', 'version': 1},
                         {'id': 'absent', 'evaluator': 'os', 'version': 1},
                         {'id': 'controle-final-s2', 'evaluator': None, 'version': 1}]
        for contract in bad_contracts:
            with self.subTest(contract=contract), self.assertRaises(ContractError):
                resolve_notebook({'metadata': {'tal': contract}, 'cells': []})

    def test_legacy_requires_explicit_route_and_mismatch_never_falls_back(self):
        with self.assertRaises(ContractError):
            resolve_notebook({'cells': []})
        self.assertIsNone(resolve_notebook({'cells': []}, 'td2-s1', require_metadata=False))
        with self.assertRaises(ContractError):
            resolve_notebook(notebook(), 'Controletilt-s1', require_metadata=False)

    def test_resolution_is_non_mutating_and_cannot_override_mode(self):
        nb = notebook('td2-S2')
        nb['metadata']['tal']['mode'] = 'td'
        before = copy.deepcopy(nb)
        entry = resolve_notebook(nb)
        self.assertEqual(entry['mode'], 'controle')
        self.assertEqual(nb, before)

    def test_explicit_cells_ignore_changed_markers_and_refuse_duplicates(self):
        answer = cell()
        nb = {'cells': [answer]}
        fallback = Mock(return_value=[{'source': 'WRONG'}])
        self.assertEqual(resolve_cells(nb, 'Q1', legacy=fallback), [answer])
        self.assertEqual(resolve_cells(nb, 'Q2', legacy=fallback), [])
        fallback.assert_not_called()
        with self.assertRaises(ContractError):
            validate_cell_metadata({'cells': [answer, copy.deepcopy(answer)]})

    def test_distribution_cell_is_excluded_and_does_not_disable_legacy(self):
        old = {'cell_type': 'code', 'source': ['print("Résultat Q1")']}
        nb = {'cells': [old, cell('submission', 'submission')]}
        fallback = Mock(return_value=[old])
        self.assertEqual(evaluation_cells(nb), [old])
        self.assertEqual(resolve_cells(nb, 'Q1', legacy=fallback), [old])
        fallback.assert_called_once()


class AutomaticSubmissionTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        base = patch.object(outils, 'BASE_DIR', directory.name)
        base.start()
        self.addCleanup(base.stop)
        self.root = Path(directory.name)
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()
        self.checker = Mock(return_value=(13.37, [{'check': 'PRIVATE_CHECK',
            'student_answer': 'PRIVATE_ANSWER', 'correct_answer': 'PRIVATE_SOLUTION',
            'status': '✅', 'points': 13.37, 'max_points': 20}], 20,
            {'nom': 'Exemple', 'prenom': 'Test', 'classe': 'G1'}, None))
        imports = patch.object(routes, 'import_module', return_value=SimpleNamespace(check_notebook=self.checker))
        self.importer = imports.start()
        self.addCleanup(imports.stop)

    def post(self, nb, path='/submit'):
        raw = nb if isinstance(nb, bytes) else json.dumps(nb).encode()
        return self.client.post(path, data={'file': (io.BytesIO(raw), 'renomme.IPYNB')})

    def test_entry_and_form_work_behind_proxy(self):
        for path in ('/', '/submit'):
            response = self.client.get(path, headers={'X-Forwarded-Prefix': '/universite/tal'})
            self.assertEqual(response.status_code, 200)
            self.assertIn('action="/universite/tal/submit"', response.get_data(as_text=True))
        self.assertEqual(self.client.get('/health').json, {'status': 'ok', 'evaluators': 32})

    def test_renamed_td_is_dispatched_and_saved(self):
        nb = notebook()
        nb['cells'].append(cell())
        response = self.post(nb)
        self.assertEqual(response.status_code, 200)
        self.importer.assert_called_once_with('app_correction_TD2_S1')
        self.assertIn('PRIVATE_CHECK', response.get_data(as_text=True))
        saved = list(self.root.rglob('*.IPYNB'))
        self.assertEqual(len(saved), 1)
        self.assertEqual(json.loads(saved[0].read_text()), nb)

    def test_control_mode_is_server_side_and_report_stays_private(self):
        nb = notebook('td2-S2')
        nb['metadata']['tal']['mode'] = 'td'
        response = self.post(nb)
        body = response.get_data(as_text=True)
        self.assertIn('Copie reçue et enregistrée', body)
        for private in ('PRIVATE_', '13.37', '✅'):
            self.assertNotIn(private, body)
        self.assertIn('PRIVATE_CHECK', next(self.root.rglob('*.html')).read_text())

    def test_invalid_and_ambiguous_uploads_never_load_or_correct(self):
        duplicate = notebook()
        duplicate['cells'] = [cell(), cell()]
        invalid = [b'{broken', b'{"metadata":{},"metadata":{},"cells":[]}', [],
                   {'cells': []}, {'metadata': notebook()['metadata']},
                   dict(notebook(), cells=None), notebook('missing'), duplicate]
        for nb in invalid:
            with self.subTest(nb=nb):
                self.assertEqual(self.post(nb).status_code, 400)
        self.importer.assert_not_called()
        self.checker.assert_not_called()
        self.assertEqual(list(self.root.rglob('*.html')), [])

    def test_legacy_endpoint_refuses_metadata_contradiction(self):
        response = self.post(notebook('Controletilt-s1'), '/eval/td2-s1')
        self.assertIn('ne correspond pas au dépôt', response.get_data(as_text=True))
        self.checker.assert_not_called()
        self.assertEqual(list(self.root.rglob('*.html')), [])

    def test_identified_notebook_without_cells_is_rejected_on_legacy_route(self):
        response = self.post({'metadata': notebook()['metadata']}, '/eval/td2-s1')
        self.assertIn('liste de cellules', response.get_data(as_text=True))
        self.checker.assert_not_called()
        self.assertEqual(list(self.root.rglob('*.html')), [])

    def test_persistence_failure_cannot_be_a_successful_control_receipt(self):
        with patch.object(routes, 'process_submission', side_effect=OSError('PRIVATE_SOLUTION')):
            with self.assertLogs(self.app.logger, level='ERROR'):
                response = self.post(notebook('controle-td1-s3'))
        body = response.get_data(as_text=True)
        self.assertNotIn('Copie reçue et enregistrée', body)
        self.assertNotIn('PRIVATE_SOLUTION', body)


if __name__ == '__main__':
    unittest.main()
