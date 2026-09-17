import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from app import create_app
import outils
import routes
from app_correction_TD0_S3 import check_notebook
from app_correction_R0_S3 import check_notebook as check_r0
from app_correction_R1_S3 import check_notebook as check_r1
from app_correction_R2_S3 import check_notebook as check_r2


def notebook(cells):
    return json.dumps({"cells": cells, "nbformat": 4, "nbformat_minor": 5})


def code(source, outputs=None):
    return {
        "cell_type": "code",
        "source": source.splitlines(keepends=True),
        "outputs": outputs or [],
    }


def stdout(text):
    return [{"output_type": "stream", "name": "stdout", "text": text}]


class S3FormativeTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.base_dir = outils.BASE_DIR
        outils.BASE_DIR = self.tempdir.name
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def tearDown(self):
        outils.BASE_DIR = self.base_dir
        self.tempdir.cleanup()

    def test_registry_and_get_routes(self):
        for identifier in ("td0-s3", "td-r0-s3", "td-r1-s3", "td-r2-s3"):
            self.assertIn(identifier, routes.EVALUATORS)
            response = self.client.get(f"/eval/{identifier}")
            self.assertEqual(response.status_code, 200)

    def test_td0_reports_ready_without_executing_notebook_code(self):
        content = notebook([
            code('raise RuntimeError("ne doit jamais être exécuté")\nwith open("x", encoding="utf-8") as f: pass\nmots = texte.split()\nprint(len(mots))\n', stdout("Résultat Q1 : 12\nRésultat Q2 : []\nRésultat Q3 : 0\nRésultat Q4 : limite\n")),
        ])
        score, details, maximum, _, error = check_notebook(content, "td0.ipynb")
        self.assertIsNone(error)
        self.assertEqual((score, maximum), (4.0, 4.0))
        self.assertIn("PRÊT", details[0]["student_answer"])

    def test_comments_do_not_satisfy_r0_code_check(self):
        content = notebook([
            code('# def compter_mots(texte): return 0\n', stdout("Résultat Q1 : 0\nRésultat Q2 : []\nRésultat Q3 : {}\nRésultat Q4 : limite\n")),
        ])
        score, _, maximum, _, error = check_r0(content, "r0.ipynb")
        self.assertIsNone(error)
        self.assertLess(score, maximum)

    def test_r0_r1_r2_accept_expected_code_forms(self):
        output = stdout("Résultat Q1 : ok\nRésultat Q2 : ok\nRésultat Q3 : ok\nRésultat Q4 : ok\n")
        r0 = notebook([code(
            "def compter_mots(texte):\n    return len(texte.split())\n"
            "mots = texte.lower().split()\n"
            "def frequences(texte):\n    return {mot: mots.get(mot, 0) for mot in []}\n",
            output,
        )])
        r1 = notebook([code(
            "doc = nlp(texte)\nfor token in doc:\n    print(token.text)\n"
            "noms = [token.lemma_ for token in doc if token.pos_ == 'NOUN']\n"
            "verbes = [token.lemma_ for token in doc if token.pos_ == 'VERB']\n",
            output,
        )])
        r2 = notebook([code(
            "from collections import Counter\n"
            "def frequences_lemmas(texte, stopwords=None):\n"
            "    return Counter(token.lemma_ for token in nlp(texte) "
            "if token.pos_ in {'NOUN'} and not token.is_stop).most_common()\n",
            output,
        )])
        for checker, content in ((check_r0, r0), (check_r1, r1), (check_r2, r2)):
            score, _, maximum, _, error = checker(content, "passerelle.ipynb")
            self.assertIsNone(error)
            self.assertEqual(score, maximum)

    def test_invalid_json_returns_controlled_page(self):
        response = self.client.post(
            "/eval/td0-s3",
            data={"file": (io.BytesIO(b"{invalide"), "td0.ipynb")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Erreur JSON", response.get_data(as_text=True))

    def test_persistence_failure_is_propagated(self):
        with patch("routes.outils.log_grade_to_csv", side_effect=OSError("disque indisponible")):
            with self.assertRaisesRegex(RuntimeError, "Erreur lors de la sauvegarde"):
                routes.process_submission(
                    type("File", (), {"filename": "test.ipynb"})(),
                    b"{}", "<html></html>", {}, 1.0, "td0-s3"
                )


if __name__ == "__main__":
    unittest.main()
