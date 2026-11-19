"""Contrat S1 approuvé : traces inertes, pas d'exécution d'une copie."""
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from app import create_app
import app_correction_controle_S1 as control
import outils
from notebook_contract import load_catalog, resolve_notebook, validate_cell_metadata

SUBJECT = ROOT / next(entry['notebook'] for entry in load_catalog()
                      if entry['id'] == 'Controletilt-s1')
# Références indépendantes du dictionnaire de l'évaluateur. Injection de traces
# uniquement dans les fixtures : aucune sortie n'est ajoutée au sujet/modèle.
EXPECTED = [150.0, {'deb': 19, 'fin': 29}, True, 'Terminologie', False,
            ['tokenisation', 'lemme', 'segmentation'], 3, ['MACHINE', 'LEARNING', 'NLP'],
            [15, 12, 9], [5, 4, 3, 2, 1], 'inconnu', {'le': 2, 'chat': 1},
            {'talk': 2, 'is': 1, 'cheap': 1}, 'Vrai', {'code': 'nom'},
            'Bonjour, David', 16, 'analyse', 'nltk', {'longueur': 7, 'minuscules': 'termino'},
            3, 15, 10, [4, 8, 16, 32], ["l'analyse,", '', 'deux  mots !'],
            {'avec': ['Python', 'TAL', 'Nlp'], 'sans': ['code', 'texte']},
            {'phrase': 6, 'texte': 5, 'mot': 3}, ['chien', 'cat'],
            {'mots_nettoyés': ['le', 'tal', 'est', 'cool'], 'nb_caracteres': 16},
            ['bibliothèque', 'livre', '']]


def trace(nb, number, text):
    cell = validate_cell_metadata(nb)[(f'Q{number}', 'answer')]
    cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': text}]


def reference_fixture():
    nb = json.loads(SUBJECT.read_text())
    index = validate_cell_metadata(nb)
    index[('identity', 'identification')]['source'] = ['nom="Modele"\nprenom="Camille"\nclasse="S1"']
    for number, expected in enumerate(EXPECTED, 1):
        question = f'Q{number}'
        # Le code arbitraire doit rester une donnée, même avec de bonnes traces.
        index[(question, 'answer')]['source'] = ['raise RuntimeError("NEVER_EXECUTE")']
        value = repr(expected)
        if number == 1:
            value = 'Coût total : 150.0 €'
        elif number == 2:
            value = "Le mot extrait est 'extraction' (Indices 19:29)"
        elif number == 21:
            value = 'Choix 3'
        trace(nb, number, f'Résultat {question} : {value}\n')
    index[('Q2', 'answer')]['source'] = ['valeur_Q2_deb = 19\nvaleur_Q2_fin = 29\nraise RuntimeError("NEVER_EXECUTE")']
    return nb


def grade(nb):
    return control.check_notebook(json.dumps(nb), 'copie_renommee.ipynb')


