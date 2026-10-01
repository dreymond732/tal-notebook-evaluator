"""Pre-design S2 evidence and deployment isolation, without running notebook code."""
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from notebook_contract import load_catalog, resolve_notebook, validate_cell_metadata
import prepare_student_notebooks as prep
from test_notebook_migration_integrity import S2_RENAMED_SUBJECTS

BASELINE = ROOT / 'tests/fixtures/s2_complete_review_source_baseline.json'
COUNTS = {'td3-S2': 30, 'td5-S2': 25, 'td6-S2': 10, 'td2-S2': 13,
          'td4-S2': 14, 'ControleDevoirMaisonS2': 30, 'controle-final-s2': 18}


class S2Preservation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads(BASELINE.read_text())
        cls.entries = [e for e in load_catalog() if e['semester'] == 'S2']

    def test_exact_inventory_paths_questions_and_empty_outputs(self):
        self.assertEqual(self.baseline['source_commit'], 'b7650e3d035846a67014b94e463a08cd43b67fb5')
        self.assertEqual(set(self.baseline['subjects']), set(S2_RENAMED_SUBJECTS))
        self.assertEqual({e['notebook'] for e in self.entries}, set(S2_RENAMED_SUBJECTS.values()))
        self.assertEqual(len(self.entries), 7)
        self.assertEqual(sum(COUNTS.values()), 140)
        self.assertEqual(sum(COUNTS[e['id']] for e in self.entries if e['active']), 122)
        for entry in self.entries:
            with self.subTest(subject=entry['id']):
                nb = json.loads((ROOT / entry['notebook']).read_text())
                self.assertEqual(nb['metadata']['tal'], {'id': entry['id'], 'evaluator': entry['evaluator'], 'version': 2})
                indexed = validate_cell_metadata(nb)
                self.assertEqual(len(indexed), len(nb['cells']))
                self.assertEqual({q for q, role in indexed if role == 'answer'}, {f'Q{q}' for q in range(1, COUNTS[entry['id']] + 1)})
                self.assertIn(('identity', 'identification'), indexed)
                ids = [c['id'] for c in nb['cells']]
                self.assertEqual(len(set(ids)), len(ids))
                self.assertEqual(ids[0], 'tal-tutor-instructions')
                self.assertEqual(nb['cells'][-1], prep.submission_cell())
                if entry['active']:
                    self.assertEqual(resolve_notebook(nb)['evaluator'], entry['id'])
                else:
                    self.assertIsNone(entry['evaluator'])
                for cell in nb['cells']:
                    if cell['cell_type'] == 'code':
                        self.assertEqual(cell.get('outputs', []), [])
                        self.assertIsNone(cell.get('execution_count'))
        for previous in S2_RENAMED_SUBJECTS:
            self.assertFalse((ROOT / previous).exists(), previous)

    def test_every_original_activity_is_retained_in_order(self):
        slugs = {'td3-S2': 'td3', 'td5-S2': 'td5', 'td6-S2': 'td6',
                 'td2-S2': 'td2', 'td4-S2': 'td4',
                 'ControleDevoirMaisonS2': 'dm', 'controle-final-s2': 'final'}
        by_path = {e['notebook']: e for e in self.entries}
        for old_path, old_nb in self.baseline['subjects'].items():
            new_path = S2_RENAMED_SUBJECTS[old_path]
            entry = by_path[new_path]
            current = json.loads((ROOT / new_path).read_text())
            cells = {c['id']: c for c in current['cells']}
            expected_ids = []
            for index, original in enumerate(old_nb['cells']):
                identifier = ('tal-tutor-instructions' if index == 0 else
                    original.get('id') or original.get('metadata', {}).get('id') or
                    (f'{slugs[entry["id"]]}-s2-source-{index:03d}' if entry['mode'] == 'td' else
                     f's2-{slugs[entry["id"]]}-legacy-{index:03d}'))
                expected_ids.append(identifier)
                with self.subTest(notebook=new_path, original_cell=index):
                    self.assertIn(identifier, cells)
                    revised = cells[identifier]
                    self.assertEqual(revised['cell_type'], original['cell_type'])
                    if index == 0:
                        continue  # Full synchronized policy independently checked.
                    role = revised['metadata']['tal']['role']
                    if role == 'identification':
                        self.assertIn('numero_etudiant', ''.join(revised['source']))
                        continue
                    old_source = ''.join(original['source'])
                    if old_path == 'Notebooks TD/TD4_S2.ipynb' and index == 1:
                        old_source = old_source.replace('# 📘 Contrôle S3 :', '# 📘 Contrôle S2 :', 1)
                    # Only exact recorded-result print wrappers change; variable,
                    # question number, data and student computation stay intact.
                    if original['cell_type'] == 'code' and entry['active']:
                        old_source = re.sub(r'print\(f"Résultat (Q[1-9][0-9]*) : \{([A-Za-z_][A-Za-z_0-9]*)\}"\)',
                                            r'print("Résultat \1 :", \2)', old_source)
                        old_source = old_source.replace('print(f"Résultat Q1 : {cout_total} €")',
                                                        'print("Résultat Q1 :", cout_total)')
                        old_source = re.sub(r'print\(f"Résultat (Q[1-9][0-9]*) :"\s*, ([A-Za-z_][A-Za-z_0-9]*)\)',
                                            r'print("Résultat \1 :", \2)', old_source)
                    self.assertTrue(''.join(revised['source']).startswith(old_source),
                                    f'Original content reduced or modified: {new_path} cell {index}')
                    for key, value in original.get('metadata', {}).items():
                        if key != 'tal':
                            self.assertEqual(revised['metadata'].get(key), value)
                    for key, value in original.items():
                        if key not in {'id', 'metadata', 'source', 'outputs', 'execution_count'}:
                            self.assertEqual(revised.get(key), value)
                    previous_contract = original.get('metadata', {}).get('tal')
                    if previous_contract is not None:
                        self.assertEqual(revised['metadata']['tal'], previous_contract)
            self.assertEqual([c['id'] for c in current['cells'] if c['id'] in expected_ids], expected_ids)

    def test_all_other_notebooks_are_byte_identical(self):
        self.assertEqual(len(self.baseline['unchanged_notebooks_sha256']), 37)
        for path, expected in self.baseline['unchanged_notebooks_sha256'].items():
            with self.subTest(notebook=path):
                self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), expected)

    def test_six_active_distributions_change_only_final_url(self):
        entries = [e for e in self.entries if e['active']]
        self.assertEqual(len(entries), 6)
        url = 'https://example.test/universite/tal'
        originals = {e['notebook']: (ROOT / e['notebook']).read_bytes() for e in entries}
        with tempfile.TemporaryDirectory() as temp, patch.object(prep, 'load_catalog', return_value=self.entries):
            output = Path(temp) / 'dist'
            self.assertEqual(prep.render(output, url), 6)
            self.assertEqual(prep.verify_rendered(output, url), 6)
            for path, raw in originals.items():
                with self.subTest(notebook=path):
                    self.assertEqual((ROOT / path).read_bytes(), raw)
                    original = json.loads(raw)
                    rendered = json.loads((output / path).read_text())
                    self.assertEqual(original['cells'].pop(), prep.submission_cell())
                    self.assertEqual(rendered['cells'].pop(), prep.submission_cell(url))
                    self.assertEqual(original, rendered)
                    self.assertNotIn(url.encode(), raw)
            inactive = next(e for e in self.entries if not e['active'])
            self.assertFalse((output / inactive['notebook']).exists())

    def test_practice_interpretations_reach_safe_human_report_without_scoring(self):
        from app import create_app
        from flask import render_template
        from s3_review import review_evidence
        from s1_revision import collect
        for entry in self.entries:
            if entry['mode'] != 'td':
                continue
            nb = json.loads((ROOT / entry['notebook']).read_text())
            original_outputs = collect(nb)[1]
            practices = [c for c in nb['cells'] if c['metadata']['tal']['role'] == 'practice']
            self.assertTrue(practices)
            for cell in practices:
                with self.subTest(notebook=entry['notebook'], cell=cell['id']):
                    question = cell['metadata'].get('tal_review', {}).get('question')
                    self.assertIn(question, {f'Q{q}' for q in range(1, COUNTS[entry['id']] + 1)})
                    personal = 'Prédiction puis interprétation ' + cell['id'] + ' <script>preuve</script>'
                    cell['source'] = [personal]
                    if cell['cell_type'] == 'code':
                        cell['source'] = ['# ' + personal + '\nprint("Résultat ' + question + ' :", 123)']
                        cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout',
                                            'text': 'Résultat ' + question + ' : 123\n'}]
            self.assertEqual(collect(nb)[1], original_outputs)
            evidence = review_evidence(nb, COUNTS[entry['id']])
            by_question = {g['question']: g['cells'] for g in evidence}
            included = {c['cell_id'] for g in evidence for c in g['cells']}
            for cell in practices:
                self.assertIn(cell['id'], {c['cell_id'] for c in by_question[cell['metadata']['tal_review']['question']]})
            for cell in nb['cells']:
                if cell['metadata']['tal']['role'] in {'prompt', 'example', 'provided', 'infrastructure', 'submission'}:
                    self.assertNotIn(cell['id'], included)
            with create_app().test_request_context('/submit'):
                html = render_template('corrector_template.html', display_name='TD S2',
                    student_info={'review_evidence': evidence, 'prenom': 'Essai', 'nom': 'Modele',
                                  'classe': 'S2', 'score_nature': 'technique_provisoire'},
                    details=[], score=0, max_score=COUNTS[entry['id']], evaluator_name=entry['id'])
            self.assertIn('&lt;script&gt;preuve&lt;/script&gt;', html)
            self.assertNotIn('<script>preuve</script>', html)
            for cell in practices:
                self.assertIn('Prédiction puis interprétation ' + cell['id'], html)

    def test_every_active_s2_source_requires_canonical_restitution(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for entry in self.entries:
                if not entry['active']:
                    continue
                nb = json.loads((ROOT / entry['notebook']).read_text())
                self.assertEqual(nb['cells'].pop(), prep.submission_cell())
                path = root / entry['notebook']
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(nb))
                with self.subTest(notebook=entry['notebook']), patch.object(prep, 'load_catalog', return_value=[entry]):
                    with self.assertRaisesRegex(ValueError, 'Cellule source de restitution absente'):
                        prep.check_sources(root)


if __name__ == '__main__':
    unittest.main()
