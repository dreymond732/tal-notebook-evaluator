import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from app import create_app
import outils
import routes


def notebook(source, output):
    return json.dumps({
        "cells": [{
            "cell_type": "code",
            "source": source.splitlines(keepends=True),
            "outputs": [{"output_type": "stream", "name": "stdout", "text": output}],
        }],
        "nbformat": 4,
        "nbformat_minor": 5,
    })


class S1FormativeTests(unittest.TestCase):
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
        for number in range(1, 8):
            identifier = f"td{number}-s1"
            self.assertIn(identifier, routes.EVALUATORS)
            self.assertEqual(self.client.get(f"/eval/{identifier}").status_code, 200)

    def test_all_s1_correctors_reject_unversioned_copies_without_execution(self):
        for number in range(1, 8):
            with self.subTest(number=number):
                module = importlib.import_module(f"app_correction_TD{number}_S1")
                source = 'raise RuntimeError("le code étudiant ne doit pas être exécuté")'
                score, details, maximum, _, error = module.check_notebook(
                    notebook(source, "Résultat Q1 : ok"), f"td{number}.ipynb")
                self.assertEqual(score, 0)
                self.assertEqual(error, "mauvaise version du notebook")
                self.assertEqual(maximum, module.MAX_SCORE_TOTAL)

    def test_invalid_json_is_controlled(self):
        module = importlib.import_module("app_correction_TD1_S1")
        score, _, maximum, _, error = module.check_notebook("{invalide", "td1.ipynb")
        self.assertEqual(score, 0.0)
        self.assertEqual(maximum, module.MAX_SCORE_TOTAL)
        self.assertIn("Erreur notebook", error)
