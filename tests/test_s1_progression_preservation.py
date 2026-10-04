"""Preserve executable and assessment contracts while permitting editorial revision.

The previous prose-prefix assertion was appropriate for additive enrichment, but
prevented the explicitly requested rewrite of confusing statements (including
TD2). Both exact historical snapshots remain evidence for independent coverage
review; no automated assertion claims to validate pedagogical equivalence.
"""
import ast
import copy
import json
import re
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from notebook_contract import resolve_notebook, validate_cell_metadata
from prepare_student_notebooks import submission_cell

BASELINE = ROOT / 'tests/fixtures/s1_editorial_source_baseline.json'
HISTORICAL = ROOT / 'tests/fixtures/s1_progression_v2_source_baseline.json'


class S1ProgressionPreservationTests(unittest.TestCase):
    def test_seven_v2_subjects_preserve_code_ids_and_contracts_in_order(self):
        baseline = json.loads(BASELINE.read_text())
        self.assertEqual(baseline['source_commit'], '670e6c104a6d0228fcad8a91cfc8776117b038bb')
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
                    old_source = ''.join(old.pop('source'))
                    new_source = ''.join(new.pop('source'))
                    if old['cell_type'] == 'code':
                        # All existing code, including examples and exercises:
                        # comments may be clarified, executable meaning stays.
                        self.assertEqual(ast.dump(ast.parse(new_source)), ast.dump(ast.parse(old_source)), old['id'])
                        if old['metadata']['tal']['role'] == 'answer':
                            # Supplied print calls are initially commented out;
                            # AST alone would overlook removal of their markers.
                            def displays(source):
                                return [ast.dump(ast.parse(line.strip()[1:].strip()))
                                        for line in source.splitlines()
                                        if re.match(r'^\s*#\s*print\(', line)]
                            expected_displays = displays(old_source)
                            if (path == 'Notebooks TD/S1/TD6_S1_fichiers_csv.ipynb'
                                    and old['id'] == 'td6-s1-answer-q6'):
                                # The old unescaped multiline display explicitly
                                # said to remain disabled. The existing repr
                                # display is the actual v2 submission contract.
                                obsolete = ast.dump(ast.parse(
                                    'print("Résultat Q6 :", Path("affiliations_uniques.csv").read_text(encoding="utf-8"))'))
                                self.assertIn(obsolete, expected_displays)
                                expected_displays.remove(obsolete)
                            self.assertEqual(displays(new_source), expected_displays, old['id'])
                    self.assertEqual(new, old, f"Original cell metadata/state changed: {old['id']}")
                old_root = copy.deepcopy(previous)
                new_root = copy.deepcopy(current)
                for root in (old_root, new_root):
                    root.pop('cells')
                    # Dedicated tutor profiles are reviewed separately by the
                    # Prof and the complete tutor synchronization checks.
                    root['metadata'].pop('tal_tutor')
                    root['metadata']['colab'].pop('aiContexts')
                self.assertEqual(new_root, old_root)
        self.assertEqual(total_questions, 45)

    def test_historical_activities_still_have_their_ids_and_answer_contracts(self):
        historical = json.loads(HISTORICAL.read_text())
        self.assertEqual(historical['source_commit'], '322abf53b4a1ff96c1652acfa21b4d27185bfa1a')
        for path, previous in historical['subjects'].items():
            current = json.loads((ROOT / path).read_text())
            cells = {cell['id']: cell for cell in current['cells']}
            old_ids = [cell['id'] for cell in previous['cells']]
            self.assertEqual([c['id'] for c in current['cells'] if c['id'] in old_ids], old_ids)
            for old in previous['cells']:
                with self.subTest(notebook=path, cell=old['id']):
                    self.assertEqual(cells[old['id']]['metadata']['tal'], old['metadata']['tal'])


if __name__ == '__main__':
    unittest.main()
