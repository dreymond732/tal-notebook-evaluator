"""DM S1: inert analysis, partial credit and teacher-only provisional report."""
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
import app_correction_DM_intermediaire_S1 as dm
from app import create_app
import outils


def answer(q, source, output):
    return {'cell_type': 'code', 'metadata': {'tal': {'question': f'Q{q}', 'role': 'answer'}},
            'source': source, 'outputs': [{'output_type': 'stream', 'name': 'stdout',
                                          'text': f'Résultat Q{q} : {output!r}\n'}]}


def notebook(*cells):
    identity = {'cell_type': 'code', 'metadata': {'tal': {'question': 'identity', 'role': 'identification'}},
                'source': 'nom="Modele"\nprenom="Test"\nclasse="S1"\nnumero_etudiant="TEST2026"', 'outputs': []}
    return {'cells': [identity, *cells], 'metadata': {'tal': {'id': dm.EVAL_ID, 'version': 1, 'evaluator': dm.EVAL_ID}}}


BUDGET = '''inscrits_saisis = "12"
nb_inscrits = int(inscrits_saisis)
recette = nb_inscrits * 7.5
budget_total = recette + 18
cout_moyen = budget_total / nb_inscrits
print("Résultat Q1 :", [nb_inscrits, recette, budget_total, cout_moyen, type(nb_inscrits) == int])
'''
NORMALISER = '''def normaliser_notice(contenu):
    intermediaire = contenu.strip()
    return intermediaire.lower()
print("Résultat Q15 :", [normaliser_notice("  LIVRE  "), normaliser_notice(""), normaliser_notice("  Deux  MOTS !  ")])
'''
COMPTER = '''def compter_elements(collection):
    bilan = {}
    for item in collection:
        if item in bilan:
            bilan[item] += 1
        else:
            bilan[item] = 1
    return bilan
print("Résultat Q16 :", [compter_elements(["livre", "récit", "livre"]), compter_elements([]), compter_elements(["Livre", "livre"])])
'''
SERIES = '''numeros_pairs = []
for n in range(2,13,2):
    numeros_pairs.append(n)
diffusion = []
effectif = 3
total_contacts = 0
while len(diffusion) < 6:
    diffusion.append(effectif)
    total_contacts += effectif
    effectif *= 2
print("Résultat Q12 :", [numeros_pairs, diffusion, total_contacts])
'''


