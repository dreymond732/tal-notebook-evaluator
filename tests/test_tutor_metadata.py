"""Structural regression tests, not a claim about live Colab LLM behavior."""

import copy
import json
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))
from tutor_metadata import CONTEXT_BUDGET, migrate_notebook, render_context


class TutorMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sessions = json.loads((ROOT / "docs/pedagogy/tutor_sessions.json").read_text(encoding="utf-8"))["sessions"]

    def test_pilots_match_manifest_and_regeneration_is_idempotent(self):
        for session in self.sessions:
            with self.subTest(session=session["id"]):
                notebook = json.loads((ROOT / session["notebook"]).read_text(encoding="utf-8"))
                self.assertEqual(migrate_notebook(notebook, session), notebook)
                contexts = notebook["metadata"]["colab"]["aiContexts"]
                self.assertEqual(len(contexts), 1)
                context = next(iter(contexts.values()))["context"]
                self.assertEqual(context, render_context(session))
                self.assertLessEqual(len(context), CONTEXT_BUDGET)
                self.assertFalse(any("LLM_PEDAGOGICAL_CONTEXT_START" in "".join(c["source"]) for c in notebook["cells"]))

    def test_migration_consolidates_both_legacy_contexts_without_changing_work(self):
        notebook = {
            "nbformat": 4,
            "metadata": {"kernelspec": {"name": "python3"}, "colab": {
                "provenance": [],
                "aiContexts": {"old-id": {"id": "old-id", "name": "NLP tutor", "context": "old truncated rule"}},
            }},
            "cells": [
                {"cell_type": "markdown", "source": ["## Exercice\n", "Décrivez le résultat."], "metadata": {"id": "title"}},
                {"cell_type": "markdown", "source": ["<!-- LLM_PEDAGOGICAL_CONTEXT_START\nobsolete rules\n<!-- LLM_PEDAGOGICAL_CONTEXT_END -->\n"], "metadata": {}},
                {"cell_type": "code", "source": ["raise RuntimeError('must not run')"], "outputs": [], "metadata": {"id": "answer"}, "execution_count": None},
            ],
        }
        untouched = copy.deepcopy(notebook)
        result = migrate_notebook(notebook, self.sessions[1])
        self.assertEqual(notebook, untouched)
        self.assertEqual(result["cells"], [notebook["cells"][0], notebook["cells"][2]])
        self.assertEqual(result["metadata"]["kernelspec"], notebook["metadata"]["kernelspec"])
        self.assertEqual(result["metadata"]["colab"]["provenance"], [])
        self.assertEqual(len(result["metadata"]["colab"]["aiContexts"]), 1)
        self.assertNotIn("old-id", result["metadata"]["colab"]["aiContexts"])
        self.assertEqual(migrate_notebook(result, self.sessions[1]), result)

    def test_mixed_markdown_retains_teaching_material(self):
        before = "Énoncé à conserver.\n\n"
        after = "\nExemple enseignant à conserver."
        notebook = {"cells": [{"cell_type": "markdown", "source": before + "<!-- LLM_PEDAGOGICAL_CONTEXT_START\nold\nLLM_PEDAGOGICAL_CONTEXT_END -->" + after}]}
        result = migrate_notebook(notebook, self.sessions[0])
        self.assertEqual(result["cells"][0]["source"], before + after)

    def test_partial_or_misplaced_legacy_blocks_require_review(self):
        for kind in ("markdown", "code"):
            notebook = {"cells": [{"cell_type": kind, "source": "<!-- LLM_PEDAGOGICAL_CONTEXT_START\nunfinished"}]}
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                migrate_notebook(notebook, self.sessions[0])

    def test_unrelated_user_context_is_not_silently_deleted(self):
        notebook = {"cells": [], "metadata": {"colab": {"aiContexts": {"custom": {"name": "Conventions personnelles", "context": "keep me"}}}}}
        with self.assertRaisesRegex(ValueError, "arbitrage"):
            migrate_notebook(notebook, self.sessions[0])

    def test_context_is_never_silently_truncated(self):
        session = copy.deepcopy(self.sessions[0])
        session["title"] = "x" * CONTEXT_BUDGET
        with self.assertRaisesRegex(ValueError, "aucune troncature"):
            render_context(session)

    def test_mode_must_be_explicit_even_with_misleading_filename(self):
        session = copy.deepcopy(self.sessions[0])
        session["notebook"] = "Notebooks TD/TD_controle.ipynb"
        session["activity"] = "controle"
        session["semester"] = 3
        session["exercises"][0]["topic"] = "SOLUTION_SECRETE"
        context = render_context(session)
        self.assertIn("CONTRÔLE — AUCUNE ASSISTANCE", context)
        self.assertIn("ne déclenchent JAMAIS le mode quiz", context)
        self.assertNotIn("SOLUTION_SECRETE", context)
        self.assertNotIn("PÉRIMÈTRE PAR EXERCICE", context)
        del session["activity"]
        with self.assertRaisesRegex(ValueError, "explicite"):
            render_context(session)

    def test_early_exercise_cannot_inherit_later_notions(self):
        session = copy.deepcopy(self.sessions[0])
        session["exercises"][0]["available_concepts"] = ["variable"]
        session["exercises"][0]["introduced_here"] = []
        session["exercises"][-1]["available_concepts"].append("NOTION_TARDIVE")
        context = render_context(session)
        first_line = next(line for line in context.splitlines() if line.startswith("Q1 —"))
        self.assertNotIn("NOTION_TARDIVE", first_line)
        self.assertIn("pas d'union avec les exercices suivants", context)
        self.assertIn("aucun code fourni par le tuteur", context)

    def test_td0_question_markers_map_to_the_visible_exercise_titles(self):
        session = next(s for s in self.sessions if s["id"] == "TD0_S3")
        notebook = json.loads((ROOT / session["notebook"]).read_text(encoding="utf-8"))
        locations = {}
        current_exercise = None
        for cell in notebook["cells"]:
            source = "".join(cell["source"])
            if cell["cell_type"] == "markdown":
                heading = re.search(r"^## Exercice (\d+)", source, re.MULTILINE)
                if heading:
                    current_exercise = heading.group(1)
            elif current_exercise:
                for marker in re.findall(r"Résultat (Q\d+)\s*:", source):
                    locations[marker] = current_exercise
        self.assertEqual(set(locations), {e["id"] for e in session["exercises"]})
        context = render_context(session)
        for exercise in session["exercises"]:
            self.assertTrue(exercise["topic"].startswith("Exercice " + locations[exercise["id"]]))
            self.assertIn(exercise["topic"], context)

    def test_supplied_library_is_distinct_from_allowed_library(self):
        context = render_context(self.sessions[1])
        self.assertIn("Bibliothèques autorisées : aucune", context)
        self.assertIn("Préparation fournie seulement : pathlib", context)
        session = copy.deepcopy(self.sessions[1])
        session["allowed_libraries"].append("pathlib")
        with self.assertRaisesRegex(ValueError, "préparation"):
            render_context(session)

    def test_invalid_exercise_references_and_paths_are_rejected(self):
        session = copy.deepcopy(self.sessions[0])
        session["notebook"] = "../outside.ipynb"
        with self.assertRaises(ValueError):
            render_context(session)
        session = copy.deepcopy(self.sessions[0])
        session["exercises"][0]["introduced_here"].append("inconnu")
        with self.assertRaisesRegex(ValueError, "périmètre"):
            render_context(session)


if __name__ == "__main__":
    unittest.main()
