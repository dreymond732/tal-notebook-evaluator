"""Portail individuel : tests avec données fictives et SMTP simulé."""
import csv
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import outils
import student_access
from app import create_app
from student_progress import individual_progress, student_exists


class IndividualProgressTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.storage_patch = patch.object(outils, "BASE_DIR", self.folder.name)
        self.storage_patch.start()
        self.addCleanup(self.storage_patch.stop)
        self.environment_patch = patch.dict(os.environ, {
            "FLASK_SECRET_KEY": "fixture-secret-key-not-for-production",
            "TAL_ACADEMIC_YEAR": "2026-2027",
            "TAL_SMTP_HOST": "smtp.example.invalid",
            "TAL_SMTP_PORT": "465",
            "TAL_SMTP_SECURITY": "ssl",
            "TAL_SMTP_FROM": "tal@example.invalid",
        })
        self.environment_patch.start()
        self.addCleanup(self.environment_patch.stop)
        self.sent = []
        self.smtp_patch = patch.object(student_access, "_send_code",
                                       side_effect=lambda email, code: self.sent.append((email, code)))
        self.smtp_patch.start()
        self.addCleanup(self.smtp_patch.stop)
        base = Path(self.folder.name) / "suivi"
        base.mkdir(parents=True)
        with (base / "progression_S1.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["Numéro étudiant", "Nom", "Prénom",
                             "td1-s1__min", "td1-s1__max", "td1-s1__essais",
                             "controle-td1-s3__min", "controle-td1-s3__max", "controle-td1-s3__essais"])
            writer.writerow(["00123", "MARTIN", "Léa", "2,00", "6,00", 3,
                             "19,00", "19,00", 1])
            writer.writerow(["00124", "DURAND", "Paul", "1,00", "5,00", 2,
                             "18,00", "18,00", 1])
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

    def csrf(self):
        page = self.client.get("/ma-progression")
        self.assertEqual(page.status_code, 200)
        code = re.search(r'name="csrf" value="([^"]+)"',
                         page.get_data(as_text=True))
        self.assertIsNotNone(code)
        return code.group(1)

    def ask(self, number="00123", email="lea@example.invalid", csrf=None):
        return self.client.post("/ma-progression/demander-code", data={
            "numero": number, "email": email,
            "csrf": csrf if csrf is not None else self.csrf(),
        }, follow_redirects=True)

    def login(self, number="00123", email="lea@example.invalid", code="", csrf=None):
        return self.client.post("/ma-progression/connexion", data={
            "numero": number, "email": email, "code": code,
            "csrf": csrf if csrf is not None else self.csrf(),
        }, follow_redirects=True)

    def test_individual_only_td_not_control_or_other_student(self):
        self.assertTrue(student_exists("00123"))
        self.assertFalse(student_exists("00125"))
        data = individual_progress("00123")
        self.assertEqual(data["name"], "MARTIN")
        self.assertEqual(data["semesters"][0]["completed"], 1)
        self.assertTrue(any(a["name"] == "td1-s1" and a["attempts"] == 3
                            for a in data["semesters"][0]["activities"]))
        self.assertFalse(any(a["name"].startswith("controle")
                             for sem in data["semesters"] for a in sem["activities"]))

    def test_first_claim_only_after_email_code_confirmation(self):
        self.assertNotIn("MARTIN", self.client.get("/ma-progression").get_data(as_text=True))
        self.assertEqual(self.ask().status_code, 200)
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(self.sent[0][0], "lea@example.invalid")
        self.assertNotIn("MARTIN", self.client.get("/ma-progression").get_data(as_text=True))
        self.assertEqual(len(self.sent[0][1]), 18)
        db = student_access._db()
        try:
            self.assertIsNone(db.execute("SELECT number FROM accounts").fetchone())
            self.assertNotIn(self.sent[0][1], db.execute("SELECT digest FROM pending").fetchone()[0])
        finally:
            db.close()
        incorrect = self.login(code="BAD")
        self.assertNotIn("MARTIN", incorrect.get_data(as_text=True))
        success = self.login(code=self.sent[0][1])
        html = success.get_data(as_text=True)
        self.assertIn("MARTIN", html)
        self.assertIn("6,00", html)
        self.assertIn("3</td>", html)
        self.assertNotIn("DURAND", html)
        self.assertNotIn("19,00", html)
        self.assertNotIn("controle-td1-s3", html)
        self.assertNotIn("acces_etudiants.sqlite3", html)
        self.assertEqual(success.headers["Cache-Control"], "no-store, private")
        self.assertTrue((Path(self.folder.name) / "suivi" / "acces_etudiants.sqlite3").is_file())

    def test_existing_account_rejects_other_email_without_disclosure(self):
        self.ask()
        code = self.sent[-1][1]
        self.login(code=code)
        self.assertEqual(len(self.sent), 1)
        self.client.post("/ma-progression/deconnexion", data={"csrf": self.csrf()})
        result = self.ask(email="pirate@example.invalid")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(self.sent), 1)
        self.assertNotIn("lea@example.invalid", result.get_data(as_text=True))
        refused = self.login(email="pirate@example.invalid", code=code)
        self.assertNotIn("MARTIN", refused.get_data(as_text=True))
        original = self.login(code=code)
        self.assertIn("MARTIN", original.get_data(as_text=True))

    def test_new_code_replaces_old_only_after_confirmation(self):
        self.ask()
        old = self.sent[-1][1]
        self.login(code=old)
        self.ask()
        new = self.sent[-1][1]
        self.assertNotEqual(new, old)
        self.assertIn("MARTIN", self.login(code=old).get_data(as_text=True))
        self.assertIn("MARTIN", self.login(code=new).get_data(as_text=True))
        self.client.post("/ma-progression/deconnexion", data={"csrf": self.csrf()})
        self.assertNotIn("MARTIN", self.login(code=old).get_data(as_text=True))
        self.assertIn("MARTIN", self.login(code=new).get_data(as_text=True))

    def test_unknown_student_cannot_claim_and_csrf_required(self):
        response = self.ask(number="00000")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.sent, [])
        bad = self.client.post("/ma-progression/demander-code",
                               data={"numero": "00123", "email": "lea@example.invalid"})
        self.assertEqual(bad.status_code, 400)
        self.assertEqual(self.sent, [])
        result = self.client.post("/ma-progression/connexion",
                                  data={"numero": "00123", "email": "lea@example.invalid",
                                        "code": "FAKE"}, follow_redirects=True)
        self.assertEqual(result.status_code, 400)

    def test_email_delivery_failure_never_claims_identity(self):
        with patch.object(student_access, "_send_code", side_effect=OSError("SMTP offline")):
            response = self.ask()
        self.assertIn("indisponible", response.get_data(as_text=True))
        db = student_access._db()
        try:
            self.assertIsNone(db.execute("SELECT number FROM accounts").fetchone())
            self.assertIsNone(db.execute("SELECT number FROM pending").fetchone())
        finally:
            db.close()

    def test_http_is_rejected_in_production_but_proxy_https_is_accepted(self):
        self.app.config["TESTING"] = False
        self.assertEqual(self.client.get("/ma-progression").status_code, 503)
        secure = self.client.get(
            "/ma-progression",
            headers={"X-Forwarded-Proto": "https",
                     "X-Forwarded-Prefix": "/universite/tal"},
        )
        self.assertEqual(secure.status_code, 200)
        self.assertIn('action="/universite/tal/ma-progression/connexion"',
                      secure.get_data(as_text=True))

    def test_disabled_without_year_or_sender(self):
        with patch.dict(os.environ, {"TAL_ACADEMIC_YEAR": ""}):
            self.assertEqual(self.client.get("/ma-progression").status_code, 503)
        with patch.dict(os.environ, {"TAL_SMTP_HOST": ""}):
            self.assertEqual(self.client.get("/ma-progression").status_code, 503)

    def test_request_rate_limit(self):
        for _ in range(8):
            self.ask()
        self.assertEqual(len(self.sent), 6)
        self.assertFalse(student_access.normalize("?", "valid@example.fr"))
        self.assertFalse(student_access.normalize("00123", "bad email"))


if __name__ == "__main__":
    unittest.main()
