"""Lecture strictement individuelle des synthèses privées du suivi TAL.

Une route publique ne lit jamais les cahiers, rapports ni résultats des
contrôles. Seules les évaluations formatives (mode td) sont affichables.
"""
import csv
import re
from pathlib import Path

import outils
from progression import _catalog, SEMESTERS
from routes import EVALUATORS
from teacher_scores import scaled_score
from student_reports import latest_td_report
from dm_hybrid import current_for_student



def _order_activity(activity, semester):
    """Ordre TD S1 et A/B/C, sans changer les identifiants internes."""
    if semester == "S1":
        found = re.fullmatch(r"td([1-7])(?:-(one|bis|ter))?-s1", activity["name"])
        if found:
            return (int(found[1]), {"one": 1, "bis": 2, "ter": 3}.get(found[2], 0))
    return (100, 0)


def _rows(path):
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            yield from csv.DictReader(stream, delimiter=";")
    except (OSError, UnicodeError, csv.Error):
        return


def student_exists(number):
    """Existence du numéro sans révéler un nom ou un effectif au visiteur."""
    base = Path(outils.BASE_DIR) / "suivi"
    return any(
        row.get("Numéro étudiant") == number
        for sem in SEMESTERS
        for row in _rows(base / ("progression_" + sem + ".csv"))
    )


def individual_progress(number):
    """Données limitées à un étudiant vérifié, sans scores de contrôles/DM."""
    if not number:
        return None
    base = Path(outils.BASE_DIR) / "suivi"
    catalog = _catalog()
    semesters = []
    name = ""
    first_name = ""
    for sem in SEMESTERS:
        matching = next((r for r in _rows(base / ("progression_" + sem + ".csv"))
                         if r.get("Numéro étudiant") == number), None)
        if matching:
            name = matching.get("Nom", "") or name
            first_name = matching.get("Prénom", "") or first_name
        activities = []
        for entry in catalog:
            if entry["semester"] != sem or entry["mode"] != "td":
                continue
            slug = entry["evaluator"]
            # Données du propre étudiant seulement. Aucun accès aux copies.
            attempts = matching.get(slug + "__essais", "0") if matching else "0"
            try:
                count = max(0, int(attempts))
            except (ValueError, TypeError):
                count = 0
            minimum = matching.get(slug + "__min", "") if matching and count else ""
            maximum = matching.get(slug + "__max", "") if matching and count else ""
            is_extra = bool(
                sem == "S1" and re.fullmatch(r"td[3-6]-(one|bis|ter)-s1", slug)
            )
            is_revision = sem == "S3" and slug in {
                "td-r0-s3", "td-r1-s3", "td-r2-s3"
            }
            activities.append({
                "name": slug,
                "label": EVALUATORS[slug][0],
                "subactivity": is_extra,
                "is_complement": is_extra or is_revision,
                "attempts": count,
                "report": bool(count and latest_td_report(number, slug)),
                "min": scaled_score(minimum, slug, 10) if count else "",
                "max": scaled_score(maximum, slug, 10) if count else "",
            })
        if sem == "S1":
            activities.sort(key=lambda item: _order_activity(item, sem))
        main_activities = [a for a in activities if not a["is_complement"]]
        complements = [a for a in activities if a["is_complement"]]
        semesters.append({
            "name": sem,
            "activities": activities,
            "completed": sum(a["attempts"] > 0 for a in main_activities),
            "total": len(main_activities),
            "extra_completed": sum(a["attempts"] > 0 for a in complements),
            "extra_total": len(complements),
        })
    if not name and not first_name:
        return None
    dm = current_for_student(number)
    return {"number": number, "name": name, "first_name": first_name,
            "semesters": semesters, "dm": dm}
