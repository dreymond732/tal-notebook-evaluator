"""Vues privées de suivi de promotion, à partir des exports existants.

Ne lit ni les cahiers ni les rapports des étudiants, et ne modifie jamais
les données sources. Le tableau enseignant inclut les TD, DM et contrôles,
contrairement au portail public des étudiants.
"""
from __future__ import annotations

import csv
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import outils
from progression import (SEMESTERS, _catalog, _academic_start, _date, _key,
                         _load_mapping, _score, NUMBER_RE)
from routes import EVALUATORS
from storage_layout import GRADE_COLUMNS

CSV_HEADER = ("Numéro étudiant", "Nom", "Prénom")
CATEGORIES = ("TD", "Approfondissement", "Révision", "DM", "Contrôle")


def _type_for(entry):
    """Distinguer les TD principaux des variantes et révisions, sans changer le catalogue."""
    if entry["kind"] != "TD":
        return entry["kind"]
    evaluator = entry["evaluator"]
    if entry["semester"] == "S1" and re.fullmatch(r"td[3-6]-(one|bis|ter)-s1", evaluator):
        return "Approfondissement"
    if entry["semester"] == "S3" and evaluator in {"td-r0-s3", "td-r1-s3", "td-r2-s3"}:
        return "Révision"
    return "TD"



def semester_entries(semester):
    if semester not in SEMESTERS:
        raise ValueError("Semestre inconnu")
    return [
        {
            "id": item["evaluator"],
            "label": EVALUATORS[item["evaluator"]][0],
            "type": _type_for(item),
            "semester": semester,
        }
        for item in _catalog() if item["semester"] == semester
    ]


def _source(semester):
    if semester not in SEMESTERS:
        raise ValueError("Semestre inconnu")
    return Path(outils.BASE_DIR) / "suivi" / f"progression_{semester}.csv"


def _older_versions(semester, evaluations):
    """Identifier les travaux des contrats anciens sans mélanger leurs notes.

    Le contrôle porte sur les lignes effectivement scorées de l'année courante.
    Les correspondances sans numéro sont appliquées UNIQUEMENT si déjà validées
    dans correspondances_validees.csv ; aucun rapprochement automatique.
    """
    root = Path(outils.BASE_DIR)
    year = _academic_start(os.getenv("TAL_ACADEMIC_YEAR", "").strip())
    mapping = _load_mapping(root / "suivi" / "correspondances_validees.csv", [])
    attempts = defaultdict(int)
    identities = {}
    for item in evaluations:
        evaluator = item["id"]
        entry = next(i for i in _catalog() if i["evaluator"] == evaluator)
        storage = entry["storage"]
        path = root / storage / ("notes_" + storage + ".csv")
        if not path.is_file():
            continue
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter=";")
            if reader.fieldnames != list(GRADE_COLUMNS):
                raise ValueError("Journal invalide pour la consultation des contrats anciens")
            for row in reader:
                if None in row or any(v is None for v in row.values()):
                    continue
                version = (row["Version du contrat"] or "").strip()
                if not version.isdecimal() or int(version) >= int(entry["version"]):
                    continue
                date = _date(row["Date"])
                if date is None or (year is not None and not (
                    datetime(year, 9, 1) <= date < datetime(year + 1, 9, 1)
                )):
                    continue
                if _score(row["Score"]) is None:
                    continue
                if row["Nature du score"] not in {"note", "technique_provisoire"}:
                    continue
                identity = tuple((row.get(k) or "").strip() for k in ("Nom", "Prénom", "Classe"))
                if not all(identity):
                    continue
                number = (row["Numéro étudiant"] or "").strip()
                if number and not NUMBER_RE.fullmatch(number):
                    continue
                if not number:
                    number = mapping.get(_key(*identity)) or ""
                if not number:
                    continue
                attempts[(number, evaluator)] += 1
                previous = identities.get(number)
                if previous is None or previous[0] < date:
                    identities[number] = (date, identity[:2])
    return attempts, identities


def cohort(semester):
    """Bilan de la promotion, y compris les dépôts scorés sous ancien contrat.

    Les anciens scores ne sont JAMAIS fusionnés avec les min/max du contrat
    actuel ; seuls leurs compteurs d'activité sont conservés séparément.
    """
    evaluations = semester_entries(semester)
    path = _source(semester)
    expected_header = list(CSV_HEADER)
    for item in evaluations:
        expected_header.extend(
            f"{item['id']}__{suffix}" for suffix in ("min", "max", "essais")
        )
    current = {}
    if path.is_file():
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter=";")
            if reader.fieldnames != expected_header:
                raise ValueError("Schéma du relevé de progression incompatible")
            for raw in reader:
                if None in raw or any(v is None for v in raw.values()):
                    raise ValueError("Ligne de progression incomplète")
                number = raw["Numéro étudiant"]
                if not number or number in current:
                    raise ValueError("Numéro étudiant absent ou dupliqué")
                current[number] = raw

    earlier, old_names = _older_versions(semester, evaluations)
    students = []
    all_numbers = set(current) | set(old_names)
    for number in all_numbers:
        raw = current.get(number)
        old_identity = old_names.get(number)
        if raw is not None:
            last_name, first_name = raw["Nom"], raw["Prénom"]
        else:
            last_name, first_name = old_identity[1]
        details = []
        done = dict.fromkeys(CATEGORIES, 0)
        from_old_only = dict.fromkeys(CATEGORIES, 0)
        attempts_total = 0
        for item in evaluations:
            slug = item["id"]
            try:
                count = int(raw[f"{slug}__essais"]) if raw else 0
            except (TypeError, ValueError) as exc:
                raise ValueError("Nombre d'essais invalide") from exc
            if count < 0:
                raise ValueError("Nombre d'essais négatif")
            minimum = raw[f"{slug}__min"] if raw else ""
            maximum = raw[f"{slug}__max"] if raw else ""
            if count == 0 and (minimum or maximum):
                raise ValueError("Score sans essai dans le relevé")
            if count and (not minimum or not maximum):
                raise ValueError("Score manquant pour un essai")
            older = earlier.get((number, slug), 0)
            attempts_total += count + older
            if count or older:
                done[item["type"]] += 1
            if older and count == 0:
                from_old_only[item["type"]] += 1
            details.append({
                **item,
                "attempts": count, "legacy_attempts": older,
                "min": minimum, "max": maximum,
            })
        students.append({
            "number": number, "last_name": last_name, "first_name": first_name,
            "details": details, "done": done, "older_only": from_old_only,
            "attempts": attempts_total,
            "legacy_attempts": sum(i["legacy_attempts"] for i in details),
        })
    students.sort(key=lambda student: (
        student["last_name"].casefold(),
        student["first_name"].casefold(), student["number"],
    ))
    totals = {kind: sum(item["type"] == kind for item in evaluations)
              for kind in CATEGORIES}
    evaluation_stats = []
    for entry in evaluations:
        observed = [
            row for student in students for row in student["details"]
            if row["id"] == entry["id"]
            and (row["attempts"] or row["legacy_attempts"])
        ]
        evaluation_stats.append({
            **entry, "students": len(observed),
            "attempts": sum(row["attempts"] for row in observed),
            "legacy_attempts": sum(row["legacy_attempts"] for row in observed),
        })
    updated = (datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
               .strftime("%d/%m/%Y à %H:%M UTC") if path.is_file() else "")
    return {
        "semester": semester, "students": students,
        "evaluations": evaluations,
        "totals": totals, "evaluation_stats": evaluation_stats,
        "updated": updated,
        "exists": path.is_file(),
        "historical_students": sum(s["legacy_attempts"] > 0 for s in students),
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
