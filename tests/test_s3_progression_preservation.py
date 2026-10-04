"""Frozen parent evidence for the additive review of all eleven S3 TD subjects."""
import copy
import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from notebook_contract import load_catalog, resolve_notebook, validate_cell_metadata
import prepare_student_notebooks as prep

EDITORIAL_PILOTS = {'Notebooks TD/S3/TD1_S3_fondations_spacy.ipynb',
                    'Notebooks TD/S3/R2_S3_frequences_reutilisables.ipynb'}
R1_EDITORIAL = {'Notebooks TD/S3/R1_S3_doc_spacy.ipynb'}
NEXT_EDITORIAL = {f'Notebooks TD/S3/{name}' for name in (
    'TD2_S3_analyse_corpus.ipynb', 'TD3_S3_concordances_citations.ipynb',
    'TD4_S3_cooccurrences.ipynb', 'TD5_S3_associations.ipynb',
    'TD6_S3_visualisations.ipynb', 'TD7_S3_audit_llm.ipynb')}
EDITORIAL_SUBJECTS = EDITORIAL_PILOTS | R1_EDITORIAL | NEXT_EDITORIAL
BASELINE = ROOT / 'tests/fixtures/s3_progression_review_source_baseline.json'
# Only original student interpretation slots may gain a human-review link.
# Ordinary instructions/examples must not become submitted analytic evidence.
REVIEW_LINK_ADDITIONS = {
    **{f's3-td{td}-{start + 3 * (q - 1):02d}': f'Q{q}'
       for td, start in ((4, 7), (5, 7), (6, 8), (7, 9))
       for q in range(1, 8)},
    's3-td7-06': 'Q1',
}


