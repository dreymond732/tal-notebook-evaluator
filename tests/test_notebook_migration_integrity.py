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


# New additions and the three reviewed R0–R2 revisions are explicit.
# The frozen fixture remains unchanged; the other 39 historical notebooks
# retain every original field/byte integrity assertion. See r012_v2_spec.md.
REVISED_SUBJECTS = {
    "Notebooks TD/S3/R0_S3_python_texte.ipynb": "td-r0-s3",
    "Notebooks TD/S3/R1_S3_doc_spacy.ipynb": "td-r1-s3",
    "Notebooks TD/S3/R2_S3_frequences_reutilisables.ipynb": "td-r2-s3",
}
ADDED_ACTIVE_SUBJECTS = {
    "Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb",
}
ADDED_EXCLUDED_NOTEBOOKS = {
    "Corrigés modèles/Contrôles finaux/dm-intermediaire-s1/DM_intermediaire_S1_corrige_non_execute.ipynb",
}


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
        self.assertEqual(len(set(self.baseline["active"]) - set(REVISED_SUBJECTS)), 29)
        self.assertTrue(set(REVISED_SUBJECTS) <= set(self.baseline["active"]))
        for path, expected in self.baseline["active"].items():
            if path in REVISED_SUBJECTS:
                continue
            with self.subTest(notebook=path):
                notebook = json.loads((ROOT / path).read_text())
                self.assertEqual(canonical_hash(without_routing_metadata(notebook)), expected,
                                 "Content, outputs, cell order, IDs and tutor policy must be unchanged")
                entry = resolve_notebook(notebook)
                self.assertEqual(entry["notebook"], path)
                validate_cell_metadata(notebook)

    def test_reviewed_revisions_have_explicit_version_two_contracts(self):
        self.assertEqual(len(REVISED_SUBJECTS), 3)
        for path, evaluator in REVISED_SUBJECTS.items():
            with self.subTest(notebook=path):
                notebook = json.loads((ROOT / path).read_text())
                self.assertEqual(notebook["metadata"]["tal"], {
                    "id": evaluator, "evaluator": evaluator, "version": 2})
                entry = resolve_notebook(notebook)
                self.assertEqual(entry["notebook"], path)
                self.assertEqual((entry["semester"], entry["mode"], entry["version"]),
                                 ("S3", "td", 2))
                indexed = validate_cell_metadata(notebook)
                self.assertEqual({q for q, role in indexed if role == "answer"},
                                 {"Q1", "Q2", "Q3", "Q4"})
                self.assertIn(("identity", "identification"), indexed)
                self.assertNotIn(("submission", "submission"), indexed)
                for cell in notebook["cells"]:
                    if cell["cell_type"] == "code":
                        self.assertEqual(cell.get("outputs", []), [])
                        self.assertIsNone(cell.get("execution_count"))

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
        self.assertEqual(set(self.baseline["active"]) | ADDED_ACTIVE_SUBJECTS,
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
