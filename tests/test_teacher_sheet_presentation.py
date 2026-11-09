"""Fiches enseignant : regroupement TD, barèmes /10-/20 et actualisation."""
import csv
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

import outils
from notebook_contract import load_catalog
from progression import SEMESTERS
from routes import EVALUATORS
from teacher_progress import cohort, semester_entries, student_sheet
from teacher_scores import max_raw_score, scaled_score


class TeacherSheetPresentationTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / "suivi").mkdir()
        p = patch.object(outils, "BASE_DIR", str(self.root))
        p.start()
        self.addCleanup(p.stop)
        env = patch.dict(os.environ, {"TAL_ACADEMIC_YEAR": "2026-2027"})
        env.start()
        self.addCleanup(env.stop)

    def csv(self, semester, scored):
        evaluations = semester_entries(semester)
        header = ["Numéro étudiant", "Nom", "Prénom"]
        for entry in evaluations:
            header.extend(entry["id"] + "__" + suffix
                          for suffix in ("min", "max", "essais"))
        row = {"Numéro étudiant": "000123", "Nom": "MARTIN", "Prénom": "Léa"}
        for item in evaluations:
            values = scored.get(item["id"], ("", "", "0"))
            for field, value in zip(("min", "max", "essais"), values):
                row[item["id"] + "__" + field] = value
        path = self.root / "suivi" / f"progression_{semester}.csv"
        with path.open("w", newline="", encoding="utf-8") as out:
            writer = csv.DictWriter(out, fieldnames=header, delimiter=";")
            writer.writeheader()
            writer.writerow(row)

    def test_all_active_evaluators_have_positive_raw_maximum(self):
        # Le dénominateur n'est jamais une estimation : vérifié dans chaque correcteur.
        all_eval = [e for e in load_catalog() if e["active"] and e["evaluator"]
                    and e["evaluator"] != "Controletilt-s1"]
        self.assertEqual(len(all_eval), 45)
        for entry in all_eval:
            with self.subTest(evaluator=entry["evaluator"]):
                ev = entry["evaluator"]
                raw = max_raw_score(ev)
                self.assertGreater(raw, 0)
                target = 10 if entry["mode"] == "td" else 20
                self.assertEqual(scaled_score(str(raw), ev, target),
                                 f"{target},00")

    def test_labels_are_exact_and_ids_remain_stable(self):
        self.assertEqual(EVALUATORS["td3-s1"][0], "S1_TD3 — Collections")
        self.assertEqual(EVALUATORS["td4-s1"][0], "S1_TD4 — Boucles et conditions")
        self.assertEqual(EVALUATORS["td5-s1"][0], "S1_TD5 — Fonctions")
        self.assertEqual(EVALUATORS["td6-s1"][0], "S1_TD6 — Fichiers et données")
        self.assertEqual(EVALUATORS["dm-intermediaire-s1"][0],
                         "Devoir maison intermédiaire S1")
        for part, letter in [("one", "A"), ("bis", "B"), ("ter", "C")]:
            self.assertTrue(EVALUATORS[f"td3-{part}-s1"][0].startswith(f"S1_TD3_{letter}"))
        catalog = {e["evaluator"]: e for e in load_catalog()
                   if e["active"] and e.get("evaluator")}
        self.assertEqual(catalog["td3-one-s1"]["notebook"],
                         "Notebooks TD/S1/S1_TD3_A_listes.ipynb")

    def test_s1_variants_nested_under_their_main_td(self):
        self.csv("S1", {
            "td3-s1": ("3,00", "6,00", "2"),
            "td3-one-s1": ("2,00", "6,00", "2"),
            "td3-bis-s1": ("1,00", "3,00", "1"),
            "td3-ter-s1": ("0,00", "6,00", "1"),
            "td4-s1": ("3,50", "7,00", "2"),
            "dm-intermediaire-s1": ("10,00", "20,00", "2"),
        })
        listing, sheet = student_sheet("S1", "000123")
        self.assertEqual(listing["totals"]["TD"], 7)
        sections = sheet["display_sections"]
        self.assertNotIn("Approfondissement", [s["title"] for s in sections])
        self.assertEqual([s["title"] for s in sections], ["TD", "DM"])
        children = sections[0]["items"]
        ids = [c["id"] for c in children]
        i = ids.index("td3-s1")
        self.assertEqual(ids[i:i+5],
                         ["td3-s1", "td3-one-s1", "td3-bis-s1",
                          "td3-ter-s1", "td4-s1"])
        self.assertFalse(children[i]["subactivity"])
        self.assertTrue(children[i+1]["subactivity"])
        self.assertEqual(children[i]["min_display"], "5,00")
        self.assertEqual(children[i]["max_display"], "10,00")
        self.assertEqual(children[i+4]["min_display"], "5,00")
        self.assertEqual(children[i+4]["max_display"], "10,00")
        dm = sections[1]["items"][0]
        self.assertEqual(dm["label"], "Devoir maison intermédiaire S1")
        self.assertEqual(dm["scale"], 20)
        self.assertEqual(dm["min_display"], "10,00")
        self.assertEqual(dm["max_display"], "20,00")
        self.assertEqual(children[i+1]["scale"], 10)

    def test_s3_revisions_are_on_10_and_control_on_20(self):
        self.csv("S3", {
            "td-r0-s3": ("2,00", "4,00", "2"),
            "td1-s3": ("3,00", "6,00", "2"),
            "controle-td1-s3": ("15,00", "20,00", "2"),
        })
        _, sheet = student_sheet("S3", "000123")
        sections = {section["title"]: section for section in sheet["display_sections"]}
        main = next(x for x in sections["TD"]["items"] if x["id"] == "td1-s3")
        revision = next(x for x in sections["Révision"]["items"] if x["id"] == "td-r0-s3")
        control = sections["Contrôle"]["items"][0]
        self.assertEqual((main["max_display"], main["scale"]), ("10,00", 10))
        self.assertEqual((revision["min_display"], revision["scale"]), ("5,00", 10))
        self.assertEqual((control["min_display"], control["scale"]), ("15,00", 20))
        self.assertEqual((control["max_display"], control["scale"]), ("20,00", 20))

    def test_s2_td_and_control_have_different_display_scales(self):
        self.csv("S2", {
            "td3-S2": (str(max_raw_score("td3-S2")), str(max_raw_score("td3-S2")), "1"),
            "td2-S2": (str(max_raw_score("td2-S2")), str(max_raw_score("td2-S2")), "1"),
        })
        _, sheet = student_sheet("S2", "000123")
        sections = {section["title"]: section for section in sheet["display_sections"]}
        self.assertEqual(sections["TD"]["items"][0]["max_display"], "10,00")
        self.assertEqual(sections["Contrôle"]["items"][0]["max_display"], "20,00")

    def test_sheet_reloads_updated_csv_without_browser_polling(self):
        self.csv("S1", {"td3-s1": ("1,00", "2,00", "1")})
        _, first = student_sheet("S1", "000123")
        self.csv("S1", {"td3-s1": ("1,00", "6,00", "2")})
        _, second = student_sheet("S1", "000123")
        get_td3 = lambda sheet: next(a for a in sheet["display_sections"][0]["items"]
                                     if a["id"] == "td3-s1")
        self.assertEqual(get_td3(first)["attempts"], 1)
        self.assertEqual(get_td3(second)["attempts"], 2)
        self.assertEqual(get_td3(second)["max_display"], "10,00")

    def test_invalid_or_unknown_score_is_never_made_up(self):
        self.assertEqual(scaled_score("", "td3-s1", 10), "")
        with self.assertRaises(ValueError):
            scaled_score("NaN", "td3-s1", 10)
        with self.assertRaises(ValueError):
            max_raw_score("unknown")


if __name__ == "__main__":
    unittest.main()