class S3ProgressionPreservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads(BASELINE.read_text())
        cls.editorial_parent = json.loads((ROOT / 'tests/fixtures/s3_editorial_pilots_source_baseline.json').read_text())
        cls.next_parent = json.loads((ROOT / 'tests/fixtures/s3_next_editorial_source_baseline.json').read_text())
        cls.r1_parent = json.loads((ROOT / 'tests/fixtures/s3_r1_editorial_source_baseline.json').read_text())

    def test_all_eleven_subjects_preserve_activities_order_and_question_contracts(self):
        self.assertEqual(self.baseline['source_commit'], '933b0df6565fbd7d64f02db941eda5e8358eb16e')
        entries = [e for e in load_catalog() if e['active'] and e['semester'] == 'S3' and e['mode'] == 'td'
                   and e['evaluator'] is not None and e['id'] != 'td1b-s3']
        self.assertEqual(len(entries), 11)
        self.assertEqual(set(self.baseline['subjects']), {e['notebook'] for e in entries})
        self.assertEqual(set(self.editorial_parent['subjects']), EDITORIAL_PILOTS)
        self.assertEqual(self.r1_parent['source_commit'], '2c7dc3c696ef0f5f70046a2c6ef005f7e21cc1ac')
        self.assertEqual(set(self.r1_parent['subjects']), R1_EDITORIAL)
        self.assertEqual(self.next_parent['source_commit'], 'cdc52d08cc02c8880003d962d0631658f04392c1')
        self.assertEqual(set(self.next_parent['subjects']), NEXT_EDITORIAL | {'Notebooks TD/S3/TD1B_S3_entites_similarite_regles.ipynb'})
        for path, previous in self.baseline['subjects'].items():
            if path in EDITORIAL_PILOTS:
                previous = json.loads(self.editorial_parent['subjects'][path])
            elif path in R1_EDITORIAL:
                previous = json.loads(self.r1_parent['subjects'][path])
            if path in NEXT_EDITORIAL:
                previous = json.loads(self.next_parent['subjects'][path])
            current = json.loads((ROOT / path).read_text())
            with self.subTest(notebook=path):
                self.assertEqual(resolve_notebook(current)['version'], 2)
                indexed = validate_cell_metadata(current)
                self.assertEqual(len(indexed), len(current['cells']))
                self.assertEqual(current['cells'][0]['id'], 'tal-tutor-instructions')
                self.assertEqual(current['cells'][-1], prep.submission_cell())
                old_ids = [cell['id'] for cell in previous['cells']]
                cells = {cell['id']: cell for cell in current['cells']}
                self.assertEqual(len(cells), len(current['cells']))
                self.assertEqual([c['id'] for c in current['cells'] if c['id'] in old_ids], old_ids)
                old_questions = {c['metadata']['tal']['question'] for c in previous['cells']
                                 if c['metadata'].get('tal', {}).get('role') == 'answer'}
                self.assertEqual({q for q, role in indexed if role == 'answer'}, old_questions)
                for old in previous['cells']:
                    new = copy.deepcopy(cells[old['id']])
                    old = copy.deepcopy(old)
                    # Full synchronized tutor text is checked independently by
                    # test_tutor_metadata and check_tutor_policy --check.
                    if old['id'] == 'tal-tutor-instructions':
                        self.assertEqual(new['cell_type'], 'markdown')
                        self.assertEqual(new['metadata']['tal']['role'], 'infrastructure')
                        continue
                    old_source = ''.join(old.pop('source'))
                    new_source = ''.join(new.pop('source'))
                    if path in EDITORIAL_SUBJECTS:
                        # Explicitly reviewed subjects may clarify prose/comments.
                        # Keep every original executable statement and contract;
                        # independent pedagogical/editorial reviews prove coverage.
                        if old['cell_type'] == 'code':
                            expected_code = ast.parse(old_source)
                            if (path == 'Notebooks TD/S3/TD1_S3_fondations_spacy.ipynb'
                                    and old['id'] == 'c4eb9544f889'):
                                # Exact runtime compatibility change only: spaCy
                                # 3.8.7 displaCy's Jupyter renderer imports display
                                # from a location removed in IPython 9.17.1.
                                calls = [node for node in ast.walk(expected_code)
                                         if isinstance(node, ast.Call)
                                         and isinstance(node.func, ast.Attribute)
                                         and isinstance(node.func.value, ast.Name)
                                         and node.func.value.id == 'subprocess'
                                         and node.func.attr == 'check_call']
                                self.assertEqual(len(calls), 1)
                                self.assertIsInstance(calls[0].args[0], ast.List)
                                calls[0].args[0].elts.append(ast.Constant(value='IPython==8.37.0'))
                            self.assertEqual(ast.dump(ast.parse(new_source)),
                                             ast.dump(expected_code),
                                             f'Original executable code changed: {path}, {old["id"]}')
                    else:
                        self.assertTrue(new_source.startswith(old_source),
                                        f'Original activity reduced or replaced: {path}, {old["id"]}')
                    if 'tal' not in old['metadata']:
                        self.assertIn(new['metadata'].pop('tal')['role'],
                                      {'prompt', 'provided', 'example', 'practice', 'infrastructure'})
                    if old['id'] in REVIEW_LINK_ADDITIONS and 'tal_review' not in old['metadata']:
                        self.assertEqual(new['metadata'].pop('tal_review'),
                                         {'question': REVIEW_LINK_ADDITIONS[old['id']]})
                    self.assertEqual(new, old, f'Original cell contract changed: {path}, {old["id"]}')
                old_root, new_root = copy.deepcopy(previous), copy.deepcopy(current)
                for root in (old_root, new_root):
                    root.pop('cells')
                    root['metadata'].pop('tal_tutor')
                    root['metadata']['colab'].pop('aiContexts')
                self.assertEqual(new_root, old_root)

    def test_companion_v3_preserves_activities_and_declares_only_new_correction_contract(self):
        path = 'Notebooks TD/S3/TD1B_S3_entites_similarite_regles.ipynb'
        old = json.loads(self.next_parent['subjects'][path])
        new = json.loads((ROOT / path).read_text())
        self.assertEqual(resolve_notebook(new)['version'], 3)
        expected_contract = dict(old['metadata']['tal'], evaluator='td1b-s3', version=3)
        self.assertEqual(new['metadata']['tal'], expected_contract)
        old_ids = [c['id'] for c in old['cells']]
        self.assertEqual([c['id'] for c in new['cells'] if c['id'] in old_ids], old_ids)
        current = {c['id']: c for c in new['cells']}
        self.assertEqual(len(current), len(new['cells']))
        for previous in old['cells']:
            revised = current[previous['id']]
            self.assertEqual(revised['cell_type'], previous['cell_type'])
            self.assertEqual(revised['metadata'], previous['metadata'])
            if previous['cell_type'] == 'code' and previous['metadata']['tal']['role'] != 'answer':
                self.assertEqual(ast.dump(ast.parse(''.join(revised['source']))),
                                 ast.dump(ast.parse(''.join(previous['source']))))
        # Only the four answer templates gain provided JSON serialization.
        self.assertEqual({q for q, role in validate_cell_metadata(new) if role == 'answer'},
                         {'Q1', 'Q2', 'Q3', 'Q4'})
        self.assertEqual(new['cells'][-1], prep.submission_cell())

    def test_original_student_interpretations_remain_in_rendered_human_report(self):
        from app import create_app
        from flask import render_template
        from s3_review import review_evidence
        seen = set()
        for path in self.baseline['subjects']:
            nb = json.loads((ROOT / path).read_text())
            targets = [cell for cell in nb['cells'] if cell['id'] in REVIEW_LINK_ADDITIONS]
            if not targets:
                continue
            for cell in targets:
                cell['source'] = ['Analyse personnelle ' + cell['id'] + ' <preuve>']
                seen.add(cell['id'])
            evidence = review_evidence(nb, 7)
            by_question = {group['question']: group['cells'] for group in evidence}
            included_ids = {cell['cell_id'] for group in evidence for cell in group['cells']}
            for cell in targets:
                question = REVIEW_LINK_ADDITIONS[cell['id']]
                self.assertIn(cell['id'], {c['cell_id'] for c in by_question[question]})
            for cell in nb['cells']:
                if cell['metadata']['tal']['role'] in {'prompt', 'provided', 'example', 'infrastructure', 'submission'} and 'tal_review' not in cell['metadata']:
                    self.assertNotIn(cell['id'], included_ids)
            with create_app().test_request_context('/submit'):
                html = render_template('corrector_template.html', display_name='TD S3',
                    student_info={'review_evidence': evidence, 'prenom': 'Alice', 'nom': 'Dupont',
                                  'classe': 'G1', 'score_nature': 'technique_provisoire'},
                    details=[], score=0, max_score=7, evaluator_name=nb['metadata']['tal']['evaluator'])
            for cell in targets:
                self.assertIn('Analyse personnelle ' + cell['id'], html)
            self.assertIn('&lt;preuve&gt;', html)
            self.assertNotIn('<preuve>', html)
        self.assertEqual(seen, set(REVIEW_LINK_ADDITIONS))

    def test_seven_controls_are_byte_identical(self):
        controls = self.baseline['unchanged_controls_sha256']
        self.assertEqual(len(controls), 7)
        for path, expected in controls.items():
            with self.subTest(notebook=path):
                self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), expected)

    def test_s3_distribution_changes_only_final_url_and_never_sources(self):
        entries = [e for e in load_catalog() if e['active'] and e['semester'] == 'S3' and e['mode'] == 'td'
                   and e['evaluator'] is not None]
        url = 'https://example.test/universite/tal'
        originals = {e['notebook']: (ROOT / e['notebook']).read_bytes() for e in entries}
        with tempfile.TemporaryDirectory() as temporary, patch.object(prep, 'load_catalog', return_value=entries):
            output = Path(temporary) / 'dist'
            self.assertEqual(prep.render(output, url), 12)
            self.assertEqual(prep.verify_rendered(output, url), 12)
            for path, raw in originals.items():
                with self.subTest(notebook=path):
                    self.assertEqual((ROOT / path).read_bytes(), raw)
                    original = json.loads(raw)
                    rendered = json.loads((output / path).read_text())
                    self.assertEqual(original['cells'].pop(), prep.submission_cell())
                    self.assertEqual(rendered['cells'].pop(), prep.submission_cell(url))
                    self.assertEqual(rendered, original)
                    self.assertNotIn(prep.URL_PLACEHOLDER, json.dumps(rendered))
                    self.assertNotIn(url.encode(), raw)

    def test_every_s3_source_requires_its_canonical_final_restitution(self):
        entries = [e for e in load_catalog() if e['active'] and e['semester'] == 'S3' and e['mode'] == 'td'
                   and e['evaluator'] is not None]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for entry in entries:
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
