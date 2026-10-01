"""Independent pre-change evidence: the S1 enrichment cannot remove an activity."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from notebook_contract import resolve_notebook, validate_cell_metadata
from prepare_student_notebooks import submission_cell


class S1ProgressionPreservationTests(unittest.TestCase):
    def test_seven_v2_subjects_preserve_every_original_activity_in_order(self):
        baseline = json.loads((ROOT / 'tests/fixtures/s1_progression_v2_source_baseline.json').read_text())
        self.assertEqual(baseline['source_commit'], '322abf53b4a1ff96c1652acfa21b4d27185bfa1a')
        self.assertEqual(len(baseline['subjects']), 7)
        total_questions = 0
        for path, previous in baseline['subjects'].items():
            current = json.loads((ROOT / path).read_text())
            with self.subTest(notebook=path):
                self.assertEqual(resolve_notebook(current)['version'], 2)
                indexed = validate_cell_metadata(current)
                self.assertEqual(len(indexed), len(current['cells']))
                self.assertEqual(current['cells'][-1], submission_cell())
                old_ids = [cell['id'] for cell in previous['cells']]
                cells = {cell['id']: cell for cell in current['cells']}
                self.assertEqual(len(cells), len(current['cells']))
                self.assertEqual([c['id'] for c in current['cells'] if c['id'] in old_ids], old_ids)
                old_questions = {c['metadata']['tal']['question'] for c in previous['cells']
                                 if c['metadata']['tal']['role'] == 'answer'}
                self.assertEqual({q for q, role in indexed if role == 'answer'}, old_questions)
                total_questions += len(old_questions)
                for old in previous['cells']:
                    new = copy.deepcopy(cells[old['id']])
                    old = copy.deepcopy(old)
                    # The shared tutor is regenerated from the reviewed manifest;
                    # check_tutor_policy independently verifies its complete text.
                    if old['id'] == 'tal-tutor-instructions':
                        self.assertEqual(new['metadata']['tal'], old['metadata']['tal'])
                        continue
                    old_source = ''.join(old.pop('source'))
                    new_source = ''.join(new.pop('source'))
                    self.assertTrue(new_source.startswith(old_source),
                                    f"Original activity reduced or replaced: {path}, {old['id']}")
                    new['metadata'].pop('tal_review', None)
                    self.assertEqual(new, old, f"Original cell contract changed: {old['id']}")
                # Original root fields remain intact; only version and tutor context evolve.
                old_root = copy.deepcopy(previous)
                new_root = copy.deepcopy(current)
                for root in (old_root, new_root):
                    root.pop('cells')
                    root['metadata'].pop('tal_tutor')
                    root['metadata']['colab'].pop('aiContexts')
                    root['metadata']['tal'].pop('version')
                self.assertEqual(new_root, old_root)
        self.assertEqual(total_questions, 45)

    def test_td2_pedagogical_content_is_unchanged(self):
        baseline = json.loads((ROOT / 'tests/fixtures/s1_progression_v2_source_baseline.json').read_text())
        path = 'Notebooks TD/S1/TD2_S1_chaines_sequences.ipynb'
        current = json.loads((ROOT / path).read_text())
        cells = {cell['id']: cell for cell in current['cells']}
        for old in baseline['subjects'][path]['cells']:
            role = old['metadata']['tal']['role']
            if old['id'] == 'tal-tutor-instructions' or role == 'identification':
                continue
            with self.subTest(cell=old['id']):
                self.assertEqual(cells[old['id']]['source'], old['source'])


if __name__ == '__main__':
    unittest.main()
