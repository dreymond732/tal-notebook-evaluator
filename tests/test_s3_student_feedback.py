"""Formative evidence and authored examples, never execution of uploaded code."""
import ast
import contextlib
import copy
import importlib
import io
import json
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from notebook_contract import load_catalog, QUESTION_COUNTS
from report_evidence import answer_evidence
from s3_feedback import EXAMPLES, solution_for
from s3_audit_data import TEXT0
from s3_audit import check_audit
from test_revision_s3_v2 import fixture as revision_fixture
from s3_v2_fixture import notebook as trace_notebook


class S3StudentFeedbackTests(unittest.TestCase):
    def test_every_active_formative_question_has_a_compilable_specific_example(self):
        expected = {(entry['evaluator'], q)
                    for entry in load_catalog()
                    if entry['active'] and entry['semester'] == 'S3' and entry['mode'] == 'td'
                    for q in range(1, QUESTION_COUNTS[entry['evaluator']] + 1)}
        self.assertEqual(set(EXAMPLES), expected)
        self.assertEqual(len(expected), 71)
        for evaluator, q in expected:
            with self.subTest(evaluator=evaluator, question=q):
                code, explanation = solution_for(evaluator, q)
                tree = ast.parse(code)
                self.assertTrue(any(isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                                    and node.func.id == 'print' for node in ast.walk(tree)))
                self.assertGreater(len(explanation), 35)
                self.assertNotIn('controle', evaluator)

    def test_saved_evidence_keeps_source_stderr_plain_text_duplicates_and_malformed_trace(self):
        source = 'raise RuntimeError("NEVER_EXECUTE")\nprint("S3_TD0_Q1:", data)'
        outputs = [
            {'output_type': 'stream', 'name': 'stdout', 'text': ['S3_TD0_Q1: {bad}\n', 'S3_TD0_Q1: {}\n']},
            {'output_type': 'stream', 'name': 'stderr', 'text': 'avertissement\n'},
            {'output_type': 'execute_result', 'data': {'text/plain': ['texte ', 'affiché']}},
            {'output_type': 'error', 'ename': 'ValueError', 'evalue': 'erreur visible'},
            {'output_type': 'display_data', 'data': {'text/html': '<script>bad()</script>'}},
        ]
        cell = {'cell_type': 'code', 'metadata': {'tal': {'question': 'Q1', 'role': 'answer'}},
                'source': source, 'outputs': outputs}
        notebook = trace_notebook([cell], 'td0-s3')
        module = importlib.import_module('app_correction_TD0_S3')
        result = module.check_notebook(json.dumps(notebook), 'copie.ipynb')
        self.assertIsNone(result[4])
        detail = result[1][0]
        self.assertEqual(detail['student_code'], source)
        self.assertEqual(detail['answer_cells'], [2])
        self.assertIn('S3_TD0_Q1: {bad}\nS3_TD0_Q1: {}\n', detail['student_output'])
        self.assertIn('avertissement', detail['student_output'])
        self.assertIn('texte affiché', detail['student_output'])
        self.assertIn('ValueError: erreur visible', detail['student_output'])
        self.assertNotIn('<script>', detail['student_output'])
        self.assertEqual(detail['evaluation_status'], 'preuve_absente')
        self.assertTrue(detail['solution_code'])
        self.assertTrue(detail['action'])

    def test_missing_outputs_keep_the_actual_code_and_empty_output(self):
        notebook = trace_notebook([], 'td0-s3')
        notebook['cells'][1]['source'] = '# Mon essai\nresultat = 42'
        result = importlib.import_module('app_correction_TD0_S3').check_notebook(json.dumps(notebook), 'copie.ipynb')
        detail = result[1][0]
        self.assertEqual(detail['student_code'], '# Mon essai\nresultat = 42')
        self.assertEqual(detail['student_output'], '')
        self.assertNotEqual(detail['student_answer'], detail['diagnostic'])

    def test_non_text_traceback_does_not_crash_a_valid_submission(self):
        notebook = trace_notebook([], 'td0-s3')
        notebook['cells'][1]['outputs'] = [{'output_type': 'error', 'ename': 'TypeError',
                                          'traceback': ['ligne', None]}]
        result = importlib.import_module('app_correction_TD0_S3').check_notebook(json.dumps(notebook), 'copie.ipynb')
        self.assertIsNone(result[4])
        self.assertIn('null', result[1][0]['student_output'])

    def test_answer_positions_follow_the_uploaded_cell_order(self):
        notebook = trace_notebook([], 'td0-s3')
        notebook['cells'].reverse()
        answer = answer_evidence(notebook, 1)
        expected = next(i for i, c in enumerate(notebook['cells'], 1)
                        if c['metadata']['tal']['question'] == 'Q1')
        self.assertEqual(answer['answer_cells'], [expected])

    def test_revision_authored_sources_preserve_scores_and_expose_saved_outputs(self):
        for revision in range(3):
            evaluator = f'td-r{revision}-s3'
            notebook = revision_fixture(revision)
            for q, cell in enumerate(notebook['cells'][1:], 1):
                cell['source'] = solution_for(evaluator, q)[0]
            result = importlib.import_module('revision_s3').check_revision(json.dumps(notebook), evaluator)
            self.assertIsNone(result[4])
            self.assertEqual(result[0], 4, result[1])
            for q, detail in enumerate(result[1][:4], 1):
                self.assertEqual(detail['student_code'], notebook['cells'][q]['source'])
                self.assertEqual(detail['student_output'], notebook['cells'][q]['outputs'][0]['text'])
                self.assertEqual(detail['answer_cells'], [q + 1])
                self.assertTrue(detail['solution_code'])
            self.assertEqual(result[1][-1]['check'], 'Portée du score')

    def test_revision_malformed_and_duplicate_saved_traces_are_visible(self):
        for revision in range(3):
            notebook = revision_fixture(revision)
            notebook['cells'][1]['outputs'][0]['text'] = 'Résultat Q1 : {malforme}\nRésultat Q1 : {}\n'
            result = importlib.import_module('revision_s3').check_revision(json.dumps(notebook), f'td-r{revision}-s3')
            self.assertIsNone(result[4])
            detail = result[1][0]
            self.assertIn('{malforme}', detail['student_output'])
            self.assertEqual(detail['student_output'].count('Résultat Q1 :'), 2)
            self.assertEqual(detail['points'], 0)

    def test_authored_deterministic_examples_compute_expected_microcases(self):
        # Only trusted, versioned examples from s3_feedback are executed here.
        # The application itself reads uploaded code as text and never runs it.
        for td in (0, 4, 5, 6, 7):
            evaluator = f'td{td}-s3'
            module = importlib.import_module(f'app_correction_TD{td}_S3')
            with tempfile.TemporaryDirectory() as directory:
                resources = Path(directory)
                (resources / 'faguet_source.txt').write_bytes(TEXT0.encode())
                (resources / 'corpus_td0.txt').write_text(TEXT0, encoding='utf-8')
                namespace = {'texte_source': TEXT0, 'RESSOURCES': resources, 'plt': Mock()}
                for q in range(1, len(module.CHECKS) + 1):
                    code, _ = solution_for(evaluator, q)
                    if td == 0 and q == 1:
                        code = code.replace('"corpus_td0.txt"', repr(str(resources / 'corpus_td0.txt')))
                    with contextlib.redirect_stdout(io.StringIO()):
                        exec(compile(code, '<trusted-feedback-example>', 'exec'), namespace)
                    value = namespace[f'resultat_q{q}']
                    with self.subTest(evaluator=evaluator, question=q):
                        self.assertTrue(module.CHECKS[q-1]['validate'](value), value)
                        json.dumps(value, ensure_ascii=False)

    def test_shared_control_grading_never_gets_formative_solutions(self):
        from s3_audit import grade_traces
        checks = [dict(label='mesure', validate=lambda value: value == 3, feedback='critère')]
        detail = grade_traces({1: [(0, False)]}, {1: [(0, '3')]}, checks, [1])[1][0]
        self.assertNotIn('solution_code', detail)
        self.assertNotIn('solution_explanation', detail)

    def test_authored_td3_python_examples_use_the_actual_original_resources(self):
        module = importlib.import_module('app_correction_TD3_S3')
        from s3_audit_data import TEXT3
        directory = ROOT / 'Notebooks TD/S3/ressources'
        namespace = {'RESSOURCES': directory, 'hashlib': hashlib,
                     'source_test': TEXT3,
                     'texte_faguet': (directory / 'faguet_source.txt').read_bytes().decode('utf-8'),
                     'affirmations': json.loads((directory / 'affirmations_gemini.json').read_text()),
                     'citations': json.loads((directory / 'citations_gemini.json').read_text())}
        for q in (1, 2, 4, 5, 6):
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(solution_for('td3-s3', q)[0], '<trusted-feedback-example>', 'exec'), namespace)
            self.assertTrue(module.CHECKS[q-1]['validate'](namespace[f'resultat_q{q}']))

    def test_authored_r0_examples_compute_their_traces(self):
        from revision_s3 import TEXT_R0, check_revision
        notebook = revision_fixture(0)
        namespace = {'texte': TEXT_R0}
        for q, cell in enumerate(notebook['cells'][1:], 1):
            cell['source'] = solution_for('td-r0-s3', q)[0]
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exec(compile(cell['source'], '<trusted-feedback-example>', 'exec'), namespace)
            cell['outputs'][0]['text'] = output.getvalue()
        result = check_revision(json.dumps(notebook), 'td-r0-s3')
        self.assertEqual(result[0], 4, result[1])


if __name__ == '__main__':
    unittest.main()
