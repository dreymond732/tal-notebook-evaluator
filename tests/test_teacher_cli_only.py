"""L'envoi du code enseignant n'est accessible qu'à l'administrateur CLI."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import outils
import teacher_access
import send_teacher_code
from app import create_app


class TeacherCliOnlyTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        storage = patch.object(outils, "BASE_DIR", temp.name)
        storage.start()
        self.addCleanup(storage.stop)
        env = patch.dict(os.environ, {
            "FLASK_SECRET_KEY": "cli-only-teacher-fixture-secret-123456789012",
            "TAL_ACADEMIC_YEAR": "2026-2027",
            "TAL_SMTP_HOST": "smtp.example.invalid",
            "TAL_SMTP_PORT": "465",
            "TAL_SMTP_SECURITY": "ssl",
            "TAL_SMTP_FROM": "tal@example.invalid",
            "TAL_TEACHER_EMAIL": "prof@example.invalid",
        })
        env.start()
        self.addCleanup(env.stop)
        self.messages = []
        mail = patch.object(teacher_access, "_deliver_code",
                            side_effect=lambda to, code: self.messages.append((to, code)))
        mail.start()
        self.addCleanup(mail.stop)
        self.app = create_app()
        self.app.config["TESTING"] = True

    def test_no_public_get_or_post_ever_sends_email(self):
        client = self.app.test_client()
        for path in ("/enseignant/progression/",
                     "/enseignant/progression/demander-code"):
            for method in ("get", "post"):
                response = getattr(client, method)(path)
                self.assertIn(response.status_code, {200, 404, 405})
        self.assertEqual(self.messages, [])
        self.assertEqual(client.post("/enseignant/progression/demander-code").status_code, 404)

    def test_cli_sends_only_to_authorized_email_and_no_code_stdout(self):
        from io import StringIO
        out = StringIO()
        with patch("sys.stdout", out):
            self.assertEqual(send_teacher_code.main(), 0)
        self.assertEqual(len(self.messages), 1)
        destination, code = self.messages[0]
        self.assertEqual(destination, "prof@example.invalid")
        self.assertNotIn(code, out.getvalue())
        self.assertNotIn(destination, out.getvalue())
        self.assertTrue(self.app.test_client().get("/enseignant/progression/").status_code == 200)

    def test_email_and_otp_both_required_and_single_use(self):
        self.assertTrue(teacher_access.issue_cli_code())
        email, code = self.messages[-1]
        self.assertFalse(teacher_access.consume_code(code, "127.0.0.1", "someone@example.invalid"))
        self.assertFalse(teacher_access.consume_code("WRONGPASSWORD", "127.0.0.1", email))
        self.assertTrue(teacher_access.consume_code(code, "127.0.0.1", email.upper()))
        self.assertFalse(teacher_access.consume_code(code, "127.0.0.1", email))

    def test_failed_smtp_keeps_cli_failure_visible_without_secrets(self):
        from io import StringIO
        err = StringIO()
        with patch.object(teacher_access, "_deliver_code", side_effect=OSError("offline")):
            with patch("sys.stderr", err):
                self.assertEqual(send_teacher_code.main(), 1)
        self.assertIn("Envoi impossible", err.getvalue())

    def test_login_must_never_be_an_email_trigger(self):
        client = self.app.test_client()
        result = client.post("/enseignant/progression/connexion", data={
            "email": "prof@example.invalid", "code": "ABCDABCDABCD",
        }, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(self.messages, [])


if __name__ == "__main__":
    unittest.main()
