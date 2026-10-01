"""Frozen pre-migration proof: only metadata.tal may change in subjects.

The fixture was computed from Git revision 2a367529963f66a186dff1658b5951d0dbc27642,
never from the migrated working tree. Updating it requires a separately reviewed
pedagogical change; normal CI does not regenerate it. New subjects are listed
explicitly below. Pedagogically reviewed revisions keep the original baseline
fixture intact and are checked against their new contract separately.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))
from notebook_contract import load_catalog, resolve_notebook, validate_cell_metadata
import routes
from prepare_student_notebooks import submission_cell


# Reviewed S3 v2 revisions are explicit. The historical fixture stays frozen;
# the other 17 original notebooks retain all field/byte integrity assertions.
# The fifteen later revisions also retain a separate pre-change cell baseline.
R012_REVISED_SUBJECTS = {
    "Notebooks TD/S3/R0_S3_python_texte.ipynb": "td-r0-s3",
    "Notebooks TD/S3/R1_S3_doc_spacy.ipynb": "td-r1-s3",
    "Notebooks TD/S3/R2_S3_frequences_reutilisables.ipynb": "td-r2-s3",
}
S3_REVISED_SUBJECTS = {
    "Notebooks TD/S3/TD0_S3_diagnostic_texte.ipynb": "td0-s3",
    "Notebooks TD/S3/TD1_S3_fondations_spacy.ipynb": "td1-s3",
    "Notebooks TD/S3/TD2_S3_analyse_corpus.ipynb": "td2-s3",
    "Notebooks TD/S3/TD3_S3_concordances_citations.ipynb": "td3-s3",
    "Notebooks TD/S3/TD4_S3_cooccurrences.ipynb": "td4-s3",
    "Notebooks TD/S3/TD5_S3_associations.ipynb": "td5-s3",
    "Notebooks TD/S3/TD6_S3_visualisations.ipynb": "td6-s3",
    "Notebooks TD/S3/TD7_S3_audit_llm.ipynb": "td7-s3",
    **{f"Notebooks contrôles finaux/S3/Controle_TD{n}_S3.ipynb":
       f"controle-td{n}-s3" for n in range(1, 8)},
}
S1_REVISED_SUBJECTS = {f"Notebooks TD/S1/TD{n}_S1_python_texte.ipynb": f"td{n}-s1" for n in range(1, 8)}
REVISED_SUBJECTS = R012_REVISED_SUBJECTS | S3_REVISED_SUBJECTS | S1_REVISED_SUBJECTS
ADDED_ACTIVE_SUBJECTS = {
    "Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb",
}
ADDED_EXCLUDED_NOTEBOOKS = {
    "Corrigés modèles/Contrôles finaux/dm-intermediaire-s1/DM_intermediaire_S1_corrige_non_execute.ipynb",
}


# The PR19 rename remains independently checked against the historical fixture.
# The seven newly revised subjects are separately checked against PR19 below.
S1_RENAMED_SUBJECTS = {
    f"Notebooks TD/S1/TD{n}_S1_python_texte.ipynb": f"Notebooks TD/S1/TD{n}_S1_{topic}.ipynb"
    for n, topic in enumerate((
        "variables_types", "chaines_sequences", "collections",
        "boucles_conditions_comptages", "fonctions_reutilisation",
        "fichiers_csv", "expressions_regulieres_pipeline"), 1)
}


def original_s1_content(notebook):
    """Remove only the exact canonical final addition; reject any hidden edit."""
    original = copy.deepcopy(notebook)
    if not original["cells"] or original["cells"][-1] != submission_cell():
        raise AssertionError("The S1 source must end with the canonical URL placeholder")
    original["cells"].pop()
    evaluator = original["metadata"]["tal"]["id"]
    number = int(evaluator.split("-")[0][2:])
    old_path = f"Notebooks TD/S1/TD{number}_S1_python_texte.ipynb"
    session = original["metadata"]["tal_tutor"]["session"]
    if session["notebook"] != S1_RENAMED_SUBJECTS[old_path]:
        raise AssertionError("The tutor session must point to the renamed subject")
    session["notebook"] = old_path
    # At the frozen revision only the first tutor cell already had an ID.
    # Verify the exact reviewed ID scheme before removing newly added IDs.
    if original["cells"][0].get("id") != "tal-tutor-instructions":
        raise AssertionError("The existing tutor ID must remain unchanged")
    for cell in original["cells"][1:]:
        contract = cell["metadata"]["tal"]
        expected = f'{evaluator}-{contract["role"]}-{contract["question"]}'.lower()
        if cell.pop("id", None) != expected:
            raise AssertionError("Missing or modified reviewed S1 cell ID")
    return original


def without_routing_metadata(notebook):
    stripped = copy.deepcopy(notebook)
    stripped.get("metadata", {}).pop("tal", None)
    for cell in stripped["cells"]:
        cell.get("metadata", {}).pop("tal", None)
    return stripped


def canonical_hash(value):
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class MigrationIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = json.loads((ROOT / "tests/fixtures/notebook_migration_baseline.json").read_text())
        cls.catalog = load_catalog()
        cls.tutors = json.loads((ROOT / "docs/pedagogy/tutor_sessions.json").read_text())

    def test_unrevised_subjects_preserve_every_field_except_routing_metadata(self):
        self.assertEqual(len(self.baseline["active"]), 32)
        self.assertEqual(len(set(self.baseline["active"]) - set(REVISED_SUBJECTS)), 7)
        self.assertTrue(set(REVISED_SUBJECTS) <= set(self.baseline["active"]))
        for path, expected in self.baseline["active"].items():
            if path in REVISED_SUBJECTS:
                continue
            with self.subTest(notebook=path):
                current_path = S1_RENAMED_SUBJECTS.get(path, path)
                notebook = json.loads((ROOT / current_path).read_text())
                original = original_s1_content(notebook) if path in S1_RENAMED_SUBJECTS else notebook
                self.assertEqual(canonical_hash(without_routing_metadata(original)), expected,
                                 "Content, outputs, cell order, IDs and tutor policy must be unchanged")
                entry = resolve_notebook(notebook)
                self.assertEqual(entry["notebook"], current_path)
                validate_cell_metadata(notebook)

    def test_pr19_frozen_s1_baseline_retains_original_migration_proof(self):
        baseline = json.loads((ROOT / "tests/fixtures/s1_progression_v2_source_baseline.json").read_text())
        self.assertEqual(baseline["source_commit"], "322abf53b4a1ff96c1652acfa21b4d27185bfa1a")
        self.assertEqual(set(baseline["subjects"]), set(S1_RENAMED_SUBJECTS.values()))
        for old_path, current_path in S1_RENAMED_SUBJECTS.items():
            with self.subTest(notebook=current_path):
                original = original_s1_content(baseline["subjects"][current_path])
                self.assertEqual(canonical_hash(without_routing_metadata(original)),
                                 self.baseline["active"][old_path])

    def test_reviewed_revisions_have_explicit_version_two_contracts(self):
        self.assertEqual(len(REVISED_SUBJECTS), 25)
        for path, evaluator in (R012_REVISED_SUBJECTS | S3_REVISED_SUBJECTS).items():
            with self.subTest(notebook=path):
                notebook = json.loads((ROOT / path).read_text())
                self.assertEqual(notebook["metadata"]["tal"], {
                    "id": evaluator, "evaluator": evaluator, "version": 2})
                entry = resolve_notebook(notebook)
                self.assertEqual(entry["notebook"], path)
                self.assertEqual((entry["semester"], entry["mode"], entry["version"]),
                                 ("S3", "controle" if evaluator.startswith("controle-") else "td", 2))
                indexed = validate_cell_metadata(notebook)
                self.assertEqual({q for q, role in indexed if role == "answer"},
                                 {f"Q{q}" for q in range(1, (4 if path in R012_REVISED_SUBJECTS else 6 if evaluator == "td1-s3" else 7) + 1)})
                self.assertIn(("identity", "identification"), indexed)
                self.assertNotIn(("submission", "submission"), indexed)
                for cell in notebook["cells"]:
                    if cell["cell_type"] == "code":
                        self.assertEqual(cell.get("outputs", []), [])
                        self.assertIsNone(cell.get("execution_count"))

    def test_fifteen_revisions_preserve_frozen_cells_and_only_append_declared_text(self):
        # Captured from the parent merge commit, never regenerated from revisions.
        baseline = json.loads((ROOT / "tests/fixtures/s3_complete_v2_source_baseline.json").read_text())
        self.assertEqual(baseline["source_commit"], "02f435dc770834b21e242592804d231e0836a4b7")
        self.assertEqual(set(baseline["subjects"]), set(S3_REVISED_SUBJECTS))
        prefixes, reviews = 0, 0
        for path, expected in baseline["subjects"].items():
            notebook = json.loads((ROOT / path).read_text())
            cells = notebook.pop("cells")
            with self.subTest(notebook=path):
                self.assertEqual(canonical_hash(notebook), expected["notebook_without_cells_sha256"])
                self.assertEqual(len(cells), len(expected["cells"]))
            for number, (cell, previous) in enumerate(zip(cells, expected["cells"])):
                with self.subTest(notebook=path, cell=number):
                    self.assertEqual(cell.get("id"), previous["id"])
                    if "review_question" in previous:
                        self.assertEqual(cell["metadata"].pop("tal_review"),
                                         {"question": previous["review_question"]})
                        reviews += 1
                    if "source_prefix" in previous:
                        self.assertTrue("".join(cell.pop("source")).startswith(previous["source_prefix"]),
                                        "The original instructions and identity code must remain an exact prefix")
                        self.assertEqual(canonical_hash(cell), previous["other_fields_sha256"])
                        prefixes += 1
                    else:
                        self.assertEqual(canonical_hash(cell), previous["sha256"],
                                         "Undeclared changes to content, examples, figures or tutor policy")
        self.assertEqual(prefixes, 37)  # two common cells per subject + seven named prompts
        self.assertEqual(reviews, 49)

    def test_inactive_subject_and_nine_excluded_notebooks_are_byte_identical(self):
        self.assertEqual(len(self.baseline["unchanged"]), 10)
        for path, expected in self.baseline["unchanged"].items():
            with self.subTest(notebook=path):
                self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), expected)

    def test_baseline_catalog_tutors_and_registry_cover_the_same_subjects(self):
        active = [entry for entry in self.catalog if entry["active"]]
        inactive = [entry for entry in self.catalog if not entry["active"]]
        self.assertTrue(ADDED_ACTIVE_SUBJECTS.isdisjoint(self.baseline["active"]))
        self.assertTrue(ADDED_EXCLUDED_NOTEBOOKS.isdisjoint(self.baseline["unchanged"]))
        current_original_paths = {S1_RENAMED_SUBJECTS.get(path, path) for path in self.baseline["active"]}
        self.assertEqual(current_original_paths | ADDED_ACTIVE_SUBJECTS,
                         {e["notebook"] for e in active})
        self.assertEqual(set(self.baseline["unchanged"]) | ADDED_EXCLUDED_NOTEBOOKS,
                         {e["notebook"] for e in inactive} |
                         {e["notebook"] for e in self.tutors["excluded_notebooks"]})
        self.assertEqual({e["notebook"] for e in self.catalog},
                         {e["notebook"] for e in self.tutors["sessions"]})
        sessions = {e["id"]: e for e in self.tutors["sessions"]}
        for entry in self.catalog:
            with self.subTest(subject=entry["id"]):
                tutor = sessions[entry["tutor_session"]]
                self.assertEqual(entry["notebook"], tutor["notebook"])
                self.assertEqual(entry["semester"], f'S{tutor["semester"]}')
                self.assertEqual(entry["mode"], tutor["activity"])
                if entry["active"]:
                    self.assertEqual(entry["mode"], routes.EVALUATOR_MODES[entry["evaluator"]])
                    self.assertEqual(entry["semester"], routes.EVALUATOR_SEMESTERS[entry["evaluator"]])

    def test_new_subject_is_resolvable_and_model_is_explicitly_excluded(self):
        for path in ADDED_ACTIVE_SUBJECTS:
            with self.subTest(notebook=path):
                notebook = json.loads((ROOT / path).read_text())
                entry = resolve_notebook(notebook)
                self.assertEqual(entry["notebook"], path)
                self.assertEqual(entry["semester"], "S1")
                self.assertEqual(entry["mode"], "controle")
                validate_cell_metadata(notebook)
        exclusions = {e["notebook"]: e for e in self.tutors["excluded_notebooks"]}
        for path in ADDED_EXCLUDED_NOTEBOOKS:
            with self.subTest(notebook=path):
                self.assertTrue((ROOT / path).is_file())
                self.assertTrue(exclusions[path]["reason"].strip())
                self.assertNotIn(path, {e["notebook"] for e in self.catalog})


if __name__ == "__main__":
    unittest.main()
