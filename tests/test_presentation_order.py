"""Exact parent evidence for global H1 move and explicit S3 presentation changes."""
import ast
import copy
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from presentation_order_evidence import SNAPSHOT, RENAMED, current_path, before_title_move
from tutor_metadata import migrate_notebook, CELL_START, CELL_END
from notebook_contract import load_catalog, resolve_notebook


class PresentationOrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads(SNAPSHOT.read_text())
        cls.sessions = json.loads((ROOT / 'docs/pedagogy/tutor_sessions.json').read_text())['sessions']

    def test_all_35_subjects_have_exact_title_and_context_in_one_cell(self):
        self.assertEqual(self.baseline['source_commit'], '1ee45813283cec79463a8acc4b6204f50cbafe74')
        self.assertEqual(len(self.baseline['subjects']), 35)
        for oldpath, raw in self.baseline['subjects'].items():
            old = json.loads(raw)
            new = json.loads((ROOT / current_path(oldpath)).read_text())
            with self.subTest(notebook=oldpath):
                first = new['cells'][0]
                self.assertEqual(first.get('id'), old['cells'][0].get('id'))
                self.assertEqual(first['metadata'], old['cells'][0]['metadata'])
                source = ''.join(first['source'])
                heading, body = source.split('\n\n', 1)
                self.assertRegex(heading, r'^# [^\n]+$')
                context = next(iter(new['metadata']['colab']['aiContexts'].values()))['context']
                self.assertEqual(body, f'<!-- {CELL_START}\n{context}{CELL_END} -->\n')
                self.assertEqual(sum(CELL_START in ''.join(c['source']) for c in new['cells']), 1)
                self.assertEqual([c.get('id') for c in new['cells']], [c.get('id') for c in old['cells']])
                self.assertEqual(new['metadata']['tal'], old['metadata']['tal'])
                # Every pre-existing executable statement and data value remains.
                for previous, revised in zip(old['cells'], new['cells']):
                    self.assertEqual(previous['metadata'], revised['metadata'])
                    if previous['cell_type'] == 'code':
                        try:
                            expected_ast = ast.dump(ast.parse(''.join(previous['source'])))
                        except SyntaxError:
                            # Some controls deliberately supply erroneous code
                            # to debug. Preserve that exact source, not an AST.
                            self.assertEqual(previous['source'], revised['source'])
                        else:
                            self.assertEqual(expected_ast, ast.dump(ast.parse(''.join(revised['source']))), previous.get('id'))
                        self.assertEqual(previous.get('outputs'), revised.get('outputs'))
                        self.assertEqual(previous.get('execution_count'), revised.get('execution_count'))
                old_session = old['metadata']['tal_tutor']['session']
                new_session = new['metadata']['tal_tutor']['session']
                self.assertEqual(old_session['allowed_libraries'], new_session['allowed_libraries'])
                self.assertEqual(old_session['provided_libraries'], new_session['provided_libraries'])
                for before, after in zip(old_session['exercises'], new_session['exercises']):
                    self.assertEqual(before['id'], after['id'])
                    for key in ('available_concepts', 'introduced_here', 'allowed_libraries'):
                        self.assertEqual(before[key], after[key])
                self.assertEqual(len(old_session['exercises']), len(new_session['exercises']))

    def test_outside_s3_td_only_title_moves_no_field_or_prose_changes(self):
        for path, raw in self.baseline['subjects'].items():
            if path.startswith('Notebooks TD/S3/'):
                continue
            with self.subTest(notebook=path):
                current = json.loads((ROOT / path).read_text())
                # Reversal is independent of migrate_notebook and fails on any
                # alteration to title, remaining prose, code, IDs or metadata.
                expected = json.loads(raw)
                if path == 'Notebooks contrôles finaux/S3/Controle_TD1_S3.ipynb':
                    # Only the name of the unchanged prerequisite is updated.
                    prerequisites = expected['metadata']['tal_tutor']['session']['prerequisites']
                    self.assertEqual(prerequisites[0], 'TD0 à TD1 du S3 : compétences déjà pratiquées')
                    prerequisites[0] = 'TD0 à TD1.a du S3 : compétences déjà pratiquées'
                self.assertEqual(before_title_move(current, path), expected)

    def test_user_heading_is_preserved_and_migration_is_idempotent(self):
        old = json.loads(next(iter(self.baseline['subjects'].values())))
        session = old['metadata']['tal_tutor']['session']
        first = old['cells'][0]
        first['source'] = ('# Mon titre personnel\n\n' + ''.join(first['source'])).splitlines(keepends=True)
        first['metadata']['custom_annotation'] = 'intacte'
        # Existing user title wins; no other title/prose is silently rewritten.
        remaining = copy.deepcopy(old['cells'][1:])
        new = migrate_notebook(old, session)
        self.assertEqual(''.join(new['cells'][0]['source']).splitlines()[0], '# Mon titre personnel')
        self.assertEqual(new['cells'][0]['metadata']['custom_annotation'], 'intacte')
        self.assertEqual(new['cells'][1:], remaining)
        self.assertEqual(migrate_notebook(new, session), new)

    def test_intro_heading_only_moves_and_late_heading_stays(self):
        old = json.loads(next(iter(self.baseline['subjects'].values())))
        session = old['metadata']['tal_tutor']['session']
        old['cells'] = [old['cells'][0], {'id': 'intro', 'cell_type': 'markdown',
                         'metadata': {'custom': 'preserve'}, 'source': '# Titre\n\nCours intégral.\n'},
                        {'id': 'later', 'cell_type': 'markdown', 'metadata': {}, 'source': '# Sauvegarde\nExplication.'}]
        new = migrate_notebook(old, session)
        self.assertEqual(new['cells'][1], dict(old['cells'][1], source='\nCours intégral.\n'))
        self.assertEqual(new['cells'][2], old['cells'][2])
        self.assertEqual(migrate_notebook(new, session), new)

    def test_missing_title_fails_without_mutating_input(self):
        session = self.sessions[0]
        old = {'cells': [{'cell_type': 'markdown', 'source': 'Texte sans titre', 'metadata': {}}]}
        saved = copy.deepcopy(old)
        with self.assertRaisesRegex(ValueError, 'Titre H1'):
            migrate_notebook(old, session)
        self.assertEqual(old, saved)

    def test_renames_keep_routing_and_versions_and_menu_order(self):
        from routes import EVALUATORS
        from app import create_app
        expected = [('td1-s3', 'TD1.a', 2), ('td-r1-s3', 'TD1.b', 2), ('td1b-s3', 'TD1.c', 3)]
        for (oldpath, newpath), (identifier, label, version) in zip(RENAMED.items(), expected):
            self.assertFalse((ROOT / oldpath).exists())
            nb = json.loads((ROOT / newpath).read_text())
            entry = resolve_notebook(nb)
            self.assertEqual((entry['id'], entry['version'], entry['notebook']), (identifier, version, newpath))
            self.assertTrue(EVALUATORS[identifier][0].startswith(label))
            self.assertTrue(''.join(nb['cells'][0]['source']).startswith('# ' + label + ' S3 — '))
        client = create_app().test_client()
        response = client.get('/semestre/S3')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        order = ['td0-s3', 'td-r0-s3', 'td1-s3', 'td-r1-s3', 'td1b-s3', 'td-r2-s3'] + [f'td{i}-s3' for i in range(2, 8)]
        positions = [html.index(f'/eval/{identifier}"') for identifier in order]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('bonus facultatif', html)
        self.assertGreater(html.index('/eval/controle-td1-s3"'), positions[-1])

    def test_distribution_uses_new_paths_and_keeps_context(self):
        import prepare_student_notebooks as prep
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'dist'
            self.assertEqual(prep.render(output, 'https://example.test/tal'), 34)
            self.assertEqual(prep.verify_rendered(output, 'https://example.test/tal'), 34)
            for oldpath, newpath in RENAMED.items():
                self.assertFalse((output / oldpath).exists())
                rendered = json.loads((output / newpath).read_text())
                source = json.loads((ROOT / newpath).read_text())
                self.assertEqual(rendered['cells'][0], source['cells'][0])
                self.assertEqual(rendered['metadata'], source['metadata'])


if __name__ == '__main__':
    unittest.main()
