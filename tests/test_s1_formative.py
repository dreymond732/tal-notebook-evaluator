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

    def test_all_s1_correctors_are_static_and_complete(self):
        for number in range(1, 8):
            module = importlib.import_module(f"app_correction_TD{number}_S1")
            source = 'raise RuntimeError("le code étudiant ne doit pas être exécuté")\n'
            source += "\n".join(fragment for check in module.CHECKS for fragment in check["source"])
            outputs = "\n".join(check["output"] + " ok" for check in module.CHECKS)
            score, details, maximum, _, error = module.check_notebook(
                notebook(source, outputs), f"td{number}.ipynb"
            )
            self.assertIsNone(error)
            if number == 2:
                self.assertEqual(score, 0.0)  # Des marqueurs « ok » ne sont pas des réponses.
            else:
                self.assertEqual(score, maximum)
            self.assertEqual(len(details), len(module.CHECKS))

    def test_invalid_json_is_controlled(self):
        module = importlib.import_module("app_correction_TD1_S1")
        score, _, maximum, _, error = module.check_notebook("{invalide", "td1.ipynb")
        self.assertEqual(score, 0.0)
        self.assertEqual(maximum, module.MAX_SCORE_TOTAL)
        self.assertIn("Erreur JSON", error)
