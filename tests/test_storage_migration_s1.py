"""Migration v2 des 19 répertoires S1 : copies fictives, aucun réseau."""
import csv
import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import outils
from migrate_storage_s1 import execute
from storage_layout import GRADE_COLUMNS, legacy_storage_id, storage_id


def record(score, origin, number="0000123", version="2", name="Martin"):
    return dict(zip(GRADE_COLUMNS, (
        "03/11/2026 10:00", name, "Alice", "Master_TILT", str(score), "0,00",
        "technique_provisoire", "7", "requise", number, version, origin, "",
    )))


class MigrationS1LayoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.patcher = patch.object(outils, "BASE_DIR", str(self.root))
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.old = self.root / "TD4_S1"
        self.new = self.root / "S1_TD4"

    def csv(self, path, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=GRADE_COLUMNS, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)
        return path

    def read(self, path):
        with path.open("r", encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream, delimiter=";"))

    def old_csv(self, rows):
        return self.csv(self.old / "notes_TD4_S1.csv", rows)

    def new_csv(self, rows):
        return self.csv(self.new / "notes_S1_TD4.csv", rows)

    def archive(self, directory, sub, name, content):
        folder = directory / sub
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / name
        path.write_bytes(content)
        return path

    def test_nineteen_names_and_non_s1_untouched(self):
        for number in range(1, 8):
            self.assertEqual(storage_id(f"td{number}-s1"), f"S1_TD{number}")
            self.assertEqual(legacy_storage_id(f"td{number}-s1"), f"TD{number}_S1")
        for number in range(3, 7):
            for part in ("one", "bis", "ter"):
                suffix = part if number == 3 else {"one": "A", "bis": "B", "ter": "C"}[part]
                self.assertEqual(storage_id(f"td{number}-{part}-s1"),
                                 f"S1_TD{number}_{suffix}")
                self.assertEqual(legacy_storage_id(f"td{number}-{part}-s1"),
                                 f"TD{number}_{part}_S1")
        for other in ("td2-S2", "td1-s3", "dm-intermediaire-s1", "controle-td1-s3"):
            self.assertEqual(storage_id(other), legacy_storage_id(other))

    def test_dry_run_no_files_and_safe_repeat(self):
        src = self.old_csv([record("2,00", "direct:one"),
                            record("6,00", "direct:two")])
        nb = self.archive(self.old, "nb", "copie.ipynb", b"synthetic notebook")
        html = self.archive(self.old, "rapport", "rapport.html", b"<p>synthetic</p>")
        original = {p: p.read_bytes() for p in (src, nb, html)}
        result = execute(self.root)
        self.assertEqual(result["evaluations_s1"], 19)
        self.assertEqual(result["lignes_sources"], 2)
        self.assertEqual(result["nouvelles_lignes"], 2)
        self.assertEqual(result["fichiers_a_copier"], 2)
        self.assertEqual(result["mode"], "SIMULATION")
        self.assertFalse(self.new.exists())
        self.assertFalse((self.root / "suivi").exists())
        with self.assertRaisesRegex(ValueError, "backup-confirmed"):
            execute(self.root, apply=True)

        result = execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        self.assertEqual(result["nouvelles_lignes"], 2)
        new_records = self.read(self.new / "notes_S1_TD4.csv")
        self.assertEqual(len(new_records), 2)
        self.assertTrue(all(r["Origine"].startswith("migration-s1-v2:TD4_S1:")
                            for r in new_records))
        self.assertEqual(new_records[0]["Numéro étudiant"], "0000123")
        self.assertEqual((self.new / "nb" / nb.name).read_bytes(), nb.read_bytes())
        self.assertEqual((self.new / "rapport" / html.name).read_bytes(), html.read_bytes())
        for path, content in original.items():
            self.assertEqual(path.read_bytes(), content)
        # La synthèse initiale TD4 constitue désormais un vrai TD suivi.
        self.assertEqual(result["progression"]["essais"], 2)
        records = self.read(self.root / "suivi" / "progression_S1.csv")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["td4-s1__essais"], "2")
        repeated = execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        self.assertEqual(repeated["nouvelles_lignes"], 0)
        self.assertEqual(repeated["lignes_deja_importees"], 2)
        self.assertEqual(repeated["fichiers_a_copier"], 0)
        self.assertEqual(len(self.read(self.new / "notes_S1_TD4.csv")), 2)

    def test_current_activity_preserves_attempts_and_progression(self):
        old = self.root / "TD4_one_S1"
        target = self.root / "S1_TD4_A"
        self.csv(old / "notes_TD4_one_S1.csv", [
            record("1,00", "direct:attempt1"), record("3,00", "direct:attempt2"),
        ])
        self.csv(target / "notes_S1_TD4_A.csv", [
            record("5,00", "direct:after-deploy")
        ])
        source = self.archive(old, "nb", "original.ipynb", b"original")
        other = self.archive(target, "nb", "new.ipynb", b"new version")
        execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        merged = self.read(target / "notes_S1_TD4_A.csv")
        self.assertEqual(len(merged), 3)
        self.assertEqual(merged[0]["Origine"], "direct:after-deploy")
        self.assertEqual(source.read_bytes(), (target / "nb" / source.name).read_bytes())
        self.assertEqual(other.read_bytes(), b"new version")
        with (self.root / "suivi" / "progression_S1.csv").open(
            encoding="utf-8", newline=""
        ) as f:
            student = next(csv.DictReader(f, delimiter=";"))
        self.assertEqual(student["td4-one-s1__essais"], "3")
        self.assertEqual(student["td4-one-s1__min"], "1,00")
        self.assertEqual(student["td4-one-s1__max"], "5,00")

    def test_same_name_distinct_content_kept_without_overwrite(self):
        self.old_csv([record("4,00", "direct:one")])
        self.archive(self.old, "nb", "copie.ipynb", b"previous")
        current = self.archive(self.new, "nb", "copie.ipynb", b"current")
        result = execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        self.assertEqual(result["fichiers_a_copier"], 1)
        self.assertEqual(current.read_bytes(), b"current")
        variants = list((self.new / "nb").glob("copie__s1_source_*.ipynb"))
        self.assertEqual(len(variants), 1)
        self.assertEqual(variants[0].read_bytes(), b"previous")
        self.assertEqual(execute(self.root, apply=True, backup_confirmed=True,
                                 year="2026-2027")["fichiers_a_copier"], 0)

    def test_identical_name_identical_content_not_recopied(self):
        self.old_csv([record("4,00", "direct:one")])
        self.archive(self.old, "nb", "copie.ipynb", b"same")
        self.archive(self.new, "nb", "copie.ipynb", b"same")
        result = execute(self.root)
        self.assertEqual(result["fichiers_a_copier"], 0)

    def test_source_rewrite_after_migration_fails_closed(self):
        source = self.old_csv([record("4,00", "direct:one")])
        execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        self.old_csv([record("99,00", "direct:one")])
        with self.assertRaisesRegex(ValueError, "source modifié"):
            execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        self.assertEqual(self.read(self.new / "notes_S1_TD4.csv")[0]["Score"], "4,00")

    def test_missing_source_row_after_migration_fails_closed(self):
        self.old_csv([record("4,00", "direct:one"),
                      record("6,00", "direct:two")])
        execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        self.old_csv([record("4,00", "direct:one")])
        with self.assertRaisesRegex(ValueError, "sources disparues"):
            execute(self.root)

    def test_invalid_header_and_symlink_prevent_all_writes(self):
        self.old.mkdir()
        bad = self.old / "notes_TD4_S1.csv"
        bad.write_text("Bad;Header\n42;Test\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "schéma consolidé"):
            execute(self.root, apply=True, backup_confirmed=True)
        self.assertFalse(self.new.exists())
        bad.unlink()
        (self.old / "nb").symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symbolique"):
            execute(self.root)

    def test_unrecognized_files_abort_without_copy(self):
        self.old_csv([record("2,00", "direct:one")])
        (self.old / "unknown.txt").write_text("do not discard")
        with self.assertRaisesRegex(ValueError, "imprévu"):
            execute(self.root, apply=True, backup_confirmed=True)
        self.assertFalse(self.new.exists())

    def test_identical_plain_row_in_target_is_ambiguous(self):
        row = record("2,00", "direct:one")
        self.old_csv([row])
        self.new_csv([row])
        with self.assertRaisesRegex(ValueError, "sans provenance"):
            execute(self.root)

    def test_missing_s1_no_empty_directory_created(self):
        result = execute(self.root, apply=True, backup_confirmed=True, year="2026-2027")
        self.assertEqual(result["nouvelles_lignes"], 0)
        self.assertEqual(result["dossiers_sources_presents"], 0)
        self.assertFalse((self.root / "S1_TD1").exists())


if __name__ == "__main__":
    unittest.main()
