"""Fixtures de traces: aucun notebook soumis n'est exécuté par ces tests."""
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))
import app_correction_TD2_S1 as evaluator
from app import create_app
import outils


SOURCES = [
    '''texte_brut = "   Le TAL transforme des textes.   "
texte_propre = texte_brut.strip()
print("Résultat Q1 :", texte_propre)
print("Résultat Q1b :", len(texte_brut), len(texte_propre))''',
    '''texte_transforme = texte_propre.lower().replace("textes", "corpus")
print("Résultat Q2 :", texte_transforme)
print("Résultat Q2b :", "corpus" in texte_transforme, "textes" in texte_transforme)''',
    '''mot = "tokenisation"
premier = mot[0]
dernier = mot[-1]
debut = mot[:4]
milieu = mot[1:5]
print("Résultat Q3 :", premier, dernier, debut)
print("Résultat Q3b :", milieu, len(mot))''',
    '''phrase = "La traduction automatique aide parfois"
tokens = phrase.split()
print("Résultat Q4 :", tokens, tokens[2])
print("Résultat Q4b :", len(tokens), tokens[-1])''',
    '''phrase_avec_barres = " | ".join(tokens)
tokens_reconstruits = phrase_avec_barres.split(" | ")
print("Résultat Q5 :", phrase_avec_barres)
print("Résultat Q5b :", tokens_reconstruits, tokens_reconstruits == tokens)''',
    '''exemples = ["  Bonjour  ", "TAL", "  Corpus Français"]
exemple_0 = exemples[0].strip().lower()
exemple_1 = exemples[1].strip().lower()
exemple_2 = exemples[2].strip().lower()
exemples_nettoyes = [exemple_0, exemple_1, exemple_2]
print("Résultat Q6 :", exemples_nettoyes)
print("Résultat Q6b :", exemples)''',
    '''phrase_limite = "L’analyse, c’est utile !"
tokens_limite = phrase_limite.split()
commentaire = "La virgule demeure attachée au premier élément."
print("Résultat Q7 :", commentaire)
print("Résultat Q7b :", tokens_limite)''',
]
OUTPUTS = [
    "Résultat Q1 : Le TAL transforme des textes.\nRésultat Q1b : 35 29\n",
    "Résultat Q2 : le tal transforme des corpus.\nRésultat Q2b : True False\n",
    "Résultat Q3 : t n toke\nRésultat Q3b : oken 12\n",
    "Résultat Q4 : ['La', 'traduction', 'automatique', 'aide', 'parfois'] automatique\nRésultat Q4b : 5 parfois\n",
    "Résultat Q5 : La | traduction | automatique | aide | parfois\nRésultat Q5b : ['La', 'traduction', 'automatique', 'aide', 'parfois'] True\n",
    "Résultat Q6 : ['bonjour', 'tal', 'corpus français']\nRésultat Q6b : ['  Bonjour  ', 'TAL', '  Corpus Français']\n",
    "Résultat Q7 : La virgule demeure attachée au premier élément.\nRésultat Q7b : ['L’analyse,', 'c’est', 'utile', '!']\n",
]


def fixture():
    return {"cells": [{"cell_type": "code", "source": source,
                       "outputs": [{"output_type": "stream", "name": "stdout", "text": output}]}
                      for source, output in zip(SOURCES, OUTPUTS)],
            "nbformat": 4, "nbformat_minor": 5}


def filled_subject():
    path = Path(__file__).resolve().parents[1] / "Notebooks TD/S1/TD2_S1_python_texte.ipynb"
    nb = json.loads(path.read_text())
    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell["source"])
        for field, value in (("nom", "Modele"), ("prenom", "Test"), ("classe", "S1")):
            source = re.sub(rf'^{field} = "\.\.\."$', f'{field} = "{value}"', source, flags=re.M)
        cell["source"] = source.splitlines(keepends=True)
    return nb


def grade(notebook):
    return evaluator.check_notebook(json.dumps(notebook), "copie.ipynb")


