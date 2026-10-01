"""Regression tests for inert S1 proof collection, strict types and routing."""
import ast
import json
import io
import tempfile
from unittest.mock import patch
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from s1_revision import collect, matches, same
from notebook_contract import ContractError, WRONG_VERSION, resolve_notebook, strict_contract_identity


def answer(source, output='Résultat Q1 : 3\n', question='Q1'):
    return {'cell_type': 'code', 'metadata': {'tal': {'role': 'answer', 'question': question}},
            'source': source, 'outputs': [{'output_type': 'stream', 'name': 'stdout', 'text': output}]}


def notebook(source):
    return {'cells': [answer(source)]}


class InertS1EngineTests(unittest.TestCase):
    def proof(self, source):
        displays, _ = collect(notebook(source))
        return displays['Q1'][0][1]

    def test_typed_literal_outputs_and_unordered_containers(self):
        self.assertTrue(matches("{'b': 2, 'a': 1} {'texte', 'corpus'}", ({'a': 1, 'b': 2}, {'corpus', 'texte'})))
        self.assertFalse(matches("{'a': True}", ({'a': 1},)))
        self.assertFalse(matches("{'a': 0, 'a': 1}", ({'a': 1},)))
        self.assertFalse(matches('False', (0,)))
        self.assertFalse(matches('3.0', (3,)))
        self.assertFalse(matches('nan', (1.0,)))
        self.assertFalse(same([True], [1]))
        self.assertTrue(matches("100 <class 'int'>", (100, "<class 'int'>")))
        self.assertTrue(matches('Le TAL 3', ('Le TAL', 3)))

    def test_linked_assignments_only_before_print(self):
        proof = self.proof('unused = len("abc")\nvalue = 3\nprint("Résultat Q1 :", value)\nlater = len("abc")')
        self.assertFalse(proof.calls('len'))
        proof = self.proof('value = len("abc")\nother = value\nprint("Résultat Q1 :", other)')
        self.assertTrue(proof.calls('len'))

    def test_called_functions_follow_returns_not_dead_assignments(self):
        proof = self.proof('def f(x):\n    unused = len(x)\n    return 3\nprint("Résultat Q1 :", f("abc"))')
        self.assertFalse(proof.calls('len'))
        proof = self.proof('def f(x):\n    return len(x)\nprint("Résultat Q1 :", f("abc"))')
        self.assertTrue(proof.calls('len'))
        proof = self.proof('def f(x):\n    return 3\n    return len(x)\nprint("Résultat Q1 :", f("abc"))')
        self.assertFalse(proof.calls('len'))
        proof = self.proof('def unused(x):\n    return len(x)\nprint("Résultat Q1 :", 3)')
        self.assertFalse(proof.calls('len'))

    def test_aliases_and_mutating_loop_are_linked(self):
        proof = self.proof('import re as regex\nvalue = regex.findall(r"x", "xxx")\nprint("Résultat Q1 :", value)')
        self.assertTrue(proof.calls('re.findall'))
        proof = self.proof('values = []\nfor word in ["abc"]:\n    values.append(word.upper())\nprint("Résultat Q1 :", values)')
        self.assertTrue(proof.has_node(ast.For))
        self.assertTrue(proof.calls('upper'))

    def test_reassigned_function_does_not_keep_old_body(self):
        proof = self.proof('def f(x):\n    return len(x)\nf = lambda x: 3\nprint("Résultat Q1 :", f("abc"))')
        self.assertFalse(proof.calls('len'))

    def test_statically_dead_loops_do_not_supply_syntax(self):
        for code in ('values=[]\nfor x in []:\n    values.append(x.upper())',
                     'values=[]\nwhile False:\n    values.append("x".upper())'):
            proof = self.proof(code + '\nprint("Résultat Q1 :", values)')
            self.assertFalse(proof.calls('upper'))
        proof = self.proof('def f(x):\n    while False:\n        return len(x)\n    return 3\nprint("Résultat Q1 :", f("abc"))')
        self.assertFalse(proof.calls('len'))

    def test_no_student_execution_and_no_example_credit(self):
        proof = self.proof('raise RuntimeError("NEVER EXECUTE")\nprint("Résultat Q1 :", len("abc"))')
        self.assertTrue(proof.calls('len'))
        nb = notebook('print("Résultat Q1 :", value)')
        extra = answer('value = len("abc")')
        extra['metadata']['tal'] = {'role': 'example', 'question': 'example1'}
        nb['cells'].insert(0, extra)
        displays, _ = collect(nb)
        self.assertFalse(displays['Q1'][0][1].calls('len'))

    def test_wrong_cell_or_ambiguous_print_has_no_unique_proof(self):
        displays, records = collect(notebook('print("Résultat Q2 :", 3)'))
        self.assertNotIn('Q2', displays)
        displays, _ = collect(notebook('print("Résultat Q1 :", 3)\nprint("Résultat Q1 :", 3)'))
        self.assertEqual(len(displays['Q1']), 2)

    def test_every_s1_old_version_rejected_on_direct_route(self):
        for number in range(1, 8):
            with self.subTest(number=number):
                for metadata in ({}, {'tal': {'id': f'TD{number}_S1', 'evaluator': f'td{number}-s1', 'version': 1}}):
                    nb = {'metadata': metadata, 'cells': []}
                    with self.assertRaises(ContractError):
                        resolve_notebook(nb, f'td{number}-s1', require_metadata=False)


