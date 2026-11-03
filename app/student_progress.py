"""Lecture strictement individuelle des synthèses privées du suivi TAL.

Une route publique ne lit jamais les cahiers, rapports ni résultats des
contrôles. Seules les évaluations formatives (mode td) sont affichables.
"""
import csv
from pathlib import Path

import outils
from progression import _catalog, SEMESTERS


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
            activities.append({
                "name": slug,
                "attempts": count,
                "min": matching.get(slug + "__min", "") if matching and count else "",
                "max": matching.get(slug + "__max", "") if matching and count else "",
            })
        semesters.append({
            "name": sem,
            "activities": activities,
            "completed": sum(activity["attempts"] > 0 for activity in activities),
            "total": len(activities),
        })
    if not name and not first_name:
        return None
    return {"number": number, "name": name, "first_name": first_name,
            "semesters": semesters}
