"""Independent saved traces for the S3 review; no student code is executed."""
import copy
import importlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))

from test_revision_s3_v2 import fixture, grade
from test_s3_audit import notebook, trace
from s3_audit import grade_traces


class RevisionRegressionTests(unittest.TestCase):
    def test_revision_review_includes_q2_and_practice_as_escaped_text(self):
        from app import create_app
        from flask import render_template
        nb = fixture(1)
        nb['cells'][2]['source'] += '\n# Observation Q2 : le modèle est discutable.'
        nb['cells'].append({'cell_type': 'markdown', 'source': '<script>essai</script>',
                            'metadata': {'tal': {'question': 'practice-q2', 'role': 'practice'},
                                         'tal_review': {'question': 'Q2'}}})
        score, details, maximum, info, error = grade(1, nb)
        self.assertIsNone(error)
        self.assertEqual(score, 4)
        q2 = next(group for group in info['review_evidence'] if group['question'] == 'Q2')
        self.assertEqual(len(q2['cells']), 2)
        self.assertIn('Observation Q2', q2['cells'][0]['source'])
        with create_app().test_request_context('/'):
            html = render_template('corrector_template.html', display_name='Révision',
                                   student_info=info, details=details, score=score,
                                   max_score=maximum, evaluator='td-r1-s3')
        self.assertIn('&lt;script&gt;essai&lt;/script&gt;', html)
        self.assertNotIn('<script>essai</script>', html)

    def test_r2_annotations_can_be_correct_without_q1_function(self):
        nb = fixture(2)
        nb['cells'][1]['source'] = ''
        nb['cells'][1]['outputs'] = []
        result = grade(2, nb)
        self.assertEqual(result[1][0]['points'], 0)
        self.assertEqual(result[1][1]['points'], 1)
        self.assertIsNone(result[4])

    def test_r1_self_contained_questions_do_not_depend_on_missing_q1(self):
        nb = fixture(1)
        nb['cells'][1]['source'], nb['cells'][1]['outputs'] = '', []
        for cell in nb['cells'][2:]:
            cell['source'] = 'doc=nlp(texte)\n' + cell['source']
        self.assertEqual(grade(1, nb)[0], 3)
        # A calculation omitted everywhere remains unsupported.
        for cell in nb['cells'][2:]:
            cell['source'] = cell['source'].replace('doc=nlp(texte)\n', '')
        self.assertEqual(grade(1, nb)[0], 0)

    def test_r2_stopword_filter_equivalent_conditions(self):
        for condition in ('token.is_stop != True', 'token.is_stop is not True',
                          'False == token.is_stop'):
            with self.subTest(condition=condition):
                nb = fixture(2)
                nb['cells'][3]['source'] = nb['cells'][3]['source'].replace('not token.is_stop', condition)
                self.assertEqual(grade(2, nb)[0], 4)
        nb = fixture(2)
        nb['cells'][3]['source'] = nb['cells'][3]['source'].replace(
            "    lemmes=[token.lemma_ for token in doc if token.pos_=='NOUN' and not token.is_stop and token.lemma_ not in stopwords]",
            "    lemmes=[]\n    for token in doc:\n        if token.is_stop:\n            continue\n        if token.pos_=='NOUN' and token.lemma_ not in stopwords:\n            lemmes.append(token.lemma_)")
        self.assertEqual(grade(2, nb)[0], 4)

    def test_positive_stopword_selection_is_not_an_exclusion(self):
        nb = fixture(2)
        nb['cells'][3]['source'] = nb['cells'][3]['source'].replace('not token.is_stop', 'token.is_stop == True')
        self.assertEqual(grade(2, nb)[1][2]['points'], 0)

    def test_pos_filter_direction_and_mirror_syntax(self):
        for revision, question, category in ((1, 3, 'NOUN'), (1, 4, 'VERB'), (2, 1, 'NOUN'), (2, 3, 'NOUN')):
            original = f"token.pos_=='{category}'"
            for replacement, points in ((f"token.pos_!='{category}'", 0),
                                        (f"'{category}'==token.pos_", 1),
                                        (f"not (token.pos_!='{category}')", 1),
                                        (f"not (token.pos_=='{category}')", 0)):
                with self.subTest(revision=revision, question=question, replacement=replacement):
                    nb = fixture(revision)
                    nb['cells'][question]['source'] = nb['cells'][question]['source'].replace(original, replacement)
                    self.assertEqual(grade(revision, nb)[1][question - 1]['points'], points)

    def test_pos_filter_can_skip_other_categories_in_a_loop(self):
        nb = fixture(1)
        nb['cells'][3]['source'] = ("noms=[]\nfor token in doc:\n"
                                    "    if token.pos_!='NOUN':\n        continue\n"
                                    "    noms.append(token.lemma_)\nprint('Résultat Q3 :',noms)")
        self.assertEqual(grade(1, nb)[1][2]['points'], 1)
        nb['cells'][3]['source'] = nb['cells'][3]['source'].replace("pos_!='NOUN'", "pos_=='NOUN'")
        self.assertEqual(grade(1, nb)[1][2]['points'], 0)

    def test_r2_early_continue_can_exclude_both_stopwords_and_lemmas(self):
        source = ("    lemmes=[]\n    for token in doc:\n"
                  "        if token.is_stop:\n            continue\n"
                  "        if token.lemma_.lower() in stopwords:\n            continue\n"
                  "        if token.pos_=='NOUN':\n            lemmes.append(token.lemma_)")
        original = "    lemmes=[token.lemma_ for token in doc if token.pos_=='NOUN' and not token.is_stop and token.lemma_ not in stopwords]"
        for replacement, points in [(source, 1),
                                    (source.replace('token.is_stop', 'other.is_stop'), 0),
                                    (source.replace('token.lemma_.lower() in', 'other.lemma_.lower() in'), 0),
                                    (source.replace('token.lemma_.lower() in', 'token.text.lower() in'), 0),
                                    (source.replace('token.is_stop:\n            continue', 'token.is_stop:\n            pass'), 0)]:
            nb = fixture(2)
            nb['cells'][3]['source'] = nb['cells'][3]['source'].replace(original, replacement)
            self.assertEqual(grade(2, nb)[1][2]['points'], points)

    def test_dead_return_cannot_supply_computational_evidence(self):
        nb = fixture(0)
        nb['cells'][1]['source'] = nb['cells'][1]['source'].replace(
            '    return len(texte.split())', '    return 15\n    return len(texte.split())')
        self.assertEqual(grade(0, nb)[1][0]['points'], 0)
        # Conversely, a later dead literal cannot erase a valid first return.
        nb = fixture(0)
        nb['cells'][1]['source'] = nb['cells'][1]['source'].replace(
            '    return len(texte.split())', '    return len(texte.split())\n    return 15')
        self.assertEqual(grade(0, nb)[1][0]['points'], 1)

    def test_practice_and_provided_cells_cannot_supply_revision_answers(self):
        for revision in range(3):
            for role in ('practice', 'provided', 'example'):
                nb = fixture(revision)
                for cell in list(nb['cells'][1:]):
                    decoy = copy.deepcopy(cell)
                    decoy['metadata']['tal']['role'] = role
                    nb['cells'].append(decoy)
                    cell['source'], cell['outputs'] = '', []
                result = grade(revision, nb)
                self.assertIsNone(result[4])
                self.assertEqual(result[0], 0)


