"""Navigation SWAG et TD effectués sous contrats anciens, données fictives."""
import csv
import os
import re
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import outils
from app import create_app
from progression import _catalog, SEMESTERS
from storage_layout import GRADE_COLUMNS
from teacher_access import session_identity
from teacher_progress import cohort, semester_entries


def row(version, number, score="2,00", date="03/11/2026 10:00", last="MARTIN"):
    return dict(zip(GRADE_COLUMNS, (
        date, last, "Léa", "M1_TILT", score, "0,00",
        "technique_provisoire", "6", "requise", number, version,
        "migration:fixture", "",
    )))


class TeacherCountsAndProxyTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / "suivi").mkdir()
        patches = [
            patch.object(outils, "BASE_DIR", str(self.root)),
            patch.dict(os.environ, {
                "FLASK_SECRET_KEY": "unique-long-fixture-secret-for-teacher-portal",
                "TAL_ACADEMIC_YEAR": "2026-2027",
                "TAL_SMTP_HOST": "smtp.example.invalid",
                "TAL_SMTP_PORT": "465",
                "TAL_SMTP_SECURITY": "ssl",
                "TAL_SMTP_FROM": "tal@example.invalid",
                "TAL_TEACHER_EMAIL": "prof@example.invalid",
                "TAL_SESSION_COOKIE_NAME": "tal_corrector_session",
                "TAL_SESSION_COOKIE_PATH": "/universite/tal/",
            }),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        for semester in SEMESTERS:
            self.export(semester, [])
        self.app = create_app()
        self.app.config["TESTING"] = False

    def export(self, semester, students):
        entries = semester_entries(semester)
        header = ["Numéro étudiant", "Nom", "Prénom"]
        for entry in entries:
            header.extend(entry["id"] + "__" + part for part in ("min", "max", "essais"))
        path = self.root / "suivi" / f"progression_{semester}.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, delimiter=";", fieldnames=header)
            writer.writeheader()
            for number, last, first, results in students:
                data = {"Numéro étudiant":number, "Nom":last, "Prénom":first}
                for item in entries:
                    values = results.get(item["id"], ("", "", 0))
                    for part,value in zip(("min", "max", "essais"), values):
                        data[item["id"] + "__" + part] = value
                writer.writerow(data)

    def journal(self, evaluator, records):
        entry = next(item for item in _catalog() if item["evaluator"] == evaluator)
        folder = self.root / entry["storage"]
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / ("notes_" + entry["storage"] + ".csv")
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, delimiter=";", fieldnames=GRADE_COLUMNS)
            writer.writeheader()
            writer.writerows(records)

    def test_main_td_counts_and_older_scores_separate(self):
        self.export("S1", [
            ("000124", "DURAND", "Paul", {"td2-s1":("1,00","5,00",2)}),
        ])
        self.journal("td1-s1", [
            row("1", "000123", "2,00"),
            row("1", "000123", "5,00"),
            row("1", "000123", "3,00"),
            row("1", "000125", "4,00", last="ROUX"),
            row("1", "000126", "7,00", date="03/11/2025 10:00"),
            row("2", "000124", "6,00"),
        ])
        report = cohort("S1")
        self.assertEqual(report["totals"]["TD"], 7)
        self.assertEqual(report["totals"]["Approfondissement"], 12)
        self.assertEqual(report["totals"]["Révision"], 0)
        self.assertEqual(len(report["students"]), 3)
        students = {s["number"]: s for s in report["students"]}
        historic = students["000123"]
        self.assertEqual(historic["done"]["TD"], 1)
        self.assertEqual(historic["older_only"]["TD"], 1)
        self.assertEqual(historic["attempts"], 3)
        self.assertEqual(historic["legacy_attempts"], 3)
        td1 = next(d for d in historic["details"] if d["id"] == "td1-s1")
        self.assertEqual((td1["min"], td1["max"]), ("", ""))
        self.assertEqual((td1["attempts"],td1["legacy_attempts"]), (0,3))
        self.assertEqual(students["000124"]["done"]["TD"], 1)
        self.assertEqual(students["000124"]["legacy_attempts"], 0)
        stats = next(r for r in report["evaluation_stats"] if r["id"] == "td1-s1")
        self.assertEqual((stats["students"],stats["attempts"],stats["legacy_attempts"]), (2,0,4))
        self.assertNotIn("000126", str([s["number"] for s in report["students"]]))

    def test_s3_counts_revisions_separate(self):
        self.export("S3", [("000124", "DURAND", "Paul", {
            "td1-s3": ("3,00","7,00",2)
        })])
        self.journal("td-r0-s3", [row("1","000123")])
        report = cohort("S3")
        self.assertEqual(report["totals"]["TD"], 9)
        self.assertEqual(report["totals"]["Révision"], 3)
        self.assertEqual(report["totals"]["Approfondissement"], 0)
        students = {s["number"]:s for s in report["students"]}
        self.assertEqual(students["000123"]["done"]["Révision"],1)
        self.assertEqual(students["000123"]["done"]["TD"],0)
        self.assertEqual(students["000124"]["done"]["TD"],1)

    def _cookie(self):
        with self.app.app_context():
            payload = {
                "teacher_authenticated_at":int(time.time()),
                "teacher_identity":session_identity(),
                "teacher_csrf":"fixture-csrf",
            }
            token = self.app.session_interface.get_signing_serializer(self.app).dumps(payload)
        return f"{self.app.config['SESSION_COOKIE_NAME']}={token}"

    def test_all_private_links_under_prefix_without_forwarded_header(self):
        self.export("S3", [("000123", "MARTIN", "Léa", {
            "td1-s3":("1,00","3,00",2)
        })])
        client = self.app.test_client(use_cookies=False)
        cookie = self._cookie()
        def headers(prefix=False):
            result = {"Cookie":cookie, "X-Forwarded-Proto":"https"}
            if prefix:
                result["X-Forwarded-Prefix"] = "/universite/tal"
            return result
        for with_prefix in (True,False):
            response = client.get(
                "/enseignant/progression/?semestre=S3",
                headers=headers(with_prefix),
            )
            self.assertEqual(response.status_code,200)
            html=response.get_data(as_text=True)
            self.assertIn("/universite/tal/enseignant/progression/?semestre=S1",html)
            self.assertIn("/universite/tal/enseignant/progression/export/S3",html)
            self.assertIn('action="/universite/tal/enseignant/progression/fiche"',html)
            self.assertIn('href="/universite/tal/static/teacher_progress.css"',html)
            self.assertIn("MARTIN",html)
            detail=client.post(
                "/enseignant/progression/fiche",
                headers=headers(with_prefix),
                data={"csrf":"fixture-csrf","semestre":"S3","numero":"000123"},
            )
            self.assertEqual(detail.status_code,200)
            self.assertIn("Fiche individuelle",detail.get_data(as_text=True))
            export=client.get(
                "/enseignant/progression/export/S3",
                headers=headers(with_prefix),
            )
            self.assertEqual(export.status_code,200)
            self.assertIn("000123",export.get_data(as_text=True))
        no_cookie=client.get(
            "/enseignant/progression/export/S3",
            headers={"X-Forwarded-Proto":"https"},
        )
        self.assertEqual(no_cookie.status_code,403)


if __name__ == "__main__":
    unittest.main()
