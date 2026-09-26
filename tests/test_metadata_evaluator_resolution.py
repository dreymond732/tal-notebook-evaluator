"""Non-executing regression checks for cell metadata across evaluator families."""
import copy
import importlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
sys.path.insert(0, str(ROOT / 'tests'))

from engine import run_evaluation
from formative_s3 import check_formative_notebook
from s3_audit import check_audit
from s3_controls import check_control
import outils
import app_correction_controle_S1 as control_s1
from notebook_contract import load_catalog
from routes import EVALUATORS
from test_td2_s1 import fixture as td2_fixture, grade as td2_grade


def cell(source='', output='', question=None, role='answer'):
    result = {'cell_type': 'code', 'source': source, 'outputs': [
        {'output_type': 'stream', 'name': 'stdout', 'text': output}] if output else []}
    if question is not None:
        result['metadata'] = {'tal': {'question': question, 'role': role}}
    return result


def encoded(cells):
    return json.dumps({'cells': cells})


def engine(cells):
    return run_evaluation(encoded(cells), 'renamed.ipynb', {'Q1': 3}, {'Q1': 1}, 1, 'test')


def audit(cells):
    return check_audit(encoded(cells), 'renamed.ipynb', 1,
                       [{'label': 'Mesure', 'validate': lambda v: v == {'n': 3}, 'feedback': 'Mesure'}])


def control(cells):
    return check_control(encoded(cells), 'renamed.ipynb', 1,
                         [{'label': 'Mesure', 'validate': lambda v, ctx: v == {'n': 3}, 'feedback': 'Mesure'}] * 7)


