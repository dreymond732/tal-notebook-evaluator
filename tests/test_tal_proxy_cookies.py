"""Régression des cookies TAL derrière le préfixe SWAG, sans réseau."""
import os
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from app import create_app


class TalPrefixCookieTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {
            "FLASK_SECRET_KEY": "fictional-session-secret-12345678901234567890",
            "TAL_ACADEMIC_YEAR": "2026-2027",
            "TAL_SMTP_HOST": "smtp.example.invalid",
            "TAL_SMTP_FROM": "tal@example.invalid",
            "TAL_SMTP_SECURITY": "starttls",
            "TAL_TEACHER_EMAIL": "prof@example.invalid",
            "TAL_SESSION_COOKIE_NAME": "tal_corrector_session",
            "TAL_SESSION_COOKIE_PATH": "/universite/tal/",
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)

    @staticmethod
    def headers():
        return {
            "X-Forwarded-Proto": "https",
            "X-Forwarded-Prefix": "/universite/tal",
            "X-Forwarded-Host": "exemple.invalid",
        }

    def test_session_cookie_is_isolated_and_proxy_urls_keep_prefix(self):
        app = create_app()
        self.assertEqual(app.config["SESSION_COOKIE_NAME"], "tal_corrector_session")
        self.assertEqual(app.config["SESSION_COOKIE_PATH"], "/universite/tal/")
        self.assertTrue(app.config["SESSION_COOKIE_HTTPONLY"])
        self.assertTrue(app.config["SESSION_COOKIE_SECURE"])
        self.assertEqual(app.config["SESSION_COOKIE_SAMESITE"], "Lax")
        client = app.test_client()
        response = client.get("/enseignant/progression/", headers=self.headers())
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('/universite/tal/enseignant/progression/connexion', html)
        self.assertIn('/universite/tal/enseignant/progression/demander-code', html)
        cookies = response.headers.getlist("Set-Cookie")
        self.assertTrue(cookies)
        self.assertTrue(any(re.match(r"tal_corrector_session=", cookie) for cookie in cookies))
        self.assertTrue(all("Path=/universite/tal/" in cookie for cookie in cookies))
        self.assertTrue(all("Secure" in cookie and "HttpOnly" in cookie
                            and "SameSite=Lax" in cookie for cookie in cookies))
        self.assertFalse(any(cookie.startswith("session=") for cookie in cookies))

    def test_teacher_link_is_visible_on_home_and_all_semesters(self):
        app = create_app()
        client = app.test_client()
        for location in ("/", "/semestre/S1", "/semestre/S2", "/semestre/S3"):
            with self.subTest(location=location):
                response = client.get(location, headers=self.headers())
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertIn("Accès enseignant" if location == "/" else "Enseignant", html)
                self.assertIn("/universite/tal/enseignant/progression", html)

    def test_teacher_login_redirect_recovers_missing_post_prefix(self):
        # GET initial proxifié puis POST sans X-Forwarded-Prefix : la
        # redirection revient toujours sous le chemin public du cookie.
        from teacher_routes import _redirect_home
        app = create_app()
        with app.test_request_context(
            "/enseignant/progression/connexion", method="POST"
        ):
            result = _redirect_home()
            self.assertEqual(result.status_code, 303)
            self.assertTrue(result.headers["Location"].startswith(
                "/universite/tal/enseignant/progression"
            ))

    def test_http_not_treated_as_https_behind_proxy(self):
        app = create_app()
        client = app.test_client()
        response = client.get("/enseignant/progression/", headers={
            "X-Forwarded-Proto": "http",
            "X-Forwarded-Prefix": "/universite/tal",
        })
        self.assertEqual(response.status_code, 503)

    def test_invalid_cookie_settings_fail_at_startup(self):
        for key, value in (
            ("TAL_SESSION_COOKIE_NAME", "tal; bad"),
            ("TAL_SESSION_COOKIE_NAME", " "),
            ("TAL_SESSION_COOKIE_PATH", "/universite/tal"),
            ("TAL_SESSION_COOKIE_PATH", "/universite//tal/"),
            ("TAL_SESSION_COOKIE_PATH", "/universite/tal/;Secure"),
        ):
            with self.subTest(key=key, value=value):
                with patch.dict(os.environ, {key: value}):
                    with self.assertRaises(ValueError):
                        create_app()

    def test_plain_install_remains_usable_until_prefix_is_configured(self):
        with patch.dict(os.environ, {
            "TAL_SESSION_COOKIE_NAME": "",
        }):
            with self.assertRaises(ValueError):
                create_app()
        os.environ.pop("TAL_SESSION_COOKIE_PATH", None)
        app = create_app()
        self.assertEqual(app.config["SESSION_COOKIE_PATH"], "/")


if __name__ == "__main__":
    unittest.main()