class S1RouteGateTests(unittest.TestCase):
    def setUp(self):
        from app import create_app
        import outils
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        patcher = patch.object(outils, 'BASE_DIR', self.temp.name)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.client = create_app().test_client()

    def fixture(self, td=1, number='900001'):
        from notebook_contract import S1_QUESTION_COUNTS
        evaluator = f'td{td}-s1'
        cells = [answer('', '', f'Q{q}') for q in range(1, S1_QUESTION_COUNTS[evaluator] + 1)]
        cells.append({'cell_type': 'code', 'metadata': {'tal': {'role': 'identification', 'question': 'identity'}},
                      'source': f'prenom="Alice"\nnom="Dupont"\nclasse="G1"\nnumero_etudiant="{number}"', 'outputs': []})
        return {'metadata': {'tal': {'id': evaluator, 'evaluator': evaluator, 'version': 2}}, 'cells': cells}

    def post(self, nb, path='/submit'):
        return self.client.post(path, data={'file': (io.BytesIO(json.dumps(nb).encode()), 'copy.ipynb')})

    def test_all_seven_old_contracts_no_correction_or_persistence(self):
        for td in range(1, 8):
            nb = self.fixture(td)
            nb['metadata']['tal']['version'] = 1
            from importlib import import_module
            module = import_module(f'app_correction_TD{td}_S1')
            with patch('routes.process_submission') as persist, patch.object(module, 'check_notebook') as grader:
                for path in ('/submit', f'/eval/td{td}-s1'):
                    self.assertIn(WRONG_VERSION, self.post(nb, path).get_data(as_text=True))
                persist.assert_not_called()
                grader.assert_not_called()
        self.assertEqual(list(Path(self.temp.name).rglob('*')), [])

    def test_missing_contract_rejected_blank_answer_accepted_and_homonyms_separate(self):
        bad = self.fixture()
        bad['cells'][0]['metadata'] = {}
        with patch('routes.process_submission') as persist:
            self.assertIn(WRONG_VERSION, self.post(bad).get_data(as_text=True))
            persist.assert_not_called()
        for number in ('900001', '900002'):
            nb = self.fixture(number=number)
            nb['cells'][0]['source'] = '# <script>alert(1)</script>'
            body = self.post(nb).get_data(as_text=True)
            self.assertIn('Score technique provisoire', body)
            self.assertIn('&lt;script&gt;', body)
        copies = list(Path(self.temp.name).rglob('*.ipynb'))
        self.assertEqual(len(copies), 2)
        self.assertTrue(all('td1-s1-v2' in str(p) and 'DUPONT_Alice_' in p.name for p in copies))
        self.assertEqual(len(list(Path(self.temp.name).rglob('*.html'))), 2)
        self.assertTrue(any('_900001_' in p.name for p in copies))
        self.assertTrue(any('_900002_' in p.name for p in copies))


if __name__ == '__main__':
    unittest.main()