class MetadataResolutionTests(unittest.TestCase):
    def test_all_catalogued_subjects_keep_existing_scores_and_feedback(self):
        for entry in load_catalog():
            if not entry['active']:
                continue
            with self.subTest(evaluator=entry['evaluator']):
                notebook = json.loads((ROOT / entry['notebook']).read_text())
                legacy = copy.deepcopy(notebook)
                legacy.get('metadata', {}).pop('tal', None)
                for item in legacy['cells']:
                    item.get('metadata', {}).pop('tal', None)
                evaluate = importlib.import_module(EVALUATORS[entry['evaluator']][1]).check_notebook
                migrated_result = evaluate(json.dumps(notebook), 'renamed.ipynb')
                legacy_result = evaluate(json.dumps(legacy), 'renamed.ipynb')
                # Identification can now resolve a tagged cell whose historical
                # comment did not match. Grading, feedback and errors must not vary.
                self.assertEqual(migrated_result[:3], legacy_result[:3])
                self.assertEqual(migrated_result[4], legacy_result[4])
                self.assertEqual(migrated_result[3].get('score_brut'), legacy_result[3].get('score_brut'))

    def test_engine_same_result_with_metadata_and_no_execution(self):
        legacy = cell('raise RuntimeError("must not run")', 'Résultat Q1 : 3')
        tagged = copy.deepcopy(legacy)
        tagged['metadata'] = {'tal': {'question': 'Q1', 'role': 'answer'}}
        self.assertEqual(engine([legacy]), engine([tagged]))
        self.assertEqual(engine([tagged])[0], 1)

    def test_engine_ignores_decoy_and_missing_metadata_answer(self):
        tagged = cell(output='Résultat Q1 : 3', question='Q1')
        decoy = cell(output='Résultat Q1 : 999', question='example', role='example')
        self.assertEqual(engine([decoy, tagged])[0], 1)
        tagged['metadata']['tal']['question'] = 'Q2'
        self.assertEqual(engine([tagged])[0], 0)
        self.assertEqual(engine([cell(question='Q1')])[0], 0)

    def test_s3_keeps_same_cell_ast_and_trace_requirements(self):
        for evaluate, prefix in [(audit, 'S3_TD1'), (control, 'S3_C1')]:
            with self.subTest(prefix=prefix):
                legacy = cell(f'print("{prefix}_Q1:", value)', f'{prefix}_Q1: {{"n":3}}')
                tagged = copy.deepcopy(legacy)
                tagged['metadata'] = {'tal': {'question': 'Q1', 'role': 'answer'}}
                self.assertEqual(evaluate([legacy]), evaluate([tagged]))
                self.assertGreater(evaluate([tagged])[0], 0)
                tagged['source'] = '# ' + tagged['source']
                self.assertEqual(evaluate([tagged])[0], 0)
                tagged['metadata']['tal']['question'] = 'Q2'
                self.assertEqual(evaluate([tagged])[0], 0)

    def test_s3_decoys_do_not_supply_answer(self):
        answer = cell(question='Q1')
        decoy = cell('print("S3_TD1_Q1:", value)', 'S3_TD1_Q1: {"n":3}', 'example', 'example')
        self.assertEqual(audit([answer, decoy])[0], 0)

    def test_duplicate_metadata_is_error_for_all_families(self):
        duplicate = cell(question='Q1')
        evaluations = [engine, audit, control,
                       lambda cells: check_formative_notebook(encoded(cells), [], 1),
                       lambda cells: td2_grade({'cells': cells}),
                       lambda cells: control_s1.check_notebook(encoded(cells), 'copy.ipynb')]
        for evaluate in evaluations:
            with self.subTest(evaluator=evaluate):
                result = evaluate([duplicate, copy.deepcopy(duplicate)])
                self.assertEqual(result[0], 0)
                self.assertTrue(result[4])

    def test_infrastructure_never_scores_or_changes_legacy_resolution(self):
        answer = cell(output='Résultat Q1 : 3')
        infra = cell('reponse_Q1 = 999', 'Résultat Q1 : 999', 'submission', 'submission')
        self.assertEqual(engine([infra, answer]), engine([answer]))
        self.assertEqual(engine([infra])[0], 0)
        checks = [{'label': 'Exercice', 'source': ['reponse_Q1'], 'output': 'Résultat Q1', 'feedback': 'Exercice', 'points': 1}]
        self.assertEqual(check_formative_notebook(encoded([infra]), checks, 1)[0], 0)

    def test_formative_keeps_global_coverage_of_examples_and_answers(self):
        cells = [cell('base = "texte"', question='example', role='example'),
                 cell('resultat = base.lower()', 'Résultat Q1', 'Q1')]
        checks = [{'label': 'Exercice', 'source': ['base =', '.lower()'], 'output': 'Résultat Q1', 'feedback': 'Exercice', 'points': 1}]
        result = check_formative_notebook(encoded(cells), checks, 1)
        legacy = copy.deepcopy(cells)
        for item in legacy:
            item.pop('metadata')
        self.assertEqual(result, check_formative_notebook(encoded(legacy), checks, 1))
        self.assertEqual(result[0], 1)

    def test_td2_cross_cell_dependencies_subquestions_and_infrastructure(self):
        legacy = td2_fixture()
        migrated = copy.deepcopy(legacy)
        for q, item in enumerate(migrated['cells'], 1):
            item['metadata'] = {'tal': {'question': f'Q{q}', 'role': 'answer'}}
        migrated['cells'].append(cell('from IPython.display import HTML, display', '', 'submission', 'submission'))
        self.assertEqual(td2_grade(legacy), td2_grade(migrated))
        self.assertEqual(td2_grade(migrated)[0], 7)

    def test_identity_uses_values_in_selected_cell_not_metadata_values(self):
        identity = cell('nom="Modele"\nprenom="Test"\nclasse="S1"', question='identity', role='identification')
        decoy = cell('# Complétez les informations entre les guillemets.\nnom="Intrus"')
        self.assertEqual(outils.extract_identification_info([decoy, identity])['nom'], 'Modele')
        identity['source'] = ''
        identity['metadata']['tal']['nom'] = 'Invented'
        self.assertEqual(outils.extract_identification_info([identity])['nom'], 'NON_RENSEIGNE')

    def test_s1_control_variable_and_output_fallback_target_cells(self):
        cells = [cell('valeur_Q2_deb = 19\nvaleur_Q2_fin = 29', question='Q2'),
                 cell('valeur_Q2_deb = 0\nvaleur_Q2_fin = 0', 'Résultat Q1 : 150', 'example', 'example'),
                 cell(output='Résultat Q1 : 150', question='Q1')]
        self.assertEqual(outils.extract_code_variable({'cells': cells}, 'valeur_Q2_deb', 'numeric'), 19)
        self.assertEqual(outils.get_ipynb_raw_output({'cells': cells}, 'Résultat Q1 :'), 'Résultat Q1 : 150')
        cells[-1]['outputs'] = []
        self.assertEqual(outils.get_ipynb_raw_output({'cells': cells}, 'Résultat Q1 :'), '')


if __name__ == '__main__':
    unittest.main()
