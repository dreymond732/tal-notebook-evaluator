"""Régression du rangement sans classe et de la migration non destructive."""
import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

import outils
import migrate_storage
import progression
from migrate_storage import execute
from progression import refresh_progression, progression_lock
from routes import process_submission
from storage_layout import GRADE_COLUMNS, storage_id, legacy_storage_id


class StorageMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Le migrateur v1 reste vérifié dans son contexte historique,
        # mais est désormais interdit en production avec le stockage S1 v2.
        for module in (migrate_storage, progression):
            guard = patch.object(module, "storage_id", legacy_storage_id)
            guard.start()
            self.addCleanup(guard.stop)

    def legacy(self, storage, group, values, technical=True):
        directory = self.root / storage / group
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / ("notes_" + storage + "_" + group + ".csv")
        header = ["Date", "Nom", "Prénom", "Classe",
                  "Score technique provisoire" if technical else "Note",
                  "Bonus"] + (["Nature du score", "Maximum technique", "Relecture humaine"] if technical else []) + ["Numéro étudiant"]
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, delimiter=";")
            writer.writerow(header)
            for name, value in values:
                writer.writerow(["03/11/2026 10:00", name, "Alice", group, value, "0,00"] +
                                (["technique_provisoire", "7", "requise"] if technical else []) + ["00123"])
        return path

    def read(self, path):
        with path.open("r", encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream, delimiter=";"))

    def test_canonical_names_follow_module_names(self):
        self.assertEqual(legacy_storage_id("td2-s1"), "TD2_S1")
        self.assertEqual(storage_id("td2-s1"), "S1_TD2")
        self.assertEqual(legacy_storage_id("td3-one-s1"), "TD3_one_S1")
        self.assertEqual(storage_id("td3-one-s1"), "S1_TD3_one")
        self.assertEqual(storage_id("td2-S2"), "TD2_S2")
        self.assertEqual(storage_id("td1b-s3"), "TD1B_S3")
        self.assertEqual(storage_id("controle-td1-s3"), "Controle_TD1_S3")

    def test_merge_versions_and_groups_preserves_each_attempt_and_artifact(self):
        files = []
        for group, score, content in [
            ("M1_TILT", "2,00", b"version one"),
            ("M1_TILT_Programmation", "5,00", b"version two"),
            ("Master_TILT", "7,00", b"version three"),
        ]:
            self.legacy("td2-s1-v2", group, [("MARTIN", score)])
            target = self.root / "td2-s1-v2" / group
            (target / "nb").mkdir()
            (target / "rapport").mkdir()
            (target / "nb" / "copie.ipynb").write_bytes(content)
            (target / "rapport" / "resultat.html").write_bytes(content)
            files.append(target)
        self.legacy("td2-s1", "ancienne", [("MARTIN", "1,00")], technical=False)
        files.append(self.root / "td2-s1" / "ancienne")
        source_checksums = {p: p.read_bytes() for d in files for p in d.rglob("*") if p.is_file()}
        first = execute(self.root)
        self.assertEqual(first["mode"], "DRY_RUN")
        self.assertEqual(first["nouvelles_lignes"], 4)
        self.assertFalse((self.root / "TD2_S1").exists())
        applied = execute(self.root, apply=True)
        self.assertEqual(applied["nouvelles_lignes"], 4)
        target = self.root / "TD2_S1"
        journal = target / "notes_TD2_S1.csv"
        merged = self.read(journal)
        self.assertEqual(len(merged), 4)
        self.assertEqual({r["Version du contrat"] for r in merged}, {"1", "2"})
        self.assertEqual(len(list((target / "nb").glob("*.ipynb"))), 3)
        self.assertEqual(len(list((target / "rapport").glob("*.html"))), 3)
        self.assertEqual({r["Classe"] for r in merged}, set([
            "M1_TILT", "M1_TILT_Programmation", "Master_TILT", "ancienne"]))
        for p, before in source_checksums.items():
            self.assertEqual(p.read_bytes(), before)
        with progression_lock(self.root):
            result = refresh_progression(self.root, "2026-2027")
        self.assertEqual(result["essais"], 3)
        record = self.read(self.root / "suivi" / "progression_S1.csv")[0]
        self.assertEqual(record["td2-s1__min"], "2,00")
        self.assertEqual(record["td2-s1__max"], "7,00")
        self.assertEqual(record["td2-s1__essais"], "3")
        repeated = execute(self.root, apply=True)
        self.assertEqual(repeated["nouvelles_lignes"], 0)
        self.assertEqual(repeated["fichiers_a_copier"], 0)
        self.assertEqual(len(self.read(journal)), 4)

    def test_direct_writes_ignore_group_and_do_not_overwrite_attempts(self):
        with patch.object(outils, "BASE_DIR", str(self.root)), patch.object(
            progression, "storage_id", storage_id
        ):
            app = Flask(__name__)
            with app.app_context():
                for score, group in ((1.0, "M1_TILT"), (3.0, "Master_TILT")):
                    process_submission(
                        SimpleNamespace(filename="TD2_S1.ipynb"), b'{"cells":[]}',
                        "<html>rapport</html>", {
                            "nom": "MARTIN", "prenom": "Alice", "classe": group,
                            "numero_etudiant": "00123", "contract_version": 2,
                            "score_nature": "technique_provisoire", "score_max": 7,
                            "relecture_humaine": "requise",
                        }, score, "td2-s1"
                    )
        folder = self.root / "S1_TD2"
        self.assertEqual(len(list((folder / "nb").glob("*.ipynb"))), 2)
        self.assertEqual(len(list((folder / "rapport").glob("*.html"))), 2)
        data = self.read(folder / "notes_S1_TD2.csv")
        self.assertEqual(len(data), 2)
        self.assertEqual(list(data[0]), list(GRADE_COLUMNS))
        self.assertEqual([r["Classe"] for r in data], ["M1_TILT", "Master_TILT"])
        self.assertTrue(all(row["Origine"].startswith("direct:") for row in data))
        self.assertEqual(self.read(self.root / "suivi" / "progression_S1.csv")[0]["td2-s1__essais"], "2")

    def test_corrupt_csv_prevents_any_copy(self):
        target = self.root / "td2-s1-v2" / "G1"
        target.mkdir(parents=True)
        (target / "notes_bad.csv").write_text("invalid;header\n123;345\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Schéma CSV inconnu"):
            execute(self.root, apply=True)
        self.assertFalse((self.root / "TD2_S1").exists())

    def test_old_migrator_refuses_to_write_with_new_layout(self):
        with patch.object(migrate_storage, "storage_id", storage_id):
            with self.assertRaisesRegex(ValueError, "obsolète"):
                execute(self.root, apply=True)

    def test_bad_csv_existing_in_destination_is_never_overwritten(self):
        target = self.root / "TD2_S1"
        target.mkdir()
        original = "Note;Nom\n1;TEST\n"
        (target / "notes_TD2_S1.csv").write_text(original)
        with self.assertRaisesRegex(ValueError, "autre schéma"):
            execute(self.root, apply=True)
        self.assertEqual((target / "notes_TD2_S1.csv").read_text(), original)


if __name__ == "__main__":
    unittest.main()
