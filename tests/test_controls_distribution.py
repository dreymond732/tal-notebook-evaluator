"""Tous les contrôles distribuables, sans activation implicite du serveur."""
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
import prepare_student_notebooks as prep
from notebook_contract import ContractError, load_catalog, resolve_notebook
from app import create_app
from presentation_order_evidence import archive_legacy_path

NEW_S1 = 'Notebooks contrôles finaux/S1/Controle_final_S1_python.ipynb'
OLD_S1 = 'Notebooks contrôles finaux/DevoirS1.ipynb'
FINAL_S2 = 'Notebooks contrôles finaux/S2/Controle_final_S2_algorithmique_fichiers.ipynb'


class AllControlsDistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / 'dist'
        self.url = 'https://example.test/universite/tal'

    def test_every_registered_control_and_only_allowed_notebooks_are_generated(self):
        entries = load_catalog()
        original = {p: p.read_bytes() for _, p in prep.distribution_sources()}
        self.assertEqual(len(list(prep.active_sources())), 46)
        self.assertEqual(prep.render(self.output, self.url), 43)
        self.assertEqual(prep.verify_rendered(self.output, self.url), 43)
        self.assertEqual({p.relative_to(self.output).as_posix() for p in self.output.rglob('*.ipynb')},
                         {e['notebook'] for e in entries
                          if not e.get('archived', False) and (e['active'] or e['mode'] == 'controle')})
        for e in entries:
            if e['mode'] == 'controle':
                self.assertTrue((self.output / e['notebook']).is_file())
        self.assertTrue((self.output / NEW_S1).is_file())
        self.assertFalse((self.output / OLD_S1).exists())
        self.assertFalse((ROOT / OLD_S1).exists())
        self.assertFalse((self.output / 'Corrigés modèles').exists())
        self.assertFalse((self.output / 'historique').exists())
        for path, raw in original.items():
            self.assertEqual(path.read_bytes(), raw)

    def test_inactive_final_keeps_all_questions_without_a_broken_deposit_link(self):
        entry = next(e for e in load_catalog() if e['notebook'] == FINAL_S2)
        source = json.loads((ROOT / FINAL_S2).read_text())
        self.assertFalse(entry['active'])
        self.assertIsNone(entry['evaluator'])
        prep.render(self.output, self.url)
        generated = json.loads((self.output / FINAL_S2).read_text())
        self.assertEqual(generated['cells'][-1], prep.saving_cell())
        self.assertNotIn(self.url, json.dumps(generated))
        self.assertNotIn(prep.URL_PLACEHOLDER, json.dumps(generated))
        self.assertIn('Les modalités de remise', ''.join(generated['cells'][-1]['source']))
        expected = copy.deepcopy(source)
        expected['cells'][-1] = prep.saving_cell()
        self.assertEqual(generated, expected)
        with self.assertRaises(ContractError):
            resolve_notebook(generated)
        client = create_app().test_client()
        self.assertEqual(client.get('/health').json['evaluators'], 46)
        with patch('routes.process_submission') as persist:
            response = client.post('/submit', data={'file': (io.BytesIO(json.dumps(generated).encode()), 'copie.ipynb')})
            self.assertEqual(response.status_code, 400)
            persist.assert_not_called()

    def test_previous_46_or_47_file_manifests_remove_compatibility_copies(self):
        archived = [entry for entry in load_catalog() if entry.get('archived', False)]
        self.assertEqual({entry['id'] for entry in archived},
                         {f'td{number}-s1' for number in (3, 4, 5, 6)})
        for old_count in (46, 47):
            with self.subTest(previous_count=old_count):
                prep.render(self.output, self.url)
                marker = self.output / prep.MANIFEST
                manifest = json.loads(marker.read_text())
                self.assertEqual(len(manifest['notebooks']), 43)
                # Recreate the former four distributed syntheses at their exact
                # original paths, preserving a realistic 47-file managed tree.
                former_paths = []
                for entry in archived:
                    former = archive_legacy_path(entry['notebook'])
                    former_paths.append(former)
                    target = self.output / former
                    target.parent.mkdir(parents=True, exist_ok=True)
                    notebook = json.loads((ROOT / entry['notebook']).read_text())
                    target.write_text(json.dumps(prep.distributable(notebook, self.url)))
                manifest['notebooks'].extend(former_paths)
                if old_count == 46:
                    # The earlier deployment also used the pre-rename S1 path
                    # and did not yet distribute the inactive final S2 control.
                    (self.output / NEW_S1).rename(self.output / OLD_S1)
                    (self.output / FINAL_S2).unlink()
                    manifest['notebooks'] = [OLD_S1 if path == NEW_S1 else path
                                             for path in manifest['notebooks'] if path != FINAL_S2]
                self.assertEqual(len(manifest['notebooks']), old_count)
                self.assertEqual({path.relative_to(self.output).as_posix()
                                  for path in self.output.rglob('*.ipynb')},
                                 set(manifest['notebooks']))
                marker.write_text(json.dumps(manifest))
                self.assertEqual(prep.render(self.output, self.url), 43)
                self.assertFalse((self.output / OLD_S1).exists())
                self.assertTrue((self.output / NEW_S1).is_file())
                self.assertTrue((self.output / FINAL_S2).is_file())
                for former in former_paths:
                    self.assertFalse((self.output / former).exists())
                self.assertFalse((self.output / 'historique').exists())
                self.assertEqual(prep.verify_rendered(self.output, self.url), 43)

    def test_inactive_source_identity_is_checked_before_replacing_distribution(self):
        entry = next(e for e in load_catalog() if e['notebook'] == FINAL_S2)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / FINAL_S2
            path.parent.mkdir(parents=True)
            original = (ROOT / FINAL_S2).read_bytes()
            path.write_bytes(original)
            with patch.object(prep, 'load_catalog', return_value=[entry]):
                output = root / 'dist'
                self.assertEqual(prep.render(output, self.url, root), 1)
                old_generated = (output / FINAL_S2).read_bytes()
                source = json.loads(original)
                source['metadata']['tal']['version'] = 999
                path.write_text(json.dumps(source))
                with self.assertRaisesRegex(ValueError, 'Identité incohérente'):
                    prep.render(output, self.url, root)
                self.assertEqual((output / FINAL_S2).read_bytes(), old_generated)

    def test_verifier_refuses_a_deposit_cell_inserted_into_inactive_subject(self):
        prep.render(self.output, self.url)
        path = self.output / FINAL_S2
        generated = json.loads(path.read_text())
        generated['cells'][-1] = prep.submission_cell(self.url)
        path.write_text(json.dumps(generated))
        with self.assertRaisesRegex(ValueError, 'Copie distribuable incohérente'):
            prep.verify_rendered(self.output, self.url)


if __name__ == '__main__':
    unittest.main()
