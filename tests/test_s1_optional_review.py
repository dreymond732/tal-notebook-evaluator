"""Formative S1 reports do not impose review of every student's explanations."""
import importlib
import json
import unittest

from test_s1_review_metadata import subjects, observed_copy
from test_s2_contract_v2 import fixture
from s1_revision import check_saved_notebook
from notebook_contract import S2_QUESTION_COUNTS


class S1OptionalReviewTests(unittest.TestCase):
    def test_seven_real_graders_keep_scores_and_make_individual_review_optional(self):
        for number, entry, subject in subjects():
            result = importlib.import_module(f'app_correction_TD{number}_S1').check_notebook(
                json.dumps(observed_copy(number, subject)), 'test.ipynb')
            with self.subTest(evaluator=entry['id']):
                self.assertIsNone(result[4])
                self.assertEqual(result[0], 1)
                self.assertEqual(result[3]['relecture_humaine'], 'facultative')
                self.assertEqual(result[3]['score_nature'], 'technique_provisoire')
                self.assertTrue(result[3]['review_evidence'])

    def test_shared_engine_keeps_review_required_for_all_s2_subjects(self):
        for evaluator in S2_QUESTION_COUNTS:
            result = check_saved_notebook(json.dumps(fixture(evaluator)), 'test.ipynb', evaluator,
                                         [{'label': 'Valeur', 'traces': {'Q1': (3,)}, 'points': 1,
                                           'feedback': 'Valeur entière.'}])
            with self.subTest(evaluator=evaluator):
                self.assertIsNone(result[4])
                self.assertEqual(result[3]['relecture_humaine'], 'requise')
                self.assertEqual(result[0], 0)


if __name__ == '__main__':
    unittest.main()
