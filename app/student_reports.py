"""Sélection sûre du dernier rapport TD, par numéro étudiant et reçu journalisé.

Ni nom de fichier ni chemin ne sont acceptés depuis une URL publique.
Une session étudiante doit être vérifiée dans student_routes avant lecture.
Les rapports de contrôles et rapports enseignants DM ne sont jamais exposés.
"""
from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path

import outils
from progression import _catalog, _academic_start, _date
from storage_layout import GRADE_COLUMNS

RECEIPT = re.compile(r"direct:([0-9a-f]{32})\Z")


def latest_td_report(number, evaluator):
    entry = next((x for x in _catalog() if x["evaluator"] == evaluator
                  and x["kind"] == "TD"), None)
    if entry is None or not number:
        return None
    root = Path(outils.BASE_DIR) / entry["storage"]
    source = root / ("notes_" + entry["storage"] + ".csv")
    if not source.is_file():
        return None
    first_year = _academic_start(__import__("os").getenv("TAL_ACADEMIC_YEAR", ""))
    rows = []
    with source.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter=";")
        if reader.fieldnames != list(GRADE_COLUMNS):
            return None
        for line, row in enumerate(reader, 2):
            if row.get("Numéro étudiant", "").strip() != number:
                continue
            if row.get("Version du contrat") != str(entry["version"]):
                continue
            match = RECEIPT.fullmatch(row.get("Origine", ""))
            if not match:
                continue
            date = _date(row.get("Date", ""))
            if date is None:
                continue
            if first_year is not None and not (
                datetime(first_year, 9, 1) <= date < datetime(first_year + 1, 9, 1)
            ):
                continue
            rows.append((date, line, match[1]))
    if not rows:
        return None
    receipt = max(rows)[2]
    reports = root / "rapport"
    if not reports.is_dir():
        return None
    # Le reçu est tiré du journal du même numéro, jamais de la requête.
    matches = [p for p in reports.iterdir()
               if p.is_file() and not p.is_symlink()
               and p.suffix == ".html" and ("_" + receipt + "_") in p.name]
    return matches[0] if len(matches) == 1 else None
