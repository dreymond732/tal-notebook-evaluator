"""Vues privées de suivi de promotion, à partir des exports existants.

Ne lit ni les cahiers ni les rapports des étudiants, et ne modifie jamais
les données sources. Le tableau enseignant inclut les TD, DM et contrôles,
contrairement au portail public des étudiants.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

import outils
from progression import SEMESTERS, _catalog
from routes import EVALUATORS

CSV_HEADER = ("Numéro étudiant", "Nom", "Prénom")


def semester_entries(semester):
    if semester not in SEMESTERS:
        raise ValueError("Semestre inconnu")
    return [
        {
            "id": item["evaluator"],
            "label": EVALUATORS[item["evaluator"]][0],
            "type": item["kind"],
            "semester": semester,
        }
        for item in _catalog() if item["semester"] == semester
    ]


def _source(semester):
    if semester not in SEMESTERS:
        raise ValueError("Semestre inconnu")
    return Path(outils.BASE_DIR) / "suivi" / f"progression_{semester}.csv"


def cohort(semester):
    """Liste de tous les étudiants effectivement présents dans le suivi."""
    evaluations = semester_entries(semester)
    path = _source(semester)
    expected_header = list(CSV_HEADER)
    for item in evaluations:
        expected_header.extend(
            f"{item['id']}__{suffix}" for suffix in ("min", "max", "essais")
        )
    students = []
    if path.is_file():
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter=";")
            if reader.fieldnames != expected_header:
                raise ValueError("Schéma du relevé de progression incompatible")
            numbers = set()
            for raw in reader:
                if None in raw or any(v is None for v in raw.values()):
                    raise ValueError("Ligne de progression incomplète")
                number = raw["Numéro étudiant"]
                if not number or number in numbers:
                    raise ValueError("Numéro étudiant absent ou dupliqué")
                numbers.add(number)
                details = []
                done = {"TD": 0, "DM": 0, "Contrôle": 0}
                total_attempts = 0
                for item in evaluations:
                    slug = item["id"]
                    try:
                        count = int(raw[f"{slug}__essais"])
                    except (TypeError, ValueError) as exc:
                        raise ValueError("Nombre d'essais invalide") from exc
                    if count < 0:
                        raise ValueError("Nombre d'essais négatif")
                    minimum = raw[f"{slug}__min"]
                    maximum = raw[f"{slug}__max"]
                    if count == 0 and (minimum or maximum):
                        raise ValueError("Score sans essai dans le relevé")
                    if count and (not minimum or not maximum):
                        raise ValueError("Score manquant pour un essai")
                    total_attempts += count
                    if count:
                        done[item["type"]] += 1
                    details.append({
                        **item, "attempts": count,
                        "min": minimum, "max": maximum,
                    })
                students.append({
                    "number": number,
                    "last_name": raw["Nom"],
                    "first_name": raw["Prénom"],
                    "details": details,
                    "done": done,
                    "attempts": total_attempts,
                })
    students.sort(key=lambda student: (
        student["last_name"].casefold(),
        student["first_name"].casefold(), student["number"],
    ))
    totals = {kind: sum(item["type"] == kind for item in evaluations)
              for kind in ("TD", "DM", "Contrôle")}
    updated = (datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
               .strftime("%d/%m/%Y à %H:%M UTC") if path.is_file() else "")
    return {
        "semester": semester, "students": students,
        "evaluations": evaluations,
        "totals": totals, "updated": updated,
        "exists": path.is_file(),
    }


def student_sheet(semester, number):
    if not isinstance(number, str) or not number or len(number) > 64:
        return None
    listing = cohort(semester)
    found = next(
        (student for student in listing["students"]
         if student["number"] == number), None
    )
    return (listing, found) if found else None


def csv_export(semester):
    """Octets du CSV existant, réservés à une route authentifiée."""
    path = _source(semester)
    if not path.is_file():
        return None
    # Garantir que le relevé exporté correspond exactement au catalogue.
    cohort(semester)
    return path.read_bytes()