class TD2Tests(unittest.TestCase):
    def test_reference_and_human_review_notice(self):
        score, details, maximum, info, error = grade(fixture())
        self.assertEqual((score, maximum, error), (7, 7, None))
        self.assertEqual(len(details), 7)
        self.assertEqual(info["score_brut"], 7)
        self.assertIn("n’est pas évalué automatiquement", details[-1]["correct_answer"])

    def test_equivalent_steps_slices_and_list_quotes(self):
        nb = fixture()
        nb["cells"][1]["source"] = SOURCES[1].replace(
            'texte_transforme = texte_propre.lower().replace("textes", "corpus")',
            'minuscules = texte_propre.lower()\ntexte_transforme = minuscules.replace("textes", "corpus")')
        nb["cells"][2]["source"] = SOURCES[2].replace("mot[:4]", "mot[0:4:1]")
        nb["cells"][3]["outputs"][0]["text"] = OUTPUTS[3].replace("'", '"')
        self.assertEqual(grade(nb)[0], 7)

    def test_equivalent_last_element_indices(self):
        for word_index, token_index in (("11", "4"), ("len(mot)-1", "len(tokens)-1"), ("-1", "-1")):
            with self.subTest(word=word_index, tokens=token_index):
                nb = fixture()
                nb["cells"][2]["source"] = SOURCES[2].replace("mot[-1]", f"mot[{word_index}]")
                nb["cells"][3]["source"] = SOURCES[3].replace("tokens[-1]", f"tokens[{token_index}]")
                self.assertEqual(grade(nb)[0], 7)

    def test_no_student_execution_even_raise_and_import(self):
        nb = fixture()
        nb["cells"].insert(0, {"cell_type": "code", "source": 'raise RuntimeError("NEVER RUN")\nimport os', "outputs": []})
        self.assertEqual(grade(nb)[0], 7)
        self.assertIn("import", grade(nb)[1][0]["correct_answer"])

    def test_wrong_values_and_types_are_not_full_credit(self):
        changes = [(0, "35 29", "35 28"), (1, "True False", "False True"),
                   (2, "t n toke", "t n token"), (3, "['La'", "[1"),
                   (4, " True", " False"), (5, "'bonjour'", "'Bonjour'"),
                   (6, "'L’analyse,'", "'L’analyse'")]
        for cell, old, new in changes:
            with self.subTest(cell=cell):
                nb = fixture()
                nb["cells"][cell]["outputs"][0]["text"] = OUTPUTS[cell].replace(old, new)
                self.assertLess(grade(nb)[0], 7)

    def test_unrelated_code_comments_and_marker_only_do_not_pass(self):
        for replacement in ('# ' + SOURCES[0].replace('\n', '\n# '),
                            'unused = "x".strip()\nprint("Résultat Q1 :", "Le TAL transforme des textes.")',
                            'print("Résultat Q1 :")'):
            with self.subTest(source=replacement):
                nb = fixture()
                nb["cells"][0]["source"] = replacement
                self.assertEqual(grade(nb)[1][0]["points"], 0)

    def test_duplicate_marker_and_wrong_cell_outputs_rejected(self):
        nb = fixture()
        nb["cells"][0]["outputs"][0]["text"] += "Résultat Q1 : Le TAL transforme des textes.\n"
        self.assertEqual(grade(nb)[1][0]["points"], 0.5)
        nb = fixture()
        nb["cells"][0]["source"] += '\nprint("Résultat Q1 :", texte_propre)'
        self.assertEqual(grade(nb)[1][0]["points"], 0.5)
        nb = fixture()
        nb["cells"][0]["outputs"], nb["cells"][1]["outputs"] = nb["cells"][1]["outputs"], nb["cells"][0]["outputs"]
        self.assertEqual(grade(nb)[1][0]["points"], 0)

    def test_each_q6_item_requires_cleaning(self):
        nb = fixture()
        nb["cells"][5]["source"] = SOURCES[5].replace('exemples[1].strip().lower()', 'exemples[1]')
        self.assertEqual(grade(nb)[1][5]["points"], 0.5)

    def test_error_output_does_not_validate_old_traces(self):
        nb = fixture()
        nb["cells"][0]["outputs"].append({"output_type": "error", "ename": "SyntaxError"})
        self.assertEqual(grade(nb)[1][0]["points"], 0)

    def test_stale_but_plausible_output_limit_is_explicit(self):
        nb = fixture()
        nb["cells"][0]["source"] = SOURCES[0].replace('   Le TAL transforme des textes.   ', 'une autre entrée')
        # Sans exécution, la présence de l'opération et une sortie plausible
        # ne prouve pas qu'elles proviennent de la même exécution.
        self.assertEqual(grade(nb)[0], 7)
        self.assertIn("périmée", grade(nb)[1][0]["correct_answer"])

    def test_comment_meaning_is_not_certified(self):
        nb = fixture()
        nb["cells"][6]["outputs"][0]["text"] = OUTPUTS[6].replace(
            "La virgule demeure attachée au premier élément.", "Le ciel est vert.")
        self.assertEqual(grade(nb)[1][-1]["points"], 1)
        self.assertIn("relire", grade(nb)[1][-1]["correct_answer"])
        for placeholder in ("", "...", "À compléter"):
            nb["cells"][6]["outputs"][0]["text"] = OUTPUTS[6].replace(
                "La virgule demeure attachée au premier élément.", placeholder)
            self.assertEqual(grade(nb)[1][-1]["points"], 0)

    def test_unfilled_notebook_and_invalid_json(self):
        nb = fixture()
        for cell in nb["cells"]:
            cell["outputs"] = []
        self.assertEqual(grade(nb)[0], 0)
        self.assertIn("Erreur JSON", evaluator.check_notebook("{", "x.ipynb")[-1])
        self.assertIsNotNone(grade([])[-1])

    def test_segmented_stdout_and_list_source_are_supported(self):
        nb = fixture()
        cell = nb["cells"][0]
        cell["source"] = cell["source"].splitlines(keepends=True)
        cell["outputs"] = [{"output_type": "stream", "name": "stdout", "text": fragment}
                           for fragment in (OUTPUTS[0][:8], OUTPUTS[0][8:23], OUTPUTS[0][23:])]
        self.assertEqual(grade(nb)[0], 7)

    def test_malformed_cells_and_outputs_return_contract_error(self):
        for bad in (None, {}, [None]):
            nb = fixture()
            nb["cells"][0]["outputs"] = bad
            self.assertEqual(len(grade(nb)), 5)
            self.assertIsNotNone(grade(nb)[-1])
        for bad in (None, 3, {"source": [None]}):
            nb = fixture()
            nb["cells"][0] = bad
            self.assertIsNotNone(grade(nb)[-1])

    def test_current_subject_identification_is_extracted(self):
        score, _, _, info, error = grade(filled_subject())
        self.assertEqual((score, error), (0, None))
        self.assertEqual({key: info[key] for key in ("nom", "prenom", "classe")},
                         {"nom": "Modele", "prenom": "Test", "classe": "S1"})

    def test_real_route_persists_valid_and_wrong_outputs(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(outils, "BASE_DIR", directory):
            app = create_app()
            app.config.update(TESTING=True)
            client = app.test_client()
            for valid in (True, False):
                nb = fixture()
                subject = filled_subject()
                identification = next(cell for cell in subject["cells"]
                                      if cell.get("cell_type") == "code" and
                                      re.search(r'^nom = "Modele"$', "".join(cell["source"]), re.M))
                nb["cells"].insert(0, identification)
                info = grade(nb)[3]
                self.assertEqual((info["nom"], info["prenom"], info["classe"]), ("Modele", "Test", "S1"))
                if not valid:
                    nb["cells"][1]["outputs"][0]["text"] = OUTPUTS[0].replace("35 29", "1 2")
                response = client.post('/eval/td2-s1', data={"file": (io.BytesIO(json.dumps(nb).encode()), "copie.ipynb")}, content_type="multipart/form-data")
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertIn("Trace du découpage", html)
                self.assertIn("périmée", html)
                if not valid:
                    self.assertIn("différent de l’attendu", html)
            root = Path(directory) / "td2-s1" / "S1"
            self.assertTrue((root / "rapport" / "MODELE_Test_td2-s1.html").is_file())
            self.assertTrue((root / "nb" / "MODELE_Test_copie.ipynb").is_file())
            csv = root / "notes_td2-s1_S1.csv"
            self.assertTrue(csv.is_file())
            self.assertIn("MODELE;Test;S1;6,50", csv.read_text())
            self.assertFalse(list(Path(directory).rglob("*NON_RENSEIGNE*")))


if __name__ == "__main__":
    unittest.main()