class AuditRegressionTests(unittest.TestCase):
    def test_excluding_all_nouns_is_an_experiment_but_figures_need_data(self):
        from app_correction_TD2_S3 import CHECKS
        before = {'notice': 2, 'livre': 2, 'lecteur': 1}
        values = {3: {'exclusions': ['notice', 'livre', 'lecteur'], 'avant': before,
                      'apres': {}, 'justification': ''},
                  6: {'frequences': {}, 'hypothese': '', 'verification': ''}}
        displays = {q: [(q, False)] for q in values}
        records = {q: [(q, json.dumps(v))] for q, v in values.items()}
        score, details, deferred = grade_traces(displays, records, CHECKS, [1] * 7)
        self.assertEqual(details[2]['points'], 1)
        self.assertEqual(details[5]['evaluation_status'], 'non_verifiable')
        self.assertEqual(deferred, 1)
        self.assertIn('réexécutez Q3 puis Q6', details[5]['correct_answer'])
        self.assertEqual(details[2]['missing_fields'], ['justification'])
        self.assertEqual(details[5]['missing_fields'], ['hypothese', 'verification'])

    def test_blank_explanation_is_reported_without_changing_quantitative_score(self):
        from app_correction_TD1_S3 import CHECKS
        value = {'split': 47, 'tokens': 56, 'non_ponctuation': 41, 'interpretation': ''}
        score, details, _ = grade_traces({5: [(0, False)]}, {5: [(0, json.dumps(value))]}, CHECKS, [1] * 6)
        self.assertEqual(score, 1)
        self.assertEqual(details[4]['missing_fields'], ['interpretation'])
        self.assertIn('sans point automatique', details[4]['diagnostic'])

    def test_practice_provided_examples_cannot_supply_any_td_trace(self):
        for td in range(8):
            module = importlib.import_module(f'app_correction_TD{td}_S3')
            for role in ('practice', 'provided', 'example'):
                decoy = trace(td, 1, {'caracteres': 277})
                decoy['metadata'] = {'tal': {'question': 'Q1', 'role': role}}
                blank = {'cell_type': 'code', 'source': '', 'outputs': [],
                         'metadata': {'tal': {'question': 'Q1', 'role': 'answer'}}}
                result = module.check_notebook(notebook([blank, decoy], td), 'copie.ipynb')
                self.assertIsNone(result[4], (td, role, result[4]))
                self.assertEqual(result[0], 0)


if __name__ == '__main__':
    unittest.main()
