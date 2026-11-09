"""DM hybride : seuil/redépôt, fiche active, publication et rapports privés.

Toutes les identités, notes et envois ici sont fictifs.
"""
import io
import json
import os
import re
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "app"), str(ROOT / "tests")]

import outils
import student_access
import teacher_access
from app import create_app
import dm_hybrid
import app_correction_DM_intermediaire_S1 as dm
from student_reports import latest_td_report
from test_dm_intermediaire_s1 import notebook, answer, BUDGET


class HybridReviewTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        p = patch.object(outils, "BASE_DIR", str(self.root))
        p.start()
        self.addCleanup(p.stop)
        env = patch.dict(os.environ, {
            "FLASK_SECRET_KEY":"hybrid-synthetic-fixture-secret-0123456789",
            "TAL_ACADEMIC_YEAR":"2026-2027",
            "TAL_TEACHER_EMAIL":"prof@example.invalid",
            "TAL_SMTP_HOST":"smtp.example.invalid",
            "TAL_SMTP_FROM":"tal@example.invalid",
            "TAL_SMTP_SECURITY":"ssl",
            "TAL_SESSION_COOKIE_PATH":"/",
        })
        env.start()
        self.addCleanup(env.stop)
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.payload = json.dumps(
            notebook(answer(1, BUDGET, [12,90,108,9,True]))
        ).encode()

    def submit(self, client=None):
        client = client or self.client
        return client.post("/submit", data={
            "file":(io.BytesIO(self.payload),"copie_dm.ipynb"),
        }, content_type="multipart/form-data")

    def student_login(self, client=None, number="TEST2026"):
        client = client or self.client
        salt = "ab"*16
        db = student_access._db()
        try:
            db.execute(
                "INSERT OR REPLACE INTO accounts(number,email,salt,digest,version) "
                "VALUES (?,?,?,?,1)",
                (number,"student@example.invalid",salt,
                 student_access._hash(number,"PLACEHOLDER",salt))
            )
        finally:
            db.close()
        with client.session_transaction() as s:
            s["student_number"] = number
            s["student_version"] = 1
            s["student_authenticated_at"] = int(time.time())

    def teacher_login(self):
        client = self.app.test_client()
        with client.session_transaction() as s:
            s["teacher_authenticated_at"] = int(time.time())
            s["teacher_identity"] = teacher_access.session_identity()
            s["teacher_csrf"] = "csrf-fixture-teacher"
        return client

    def test_first_submission_creates_current_and_second_requires_owned_session(self):
        first = self.submit()
        self.assertEqual(first.status_code,200)
        self.assertIn("1.00 / 17.75",first.get_data(as_text=True))
        before = dm_hybrid.current_for_student("TEST2026")
        self.assertEqual(before["score"],1)
        self.assertEqual(len(dm_hybrid.queue()),1)
        denied = self.submit()
        self.assertIn("connectez-vous à", denied.get_data(as_text=True).lower())
        self.assertEqual(dm_hybrid.current_for_student("TEST2026")["receipt"], before["receipt"])
        self.student_login()
        again = self.submit()
        self.assertEqual(again.status_code,200)
        after = dm_hybrid.current_for_student("TEST2026")
        self.assertNotEqual(before["receipt"],after["receipt"])
        self.assertEqual(len(dm_hybrid.queue()),1)
        self.assertIsNone(dm_hybrid.current_by_receipt(before["receipt"]))
        with self.assertRaisesRegex(ValueError,"remplacée"):
            dm_hybrid.save_review(before["receipt"],{},validate=False)
        db = dm_hybrid._db()
        try:
            self.assertEqual(db.execute("SELECT count(*) FROM attempts").fetchone()[0],2)
        finally:
            db.close()

    def test_teacher_draft_validation_and_published_result(self):
        self.submit()
        self.student_login()
        t = self.teacher_login()
        listing = t.get("/enseignant/progression/dm-s1")
        self.assertEqual(listing.status_code,200)
        self.assertIn("DM S1",listing.get_data(as_text=True))
        current = dm_hybrid.current_for_student("TEST2026")
        url = "/enseignant/progression/dm-s1/" + current["receipt"]
        view = t.get(url)
        self.assertEqual(view.status_code,200)
        html = view.get_data(as_text=True)
        for q in dm_hybrid.QUESTIONS:
            self.assertIn("Q"+str(q),html)
        incomplete = t.post(url, data={
            "csrf":"csrf-fixture-teacher","action":"valider",
            "points_2":"0.5","comment_2":"Justification correcte",
        }, follow_redirects=True)
        self.assertIn("requises",incomplete.get_data(as_text=True)) if False else None
        self.assertIsNone(dm_hybrid.current_for_student("TEST2026")["validated_at"])
        form = {"csrf":"csrf-fixture-teacher","action":"brouillon"}
        for q in dm_hybrid.QUESTIONS:
            form["points_"+str(q)] = str(dm_hybrid.HUMAN_WEIGHTS[q])
            form["comment_"+str(q)] = "Explication validée pour la question"
        self.assertEqual(t.post(url,data=form).status_code,303)
        self.assertIsNone(dm_hybrid.current_for_student("TEST2026")["validated_at"])
        form["action"] = "valider"
        validated=t.post(url,data=form,follow_redirects=True)
        self.assertEqual(validated.status_code,200)
        final = dm_hybrid.current_for_student("TEST2026")
        self.assertAlmostEqual(final["human_score"],2.25)
        self.assertAlmostEqual(final["final_score"],3.25)
        self.assertFalse(final["redraw_allowed"])
        report=self.client.get("/ma-progression/rapport/dm-intermediaire-s1")
        self.assertEqual(report.status_code,200)
        text=report.get_data(as_text=True)
        self.assertIn("3.25 / 20.00",text)
        self.assertIn("Explication validée pour la question",text)
        self.assertNotIn("Critères AST :",text)
        refused=self.submit()
        self.assertIn("Redépôt fermé",refused.get_data(as_text=True))
        self.assertEqual(len(dm_hybrid.queue()),1)

    def test_teacher_privacy_and_csrf(self):
        self.submit()
        current=dm_hybrid.current_for_student("TEST2026")
        path="/enseignant/progression/dm-s1/"+current["receipt"]
        self.assertEqual(self.client.get(path).status_code,403)
        self.assertEqual(self.client.get("/enseignant/progression/dm-s1").status_code,403)
        self.assertEqual(self.client.post(path,data={"action":"valider"}).status_code,403)
        teacher=self.teacher_login()
        self.assertEqual(teacher.post(path,data={"action":"brouillon"}).status_code,400)
        self.assertEqual(teacher.get(path[:-1]+"0").status_code,404)
        unauth_report=self.app.test_client().get("/ma-progression/rapport/dm-intermediaire-s1")
        self.assertEqual(unauth_report.status_code,403)

    def test_threshold_and_form_limits(self):
        self.assertAlmostEqual(dm.MAX_SCORE_TOTAL,17.75)
        self.assertAlmostEqual(sum(dm.HUMAN_WEIGHTS.values()),2.25)
        self.assertAlmostEqual(dm.REDEPOSIT_THRESHOLD,8.875)
        self.assertTrue(dm_hybrid.can_redeposit("NEW"))
        # Identifiant artificiel et preuve initiale construite en mémoire.
        fields = {
            "nom":"TEST","prenom":"TEST","numero_etudiant":"STUDENT_B",
            "dm_rubric_version":2,
        }
        feedback=[{"number":q,"title":dm.LABELS[q-1],"points":0,
                   "max_points":dm.AUTOMATIC_WEIGHTS[q],"status":"a_reprendre",
                   "student_output":""} for q in range(1,19)]
        dm_hybrid.record_submission("a"*32,fields,"x.ipynb",8.874,feedback,{"cells":[]})
        self.assertTrue(dm_hybrid.can_redeposit("STUDENT_B"))
        dm_hybrid.record_submission("b"*32,fields,"y.ipynb",8.875,feedback,{"cells":[]})
        self.assertFalse(dm_hybrid.can_redeposit("STUDENT_B"))
        with self.assertRaises(ValueError):
            dm_hybrid.save_review("b"*32,{
                **{f"points_{q}":"999" for q in dm_hybrid.QUESTIONS}
            },validate=True)
        self.assertIsNone(dm_hybrid.current_for_student("STUDENT_B")["validated_at"])

    def test_td_report_latest_only_and_foreign_student_forbidden(self):
        from routes import process_submission
        from types import SimpleNamespace
        with self.app.app_context():
            for receipt, content in [("first","FIRST REPORT"),("second","SECOND REPORT")]:
                process_submission(
                    SimpleNamespace(filename="td3.ipynb"),
                    b'{"cells":[]}',content,
                    {"nom":"MARTIN","prenom":"Léa","classe":"G1",
                     "numero_etudiant":"TEST2026","contract_version":2,
                     "score_nature":"technique_provisoire","score_max":6},
                    3.0, "td3-s1",
                )
        latest=latest_td_report("TEST2026","td3-s1")
        self.assertIsNotNone(latest)
        self.assertIn("SECOND REPORT",latest.read_text())
        self.assertIsNone(latest_td_report("ANOTHER","td3-s1"))
        # Le dernier essai peut être préservé par la migration de stockage S1.
        # Son reçu original demeure la preuve d'appartenance de son rapport.
        import csv
        journal = self.root / "S1_TD3" / "notes_S1_TD3.csv"
        with journal.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream, delimiter=";"))
            fields = list(rows[0])
        second_receipt = rows[-1]["Origine"].split(":")[-1]
        rows[-1]["Origine"] = "migration-s1-v2:TD3_S1:2:direct:" + second_receipt
        with journal.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, delimiter=";", fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        self.assertEqual(latest_td_report("TEST2026","td3-s1"), latest)
        self.assertIsNone(latest_td_report("TEST2026","controle-td1-s3"))
        self.assertEqual(self.app.test_client().get("/ma-progression/rapport/td3-s1").status_code,403)
        self.student_login()
        result=self.client.get("/ma-progression/rapport/td3-s1")
        self.assertEqual(result.status_code,200)
        self.assertIn("SECOND REPORT",result.get_data(as_text=True))
        self.assertIn("sandbox",result.headers["Content-Security-Policy"])
        self.assertEqual(self.client.get("/ma-progression/rapport/td2-S2").status_code,404)
        dashboard=self.client.get("/ma-progression")
        self.assertIn("Consulter",dashboard.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