class AssignmentChecks(unittest.TestCase):
    def evaluate(self, *cells):
        return dm.check_notebook(json.dumps(notebook(*cells)), 'renommee.ipynb')

    def test_signature_maximum_identity_partial_and_function_parameter_variants(self):
        cells = [answer(1, BUDGET, [12, 90., 108., 9., True]),
                 answer(15, NORMALISER, ['livre', '', 'deux  mots !']),
                 answer(16, COMPTER, [{'livre': 2, 'récit': 1}, {}, {'Livre': 1, 'livre': 1}])]
        score, details, maximum, info, error = self.evaluate(*cells)
        self.assertEqual((score, maximum, error), (4, 20, None))
        self.assertEqual(info['numero_etudiant'], 'TEST2026')
        self.assertEqual(info['score_nature'], 'technique_provisoire')
        cells[0]['outputs'][0]['text'] = 'Résultat Q1 : [12, 90.0, 999, 9.0, True]\n'
        self.assertEqual(self.evaluate(*cells)[0], 3.8)
        self.assertEqual(sum(d['max_points'] for d in details), 20)

    def test_no_execution_and_required_ast_not_comments_or_unrelated_outputs(self):
        good = answer(12, SERIES, [[2,4,6,8,10,12], [3,6,12,24,48,96], 189])
        self.assertEqual(self.evaluate(good)[0], 1)
        good['source'] = "raise RuntimeError('DO_NOT_EXECUTE')\n" + good['source']
        self.assertEqual(self.evaluate(good)[0], 1)
        bad = answer(12, '# for range while +=\nprint("Résultat Q12 :", [[2,4,6,8,10,12], [3,6,12,24,48,96], 189])',
                     [[2,4,6,8,10,12], [3,6,12,24,48,96], 189])
        self.assertEqual(self.evaluate(bad)[0], 0)
        # Saved trace in a provided cell cannot be borrowed by an answer cell.
        foreign = copy.deepcopy(good)
        foreign['metadata']['tal']['role'] = 'provided'
        empty = copy.deepcopy(good)
        empty['outputs'] = []
        self.assertEqual(self.evaluate(foreign, empty)[0], 0)

    def test_literal_return_unrelated_parameter_and_missing_test_are_not_functions(self):
        bad = NORMALISER.replace('return intermediaire.lower()', 'return "livre"')
        self.assertEqual(self.evaluate(answer(15, bad, ['livre', '', 'deux  mots !']))[0], 0)
        bad = NORMALISER.replace('normaliser_notice("")', 'normaliser_notice("  LIVRE  ")')
        self.assertEqual(self.evaluate(answer(15, bad, ['livre', '', 'deux  mots !']))[0], 1)
        bad = COMPTER.replace('for item in collection:', 'for item in ["livre", "récit", "livre"]:')
        self.assertEqual(self.evaluate(answer(16, bad, [{'livre':2, 'récit':1}, {}, {'Livre':1, 'livre':1}]))[0], 0)

    def test_composition_and_lexicon_parameter_and_punctuation_cases(self):
        translation = """def traduire_etiquette(chaine, table):
    forme = normaliser_notice(chaine)
    if forme in table:
        return table[forme]
    return forme

def traduire_annonce(annonce, table):
    traduits = []
    for token in annonce.split():
        traduits.append(traduire_etiquette(token, table))
    return " ".join(traduits)
lexique_test = {"book": "livre", "story": "récit"}
print("Résultat Q17 :", [traduire_etiquette(" BOOK ", lexique_test), traduire_etiquette(" MAP ", lexique_test), traduire_annonce("BOOK story MAP", lexique_test), traduire_annonce("", lexique_test), traduire_etiquette("BOOK", {"book": "ouvrage"})])
"""
        summary = """def bilan_notice(contenu):
    nettoye = normaliser_notice(contenu)
    fragments = nettoye.split()
    comptes = compter_elements(fragments)
    return {"texte_normalise": nettoye, "nb_caracteres": len(nettoye), "nb_fragments": len(fragments), "nb_formes": len(comptes), "frequences": comptes}
print("Résultat Q18 :", [bilan_notice("  LIVRE récit livre  "), bilan_notice(""), bilan_notice("Livre livre, LIVRE")])
"""
        cell17 = answer(17, translation, ['livre', 'map', 'livre récit map', '', 'ouvrage'])
        cell18 = answer(18, summary, [
            {'texte_normalise':'livre récit livre', 'nb_caracteres':17, 'nb_fragments':3, 'nb_formes':2, 'frequences':{'livre':2, 'récit':1}},
            {'texte_normalise':'', 'nb_caracteres':0, 'nb_fragments':0, 'nb_formes':0, 'frequences':{}},
            {'texte_normalise':'livre livre, livre', 'nb_caracteres':18, 'nb_fragments':3, 'nb_formes':2, 'frequences':{'livre':2, 'livre,':1}}])
        self.assertEqual(self.evaluate(cell17, cell18)[0], 3)
        cell17['source'] = translation.replace('forme in table', 'forme in lexique_test').replace('return table[forme]', 'return lexique_test[forme]')
        self.assertEqual(self.evaluate(cell17)[0], 0)

    def test_errors_duplicates_markdown_and_ambiguous_outputs(self):
        good = answer(1, BUDGET, [12,90,108,9,True])
        for mutate in ('duplicate', 'error', 'markdown', 'repeat-print'):
            bad = copy.deepcopy(good)
            if mutate == 'duplicate':
                bad['outputs'] *= 2
            elif mutate == 'error':
                bad['outputs'].append({'output_type':'error', 'ename':'ValueError'})
            elif mutate == 'markdown':
                bad['cell_type'] = 'markdown'
            else:
                bad['source'] += '\nprint("Résultat Q1 :", [])'
            self.assertEqual(self.evaluate(bad)[0], 0)
        self.assertIsNotNone(self.evaluate(good, good)[4])
        for value in ('[]', '{', '{"cells": [null]}'):
            result = dm.check_notebook(value, 'copie.ipynb')
            self.assertEqual(len(result), 5)
            self.assertIsNotNone(result[4])

    def test_malformed_comment_source_and_q14_output_do_not_block_deposit(self):
        bad = answer(2, [42], [])
        other = answer(14, 'pass', [])
        other['outputs'][0]['text'] = None
        result = self.evaluate(bad, other)
        self.assertEqual(result[0], 0)
        self.assertIsNone(result[4])

    def test_set_order_and_typed_values(self):
        source = '''themes_a = ["récit", "langue", "récit", "mémoire", "lecture"]
themes_b = ["lecture", "image", "langue", "image"]
a = set(themes_a)
b = set(themes_b)
print("Résultat Q10 :", [len(themes_a), len(a), a & b, a - b])'''
        self.assertEqual(self.evaluate(answer(10, source, [5,4, {'lecture','langue'}, {'mémoire','récit'}]))[0], 1)
        self.assertFalse(dm._same(True, 1))
        self.assertFalse(dm._same(['français'], ('français',)))
        with self.assertRaises(ValueError):
            dm._literal("{'a':1, 'a':2}")

    def test_no_cascade_on_saved_empty_function_result(self):
        self.assertEqual(self.evaluate(answer(16, COMPTER, [{'livre':999, 'récit':1}, {}, {'Livre':1, 'livre':1}]))[0], 1.25)
        cell = answer(1, BUDGET, [12,90,108,9,True])
        data = notebook(cell)
        data['cells'][0]['source'] = 'nom="N"\nprenom="P"\nclasse="S1"\nnumero_etudiant=""'
        self.assertIsNotNone(dm.check_notebook(json.dumps(data), 'x.ipynb')[4])

    def test_independent_unexecuted_model_accepts_all_canonical_saved_traces(self):
        # This is an acceptance probe, not evidence of executing the model or of
        # authentic outputs: attach server-owned expected literals in memory.
        root = Path(__file__).resolve().parents[1]
        path = root / 'Corrigés modèles/Contrôles finaux/dm-intermediaire-s1/DM_intermediaire_S1_corrige_non_execute.ipynb'
        model = json.loads(path.read_text())
        for cell in model['cells']:
            contract = cell.get('metadata', {}).get('tal', {})
            if contract.get('role') == 'answer':
                q = int(contract['question'][1:])
                self.assertEqual(cell.get('outputs', []), [])
                cell['outputs'] = [{'output_type': 'stream', 'name':'stdout',
                                    'text': f'Résultat Q{q} : {dm.EXPECTED[q-1]!r}\n'}]
        result = dm.check_notebook(json.dumps(model), 'model.ipynb')
        self.assertEqual((result[0], result[2], result[4]), (20, 20, None), result[1])

    def test_public_receipt_and_private_specific_rubric_and_student_number(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(outils, 'BASE_DIR', directory):
            app = create_app()
            app.config['TESTING'] = True
            payload = json.dumps(notebook(answer(1, BUDGET, [12,90,108,9,True]))).encode()
            response = app.test_client().post('/submit', data={'file': (io.BytesIO(payload), 'renommee.ipynb')}, content_type='multipart/form-data')
            public = response.get_data(as_text=True)
            self.assertIn('Copie reçue et enregistrée', public)
            self.assertNotIn('Score technique', public)
            self.assertNotIn('Budget et conversion', public)
            report = next(Path(directory).rglob('*.html')).read_text()
            self.assertIn('Généralité des fonctions', report)
            self.assertIn('TEST2026', report)
            self.assertNotIn('Qualité linguistique et retour aux passages', report)
            csv = next(Path(directory).rglob('*.csv')).read_text()
            self.assertIn('Numéro étudiant', csv)
            self.assertIn('TEST2026', csv)
            self.assertIn('technique_provisoire', csv)


if __name__ == '__main__':
    unittest.main()
