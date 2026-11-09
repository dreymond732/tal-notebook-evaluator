"""Régression de la session CSRF enseignante après changement du cookie SWAG.

Ces tests n'envoient aucun email et ne lisent aucune donnée étudiante.
"""
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
import teacher_access
from app import create_app


class TeacherCookieMigrationTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = folder.name
        storage = patch.object(outils, "BASE_DIR", self.root)
        storage.start()
        self.addCleanup(storage.stop)
        env = patch.dict(os.environ, {
            "FLASK_SECRET_KEY": "teacher-cookie-migration-fixture-secret-strong",
            "TAL_ACADEMIC_YEAR": "2026-2027",
            "TAL_TEACHER_EMAIL": "prof@example.invalid",
            "TAL_SMTP_HOST": "smtp.example.invalid",
            "TAL_SMTP_FROM": "tal@example.invalid",
            "TAL_SMTP_PORT": "465",
            "TAL_SMTP_SECURITY": "ssl",
            "TAL_SESSION_COOKIE_NAME": "tal_corrector_session",
            "TAL_SESSION_COOKIE_PATH": "/universite/tal/",
        })
        env.start()
        self.addCleanup(env.stop)
        self.app = create_app()
        self.app.config["TESTING"] = False

    def headers(self, cookie=None):
        out = {
            "X-Forwarded-Proto": "https",
            "X-Forwarded-Prefix": "/universite/tal",
        }
        if cookie is not None:
            out["Cookie"] = cookie
        return out

    def signed_cookie(self, csrf="token-for-test"):
        with self.app.app_context():
            payload = {"teacher_csrf": csrf}
            signed = self.app.session_interface.get_signing_serializer(
                self.app
            ).dumps(payload)
        return self.app.config["SESSION_COOKIE_NAME"] + "=" + signed

    def test_teacher_get_expires_previous_root_cookie_and_sets_scoped_cookie(self):
        client = self.app.test_client(use_cookies=False)
        response = client.get("/enseignant/progression/", headers=self.headers())
        self.assertEqual(response.status_code, 200)
        cookies = response.headers.getlist("Set-Cookie")
        root = [c for c in cookies if "Path=/" in c and
                "Path=/universite/tal/" not in c]
        scoped = [c for c in cookies if "Path=/universite/tal/" in c]
        self.assertEqual(len(root), 1, cookies)
        self.assertEqual(len(scoped), 1, cookies)
        self.assertTrue(root[0].startswith("tal_corrector_session=;"))
        self.assertIn("Expires=Thu, 01 Jan 1970", root[0])
        self.assertIn("Secure", root[0])
        self.assertIn("HttpOnly", root[0])
        self.assertTrue(scoped[0].startswith("tal_corrector_session="))
        self.assertIn("Secure", scoped[0])
        self.assertIn("SameSite=Lax", scoped[0])
        self.assertNotIn("JOURNALIA", str(cookies).upper())

    def test_csrf_without_cookie_is_rejected_with_helpful_explanation(self):
        client = self.app.test_client(use_cookies=False)
        page = client.get("/enseignant/progression/", headers=self.headers())
        token = re.search(r'name="csrf" value="([^"]+)"',
                          page.get_data(as_text=True)).group(1)
        with patch.object(teacher_access, "request_code") as sender:
            error = client.post(
                "/enseignant/progression/demander-code",
                headers=self.headers(),
                data={"csrf": token},
            )
        self.assertEqual(error.status_code, 400)
        self.assertIn("n'a pas été reçu", error.get_data(as_text=True))
        self.assertIn("/universite/tal/enseignant/progression/", error.get_data(as_text=True))
        self.assertIn("no-store", error.headers["Cache-Control"])
        sender.assert_not_called()

    def test_valid_cookie_and_csrf_keep_request_and_login_working(self):
        client = self.app.test_client(use_cookies=False)
        cookie = self.signed_cookie("csrf-123")
        with patch.object(teacher_access, "request_code", return_value=True) as sender:
            request = client.post(
                "/enseignant/progression/demander-code",
                headers=self.headers(cookie),
                data={"csrf": "csrf-123"},
            )
        self.assertEqual(request.status_code, 303)
        self.assertEqual(request.headers["Location"],
                         "/universite/tal/enseignant/progression/")
        sender.assert_called_once()
        with patch.object(teacher_access, "consume_code", return_value=False) as verify:
            failed = client.post(
                "/enseignant/progression/connexion",
                headers=self.headers(cookie),
                data={"csrf": "csrf-123", "code": "FAKE-CODE"},
            )
        self.assertEqual(failed.status_code, 303)
        verify.assert_called_once()
        self.assertEqual(failed.headers["Location"],
                         "/universite/tal/enseignant/progression/")

    def test_wrong_csrf_does_not_consume_single_use_teacher_code(self):
        client = self.app.test_client(use_cookies=False)
        with patch.object(teacher_access, "consume_code") as verify:
            failure = client.post(
                "/enseignant/progression/connexion",
                headers=self.headers(self.signed_cookie("correct-csrf")),
                data={"csrf": "wrong-csrf", "code": "EXAMPLECODE"},
            )
        self.assertEqual(failure.status_code, 400)
        self.assertIn("jeton", failure.get_data(as_text=True))
        verify.assert_not_called()

    def test_no_root_expiry_when_cookie_uses_root_path(self):
        with patch.dict(os.environ, {"TAL_SESSION_COOKIE_PATH": "/"}):
            app = create_app()
            response = app.test_client(use_cookies=False).get(
                "/enseignant/progression/", headers=self.headers()
            )
            cookies = response.headers.getlist("Set-Cookie")
            self.assertEqual(len(cookies), 1)
            self.assertIn("Path=/", cookies[0])
            self.assertNotIn("Expires=Thu, 01 Jan 1970", cookies[0])


if __name__ == "__main__":
    unittest.main()
