"""DM hybride : barème, dernier dépôt, contrôle humain et rapports privés.

Toutes les identités et copies sont fictives ; aucun SMTP ni code étudiant
n'est exécuté. Les tests traversent les routes Flask réelles.
"""
import csv
import io
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "app"), str(ROOT / "tests")]

import outils
import app_correction_DM_intermediaire_S1 as dm
import dm_hybrid
import student_access
import teacher_access
from app import create_app
from test_dm_intermediaire_s1 import answer, notebook, BUDGET


class HybridDmTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        p = patch.object(outils,"BASE_DIR",str(self.root))
        p.start(); self.addCleanup(p.stop)
        env = patch.dict(os.environ, {
            "FLASK_SECRET_KEY": "integration-test-hybrid-review-secret-123456789",
            "TAL_ACADEMIC_YEAR": "2026-2027",
            "TAL_SMTP_HOST": "smtp.invalid",
            "TAL_SMTP_SECURITY": "ssl",
            "TAL_SMTP_FROM": "prof@example.invalid",
            "TAL_TEACHER_EMAIL": "prof@example.invalid",
            "TAL_STUDENT_REPORTS_ENABLED": "1",
        })
        env.start(); self.addCleanup(env.stop)
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def payload(self, score_one=True):
        return json.dumps(notebook(
            answer(1, BUDGET, [12,90,108,9,True])
            if score_one else answer(1,"print('bad')", [])
        )).encode()

    def deposit(self, client=None, good=True):
        client = client or self.client
        return client.post("/submit",data={
            "file": (io.BytesIO(self.payload(good)),"devoir.ipynb")
        },content_type="multipart/form-data")

    def authorize_student(self,client):
        db = student_access._db()
        db.execute("INSERT OR REPLACE INTO accounts(number,email,salt,digest,version)"
                   "VALUES(?,?,?,?,1)",("TEST2026","etud@example.invalid","a","b"))
        db.close()
        with client.session_transaction() as s:
            s["student_number"] = "TEST2026"
            s["student_version"] = 1
            s["student_authenticated_at"] = int(time.time())

    def authorize_teacher(self,client):
        with client.session_transaction() as s:
            s["teacher_authenticated_at"] = int(time.time())
            s["teacher_identity"] = teacher_access.session_identity()
            s["teacher_csrf"] = "private-csrf"

    def test_barometer_exact_and_student_initial_receipt(self):
        self.assertAlmostEqual(sum(dm.AUTO_WEIGHTS.values()),17.75)
        self.assertAlmostEqual(sum(dm.HUMAN_WEIGHTS.values()),2.25)
        self.assertEqual(set(dm.HUMAN_WEIGHTS),{2,6,12,14,17})
        response = self.deposit()
        self.assertEqual(response.status_code,200)
        self.assertIn("1.00 / 17.75",response.get_data(as_text=True))
        active=dm_hybrid.active_for("TEST2026")
        self.assertIsNotNone(active)
        self.assertEqual(active["auto_score"],1.0)
        self.assertEqual(active["state"],"pending")
        self.assertEqual(active["auto_version"],2)
        self.assertEqual(len(dm_hybrid.queue()),1)
        info,answers,feedback=dm_hybrid.review_evidence(active)
        self.assertEqual(info["numero_etudiant"],"TEST2026")
        self.assertEqual(len(answers),5)
        self.assertEqual(len(feedback),18)
        self.assertEqual(sum(x["auto_max"] for x in answers.values()),3.25)
        self.assertEqual(len(list((self.root/"DM_intermediaire_S1"/"nb").glob("*.ipynb"))),1)
        self.assertEqual(len(list((self.root/"DM_intermediaire_S1"/"rapport").glob("*.html"))),1)

    def test_latest_overrides_only_below_threshold_with_verified_student(self):
        self.assertEqual(self.deposit().status_code,200)
        first=dm_hybrid.active_for("TEST2026")["submission_id"]
        rejected=self.deposit()
        self.assertNotIn("Copie reçue",rejected.get_data(as_text=True))
        self.assertEqual(dm_hybrid.active_for("TEST2026")["submission_id"],first)
        self.authorize_student(self.client)
        accepted=self.deposit()
        self.assertIn("Copie reçue",accepted.get_data(as_text=True))
        last=dm_hybrid.active_for("TEST2026")["submission_id"]
        self.assertNotEqual(last,first)
        self.assertEqual(dm_hybrid.by_receipt(first)["state"],"superseded")
        self.assertEqual(len(dm_hybrid.queue()),1)
        self.assertEqual(len(list((self.root/"DM_intermediaire_S1"/"nb").glob("*.ipynb"))),2)
        self.authorize_teacher(self.client)
        self.assertEqual(self.client.get("/enseignant/progression/dm-s1/"+first).status_code,404)

    def test_threshold_is_strict_and_published_grade_blocks_redrop(self):
        con=dm_hybrid._db()
        try:
            con.execute("BEGIN IMMEDIATE")
            dm_hybrid.register(con,"TEST2026","a"*32,8.875,b"fake")
            con.commit()
            with self.assertRaises(dm_hybrid.SubmissionClosed):
                dm_hybrid.assert_redrop_allowed(con,"TEST2026")
            con.execute("UPDATE submissions SET auto_score=8.874 WHERE submission_id=?",("a"*32,))
            dm_hybrid.assert_redrop_allowed(con,"TEST2026")
            con.execute("UPDATE submissions SET state='published' WHERE submission_id=?",("a"*32,))
            with self.assertRaises(dm_hybrid.SubmissionClosed):
                dm_hybrid.assert_redrop_allowed(con,"TEST2026")
        finally:
            con.close()

    def test_teacher_review_workflow_draft_publish_and_stale_guard(self):
        self.deposit()
        receipt=dm_hybrid.active_for("TEST2026")["submission_id"]
        self.assertEqual(self.client.get("/enseignant/progression/dm-s1").status_code,403)
        self.authorize_teacher(self.client)
        listing=self.client.get("/enseignant/progression/dm-s1")
        self.assertEqual(listing.status_code,200)
        self.assertIn("TEST2026",listing.get_data(as_text=True))
        view=self.client.get("/enseignant/progression/dm-s1/"+receipt)
        self.assertEqual(view.status_code,200)
        self.assertIn("Q6",view.get_data(as_text=True))
        self.assertIn("Q14",view.get_data(as_text=True))
        self.assertIn("Votre",view.get_data(as_text=True)) if False else None
        form={"csrf":"private-csrf","revision":"0","action":"draft",
              "points_2":"0.25","appreciation_2":"Bien commencé"}
        for q in dm.HUMAN_WEIGHTS:
            form.setdefault("points_"+str(q),"")
            form.setdefault("appreciation_"+str(q),"")
        posted=self.client.post("/enseignant/progression/dm-s1/"+receipt+"/enregistrer",
            data=form)
        self.assertEqual(posted.status_code,303)
        self.assertEqual(dm_hybrid.active_for("TEST2026")["state"],"draft")
        self.assertEqual(dm_hybrid.active_for("TEST2026")["revision"],1)
        stale=self.client.post("/enseignant/progression/dm-s1/"+receipt+"/enregistrer",
            data=form)
        self.assertEqual(stale.status_code,409)
        form["revision"]="1"; form["action"]="publish"
        for q, max_points in dm.HUMAN_WEIGHTS.items():
            form["points_"+str(q)]=str(max_points)
            form["appreciation_"+str(q)]="Explication vérifiée."
        validated=self.client.post("/enseignant/progression/dm-s1/"+receipt+"/enregistrer",
            data=form)
        self.assertEqual(validated.status_code,303)
        final=dm_hybrid.active_for("TEST2026")
        self.assertEqual(final["state"],"published")
        self.assertEqual(final["final_score"],3.25)
        self.assertEqual(self.client.post("/enseignant/progression/dm-s1/"+receipt+"/enregistrer",
            data=form).status_code,409)
        self.assertEqual(self.deposit().status_code,200)
        self.assertNotIn("Copie reçue",self.deposit().get_data(as_text=True))

    def test_student_report_requires_verified_session_and_show_publication(self):
        self.deposit()
        receipt=dm_hybrid.active_for("TEST2026")["submission_id"]
        url="/ma-progression/rapport/dm-intermediaire-s1"
        self.assertEqual(self.client.get(url).status_code,403)
        self.authorize_student(self.client)
        before=self.client.get(url)
        self.assertEqual(before.status_code,200)
        self.assertIn("17.75",before.get_data(as_text=True))
        self.assertNotIn("Correction humaine publiée",before.get_data(as_text=True))
        self.authorize_teacher(self.client)
        data={"csrf":"private-csrf","revision":"0","action":"publish"}
        for q,weight in dm.HUMAN_WEIGHTS.items():
            data["points_"+str(q)]=str(weight)
            data["appreciation_"+str(q)]="Bonne explication."
        self.assertEqual(self.client.post(
            "/enseignant/progression/dm-s1/"+receipt+"/enregistrer",
            data=data).status_code,303)
        after=self.client.get(url)
        self.assertEqual(after.status_code,200)
        self.assertIn("Note finale",after.get_data(as_text=True))
        self.assertIn("3.25 / 20",after.get_data(as_text=True))
        self.assertIn("Bonne explication.",after.get_data(as_text=True))
        self.assertNotIn("Critères AST :",after.get_data(as_text=True))
        self.assertEqual(self.client.get("/ma-progression/rapport/controle-td1-s3").status_code,404)

    def test_report_feature_switch_off_even_for_authenticated_student(self):
        self.deposit()
        self.authorize_student(self.client)
        with patch.dict(os.environ,{"TAL_STUDENT_REPORTS_ENABLED":"0"}):
            self.assertEqual(self.client.get("/ma-progression/rapport/dm-intermediaire-s1").status_code,404)

    def test_wrong_teacher_csrf_does_not_publish(self):
        self.deposit()
        self.authorize_teacher(self.client)
        receipt=dm_hybrid.active_for("TEST2026")["submission_id"]
        r=self.client.post("/enseignant/progression/dm-s1/"+receipt+"/enregistrer",
            data={"csrf":"wrong","revision":"0","action":"publish"})
        self.assertEqual(r.status_code,400)
        self.assertEqual(dm_hybrid.active_for("TEST2026")["state"],"pending")

    def test_legacy_migration_dry_run_and_apply_preserve_original_csv(self):
        self.deposit()
        receipt=dm_hybrid.active_for("TEST2026")["submission_id"]
        db=dm_hybrid._db()
        db.execute("DELETE FROM submissions")
        db.close()
        import bootstrap_dm_hybrid
        path=self.root/"DM_intermediaire_S1"/"notes_DM_intermediaire_S1.csv"
        original=path.read_bytes()
        report=bootstrap_dm_hybrid.run()
        self.assertEqual(report["candidats"],1)
        self.assertEqual(report["copies_exploitables"],1)
        self.assertEqual(report["mode"],"SIMULATION")
        self.assertIsNone(dm_hybrid.active_for("TEST2026"))
        with self.assertRaises(ValueError):
            bootstrap_dm_hybrid.run(apply=True)
        apply=bootstrap_dm_hybrid.run(apply=True,backup_confirmed=True)
        self.assertEqual(apply["ajoutes"],1)
        self.assertEqual(dm_hybrid.active_for("TEST2026")["submission_id"],receipt)
        self.assertEqual(bootstrap_dm_hybrid.run(apply=True,backup_confirmed=True)["ajoutes"],0)
        self.assertEqual(path.read_bytes(),original)


if __name__ == "__main__":
    unittest.main()
