"""Migration complémentaire TD3 A/B/C, données fictives, sans écraser les dépôts."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import outils
from migrate_td3_variants import execute
from storage_layout import GRADE_COLUMNS, storage_id


def sample(number="00123", score="4,00", origin="direct:fixture"):
    return dict(zip(GRADE_COLUMNS, (
        "03/11/2026 10:00", "MARTIN", "Léa", "G1", score, "0,00",
        "technique_provisoire", "6", "requise", number,
        "2", origin, "",
    ))


class Td3VariantsMigrationTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        p = patch.object(outils, "BASE_DIR", str(self.root))
        p.start()
        self.addCleanup(p.stop)

    def csv(self, path, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, delimiter=";", fieldnames=GRADE_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    def read(self, path):
        with path.open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream, delimiter=";"))

    def test_a_b_c_are_now_canonical(self):
        for part, letter in [("one","A"),("bis","B"),("ter","C")]:
            self.assertEqual(storage_id(f"td3-{part}-s1"), f"S1_TD3_{letter}")

    def test_dry_run_does_not_modify_anything(self):
        src = self.root / "S1_TD3_one"
        self.csv(src / "notes_S1_TD3_one.csv", [sample()])
        output = execute(self.root)
        self.assertEqual(output["mode"], "SIMULATION")
        self.assertEqual(output["nouvelles_lignes"], 1)
        self.assertFalse((self.root / "S1_TD3_A").exists())
        self.assertFalse((self.root / "suivi").exists())
        with self.assertRaisesRegex(ValueError, "Sauvegarde"):
            execute(self.root, apply=True)

    def test_migration_is_non_destructive_idempotent_and_preserves_scores(self):
        src = self.root / "S1_TD3_one"
        dest = self.root / "S1_TD3_A"
        notes = src / "notes_S1_TD3_one.csv"
        self.csv(notes, [sample(), sample(score="5,00", origin="direct:second")])
        (src / "nb").mkdir()
        (src / "rapport").mkdir()
        (src / "nb" / "original.ipynb").write_text("original", encoding="utf-8")
        (src / "rapport" / "rapport.html").write_text("rapport", encoding="utf-8")
        before = notes.read_bytes()
        applied = execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        self.assertEqual(applied["nouvelles_lignes"], 2)
        self.assertEqual(applied["fichiers_a_copier"], 2)
        self.assertEqual(notes.read_bytes(), before)
        self.assertEqual((dest / "nb" / "original.ipynb").read_text(), "original")
        self.assertEqual((dest / "rapport" / "rapport.html").read_text(), "rapport")
        rows = self.read(dest / "notes_S1_TD3_A.csv")
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row["Origine"].startswith("migration-s1-v2:S1_TD3_one:")
                            for row in rows))
        with (self.root / "suivi" / "progression_S1.csv").open(encoding="utf-8") as f:
            student = next(csv.DictReader(f, delimiter=";"))
        self.assertEqual(student["td3-one-s1__essais"], "2")
        repeat = execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        self.assertEqual(repeat["nouvelles_lignes"], 0)
        self.assertEqual(repeat["fichiers_a_copier"], 0)
        self.assertEqual(len(self.read(dest / "notes_S1_TD3_A.csv")), 2)

    def test_multiple_parts_and_collision_kept(self):
        for part, letter in [("bis", "B"), ("ter", "C")]:
            src = self.root / ("S1_TD3_" + part)
            dest = self.root / ("S1_TD3_" + letter)
            self.csv(src / ("notes_S1_TD3_" + part + ".csv"), [sample(origin="direct:"+part)])
            self.csv(dest / ("notes_S1_TD3_" + letter + ".csv"), [sample(origin="new:"+letter)])
        result = execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        self.assertEqual(result["nouvelles_lignes"], 2)
        for letter in "BC":
            names = self.read(self.root / ("S1_TD3_" + letter) / ("notes_S1_TD3_" + letter + ".csv"))
            self.assertEqual(len(names), 2)
        with (self.root / "suivi" / "progression_S1.csv").open(encoding="utf-8") as f:
            student = next(csv.DictReader(f, delimiter=";"))
        self.assertEqual(student["td3-bis-s1__essais"], "2")
        self.assertEqual(student["td3-ter-s1__essais"], "2")


if __name__ == "__main__":
    unittest.main()
