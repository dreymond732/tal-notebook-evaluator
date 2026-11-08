"""Contrôle systématique des 34 TD du catalogue avec des dépôts fictifs."""
import csv
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import outils
from audit_progressions import audit, format_report
from diagnostic_progression import diagnostic
from progression import _catalog, progression_lock, refresh_progression
from storage_layout import GRADE_COLUMNS


def example(number="000123", score="2,00", year=2026, version="2",
            nature="technique_provisoire"):
    values = (
        f"03/11/{year} 10:00", "MARTIN", "Léa", "M1_TILT",
        score, "0,00", nature, "6", "requise",
        number, version, "direct:synthetic", "",
    )
    return dict(zip(GRADE_COLUMNS, values))


class AuditAllTdsTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        patcher = patch.object(outils, "BASE_DIR", str(self.root))
        patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, evaluator, rows):
        entry = next(e for e in _catalog() if e["evaluator"] == evaluator)
        directory = self.root / entry["storage"]
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / ("notes_" + entry["storage"] + ".csv")
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=GRADE_COLUMNS, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)
        return path

    def recalc(self):
        with progression_lock(self.root):
            return refresh_progression(self.root, "2026-2027")

    def test_all_thirty_four_tds_eligible_and_compared_to_exports(self):
        entries = [e for e in _catalog() if e["kind"] == "TD"]
        self.assertEqual(
            {s: sum(e["semester"] == s for e in entries)
             for s in ("S1", "S2", "S3")},
            {"S1": 19, "S2": 3, "S3": 12},
        )
        self.assertEqual(len(set(e["storage"] for e in entries)), 34)
        for entry in entries:
            self.write(entry["evaluator"], [
                example(version=str(entry["version"])),
            ])
        self.recalc()
        report = audit(self.root, "2026-2027")
        self.assertEqual(report["evaluations"], 34)
        self.assertEqual(report["statuts"], {"OK": 34})
        self.assertEqual(report["semestres"], {"S1": 19, "S2": 3, "S3": 12})
        self.assertTrue(all(row["essais_suivi"] == 1 for row in report["resultats"]))
        self.assertTrue(all(row["etudiants_suivi"] == 1 for row in report["resultats"]))
        self.assertNotIn("MARTIN", format_report(report))
        self.assertNotIn("000123", repr(report))
        self.assertEqual(len(audit(self.root, "2026-2027", all_evaluations=True)["resultats"]), 45)

    def test_each_td_scanned_even_if_nothing_submitted(self):
        self.recalc()
        report = audit(self.root, "2026-2027")
        self.assertEqual(report["statuts"], {"SANS_DEPOT": 34})
        self.assertEqual(len(report["resultats"]), 34)
        self.assertEqual(
            audit(self.root, "2026-2027", semester="S2")["semestres"], {"S2": 3}
        )

    def test_missing_source_after_consolidation_is_reported(self):
        source = self.write("td4-s1", [example()])
        self.recalc()
        source.unlink()
        report = audit(self.root, "2026-2027", semester="S1")
        original = next(r for r in report["resultats"] if r["evaluation"] == "td4-s1")
        self.assertEqual(original["statut"], "ECART")
        self.assertEqual(original["essais_eligibles"], 0)
        self.assertEqual(original["essais_suivi"], 1)
        self.assertEqual(original["motifs"].get("divergences_par_etudiant"), 1)

    def test_three_students_five_tries_and_three_reports(self):
        source = self.write("td4-s1", [
            example(number="000123", score=s) for s in ("1,00", "3,00", "5,00")
        ] + [example(number="000124"), example(number="000125")])
        folder = source.parent
        (folder / "nb").mkdir()
        (folder / "rapport").mkdir()
        for index in range(5):
            (folder / "nb" / f"{index}.ipynb").write_text("{}", encoding="utf-8")
        for index in range(3):
            (folder / "rapport" / f"{index}.html").write_text("<p>test</p>", encoding="utf-8")
        self.recalc()
        record = diagnostic("td4-s1", self.root, "2026-2027")
        self.assertEqual((record["fichiers_nb"], record["fichiers_rapport"]), (5, 3))
        self.assertEqual(record["ecarts_individuels"], 0)
        report = audit(self.root, "2026-2027", semester="S1")
        row = next(x for x in report["resultats"] if x["evaluation"] == "td4-s1")
        self.assertEqual(row["statut"], "OK")
        self.assertEqual((row["lignes_csv"], row["essais_eligibles"], row["etudiants_eligibles"]), (5, 5, 3))
        self.assertEqual((row["essais_suivi"], row["etudiants_suivi"]), (5, 3))

    def test_different_student_same_totals_is_detected(self):
        source = self.write("td3-s1", [example()])
        self.recalc()
        path = self.root / "suivi" / "progression_S1.csv"
        contents = path.read_text(encoding="utf-8").replace("000123", "000124")
        path.write_text(contents, encoding="utf-8")
        report = audit(self.root, "2026-2027", semester="S1")
        row = next(x for x in report["resultats"] if x["evaluation"] == "td3-s1")
        self.assertEqual(row["essais_eligibles"], row["essais_suivi"])
        self.assertEqual(row["statut"], "ECART")
        self.assertEqual(row["motifs"].get("divergences_par_etudiant"), 2)
        self.assertNotIn("000124", format_report(report))

    def test_current_and_old_contract_are_not_mixed(self):
        self.write("td1b-s3", [
            example(version="2"), example(version="3"),
        ])
        self.recalc()
        report = audit(self.root, "2026-2027", semester="S3")
        row = next(x for x in report["resultats"] if x["evaluation"] == "td1b-s3")
        self.assertEqual(row["versions"], {"2": 1, "3": 1})
        self.assertEqual(row["essais_eligibles"], 1)
        self.assertEqual(row["essais_suivi"], 1)
        self.assertEqual(row["statut"], "A_VERIFIER")
        self.assertEqual(row["motifs"]["versions_anterieures"], 1)

    def test_student_with_manual_mapping_is_counted_correctly(self):
        self.write("td2-s1", [example(number="")])
        target = self.root / "suivi"
        target.mkdir()
        with (target / "correspondances_validees.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream, delimiter=";")
            writer.writerow(["Nom", "Prénom", "Classe", "Numéro étudiant"])
            writer.writerow(["MARTIN", "Léa", "M1_TILT", "000123"])
        self.recalc()
        row = next(e for e in audit(self.root, "2026-2027")["resultats"]
                   if e["evaluation"] == "td2-s1")
        self.assertEqual(row["statut"], "OK")
        self.assertEqual(row["essais_eligibles"], 1)
        self.assertEqual(row["etudiants_suivi"], 1)

    def test_unidentified_or_outside_year_is_flagged_not_invented(self):
        self.write("td5-s1", [
            example(number=""), example(year=2025),
        ])
        self.recalc()
        row = next(e for e in audit(self.root, "2026-2027")["resultats"]
                   if e["evaluation"] == "td5-s1")
        self.assertEqual(row["statut"], "A_VERIFIER")
        self.assertEqual(row["essais_suivi"], 0)
        self.assertEqual(row["motifs"]["hors_annee"], 1)
        self.assertEqual(row["motifs"]["sans_numero"], 1)

    def test_migrated_archive_without_csv_is_warning(self):
        base = self.root / "S1_TD6"
        (base / "nb").mkdir(parents=True)
        (base / "nb" / "copie.ipynb").write_text("{}", encoding="utf-8")
        self.recalc()
        row = next(e for e in audit(self.root, "2026-2027")["resultats"]
                   if e["evaluation"] == "td6-s1")
        self.assertEqual(row["statut"], "ECART")
        self.assertEqual(row["motifs"]["archives_sans_journal"], 1)

    def test_older_storage_detected_if_canonical_missing(self):
        old = self.root / "TD4_one_S1"
        old.mkdir()
        self.recalc()
        row = next(e for e in audit(self.root, "2026-2027")["resultats"]
                   if e["evaluation"] == "td4-one-s1")
        self.assertEqual(row["statut"], "ECART")
        self.assertEqual(row["motifs"]["ancien_dossier_sans_journal_canonique"], 1)

    def test_bad_csv_schema_is_reported_without_personal_data(self):
        file = self.write("td3-bis-s1", [example()])
        file.write_text("Nom;Note\nMARTIN;999\n", encoding="utf-8")
        self.recalc()
        r = audit(self.root, "2026-2027")
        row = next(x for x in r["resultats"] if x["evaluation"] == "td3-bis-s1")
        self.assertEqual(row["statut"], "ECART")
        self.assertEqual(row["erreur"], "ValueError")
        self.assertNotIn("MARTIN", format_report(r))

    def test_no_modification_to_export_or_notes_from_audit(self):
        journal = self.write("td1-s1", [example()])
        self.recalc()
        follow = self.root / "suivi" / "progression_S1.csv"
        old_bytes = journal.read_bytes(), follow.read_bytes()
        audit(self.root, "2026-2027")
        self.assertEqual((journal.read_bytes(), follow.read_bytes()), old_bytes)


if __name__ == "__main__":
    unittest.main()
