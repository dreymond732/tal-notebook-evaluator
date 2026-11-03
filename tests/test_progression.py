"""Tests de consolidation : données intégralement fictives, hors volume réel."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import outils
from progression import HISTORICAL, progression_lock, refresh_progression
from routes import process_submission


class ProgressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write_notes(self, storage, group, values, provisional=False):
        from storage_layout import GRADE_COLUMNS, storage_id
        from notebook_contract import load_catalog
        import re
        evaluator = re.sub(r"-v\d+$", "", storage)
        registered = {entry.get("evaluator"): entry for entry in load_catalog()
                      if entry.get("evaluator") and entry["active"]}
        current = (evaluator in registered and
                   evaluator not in {"td3-s1", "td4-s1", "td5-s1", "td6-s1", "Controletilt-s1"} and
                   (storage.endswith("-v" + str(registered[evaluator]["version"]))
                    or storage == evaluator and registered[evaluator]["version"] == 1))
        if current:
            folder = storage_id(evaluator)
            directory = self.root / folder
            path = directory / ("notes_" + folder + ".csv")
        else:
            directory = self.root / storage / group
            path = directory / ("notes_" + storage + "_" + group + ".csv")
        directory.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, delimiter=";")
            if current:
                writer.writerow(GRADE_COLUMNS)
                for date, nom, prenom, score, numero in values:
                    writer.writerow([
                        date, nom, prenom, group, score, "0,00",
                        "technique_provisoire" if provisional else "note",
                        "6" if provisional else "", "requise" if provisional else "",
                        numero, str(registered[evaluator]["version"]), "direct:test", ""
                    ])
            else:
                writer.writerow(["Date", "Nom", "Prénom", "Classe",
                                 "Score technique provisoire" if provisional else "Note",
                                 "Bonus", "Numéro étudiant"])
                for date, nom, prenom, score, numero in values:
                    writer.writerow([date, nom, prenom, group, score, "0,00", numero])
        return path

    def read_export(self, filename):
        with (self.root / "suivi" / filename).open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream, delimiter=";"))

    def test_min_max_attempts_by_student_and_semester(self):
        self.write_notes("td1-s1-v2", "G1", [
            ("03/11/2026 10:00", "Martin", "Léa", "2,00", "000123"),
            ("03/11/2026 11:00", "Martin", "Léa", "6,00", "000123"),
            ("03/11/2026 12:00", "Martin", "Léa", "4,00", "000123"),
            ("03/11/2026 11:20", "Durand", "Paul", "0,00", "000124"),
            ("03/11/2025 11:20", "Martin", "Léa", "1,00", "000123"),
        ], provisional=True)
        self.write_notes("td2-S2-v2", "G2", [
            ("03/11/2026 11:00", "Martin", "Léa", "14,00", "000123"),
        ])
        self.write_notes("dm-intermediaire-s1", "G1", [
            ("03/11/2026 11:00", "Martin", "Léa", "12,00", "000123"),
        ])
        self.write_notes("td1-s3-v2", "G3", [
            ("03/11/2026 12:00", "Martin", "Léa", "3,50", "000123"),
        ])
        with progression_lock(self.root):
            summary = refresh_progression(self.root, "2026-2027")
        self.assertEqual(summary["essais"], 7)
        s1 = {r["Numéro étudiant"]: r for r in self.read_export("progression_S1.csv")}
        self.assertEqual(len(s1), 2)
        self.assertEqual(s1["000123"]["td1-s1__min"], "2,00")
        self.assertEqual(s1["000123"]["td1-s1__max"], "6,00")
        self.assertEqual(s1["000123"]["td1-s1__essais"], "3")
        self.assertEqual(s1["000123"]["dm-intermediaire-s1__min"], "12,00")
        self.assertEqual(s1["000124"]["td1-s1__min"], "0,00")
        self.assertEqual(s1["000124"]["td2-s1__essais"], "0")
        self.assertEqual(self.read_export("progression_S2.csv")[0]["td2-S2__min"], "14,00")
        self.assertEqual(self.read_export("progression_S3.csv")[0]["td1-s3__min"], "3,50")
        catalog = self.read_export("catalogue_evaluations.csv")
        self.assertTrue(any(r["Type"] == "DM" for r in catalog))
        self.assertTrue(any(r["Type"] == "Contrôle" for r in catalog))
        self.assertTrue(any(r["Nature du score"] == "Score technique provisoire" for r in catalog))

    def test_historical_versions_and_syntheses_excluded(self):
        self.write_notes("td1-s1", "G1", [
            ("03/11/2026 09:00", "Ancien", "Test", "5", "998"),
        ])
        for historical in ("td3-s1-v2", "td4-s1-v2", "Controletilt-s1"):
            self.write_notes(historical, "G1", [
                ("03/11/2026 09:00", "Ancien", "Test", "5", "998"),
            ])
        self.assertIn("td3-s1", HISTORICAL)
        with progression_lock(self.root):
            refresh_progression(self.root, "2026-2027")
        self.assertEqual(self.read_export("progression_S1.csv"), [])
        catalog = self.read_export("catalogue_evaluations.csv")
        self.assertFalse(any(r["Évaluation"] in HISTORICAL for r in catalog))

    def test_correspondence_is_only_applied_after_manual_validation(self):
        self.write_notes("td1-s1-v2", "G1", [
            ("03/11/2026 09:00", "Martin", "Léa", "2,00", "000123"),
            ("03/11/2026 10:00", "Martin", "Léa", "4,00", ""),
        ])
        with progression_lock(self.root):
            first = refresh_progression(self.root, "2026-2027")
        self.assertEqual(first["sans_numero"], 1)
        self.assertEqual(self.read_export("progression_S1.csv")[0]["td1-s1__essais"], "1")
        suggestions = self.read_export("correspondances_a_valider.csv")
        self.assertEqual(suggestions[0]["Numéro proposé"], "000123")
        self.assertEqual(suggestions[0]["Statut"], "Candidat à valider")
        mapping = self.root / "suivi" / "correspondances_validees.csv"
        with mapping.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream, delimiter=";")
            writer.writerow(["Nom", "Prénom", "Classe", "Numéro étudiant"])
            writer.writerow(["Martin", "Léa", "G1", "000123"])
        with progression_lock(self.root):
            second = refresh_progression(self.root, "2026-2027")
        self.assertEqual(second["sans_numero"], 0)
        self.assertEqual(self.read_export("progression_S1.csv")[0]["td1-s1__essais"], "2")
        self.assertEqual(self.read_export("correspondances_a_valider.csv"), [])

    def test_invalid_rows_are_reported_not_assimilated_to_zero(self):
        p = self.write_notes("td1-s1-v2", "G1", [
            ("03/11/2026 09:00", "Martin", "Léa", "pas une note", "001"),
            ("03/11/2026 09:30", "Martin", "Léa", "3,00", "??"),
            ("date illisible", "Martin", "Léa", "3,00", "001"),
        ])
        before = p.read_bytes()
        with progression_lock(self.root):
            refresh_progression(self.root, "2026-2027")
        self.assertEqual(p.read_bytes(), before)
        self.assertEqual(self.read_export("progression_S1.csv"), [])
        self.assertEqual(len(self.read_export("anomalies.csv")), 3)

    def test_automatic_refresh_after_saved_submission(self):
        with patch.object(outils, "BASE_DIR", str(self.root)):
            app = Flask(__name__)
            with app.app_context():
                for score in (2, 5, 4):
                    process_submission(
                        SimpleNamespace(filename="TD1_S1.ipynb"), b'{"cells":[]}',
                        "<html>Rapport fictif</html>",
                        {"nom": "Martin", "prenom": "Lea", "classe": "G1",
                         "numero_etudiant": "000123", "contract_version": 2,
                         "score_nature": "technique_provisoire", "score_max": 6,
                         "relecture_humaine": "requise"},
                        score, "td1-s1",
                    )
        self.assertEqual(self.read_export("progression_S1.csv")[0]["td1-s1__essais"], "3")
        self.assertEqual(self.read_export("progression_S1.csv")[0]["td1-s1__min"], "2,00")
        self.assertEqual(self.read_export("progression_S1.csv")[0]["td1-s1__max"], "5,00")
        self.assertTrue(list((self.root / "TD1_S1" / "nb").glob("*.ipynb")))

    def test_invalid_year_is_refused(self):
        with self.assertRaisesRegex(ValueError, "TAL_ACADEMIC_YEAR"):
            refresh_progression(self.root, "2026-2026")


if __name__ == "__main__":
    unittest.main()
