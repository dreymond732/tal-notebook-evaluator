"""Tableau enseignant : contrôle d'accès, OTP SMTP et relevés fictifs."""
import csv
import os
import re
import stat
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import outils
import teacher_access
from app import create_app
from teacher_progress import cohort, semester_entries


class TeacherDashboardTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.root.joinpath("suivi").mkdir()
        storage = patch.object(outils, "BASE_DIR", str(self.root))
        storage.start()
        self.addCleanup(storage.stop)
        env = patch.dict(os.environ, {
            "FLASK_SECRET_KEY": "unique-long-fixture-secret-for-teacher-portal",
            "TAL_ACADEMIC_YEAR": "2026-2027",
            "TAL_SMTP_HOST": "smtp.example.invalid",
            "TAL_SMTP_PORT": "465",
            "TAL_SMTP_SECURITY": "ssl",
            "TAL_SMTP_FROM": "tal@example.invalid",
            "TAL_TEACHER_EMAIL": "prof@example.invalid",
            "TAL_SMTP_USER": "user",
            "TAL_SMTP_PASSWORD": "test-only",
        })
        env.start()
        self.addCleanup(env.stop)
        self.sent = []
        smtp = patch.object(
            teacher_access, "_deliver_code",
            side_effect=lambda address, code: self.sent.append((address, code))
        )
        smtp.start()
        self.addCleanup(smtp.stop)
        self._write("S1", [
            ("000123", "MARTIN", "Léa", {
                "td1-s1": ("2,00", "6,00", 3),
                "dm-intermediaire-s1": ("3,00", "9,00", 2),
            }),
            ("000124", "DURAND", "Paul", {
                "td1-s1": ("1,00", "4,00", 2),
            }),
        ])
        self._write("S2", [
            ("000123", "MARTIN", "Léa", {
                "td2-S2": ("4,00", "12,00", 3)
            })
        ])
        self._write("S3", [
            ("000123", "MARTIN", "Léa", {
                "td1-s3": ("1,00", "6,00", 2),
                "controle-td1-s3": ("5,00", "13,00", 2),
            })
        ])
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def _write(self, semester, students):
        entries = semester_entries(semester)
        fields = ["Numéro étudiant", "Nom", "Prénom"]
        for item in entries:
            fields.extend(f"{item['id']}__{col}" for col in ("min", "max", "essais"))
        path = self.root / "suivi" / f"progression_{semester}.csv"
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, delimiter=";")
            writer.writeheader()
            for number, last, first, scores in students:
                row = {"Numéro étudiant": number, "Nom": last, "Prénom": first}
                for item in entries:
                    vals = scores.get(item["id"], ("", "", 0))
                    for col, val in zip(("min", "max", "essais"), vals):
                        row[f"{item['id']}__{col}"] = val
                writer.writerow(row)
        return path

    def csrf(self):
        response = self.client.get("/enseignant/progression")
        self.assertEqual(response.status_code, 200)
        match = re.search(r'name="csrf" value="([^"]+)"',
                          response.get_data(as_text=True))
        self.assertIsNotNone(match)
        return match[1]

    def ask(self):
        # Commande administrative, sans HTTP.
        return teacher_access.issue_cli_code()

    def login(self, code, email="prof@example.invalid"):
        return self.client.post(
            "/enseignant/progression/connexion",
            data={"email": email, "code": code}, follow_redirects=True,
        )

    def authenticate(self):
        self.ask()
        self.assertEqual(len(self.sent), 1)
        response = self.login(self.sent[-1][1])
        self.assertIn("Progression du S1", response.get_data(as_text=True))
        return response

    def test_public_page_and_http_cannot_send_any_email(self):
        first = self.client.get("/enseignant/progression").get_data(as_text=True)
        self.assertIn('name="email"', first)
        self.assertIn('name="code"', first)
        self.assertNotIn("teacher-code-auto-send", first)
        self.assertNotIn("Renvoyer le code", first)
        self.assertNotIn("/demander-code", first)
        self.assertEqual(self.sent, [])
        for method in ("get", "post"):
            result = getattr(self.client, method)(
                "/enseignant/progression/demander-code"
            )
            self.assertEqual(result.status_code, 404)
        self.assertEqual(self.sent, [])
        self.assertTrue(self.ask())
        self.assertEqual(len(self.sent), 1)

    def test_original_td4_appears_in_teacher_evaluation_details(self):
        self._write("S1", [
            ("000123", "MARTIN", "Léa", {
                "td4-s1": ("2,00", "5,00", 3),
                "td4-one-s1": ("4,00", "6,00", 1),
            }),
            ("000124", "DURAND", "Paul", {
                "td4-s1": ("3,00", "3,00", 1),
            }),
            ("000125", "ROUX", "Ana", {
                "td4-s1": ("6,00", "6,00", 1),
            }),
        ])
        listing = cohort("S1")
        initial = next(item for item in listing["evaluation_stats"]
                       if item["id"] == "td4-s1")
        extension = next(item for item in listing["evaluation_stats"]
                         if item["id"] == "td4-one-s1")
        self.assertEqual((initial["students"], initial["attempts"]), (3, 5))
        self.assertEqual((extension["students"], extension["attempts"]), (1, 1))
        self.authenticate()
        page = self.client.get("/enseignant/progression?semestre=S1")
        html = page.get_data(as_text=True)
        self.assertIn("Détail des évaluations du S1", html)
        self.assertIn("td4-s1", html)
        self.assertIn("td4-one-s1", html)

    def test_public_access_and_student_session_never_expose_roster(self):
        response = self.client.get("/enseignant/progression")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("MARTIN", response.get_data(as_text=True))
        self.assertNotIn("000123", response.get_data(as_text=True))
        for path in ("/enseignant/progression/export/S1",):
            self.assertEqual(self.client.get(path).status_code, 403)
        response = self.client.post(
            "/enseignant/progression/fiche",
            data={"numero": "000123", "semestre": "S1"},
        )
        self.assertEqual(response.status_code, 403)
        with self.client.session_transaction() as sess:
            sess["student_number"] = "000123"
            sess["student_version"] = 1
        self.assertEqual(self.client.get("/enseignant/progression/export/S1").status_code, 403)

    def test_email_challenge_is_private_one_use_and_not_student_code(self):
        self.assertTrue(self.ask())
        self.assertEqual(self.sent[0][0], "prof@example.invalid")
        self.assertEqual(len(self.sent[0][1]), teacher_access.CODE_LENGTH)
        db = teacher_access._db()
        try:
            digest = db.execute("SELECT digest FROM challenge WHERE id=1").fetchone()["digest"]
        finally:
            db.close()
        self.assertNotIn(self.sent[0][1], digest)
        self.assertEqual(
            stat.S_IMODE((self.root / "suivi" / "acces_enseignant.sqlite3").stat().st_mode),
            0o600
        )
        self.assertNotIn("MARTIN", self.login("ABCDEFGHJKLM").get_data(as_text=True))
        self.assertIn("MARTIN", self.login(self.sent[0][1]).get_data(as_text=True))
        db = teacher_access._db()
        try:
            self.assertIsNone(db.execute("SELECT id FROM challenge").fetchone())
        finally:
            db.close()
        with self.client.session_transaction() as sess:
            self.assertNotIn(self.sent[0][1], repr(dict(sess)))
        self.client.post(
            "/enseignant/progression/deconnexion", data={"csrf": self.csrf()}
        )
        self.assertNotIn("MARTIN", self.login(self.sent[0][1]).get_data(as_text=True))

    def test_correct_email_is_required_and_wrong_email_does_not_use_code(self):
        self.assertTrue(self.ask())
        code = self.sent[-1][1]
        wrong = self.login(code, email="intrus@example.invalid")
        self.assertNotIn("Progression du S1", wrong.get_data(as_text=True))
        success = self.login(code, email="PROF@example.invalid")
        self.assertIn("Progression du S1", success.get_data(as_text=True))

    def test_no_anonymous_csrf_needed_for_otp_login(self):
        self.assertTrue(self.ask())
        code = self.sent[-1][1]
        # Aucun GET préalable, aucune session anonyme ni jeton CSRF requis.
        fresh = self.app.test_client()
        result = fresh.post("/enseignant/progression/connexion",
                            data={"email": "prof@example.invalid", "code": code},
                            follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Progression du S1", result.get_data(as_text=True))

    def test_semesters_cohort_detail_and_private_download(self):
        self.authenticate()
        index = self.client.get("/enseignant/progression?semestre=S1")
        data = index.get_data(as_text=True)
        self.assertIn("MARTIN", data)
        self.assertIn("DURAND", data)
        self.assertIn("1 /", data)
        self.assertIn("TD", data)
        self.assertIn("Exporter les scores actuels (CSV)", data)
        self.assertIn("teacher_progress.js", data)
        for semester in ("S2", "S3"):
            other = self.client.get(f"/enseignant/progression?semestre={semester}")
            self.assertEqual(other.status_code, 200)
            self.assertIn("MARTIN", other.get_data(as_text=True))
            self.assertNotIn("DURAND", other.get_data(as_text=True))
        sheet = self.client.post("/enseignant/progression/fiche", data={
            "csrf": self.csrf(), "numero": "000123", "semestre": "S1",
        })
        self.assertEqual(sheet.status_code, 200)
        self.assertIn("2,00", sheet.get_data(as_text=True))
        self.assertIn("6,00", sheet.get_data(as_text=True))
        self.assertIn("Devoir maison", sheet.get_data(as_text=True))
        self.assertNotIn("DURAND", sheet.get_data(as_text=True))
        sheet3 = self.client.post("/enseignant/progression/fiche", data={
            "csrf": self.csrf(), "numero": "000123", "semestre": "S3",
        })
        self.assertIn("Contrôle", sheet3.get_data(as_text=True))
        self.assertIn("13,00", sheet3.get_data(as_text=True))
        exported = self.client.get("/enseignant/progression/export/S1")
        self.assertEqual(exported.status_code, 200)
        self.assertIn("attachment;", exported.headers["Content-Disposition"])
        self.assertIn("progression_S1_2026-2027.csv", exported.headers["Content-Disposition"])
        self.assertIn("000123", exported.get_data(as_text=True))
        self.assertIn("no-store", exported.headers["Cache-Control"])
        self.assertIn("no-referrer", exported.headers["Referrer-Policy"])
        self.assertEqual(self.client.get("/enseignant/progression?semestre=S4").status_code, 404)
        self.assertEqual(self.client.get("/enseignant/progression/export/S4").status_code, 404)

    def test_unknown_student_and_csrf_rejected(self):
        self.authenticate()
        self.assertEqual(self.client.post("/enseignant/progression/fiche", data={
            "csrf": self.csrf(), "numero": "000000", "semestre": "S1",
        }).status_code, 404)
        self.assertEqual(self.client.post("/enseignant/progression/fiche", data={
            "numero": "000123", "semestre": "S1",
        }).status_code, 400)
        self.assertEqual(self.client.post(
            "/enseignant/progression/deconnexion"
        ).status_code, 400)

    def test_wrong_code_expired_and_attempts_limit(self):
        self.ask()
        db = teacher_access._db()
        try:
            db.execute("UPDATE challenge SET expires=? WHERE id=1",
                       (int(time.time()) - 1,))
        finally:
            db.close()
        self.assertNotIn("MARTIN", self.login(self.sent[-1][1]).get_data(as_text=True))
        self.ask()
        valid = self.sent[-1][1]
        for i in range(5):
            bad = self.login("AAAAAAAAAAAA")
            self.assertNotIn("MARTIN", bad.get_data(as_text=True))
        self.assertNotIn("MARTIN", self.login(valid).get_data(as_text=True))

    def test_throttling_of_smtp_requests(self):
        for i in range(6):
            self.ask()
        self.assertEqual(len(self.sent), 4)
        self.assertFalse(teacher_access.consume_code("INVALID", "127.0.0.1", "prof@example.invalid"))

    def test_email_failure_does_not_enable_access(self):
        with patch.object(teacher_access, "_deliver_code", side_effect=OSError("offline")):
            with self.assertRaisesRegex(RuntimeError, "SMTP"):
                self.ask()
        db = teacher_access._db()
        try:
            self.assertIsNone(db.execute("SELECT id FROM challenge").fetchone())
        finally:
            db.close()
        self.assertEqual(self.client.get("/enseignant/progression/export/S1").status_code, 403)

    def test_disabled_without_email_year_or_strong_secret(self):
        for var, value in (
            ("TAL_TEACHER_EMAIL", ""),
            ("TAL_SMTP_HOST", ""),
            ("TAL_ACADEMIC_YEAR", ""),
            ("FLASK_SECRET_KEY", "short"),
        ):
            with self.subTest(var=var), patch.dict(os.environ, {var: value}):
                response = self.client.get("/enseignant/progression")
                self.assertEqual(response.status_code, 503)
                self.assertNotIn("MARTIN", response.get_data(as_text=True))

    def test_http_denied_under_prod_but_https_proxy_supported(self):
        self.app.config["TESTING"] = False
        self.assertEqual(self.client.get("/enseignant/progression").status_code, 503)
        with_https = self.client.get("/enseignant/progression", headers={
            "X-Forwarded-Proto": "https",
            "X-Forwarded-Prefix": "/universite/tal",
        })
        self.assertEqual(with_https.status_code, 200)
        self.assertIn(
            'action="/universite/tal/enseignant/progression/connexion"',
            with_https.get_data(as_text=True),
        )

    def test_missing_and_malformed_csv_are_not_disclosed(self):
        (self.root / "suivi" / "progression_S2.csv").unlink()
        self.authenticate()
        view = self.client.get("/enseignant/progression?semestre=S2")
        self.assertIn("Aucun fichier de progression", view.get_data(as_text=True))
        self.assertEqual(self.client.get("/enseignant/progression/export/S2").status_code, 404)
        path = self.root / "suivi" / "progression_S1.csv"
        path.write_text("Nom;Score\nMARTIN;999\n", encoding="utf-8")
        self.assertEqual(self.client.get("/enseignant/progression?semestre=S1").status_code, 503)
        self.assertEqual(self.client.get("/enseignant/progression/export/S1").status_code, 503)

    def test_student_notified_result_must_not_leak_into_student_page(self):
        self.authenticate()
        student = self.client.get("/ma-progression")
        self.assertEqual(student.status_code, 200)
        body = student.get_data(as_text=True)
        self.assertNotIn("DURAND", body)
        self.assertNotIn("Exporter le CSV", body)


if __name__ == "__main__":
    unittest.main()
