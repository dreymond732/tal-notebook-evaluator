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
from bs4 import BeautifulSoup

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
            "TAL_STUDENT_REPORTS_ENABLED":"1",
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
        self.assertEqual(incomplete.status_code, 422)
        self.assertIn("Saisissez une note", incomplete.get_data(as_text=True))
        fields = BeautifulSoup(incomplete.get_data(as_text=True), "html.parser")
        self.assertEqual(fields.select_one('[name="points_2"]')["value"], "0.5")
        self.assertEqual(fields.select_one('[name="comment_2"]').text, "Justification correcte")
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

    def review_form(self, action="valider"):
        self.submit()
        current = dm_hybrid.current_for_student("TEST2026")
        url = "/enseignant/progression/dm-s1/" + current["receipt"]
        form = {"csrf": "csrf-fixture-teacher", "action": action}
        form.update({f"points_{q}": str(dm_hybrid.HUMAN_WEIGHTS[q])
                     for q in dm_hybrid.QUESTIONS})
        return self.teacher_login(), url, form

    def test_notes_only_publish_and_redirect_to_queue_with_three_scores(self):
        teacher, url, form = self.review_form()
        response = teacher.post(url, data=form)
        self.assertEqual(response.status_code, 303)
        self.assertTrue(response.location.endswith("/dm-s1"))
        listing = teacher.get(response.location).get_data(as_text=True)
        self.assertIn("Correction validée et publiée", listing)
        for text in ("Auto / 17,75", "Correction / 2,25", "Finale / 20", "Validée", "Consulter"):
            self.assertIn(text, listing)
        current = dm_hybrid.current_for_student("TEST2026")
        self.assertIsNotNone(current["validated_at"])
        self.assertEqual((current["human_score"], current["final_score"]), (2.25, 3.25))
        self.assertTrue(all(q["comment"] == "" for q in current["questions"]))
        item = dm_hybrid.queue()[0]
        self.assertEqual((item["score"], item["human_score"], item["final_score"], item["status"]),
                         (1, 2.25, 3.25, "Validée"))
        self.student_login()
        report = self.client.get("/ma-progression/rapport/dm-intermediaire-s1")
        self.assertEqual(report.status_code, 200)
        self.assertIn("3.25 / 20.00", report.get_data(as_text=True))
        readonly = teacher.get(url).get_data(as_text=True)
        self.assertIn("Cette fiche n'est plus modifiable", readonly)

    def test_queue_distinguishes_unstarted_draft_and_final_zero(self):
        teacher, url, form = self.review_form("brouillon")
        fresh = dm_hybrid.queue()[0]
        self.assertEqual((fresh["status"], fresh["human_score"], fresh["final_score"]),
                         ("À corriger", None, None))
        partial = {"csrf": form["csrf"], "action": "brouillon", "points_2": "0"}
        response = teacher.post(url, data=partial)
        self.assertEqual(response.status_code, 303)
        self.assertTrue(response.location.endswith(url))
        draft = dm_hybrid.queue()[0]
        self.assertEqual((draft["status"], draft["human_score"], draft["final_score"]),
                         ("Brouillon", 0, None))
        self.assertIn("En attente", teacher.get("/enseignant/progression/dm-s1").get_data(as_text=True))
        form["action"] = "valider"
        for q in dm_hybrid.QUESTIONS:
            form[f"points_{q}"] = "0"
        self.assertEqual(teacher.post(url, data=form).status_code, 303)
        final = dm_hybrid.queue()[0]
        self.assertEqual((final["status"], final["human_score"], final["final_score"]),
                         ("Validée", 0, 1))

    def test_invalid_form_preserves_all_raw_fields_and_marks_each_error(self):
        teacher, url, form = self.review_form()
        form.update(points_2="0,50", points_6="incorrect", points_12="0,50",
                    points_14="0.123", points_17="")
        for q in dm_hybrid.QUESTIONS:
            form[f"comment_{q}"] = f'Q{q} : <script>test</script> & "citation"'
        response = teacher.post(url, data=form)
        self.assertEqual(response.status_code, 422)
        html = response.get_data(as_text=True)
        self.assertIn("Les valeurs saisies sont conservées", html)
        self.assertNotIn("<script>test</script>", html)
        soup = BeautifulSoup(html, "html.parser")
        for q in dm_hybrid.QUESTIONS:
            self.assertEqual(soup.select_one(f'[name="points_{q}"]')["value"], form[f"points_{q}"])
            self.assertEqual(soup.select_one(f'[name="comment_{q}"]').text, form[f"comment_{q}"])
        for q in (6, 12, 14, 17):
            field = soup.select_one(f'[name="points_{q}"]')
            self.assertEqual(field["aria-invalid"], "true")
            self.assertIsNotNone(soup.select_one("#" + field["aria-describedby"]))
        saved = dm_hybrid.current_for_student("TEST2026")
        self.assertIsNone(saved["validated_at"])
        self.assertTrue(all(q["points"] is None for q in saved["questions"]))
        self.assertEqual(dm_hybrid.queue()[0]["status"], "À corriger")

    def test_failed_update_keeps_previous_draft_and_can_be_corrected(self):
        teacher, url, form = self.review_form("brouillon")
        form["points_2"] = "0.25"
        form["comment_2"] = "Brouillon conservé"
        self.assertEqual(teacher.post(url, data=form).status_code, 303)
        form.update(action="valider", points_2="0,50", points_6="99", comment_2="Nouvelle saisie")
        self.assertEqual(teacher.post(url, data=form).status_code, 422)
        saved = dm_hybrid.current_for_student("TEST2026")
        self.assertEqual((saved["questions"][0]["points"], saved["questions"][0]["comment"]),
                         ("0.25", "Brouillon conservé"))
        self.assertIsNone(saved["validated_at"])
        self.assertEqual(dm_hybrid.queue()[0]["status"], "Brouillon")
        form["points_6"] = "0,50"
        success = teacher.post(url, data=form)
        self.assertEqual(success.status_code, 303)
        saved = dm_hybrid.current_for_student("TEST2026")
        self.assertEqual(saved["final_score"], 3.25)
        self.assertEqual(saved["questions"][0]["comment"], "Nouvelle saisie")

    def test_retained_form_and_success_redirect_keep_proxy_prefix(self):
        teacher, url, form = self.review_form()
        headers = {"X-Forwarded-Prefix": "/universite/tal", "X-Forwarded-Proto": "https"}
        form["points_2"] = "incorrect"
        response = teacher.post(url, data=form, headers=headers)
        self.assertEqual(response.status_code, 422)
        html = response.get_data(as_text=True)
        self.assertIn('action="/universite/tal' + url + '"', html)
        self.assertIn('value="incorrect"', html)
        form["points_2"] = "0,50"
        response = teacher.post(url, data=form, headers=headers)
        self.assertEqual(response.status_code, 303)
        self.assertEqual(response.location, "/universite/tal/enseignant/progression/dm-s1")

    def test_long_comment_is_retained_and_optional_comments_still_have_limit(self):
        teacher, url, form = self.review_form()
        form["comment_2"] = "x" * 4001
        response = teacher.post(url, data=form)
        self.assertEqual(response.status_code, 422)
        soup = BeautifulSoup(response.get_data(as_text=True), "html.parser")
        self.assertEqual(soup.select_one('[name="comment_2"]').text, form["comment_2"])
        self.assertEqual(soup.select_one('[name="comment_2"]')["aria-invalid"], "true")
        self.assertIsNone(dm_hybrid.current_for_student("TEST2026")["validated_at"])

    def test_nonfinite_negative_and_overprecise_notes_are_rejected(self):
        teacher, url, form = self.review_form()
        for value in ("NaN", "Infinity", "-0.1", "1", "0.123", "abc"):
            with self.subTest(value=value):
                form["points_2"] = value
                response = teacher.post(url, data=form)
                self.assertEqual(response.status_code, 422)
                soup = BeautifulSoup(response.get_data(as_text=True), "html.parser")
                self.assertEqual(soup.select_one('[name="points_2"]')["value"], value)
                self.assertIsNone(dm_hybrid.current_for_student("TEST2026")["validated_at"])

    def test_teacher_privacy_and_csrf(self):
        self.submit()
        current=dm_hybrid.current_for_student("TEST2026")
        path="/enseignant/progression/dm-s1/"+current["receipt"]
        self.assertEqual(self.client.get(path).status_code,403)
        self.assertEqual(self.client.get("/enseignant/progression/dm-s1").status_code,403)
        self.assertEqual(self.client.post(path,data={"action":"valider"}).status_code,403)
        teacher=self.teacher_login()
        self.assertEqual(teacher.post(path,data={"action":"brouillon"}).status_code,400)
        other_path = path[:-1] + ("1" if path[-1] == "0" else "0")
        self.assertEqual(teacher.get(other_path).status_code,404)
        unauth_report=self.app.test_client().get("/ma-progression/rapport/dm-intermediaire-s1")
        self.assertEqual(unauth_report.status_code,403)

    def test_reviewer_questions_are_complete_official_source_prompts(self):
        source = json.loads(
            (ROOT / "Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb")
            .read_text(encoding="utf-8")
        )
        for q in dm_hybrid.QUESTIONS:
            with self.subTest(question=q):
                index = next(i for i, cell in enumerate(source["cells"])
                             if cell.get("metadata", {}).get("tal", {}).get("question")
                             == "Q" + str(q) and cell["metadata"]["tal"].get("role") == "answer")
                before = source["cells"][index - 1]
                expected = "".join(before["source"])
                self.assertEqual(dm_hybrid.REVIEW_PROMPTS[q], expected)
                self.assertIn("Question " + str(q), expected)

    def test_dm_isolated_between_academic_years(self):
        self.submit()
        current = dm_hybrid.current_for_student("TEST2026")
        self.assertIsNotNone(current)
        with patch.dict(os.environ, {"TAL_ACADEMIC_YEAR": "2027-2028"}):
            self.assertIsNone(dm_hybrid.current_for_student("TEST2026"))
            self.assertTrue(dm_hybrid.can_redeposit("TEST2026"))
            self.assertEqual(dm_hybrid.queue(), [])
        self.assertEqual(dm_hybrid.current_for_student("TEST2026")["receipt"],
                         current["receipt"])

    def test_late_anonymous_redeposit_is_rejected_under_lock(self):
        self.submit()
        previous = dm_hybrid.current_for_student("TEST2026")["receipt"]
        from routes import process_submission
        from types import SimpleNamespace
        with self.app.test_request_context("/submit", method="POST"):
            with self.assertRaisesRegex(ValueError, "connexion personnelle nécessaire"):
                process_submission(
                    SimpleNamespace(filename="copie.ipynb"),
                    self.payload, "<p>rapport de test</p>",
                    {"numero_etudiant": "TEST2026"}, 1.0,
                    "dm-intermediaire-s1", dm_payload=([], {}),
                )
        self.assertEqual(dm_hybrid.current_for_student("TEST2026")["receipt"],
                         previous)

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

    def test_reports_disabled_by_default_even_for_authenticated_student(self):
        self.submit()
        self.student_login()
        with patch.dict(os.environ, {"TAL_STUDENT_REPORTS_ENABLED": "0"}):
            dashboard = self.client.get("/ma-progression")
            self.assertEqual(dashboard.status_code, 200)
            self.assertNotIn("Consulter le dernier bilan du DM",
                             dashboard.get_data(as_text=True))
            self.assertEqual(
                self.client.get("/ma-progression/rapport/dm-intermediaire-s1").status_code,
                404,
            )
            self.assertEqual(
                self.client.get("/ma-progression/rapport/td3-s1").status_code,
                404,
            )
            self.assertIsNone(latest_td_report("TEST2026", "td3-s1"))

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
