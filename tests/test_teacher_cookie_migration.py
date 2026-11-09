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

    def test_old_anonymous_session_with_existing_csrf_is_reissued_at_new_path(self):
        # Un visiteur peut avoir une ancienne session anonyme avec un CSRF
        # déjà créé. Si on retire Path=/ sans la réémettre sous /universite/tal/,
        # le POST suivant perd encore sa session.
        client = self.app.test_client(use_cookies=False)
        old_cookie = self.signed_cookie("unchanged-old-csrf")
        response = client.get(
            "/enseignant/progression/", headers=self.headers(old_cookie)
        )
        self.assertEqual(response.status_code, 200)
        # Le formulaire public ne contient plus de CSRF, mais la session ancienne
        # doit encore être réémise sous le chemin TAL configuré.
        scoped = [cookie for cookie in response.headers.getlist("Set-Cookie")
                  if "Path=/universite/tal/" in cookie]
        self.assertEqual(len(scoped), 1)
        self.assertIn("tal_corrector_session=", scoped[0])

    def test_legacy_public_send_endpoint_is_deleted(self):
        client = self.app.test_client(use_cookies=False)
        with patch.object(teacher_access, "issue_cli_code") as sender:
            self.assertEqual(
                client.post("/enseignant/progression/demander-code",
                            headers=self.headers()).status_code, 404)
            self.assertEqual(
                client.get("/enseignant/progression/demander-code",
                           headers=self.headers()).status_code, 404)
        sender.assert_not_called()

    def test_otp_login_does_not_require_anonymous_csrf_cookie(self):
        client = self.app.test_client(use_cookies=False)
        with patch.object(teacher_access, "consume_code", return_value=True) as verifier:
            result = client.post(
                "/enseignant/progression/connexion",
                headers=self.headers(),
                data={"email": "prof@example.invalid", "code": "ABCDEFGHJKLM"},
            )
        self.assertEqual(result.status_code, 303)
        self.assertEqual(result.headers["Location"],
                         "/universite/tal/enseignant/progression/")
        verifier.assert_called_once_with(
            "ABCDEFGHJKLM", "127.0.0.1", "prof@example.invalid"
        )

    def test_teacher_private_form_csrf_still_required(self):
        client = self.app.test_client(use_cookies=False)
        response = client.post(
            "/enseignant/progression/deconnexion",
            headers=self.headers(),
            data={"csrf": "wrong"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("session", response.get_data(as_text=True).lower())

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