class ControlS1V2Tests(unittest.TestCase):
    def test_all_thirty_answers_and_rubric_match_36_without_execution(self):
        nb = reference_fixture()
        before = copy.deepcopy(nb)
        score, details, maximum, info, error = grade(nb)
        self.assertIsNone(error)
        self.assertEqual((score, maximum, len(details)), (36, 36, 31))
        self.assertEqual(sum(row['max_points'] for row in details), maximum)
        self.assertTrue(all(row['status'] == '✅' for row in details))
        self.assertEqual(info['classe'], 'S1')
        self.assertEqual(info['contract_version'], 2)
        self.assertEqual(nb, before)

    def test_each_corrected_question_rejects_wrong_and_missing_trace(self):
        for number in (2, 3, 4, 5, 15, 18, 22, 24, 25, 29, 30):
            for missing in (False, True):
                with self.subTest(question=number, missing=missing):
                    nb = reference_fixture()
                    trace(nb, number, '' if missing else f'Résultat Q{number} : None\n')
                    result = grade(nb)
                    points = 1 if number <= 25 else 2
                    self.assertEqual(result[0], 36 - points)
                    self.assertEqual(result[1][number]['points'], 0)
                    if missing:
                        self.assertEqual(result[1][number]['student_answer'],
                                         'Réponse non retrouvée par le correcteur')

    def test_equivalent_slicing_indices_are_accepted_and_invalid_bounds_rejected(self):
        for start, end in ((19, 29), (19, -16), (-26, 29), (-26, -16)):
            with self.subTest(start=start, end=end):
                nb = reference_fixture()
                trace(nb, 2, f"Résultat Q2 : Le mot extrait est 'extraction' (Indices {start}:{end})\n")
                # Les bornes peuvent aussi être calculées par le programme.
                validate_cell_metadata(nb)[('Q2', 'answer')]['source'] = [
                    'valeur_Q2_deb = len(corpus_brut) - 26\nvaleur_Q2_fin = 29']
                self.assertEqual(grade(nb)[0], 36)
                self.assertIn(str(start), grade(nb)[1][2]['student_answer'])
        for value in ("Le mot extrait est 'extraction' (Indices 19.1:29)",
                      "Le mot extrait est 'extraction' (Indices 19:30)",
                      "Le mot extrait est 'extraction ' (Indices 19:30)"):
            nb = reference_fixture()
            trace(nb, 2, 'Résultat Q2 : ' + value + '\n')
            self.assertEqual(grade(nb)[1][2]['points'], 0)

    def test_boolean_answers_are_not_integer_zero_or_one(self):
        for number, wrong in ((3, 1), (5, 0)):
            nb = reference_fixture()
            trace(nb, number, f'Résultat Q{number} : {wrong}\n')
            self.assertEqual(grade(nb)[1][number]['points'], 0)

    def test_integer_counts_do_not_accept_close_but_incorrect_values(self):
        cases = {7: '3.01', 24: '[4.01, 8.04, 16.08, 32.16]',
                 27: "{'phrase': 6.01, 'texte': 5.01, 'mot': 3.01}",
                 29: "{'mots_nettoyés': ['le','tal','est','cool'], 'nb_caracteres': 16.1}"}
        for number, value in cases.items():
            with self.subTest(question=number):
                nb = reference_fixture()
                trace(nb, number, f'Résultat Q{number} : {value}\n')
                self.assertEqual(grade(nb)[1][number]['points'], 0)

    def test_case_and_strict_dictionary_filter_match_the_subject(self):
        nb = reference_fixture()
        trace(nb, 4, "Résultat Q4 : 'terminologie'\n")
        trace(nb, 15, "Résultat Q15 : {'TAL':'nom','mot':'nom','code':'nom'}\n")
        self.assertEqual(grade(nb)[0], 34)

    def test_alternative_valid_code_and_dict_order_are_accepted(self):
        nb = reference_fixture()
        index = validate_cell_metadata(nb)
        index[('Q25', 'answer')]['source'] = [
            'def normaliser_etiquette(texte):\n'
            '    propre = texte.strip()\n'
            '    return propre.lower()\n'
            'valeur_Q25 = [normaliser_etiquette("  L\'ANALYSE,  "), '
            'normaliser_etiquette(""), normaliser_etiquette("  Deux  MOTS !  ")]\n'
            'print(f"Résultat Q25 : {valeur_Q25}")']
        trace(nb, 29, "Résultat Q29 : {'nb_caracteres': 16, 'mots_nettoyés': ['le','tal','est','cool']}\n")
        self.assertEqual(grade(nb)[0], 36)

    def test_split_stdout_chunks_and_extra_print_do_not_hide_the_result(self):
        nb = reference_fixture()
        cell = validate_cell_metadata(nb)[('Q17', 'answer')]
        cell['outputs'] = [
            {'output_type': 'stream', 'name': 'stdout', 'text': ['16\nRésultat Q']},
            {'output_type': 'stream', 'name': 'stdout', 'text': '17 : 16\n'},
        ]
        self.assertEqual(grade(nb)[0], 36)

    def test_decoy_and_duplicate_trace_cannot_supply_a_missing_answer(self):
        nb = reference_fixture()
        trace(nb, 30, '')
        nb['cells'].append({'cell_type': 'code', 'metadata': {'tal': {'question': 'example', 'role': 'example'}},
                            'source': [], 'outputs': [{'output_type': 'stream', 'name': 'stdout',
                            'text': "Résultat Q30 : ['bibliothèque', 'livre', '']\n"}]})
        self.assertEqual(grade(nb)[0], 34)
        trace(nb, 25, "Résultat Q25 : []\nRésultat Q25 : [\"l'analyse,\", '', 'deux  mots !']\n")
        self.assertEqual(grade(nb)[0], 33)

    def test_old_versions_missing_cells_and_duplicate_cells_fail_closed(self):
        for change in ('old_version', 'no_metadata', 'missing_answer', 'duplicate_answer'):
            with self.subTest(change=change):
                nb = reference_fixture()
                if change == 'old_version':
                    nb['metadata']['tal']['version'] = 1
                elif change == 'no_metadata':
                    nb['metadata'].pop('tal')
                elif change == 'missing_answer':
                    nb['cells'] = [c for c in nb['cells'] if c.get('metadata', {}).get('tal', {}).get('question') != 'Q30']
                else:
                    nb['cells'].append(copy.deepcopy(validate_cell_metadata(nb)[('Q30', 'answer')]))
                score, details, maximum, info, error = grade(nb)
                self.assertEqual((score, details, maximum), (0, [], 36))
                self.assertTrue(error)

    def test_malformed_outputs_and_oversized_numbers_return_a_bounded_result(self):
        for outputs in (None, [None], 'not a list', [{'output_type': 'stream', 'name': 'stdout', 'text': None}]):
            with self.subTest(outputs=outputs):
                nb = reference_fixture()
                validate_cell_metadata(nb)[('Q30', 'answer')]['outputs'] = outputs
                result = grade(nb)
                self.assertEqual(len(result), 5)
                self.assertEqual((result[0], result[2], result[4]), (34, 36, None))
        nb = reference_fixture()
        trace(nb, 17, 'Résultat Q17 : ' + '9' * 400 + '\n')
        trace(nb, 2, "Résultat Q2 : Le mot extrait est 'extraction' (Indices " + '9' * 5000 + ':29)\n')
        result = grade(nb)
        self.assertEqual((result[0], result[2], result[4]), (34, 36, None))

    def test_source_has_no_saved_results_and_identification_is_not_precredited(self):
        nb = json.loads(SUBJECT.read_text())
        self.assertEqual(resolve_notebook(nb)['version'], 2)
        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                self.assertEqual(cell['outputs'], [])
                self.assertIsNone(cell['execution_count'])
        self.assertEqual(grade(nb)[0], 0)
        self.assertIsNone(grade(nb)[4])


