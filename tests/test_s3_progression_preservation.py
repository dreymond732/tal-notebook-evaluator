"""Frozen parent evidence for the additive review of all eleven S3 TD subjects."""
import copy
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

    def test_all_eleven_subjects_preserve_activities_order_and_question_contracts(self):
        self.assertEqual(self.baseline['source_commit'], '933b0df6565fbd7d64f02db941eda5e8358eb16e')
        entries = [e for e in load_catalog() if e['active'] and e['semester'] == 'S3' and e['mode'] == 'td']
        self.assertEqual(len(entries), 11)
        self.assertEqual(set(self.baseline['subjects']), {e['notebook'] for e in entries})
        for path, previous in self.baseline['subjects'].items():
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
                    self.assertTrue(new_source.startswith(old_source),
                                    f'Original activity reduced or replaced: {path}, {old["id"]}')
                    if 'tal' not in old['metadata']:
                        self.assertIn(new['metadata'].pop('tal')['role'],
                                      {'prompt', 'provided', 'example', 'practice', 'infrastructure'})
                    if old['id'] in REVIEW_LINK_ADDITIONS:
                        self.assertEqual(new['metadata'].pop('tal_review'),
                                         {'question': REVIEW_LINK_ADDITIONS[old['id']]})
                    self.assertEqual(new, old, f'Original cell contract changed: {path}, {old["id"]}')
                old_root, new_root = copy.deepcopy(previous), copy.deepcopy(current)
                for root in (old_root, new_root):
                    root.pop('cells')
                    root['metadata'].pop('tal_tutor')
                    root['metadata']['colab'].pop('aiContexts')
                self.assertEqual(new_root, old_root)

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
        entries = [e for e in load_catalog() if e['active'] and e['semester'] == 'S3' and e['mode'] == 'td']
        url = 'https://example.test/universite/tal'
        originals = {e['notebook']: (ROOT / e['notebook']).read_bytes() for e in entries}
        with tempfile.TemporaryDirectory() as temporary, patch.object(prep, 'load_catalog', return_value=entries):
            output = Path(temporary) / 'dist'
            self.assertEqual(prep.render(output, url), 11)
            self.assertEqual(prep.verify_rendered(output, url), 11)
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
        entries = [e for e in load_catalog() if e['active'] and e['semester'] == 'S3' and e['mode'] == 'td']
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
