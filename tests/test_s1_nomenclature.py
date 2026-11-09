"""Nomenclature S1 : titres et chemins nouveaux, contrats et stockage stables."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from notebook_contract import load_catalog, resolve_notebook
from routes import EVALUATORS
from storage_layout import storage_id, legacy_storage_id


class S1NomenclatureTests(unittest.TestCase):
    def test_nineteen_subjects_use_semester_first_and_keep_contract_ids(self):
        items = [entry for entry in load_catalog()
                 if entry["semester"] == "S1"
                 and entry["notebook"].startswith("Notebooks TD/S1/")]
        self.assertEqual(len(items), 19)
        self.assertEqual(len({entry["notebook"] for entry in items}), 19)
        for item in items:
            with self.subTest(item=item["id"]):
                path = ROOT / item["notebook"]
                self.assertTrue(path.is_file())
                self.assertTrue(path.stem.startswith("S1_TD"))
                nb = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(nb["metadata"]["tal"], {
                    "id": item["id"], "evaluator": item["evaluator"], "version": 2
                })
                self.assertEqual(resolve_notebook(nb), item)
                self.assertEqual(nb["metadata"]["tal_tutor"]["session"]["notebook"],
                                 item["notebook"])
                first_heading = "".join(nb["cells"][0]["source"]).splitlines()[0]
                self.assertTrue(first_heading.startswith("# S1 — TD"),
                                first_heading)
                self.assertIn(item["evaluator"], EVALUATORS)

    def test_detailed_variants_and_legacy_route_names_are_unchanged(self):
        catalog = {e["evaluator"]: e for e in load_catalog() if e["evaluator"]}
        for number in (4, 5, 6):
            self.assertEqual(catalog[f"td{number}-s1"]["notebook"].split("/")[-1]
                             .split("_", 2)[:2], ["S1", f"TD{number}"])
            for former, suffix in (("one", "A"), ("bis", "B"), ("ter", "C")):
                identifier = f"td{number}-{former}-s1"
                path = catalog[identifier]["notebook"]
                self.assertTrue(Path(path).name.startswith(
                    f"S1_TD{number}_{suffix}_"), path)
                self.assertEqual(EVALUATORS[identifier][1],
                                 f"app_correction_TD{number}_{former}_S1")
        # TD3 rejoint désormais la même nomenclature A/B/C que TD4 à TD6.
        for part, suffix in (("one", "A"), ("bis", "B"), ("ter", "C")):
            self.assertIn(f"S1_TD3_{suffix}_",
                          catalog[f"td3-{part}-s1"]["notebook"])
            self.assertEqual(storage_id(f"td3-{part}-s1"),
                             f"S1_TD3_{suffix}")

    def test_physical_storage_uses_s1_first_and_keeps_legacy_mapping(self):
        self.assertEqual(storage_id("td4-s1"), "S1_TD4")
        self.assertEqual(storage_id("td4-one-s1"), "S1_TD4_A")
        self.assertEqual(storage_id("td1-s1"), "S1_TD1")
        self.assertEqual(legacy_storage_id("td4-s1"), "TD4_S1")
        self.assertEqual(legacy_storage_id("td4-one-s1"), "TD4_one_S1")
        self.assertEqual(legacy_storage_id("td1-s1"), "TD1_S1")


if __name__ == "__main__":
    unittest.main()