class ControlS1V2Routes(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        patcher = patch.object(outils, 'BASE_DIR', self.directory.name)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.client = create_app().test_client()

    def post(self, notebook, path):
        return self.client.post(path, data={'file': (io.BytesIO(json.dumps(notebook).encode()), 'copie.ipynb')})

    def test_old_contract_is_rejected_by_both_routes_before_persistence(self):
        for path in ('/submit', '/eval/Controletilt-s1'):
            for kind in ('old_version', 'no_metadata'):
                nb = reference_fixture()
                if kind == 'old_version':
                    nb['metadata']['tal']['version'] = 1
                else:
                    nb['metadata'].pop('tal')
                with self.subTest(path=path, kind=kind), patch('routes.process_submission') as persist:
                    response = self.post(nb, path)
                    self.assertIn('mauvaise version du notebook', response.get_data(as_text=True))
                    persist.assert_not_called()
        self.assertEqual(list(Path(self.directory.name).rglob('*')), [])

    def test_current_contract_persists_private_report_and_returns_only_receipt(self):
        for path in ('/submit', '/eval/Controletilt-s1'):
            response = self.post(reference_fixture(), path)
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Copie reçue et enregistrée', html)
            for private in ('bibliothèque', "l'analyse,", '✅', '36.00', '36,00'):
                self.assertNotIn(private, html)
        reports = list(Path(self.directory.name).rglob('*.html'))
        self.assertEqual(len(reports), 2)
        for report in reports:
            self.assertIn('bibliothèque', report.read_text())
            self.assertIn('36.00 / 36.0', report.read_text())


if __name__ == '__main__':
    unittest.main()
