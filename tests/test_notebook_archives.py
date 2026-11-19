"""Préservation exacte des archives et sélection de la progression courante."""
import copy
import hashlib
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'app'), str(ROOT / 'tests')]
from app import create_app
import notebook_contract as contract
import prepare_student_notebooks as prep
from test_s1_v2_results import notebook as saved_fixture
from s1_reference import CHECKS

SNAPSHOT = ROOT / 'tests/fixtures/archives_progression_source_sha256.json'
ARCHIVED_IDS = {'td3-s1', 'td4-s1', 'td5-s1', 'td6-s1'}


class NotebookArchivesTests(unittest.TestCase):
    def test_twelve_archives_preserve_all_original_bytes(self):
        snapshot = json.loads(SNAPSHOT.read_text())
        self.assertEqual(snapshot['source_commit'], '501413c3e5c216138595e68bee714d7902e9a393')
        self.assertEqual(len(snapshot['notebooks']), 12)
        self.assertEqual({p.relative_to(ROOT / 'historique').as_posix()
                          for p in (ROOT / 'historique').rglob('*.ipynb')}, set(snapshot['notebooks']))
        for former, digest in snapshot['notebooks'].items():
            with self.subTest(former=former):
                self.assertFalse((ROOT / former).exists())
                archive = ROOT / 'historique' / former
                self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), digest)
        # Les deux archives déjà invalides restent conservées, sans réparation.
        for former in ('Notebooks TD/TD6_S2-corrigé.ipynb', 'Notebooks contrôles finaux/DevoirS2.ipynb'):
            with self.assertRaises(json.JSONDecodeError):
                json.loads((ROOT / 'historique' / former).read_text())

    def test_current_semester_directories_only_contain_current_topics(self):
        catalog = contract.load_catalog()
        archives = [e for e in catalog if e.get('archived')]
        self.assertEqual({e['id'] for e in archives}, ARCHIVED_IDS)
        self.assertTrue(all(e['active'] and e['notebook'].startswith('historique/') for e in archives))
        self.assertEqual(len(list((ROOT / 'Notebooks TD/S1').glob('*.ipynb'))), 15)
        self.assertEqual(len(list((ROOT / 'Notebooks TD/S2').glob('*.ipynb'))), 3)
        self.assertEqual(len(list((ROOT / 'Notebooks TD/S3').glob('*.ipynb'))), 12)
        for filename in ('R0_S3_python_texte.ipynb', 'R2_S3_frequences_reutilisables.ipynb', 'TD1.b_S3_doc_spacy.ipynb'):
            self.assertTrue((ROOT / 'Notebooks TD/S3' / filename).is_file())
        self.assertTrue((ROOT / 'Corrigés modèles/Contrôles finaux/controle-s1-v2/Controle_S1_v2_corrige_non_execute.ipynb').is_file())
        self.assertTrue((ROOT / 'Notebooks contrôles finaux/S2/Controle_final_S2_algorithmique_fichiers.ipynb').is_file())

    def test_distribution_excludes_archives_but_keeps_all_current_controls(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'dist'
            self.assertEqual(prep.render(output, 'https://example.test/tal'), 43)
            self.assertEqual(prep.verify_rendered(output, 'https://example.test/tal'), 43)
            expected = {e['notebook'] for e in contract.load_catalog()
                        if not e.get('archived') and (e['active'] or e['mode'] == 'controle')}
            paths = {p.relative_to(output).as_posix() for p in output.rglob('*.ipynb')}
            self.assertEqual(paths, expected)
            self.assertFalse((output / 'historique').exists())
            self.assertFalse((output / 'Corrigés modèles').exists())
            self.assertEqual(len(list((output / 'Notebooks TD/S1').glob('*.ipynb'))), 15)
            self.assertEqual(sum(p.startswith('Notebooks contrôles finaux/') for p in paths), 13)

    def test_archived_routing_and_grading_remain_compatible_with_saved_copies(self):
        entries = {e['id']: e for e in contract.load_catalog()}
        for number in (3, 4, 5, 6):
            key = f'td{number}-s1'
            entry = entries[key]
            nb = json.loads((ROOT / entry['notebook']).read_text())
            self.assertEqual(contract.resolve_notebook(nb), entry)
            # Remplacer uniquement par des traces synthétiques déjà utilisées
            # dans les tests ; ne jamais exécuter le code d'une copie.
            replacements = {c['metadata']['tal']['question']: c for c in saved_fixture(number)['cells']}
            for cell in nb['cells']:
                tag = cell.get('metadata', {}).get('tal', {})
                if tag.get('role') == 'identification':
                    cell['source'] = 'nom="Modele"\nprenom="Camille"\nclasse="S1"\nnumero_etudiant="ARCHIVE-TEST"'
                elif tag.get('role') == 'answer':
                    replacement = replacements[tag['question']]
                    cell['source'] = replacement['source']
                    cell['outputs'] = replacement['outputs']
            module = importlib.import_module(f'app_correction_TD{number}_S1')
            result = module.check_notebook(json.dumps(nb), 'copie_deja_commencee.ipynb')
            self.assertIsNone(result[4])
            self.assertEqual(result[0], len(CHECKS[number]))

    def test_semester_menu_hides_old_editions_but_direct_routes_remain(self):
        client = create_app().test_client()
        self.assertEqual(client.get('/health').json['evaluators'], 46)
        html = client.get('/semestre/S1').get_data(as_text=True)
        for key in ARCHIVED_IDS:
            self.assertNotIn(f'/eval/{key}"', html)
            self.assertEqual(client.get('/eval/' + key).status_code, 200)
        for key in ('td3-one-s1', 'td4-bis-s1', 'td5-ter-s1', 'td6-one-s1'):
            self.assertIn(f'/eval/{key}"', html)

    def test_catalog_rejects_an_archive_flag_inconsistent_with_its_path(self):
        original = contract.load_catalog()
        for change in ('flag_missing', 'normal_path', 'non_boolean'):
            entries = copy.deepcopy(original)
            item = next(e for e in entries if e['id'] == 'td3-s1')
            if change == 'flag_missing':
                item.pop('archived')
            elif change == 'normal_path':
                item['notebook'] = item['notebook'].removeprefix('historique/')
            else:
                item['archived'] = 'true'
            raw = json.dumps({'schema_version': 1, 'notebooks': entries})
            with self.subTest(change=change), patch.object(Path, 'read_text', return_value=raw):
                with self.assertRaisesRegex(ValueError, 'archive incohérent'):
                    contract.load_catalog()


if __name__ == '__main__':
    unittest.main()
