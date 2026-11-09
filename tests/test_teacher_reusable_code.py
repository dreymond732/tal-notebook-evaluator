"""Code enseignant réutilisable : rotation, révocation et isolation du mode OTP."""
from __future__ import annotations

import io
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
import teacher_access
import send_teacher_code
from app import create_app


class TeacherReusableCodeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        storage = patch.object(outils, "BASE_DIR", temporary.name)
        storage.start()
        self.addCleanup(storage.stop)
        environment = patch.dict(os.environ, {
            "FLASK_SECRET_KEY": "long-stable-teacher-reusable-fixture-secret-2026",
            "TAL_ACADEMIC_YEAR": "2026-2027",
            "TAL_SMTP_HOST": "smtp.example.invalid",
            "TAL_SMTP_PORT": "465",
            "TAL_SMTP_SECURITY": "ssl",
            "TAL_SMTP_FROM": "tal@example.invalid",
            "TAL_TEACHER_EMAIL": "prof@example.invalid",
            "TAL_TEACHER_CODE_MODE": "reusable",
            "TAL_SESSION_COOKIE_PATH": "/",
        })
        environment.start()
        self.addCleanup(environment.stop)
        self.sent = []
        mail = patch.object(
            teacher_access, "_deliver_code",
            side_effect=lambda to, code: self.sent.append((to, code))
        )
        mail.start()
        self.addCleanup(mail.stop)
        self.app = create_app()
        self.app.config.update(TESTING=True)

    def issue(self):
        self.assertTrue(teacher_access.issue_cli_code())
        self.assertEqual(self.sent[-1][0], "prof@example.invalid")
        return self.sent[-1][1]

    def test_reuse_and_login_after_logout_without_a_new_email(self):
        code = self.issue()
        self.assertEqual(len(code), teacher_access.REUSABLE_CODE_LENGTH)
        self.assertTrue(teacher_access.consume_code(code, "192.0.2.1", "prof@example.invalid"))
        self.assertTrue(teacher_access.consume_code(code, "192.0.2.1", "PROF@example.invalid"))
        self.assertEqual(len(self.sent), 1)

        db = teacher_access._db()
        try:
            entry = db.execute(
                "SELECT owner,salt,digest FROM reusable_credential WHERE id=1"
            ).fetchone()
            self.assertIsNotNone(entry)
            self.assertNotIn(code, repr(dict(entry)))
        finally:
            db.close()

        client = self.app.test_client()
        page = client.get("/enseignant/progression").get_data(as_text=True)
        self.assertIn("Code personnel reçu par email", page)
        self.assertIn('minlength="20"', page)
        self.assertNotIn("Le code expire après 10 minutes", page)

        response = client.post(
            "/enseignant/progression/connexion",
            data={"email": "prof@example.invalid", "code": code},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Suivi des étudiants", response.get_data(as_text=True))
        # Un formulaire de déconnexion valide est obtenu sur la session authentifiée.
        csrf = re.search(
            r'name="csrf" value="([^"]+)"', response.get_data(as_text=True)
        )
        self.assertIsNotNone(csrf)
        out = client.post(
            "/enseignant/progression/deconnexion",
            data={"csrf": csrf.group(1)},
            follow_redirects=True,
        )
        self.assertEqual(out.status_code, 200)
        second = client.post(
            "/enseignant/progression/connexion",
            data={"email": "prof@example.invalid", "code": code},
            follow_redirects=True,
        )
        self.assertEqual(second.status_code, 200)
        self.assertIn("Accès enseignant confirmé.", second.get_data(as_text=True))
        self.assertEqual(len(self.sent), 1)

    def test_rotation_revokes_old_code_and_existing_sessions(self):
        old = self.issue()
        identity_before = teacher_access.session_identity()
        at = int(time.time())
        self.assertTrue(teacher_access.session_valid(at, identity_before))
        new = self.issue()
        self.assertNotEqual(old, new)
        self.assertFalse(teacher_access.consume_code(old, "192.0.2.1", "prof@example.invalid"))
        self.assertTrue(teacher_access.consume_code(new, "192.0.2.1", "prof@example.invalid"))
        self.assertFalse(teacher_access.session_valid(at, identity_before))
        self.assertTrue(teacher_access.session_valid(at, teacher_access.session_identity()))

    def test_failed_email_preserves_existing_valid_code(self):
        code = self.issue()
        with patch.object(teacher_access, "_deliver_code", side_effect=OSError("SMTP inaccessible")):
            with self.assertRaisesRegex(RuntimeError, "SMTP"):
                teacher_access.issue_cli_code()
        self.assertTrue(teacher_access.consume_code(code, "192.0.2.1", "prof@example.invalid"))
        self.assertEqual(len(self.sent), 1)

    def test_revoke_cli_invalidates_code_and_session(self):
        code = self.issue()
        old_identity = teacher_access.session_identity()
        output = io.StringIO()
        with patch("sys.stdout", output):
            self.assertEqual(send_teacher_code.main(["--revoke"]), 0)
        self.assertIn("révoqué", output.getvalue())
        self.assertNotIn(code, output.getvalue())
        self.assertFalse(teacher_access.consume_code(code, "192.0.2.1", "prof@example.invalid"))
        self.assertFalse(teacher_access.session_valid(int(time.time()), old_identity))

    def test_wrong_email_and_ip_rate_limit(self):
        code = self.issue()
        self.assertFalse(teacher_access.consume_code(code, "192.0.2.2", "autre@example.invalid"))
        self.assertTrue(teacher_access.consume_code(code, "192.0.2.2", "prof@example.invalid"))
        wrong = "A" * teacher_access.REUSABLE_CODE_LENGTH
        for _ in range(10):
            self.assertFalse(teacher_access.consume_code(wrong, "192.0.2.3", "prof@example.invalid"))
        self.assertFalse(teacher_access.consume_code(code, "192.0.2.3", "prof@example.invalid"))

    def test_legacy_one_time_mode_does_not_accept_reusable_secret(self):
        reusable = self.issue()
        with patch.dict(os.environ, {"TAL_TEACHER_CODE_MODE": "one_time"}):
            self.assertFalse(teacher_access.consume_code(reusable, "192.0.2.4", "prof@example.invalid"))
            single = self.issue()
            self.assertEqual(len(single), teacher_access.CODE_LENGTH)
            self.assertTrue(teacher_access.consume_code(single, "192.0.2.4", "prof@example.invalid"))
            self.assertFalse(teacher_access.consume_code(single, "192.0.2.4", "prof@example.invalid"))
        self.assertTrue(teacher_access.consume_code(reusable, "192.0.2.4", "prof@example.invalid"))

    def test_change_authorized_email_denies_existing_secret(self):
        code = self.issue()
        with patch.dict(os.environ, {"TAL_TEACHER_EMAIL": "new@example.invalid"}):
            self.assertFalse(teacher_access.consume_code(code, "192.0.2.5", "new@example.invalid"))
            self.assertFalse(teacher_access.consume_code(code, "192.0.2.5", "prof@example.invalid"))

    def test_invalid_mode_fails_closed(self):
        with patch.dict(os.environ, {"TAL_TEACHER_CODE_MODE": "forever"}):
            self.assertFalse(teacher_access.configured())
            self.assertEqual(self.app.test_client().get("/enseignant/progression").status_code, 503)


if __name__ == "__main__":
    unittest.main()
