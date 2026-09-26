"""Frozen pre-migration proof: only metadata.tal may change in subjects.

The fixture was computed from Git revision 2a367529963f66a186dff1658b5951d0dbc27642,
never from the migrated working tree. Updating it requires a separately reviewed
pedagogical change; normal CI does not regenerate it.
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

    def test_all_subjects_preserve_every_field_except_new_routing_metadata(self):
        self.assertEqual(len(self.baseline["active"]), 32)
        for path, expected in self.baseline["active"].items():
            with self.subTest(notebook=path):
                notebook = json.loads((ROOT / path).read_text())
                self.assertEqual(canonical_hash(without_routing_metadata(notebook)), expected,
                                 "Content, outputs, cell order, IDs and tutor policy must be unchanged")
                entry = resolve_notebook(notebook)
                self.assertEqual(entry["notebook"], path)
                validate_cell_metadata(notebook)

    def test_inactive_subject_and_nine_excluded_notebooks_are_byte_identical(self):
        self.assertEqual(len(self.baseline["unchanged"]), 10)
        for path, expected in self.baseline["unchanged"].items():
            with self.subTest(notebook=path):
                self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), expected)

    def test_baseline_catalog_tutors_and_registry_cover_the_same_subjects(self):
        active = [entry for entry in self.catalog if entry["active"]]
        inactive = [entry for entry in self.catalog if not entry["active"]]
        self.assertEqual(set(self.baseline["active"]), {e["notebook"] for e in active})
        self.assertEqual(set(self.baseline["unchanged"]),
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


if __name__ == "__main__":
    unittest.main()
