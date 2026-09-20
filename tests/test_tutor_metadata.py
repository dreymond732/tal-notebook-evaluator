"""Structural regression tests, not a claim about live Colab LLM behavior."""

import copy
import json
from pathlib import Path
import re
import sys
import unittest
import tempfile
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))
import tutor_metadata
from tutor_metadata import (CONTEXT_BUDGET, CELL_ID, CELL_START, CELL_END,
                            migrate_notebook, render_context, validate_inventory)


class TutorMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sessions = json.loads((ROOT / "docs/pedagogy/tutor_sessions.json").read_text(encoding="utf-8"))["sessions"]

    def test_all_subjects_match_manifest_and_both_locations_are_identical(self):
        manifest = json.loads(tutor_metadata.MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(validate_inventory(manifest), self.sessions)
        for session in self.sessions:
            with self.subTest(session=session["id"]):
                notebook = json.loads((ROOT / session["notebook"]).read_text(encoding="utf-8"))
                self.assertEqual(migrate_notebook(notebook, session), notebook)
                contexts = notebook["metadata"]["colab"]["aiContexts"]
                self.assertEqual(len(contexts), 1)
                context = next(iter(contexts.values()))["context"]
                self.assertEqual(context, render_context(session))
                first = notebook["cells"][0]
                self.assertEqual(first["cell_type"], "markdown")
                self.assertEqual(first["metadata"]["id"], CELL_ID)
                self.assertEqual("".join(first["source"]), f"<!-- {CELL_START}\n{context}{CELL_END} -->\n")
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
        self.assertEqual(result["cells"][1:], [notebook["cells"][0], notebook["cells"][2]])
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
        self.assertEqual(result["cells"][1]["source"], before + after)

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
                for marker in re.findall(r"S3_TD0_(Q\d+)\s*:", source):
                    locations[marker] = current_exercise
        self.assertEqual(set(locations), {e["id"] for e in session["exercises"]})
        context = render_context(session)
        for exercise in session["exercises"]:
            self.assertTrue(exercise["topic"].startswith("Exercice " + locations[exercise["id"]]))
            self.assertIn(exercise["topic"], context)

    def test_supplied_library_is_distinct_from_allowed_library(self):
        session = copy.deepcopy(next(s for s in self.sessions if s["id"] == "TD0_S3"))
        context = render_context(session)
        self.assertIn("Bibliothèques autorisées (plafond, voir chaque exercice) : json", context)
        self.assertIn("Préparation fournie seulement : pathlib", context)
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

    def test_pilot_prefix_removed_without_changing_any_teaching_source(self):
        original = {"cell_type": "markdown", "metadata": {"id": "title"}, "source": ["# Titre\n", "\n", "Activité intacte.\n"]}
        prefix = "<!-- TAL_TD2_TUTOR_REMINDER_START\nAncienne consigne.\nTAL_TD2_TUTOR_REMINDER_END -->\n\n"
        pilot = copy.deepcopy(original)
        pilot["source"] = prefix.splitlines(keepends=True) + original["source"]
        code = {"cell_type": "code", "metadata": {}, "source": "raise RuntimeError('must not run')", "execution_count": 4,
                "outputs": [{"output_type": "stream", "name": "stdout", "text": ["trace existante\n"]}]}
        result = migrate_notebook({"cells": [pilot, code]}, self.sessions[0])
        self.assertEqual(result["cells"][1:], [original, code])

    def test_invalid_pilot_location_and_delimiters_fail_closed(self):
        good = "<!-- TAL_TD2_TUTOR_REMINDER_START\nConsigne.\nTAL_TD2_TUTOR_REMINDER_END -->\n\n"
        for cells in (
            [{"cell_type": "code", "source": good}],
            [{"cell_type": "markdown", "source": "Titre"}, {"cell_type": "markdown", "source": good}],
            [{"cell_type": "markdown", "source": good.replace("_END", "_BROKEN")}],
            [{"cell_type": "markdown", "source": good + good}],
        ):
            with self.subTest(cells=cells), self.assertRaisesRegex(ValueError, "pilote"):
                migrate_notebook({"cells": cells}, self.sessions[0])

    def test_managed_cell_moves_to_first_position_and_preserves_annotations(self):
        code = {"cell_type": "code", "source": ["# réponse"], "metadata": {}, "execution_count": None, "outputs": []}
        result = migrate_notebook({"cells": [code]}, self.sessions[0])
        result["cells"][0]["metadata"]["teacher_note"] = "à conserver"
        result["cells"].reverse()
        updated = migrate_notebook(result, self.sessions[0])
        self.assertEqual(updated["cells"][0]["metadata"]["teacher_note"], "à conserver")
        self.assertEqual(updated["cells"][1], code)
        self.assertEqual(migrate_notebook(updated, self.sessions[0]), updated)

    def test_malformed_or_duplicate_managed_cells_fail_closed(self):
        prototype = migrate_notebook({"cells": []}, self.sessions[0])
        for kind in ("duplicate", "missing_id", "code", "outside_text", "bad_close"):
            notebook = copy.deepcopy(prototype)
            first = notebook["cells"][0]
            if kind == "duplicate":
                notebook["cells"].append(copy.deepcopy(first))
            elif kind == "missing_id":
                del first["metadata"]["id"]
            elif kind == "code":
                first["cell_type"] = "code"
            elif kind == "outside_text":
                first["source"].append("Énoncé ajouté à préserver")
            else:
                first["source"][-1] = "clôture perdue"
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                migrate_notebook(notebook, self.sessions[0])

    def test_mode_switch_removes_td_instructions_from_both_locations(self):
        session = copy.deepcopy(self.sessions[0])
        notebook = migrate_notebook({"cells": []}, session)
        session["activity"] = "controle"
        result = migrate_notebook(notebook, session)
        context = next(iter(result["metadata"]["colab"]["aiContexts"].values()))["context"]
        markdown = "".join(result["cells"][0]["source"])
        for text in (context, markdown):
            self.assertIn("CONTRÔLE — AUCUNE ASSISTANCE", text)
            self.assertNotIn("TUTEUR TD", text)
            self.assertNotIn("MINI-COURS SI BESOIN", text)
            self.assertNotIn("PÉRIMÈTRE PAR EXERCICE", text)
        self.assertEqual(markdown, f"<!-- {CELL_START}\n{context}{CELL_END} -->\n")

    def test_per_exercise_library_permissions_are_required_and_closed(self):
        session = copy.deepcopy(self.sessions[0])
        session["allowed_libraries"] = ["csv"]
        session["exercises"][0]["allowed_libraries"] = []
        session["exercises"][-1]["allowed_libraries"] = ["csv"]
        context = render_context(session)
        first_line = next(line for line in context.splitlines() if line.startswith("Q1 —"))
        self.assertIn("bibliothèques : aucune", first_line)
        self.assertNotIn("csv", first_line)
        session["exercises"][0]["allowed_libraries"] = ["spacy"]
        with self.assertRaisesRegex(ValueError, "Bibliothèque"):
            render_context(session)
        del session["exercises"][0]["allowed_libraries"]
        with self.assertRaisesRegex(ValueError, "allowed_libraries"):
            render_context(session)

    def test_html_comment_cannot_be_terminated_by_manifest_text(self):
        for delimiter in ("-->", "<!--", CELL_END, "TAL_TD2_TUTOR_REMINDER_START"):
            session = copy.deepcopy(self.sessions[0])
            session["title"] += delimiter
            with self.subTest(delimiter=delimiter), self.assertRaisesRegex(ValueError, "Délimiteur"):
                render_context(session)

    def test_inventory_rejects_unclassified_and_stale_paths_without_parsing_exclusions(self):
        session = copy.deepcopy(self.sessions[0])
        session["notebook"] = "Notebooks TD/sujet.ipynb"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "Notebooks TD").mkdir()
            (root / session["notebook"]).write_text("{}")
            excluded = "Notebooks TD/corrige.ipynb"
            (root / excluded).write_text("{JSON tronqué, ne pas ouvrir")
            manifest = {"schema_version": 1, "sessions": [session], "excluded_notebooks": [{"notebook": excluded, "reason": "Corrigé enseignant"}]}
            self.assertEqual(validate_inventory(manifest, root), [session])
            new = root / "Notebooks TD/nouveau.ipynb"
            new.write_text("{}")
            with self.assertRaisesRegex(ValueError, "non classés"):
                validate_inventory(manifest, root)
            new.unlink()
            manifest["excluded_notebooks"][0]["notebook"] = "../ailleurs.ipynb"
            with self.assertRaisesRegex(ValueError, "hors périmètre"):
                validate_inventory(manifest, root)

    def test_write_validates_all_notebooks_before_first_mutation(self):
        session = copy.deepcopy(self.sessions[0])
        session["notebook"] = "Notebooks TD/a.ipynb"
        second = copy.deepcopy(session)
        second.update(id="SECOND", notebook="Notebooks TD/b.ipynb")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "Notebooks TD").mkdir()
            first_path = root / session["notebook"]
            first_path.write_text('{"cells": []}')
            (root / second["notebook"]).write_text('{"cells": [{"cell_type": "markdown", "source": "TAL_TUTOR_CONTEXT_START"}]}')
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"schema_version": 1, "sessions": [session, second], "excluded_notebooks": []}))
            before = first_path.read_bytes()
            with patch.object(tutor_metadata, "ROOT", root), patch.object(tutor_metadata, "MANIFEST", manifest):
                with self.assertRaises(ValueError):
                    tutor_metadata.main(["--write"])
            self.assertEqual(first_path.read_bytes(), before)


    def test_older_notebook_formats_receive_no_invalid_top_level_cell_id(self):
        for minor in (0, 4, 5):
            notebook = {"nbformat": 4, "nbformat_minor": minor, "metadata": {}, "cells": []}
            result = migrate_notebook(notebook, self.sessions[0])
            self.assertEqual("id" in result["cells"][0], minor >= 5)
            self.assertEqual(result["nbformat_minor"], minor)
            self.assertEqual(migrate_notebook(result, self.sessions[0]), result)

    def test_long_sessions_keep_every_concept_and_library_permission(self):
        for identifier in ("TD3_S2", "TD5_S2"):
            session = next(s for s in self.sessions if s["id"] == identifier)
            context = render_context(session)
            self.assertIn("Bibliothèques par ligne : aucune sauf mention", context)
            for exercise in session["exercises"]:
                line = next(line for line in context.splitlines() if line.startswith(exercise["id"] + " — "))
                for concept in exercise["available_concepts"]:
                    self.assertIn(concept, line)
                for library in exercise["allowed_libraries"]:
                    self.assertIn(library, line)
            self.assertLessEqual(len(context), CONTEXT_BUDGET)


if __name__ == "__main__":
    unittest.main()
