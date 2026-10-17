"""S1 report evidence and executable *application-owned* teaching examples.

Only SOLUTIONS and subject preparation written by the course authors are run
here in a temporary directory. Submitted answers remain inert in the evaluator.
"""
import ast
from contextlib import redirect_stdout
import copy
import importlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from s1_feedback import SOLUTIONS, enrich_s1_details


def subject(td):
    path = next((ROOT / 'Notebooks TD' / 'S1').glob(f'TD{td}_*.ipynb'))
    notebook = json.loads(path.read_text())
    for cell in notebook['cells']:
        if cell.get('metadata', {}).get('tal', {}).get('role') == 'identification':
            cell['source'] = 'nom="Essai"\nprenom="Alex"\nclasse="S1"\nnumero_etudiant="SYNTHETIQUE-001"'
    return notebook


def evaluate(td, notebook):
    module = importlib.import_module(f'app_correction_TD{td}_S1')
    return module.check_notebook(json.dumps(notebook), 'synthetic.ipynb')


class S1FeedbackTests(unittest.TestCase):
    def test_all_45_examples_compile_run_in_order_and_satisfy_existing_rubrics(self):
        total = 0
        for td, solutions in SOLUTIONS.items():
            notebook = subject(td)
            namespace = {}
            with tempfile.TemporaryDirectory() as temp:
                previous = os.getcwd()
                try:
                    os.chdir(temp)
                    for cell in notebook['cells']:
                        tag = cell.get('metadata', {}).get('tal', {})
                        if tag.get('role') == 'provided':
                            # Trusted course preparation, never submission code.
                            with redirect_stdout(io.StringIO()):
                                exec(compile(''.join(cell['source']), '<course preparation>', 'exec'), namespace)
                        elif tag.get('role') == 'answer':
                            number = int(tag['question'][1:])
                            code = solutions[number - 1]['solution_code']
                            ast.parse(code)
                            stdout = io.StringIO()
                            with redirect_stdout(stdout):
                                exec(compile(code, '<trusted teaching example>', 'exec'), namespace)
                            cell['source'] = code
                            cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': stdout.getvalue()}]
                            total += 1
                finally:
                    os.chdir(previous)
                score, details, maximum, info, error = evaluate(td, notebook)
                with self.subTest(td=td):
                    self.assertIsNone(error)
                    self.assertEqual(score, len(solutions))
                    self.assertEqual(maximum, len(solutions))
                    answers = [c for c in notebook['cells'] if c.get('metadata', {}).get('tal', {}).get('role') == 'answer']
                    for number, cell in enumerate(answers):
                        self.assertEqual(details[number]['student_code'], cell['source'])
                        self.assertEqual(details[number]['student_output'], cell['outputs'][0]['text'])
                        self.assertEqual(details[number]['solution_code'], solutions[number]['solution_code'])
                        self.assertTrue(details[number]['solution_explanation'])
                        self.assertTrue(details[number]['diagnostic'])
                        self.assertTrue(details[number]['action'])
                        self.assertEqual(notebook['cells'][details[number]['answer_cells'][0] - 1], cell)
        self.assertEqual(total, 45)

    def test_blank_and_failed_answers_remain_visible_without_execution(self):
        for td in range(1, 8):
            notebook = subject(td)
            answer = next(c for c in notebook['cells'] if c.get('metadata', {}).get('tal', {}).get('role') == 'answer')
            source = 'raise RuntimeError("Do not execute submitted source")\n# Résultat Q1 : deliberately missing'
            answer['source'] = source.splitlines(keepends=True)
            answer['outputs'] = [
                {'output_type': 'stream', 'name': 'stderr', 'text': ['warning\n']},
                {'output_type': 'error', 'ename': 'NameError', 'evalue': "name 'resultat' is not defined"},
            ]
            # Load trusted application modules before forbidding exec itself.
            importlib.import_module(f'app_correction_TD{td}_S1')
            with patch('builtins.exec', side_effect=AssertionError('student execution forbidden')):
                result = evaluate(td, notebook)
            with self.subTest(td=td):
                self.assertIsNone(result[4])
                detail = result[1][0]
                self.assertEqual(detail['student_code'], source)
                self.assertEqual(detail['student_output'], "warning\nNameError: name 'resultat' is not defined")
                self.assertEqual(detail['points'], 0)
                self.assertIn('raise RuntimeError', detail['student_code'])
                empty = result[1][1]
                self.assertTrue(empty['student_code'])  # original subject scaffolding
                self.assertEqual(empty['student_output'], '')
                self.assertTrue(empty['answer_cells'])

    def test_unrecognized_and_duplicate_saved_traces_are_shown_in_full(self):
        notebook = subject(1)
        answer = next(c for c in notebook['cells'] if c.get('metadata', {}).get('tal', {}).get('role') == 'answer')
        answer['source'] = 'cout_total=15\nprint("Résultat Q1 :", cout_total)'
        output = 'before\nRésultat Q1 : 15\nRésultat Q1 : 99\nafter\n'
        answer['outputs'] = [{'output_type': 'stream', 'text': output}]
        result = evaluate(1, notebook)
        self.assertIsNone(result[4])
        self.assertEqual(result[1][0]['student_output'], output)
        self.assertEqual(result[1][0]['points'], 0)
        self.assertEqual(result[1][0]['student_code'], answer['source'])

    def test_feedback_enrichment_leaves_non_s1_evaluations_and_scores_unchanged(self):
        original = [{'points': 0.5, 'max_points': 1, 'diagnostic': 'existing feedback'}]
        details = copy.deepcopy(original)
        self.assertIs(enrich_s1_details(subject(1), 'td2-S2', details), details)
        self.assertEqual(details, original)
        # Expansion IDs receive their own example, never the historical TD3 answer.
        details = copy.deepcopy(original)
        enrich_s1_details(subject(1), 'td3-one-s1', details)
        self.assertTrue(details[0]['answer_cells'])
        self.assertIn('mots[0]', details[0]['solution_code'])
        self.assertNotIn('outils.append', details[0]['solution_code'])
        self.assertEqual(details[0]['points'], 0.5)

    def test_diagnostics_locate_missing_companion_display_and_dependencies(self):
        details = [dict(points=0, max_points=1, evaluation_status='preuve_absente',
                        diagnostic='Preuve absente ou inexploitable : Q6b.')]
        enrich_s1_details(subject(1), 'td1-s1', details)
        self.assertIn('Q6b', details[0]['diagnostic'])
        self.assertIn('Q6b', details[0]['action'])
        self.assertEqual(details[0]['technical_diagnostic'], 'Preuve absente ou inexploitable : Q6b.')
        details = [dict(points=0, max_points=1, evaluation_status='non_verifiable',
                        diagnostic='Construction non vérifiable : dépendance Q2 absente.')]
        enrich_s1_details(subject(5), 'td5-s1', details)
        self.assertIn('Q2', details[0]['diagnostic'])
        self.assertIn('Q2', details[0]['action'])

    def test_td2_examples_use_only_notions_allowed_before_loops(self):
        forbidden = (ast.For, ast.While, ast.ListComp, ast.SetComp, ast.DictComp,
                     ast.Import, ast.ImportFrom, ast.FunctionDef, ast.If)
        for solution in SOLUTIONS[2]:
            self.assertFalse(any(isinstance(node, forbidden) for node in ast.walk(ast.parse(solution['solution_code']))))


if __name__ == '__main__':
    unittest.main()
