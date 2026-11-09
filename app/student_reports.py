"""Sélection du dernier rapport de TD, uniquement après authentification.

Aucun chemin fourni par le navigateur. Le numéro provient de la session,
l'activité est restreinte au catalogue des TD actifs ; archives vérifiées
par correspondance exacte avec le reçu direct du CSV de notes.
"""
from __future__ import annotations

import csv
import os
import re
from datetime import datetime
from pathlib import Path

import outils
from progression import _academic_start, _catalog, _date
from storage_layout import storage_id

RECEIPT = re.compile(r"direct:([0-9a-f]{32})\Z")


def enabled():
    # Activation volontaire, APRES vérification administrative du rattachement
    # numéro étudiant / email. La procédure first-claim n'est pas une
    # authentification institutionnelle.
    return os.getenv("TAL_STUDENT_REPORTS_ENABLED", "0") == "1"


def _entry(evaluator):
    return next((item for item in _catalog()
                 if item["evaluator"] == evaluator and item["mode"] == "td"), None)


def latest_td_report(number, evaluator):
    """Dernier rapport réellement archivé du TD, sans traversée de répertoire."""
    if not enabled():
        return None
    entry = _entry(evaluator)
    if entry is None:
        return None
    year = _academic_start(os.environ.get("TAL_ACADEMIC_YEAR",""))
    if year is None:
        return None
    folder = Path(outils.BASE_DIR) / entry["storage"]
    csv_path = folder / ("notes_" + entry["storage"] + ".csv")
    if not csv_path.is_file() or csv_path.is_symlink():
        return None
    latest = None
    with csv_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream,delimiter=";")
        for index,row in enumerate(reader):
            if row.get("Numéro étudiant") != number:
                continue
            if str(row.get("Version du contrat","")).strip() != str(entry["version"]):
                continue
            date = _date(row.get("Date",""))
            if date is None or not datetime(year,9,1) <= date < datetime(year+1,9,1):
                continue
            match = RECEIPT.fullmatch(row.get("Origine",""))
            if match and (latest is None or (date,index)>latest[0]):
                latest = ((date,index),match[1])
    if latest is None:
        return None
    report_dir = folder / "rapport"
    if report_dir.is_symlink() or not report_dir.is_dir():
        return None
    items = list(report_dir.glob("*_" + latest[1] + "_" + evaluator + ".html"))
    if len(items) != 1 or not items[0].is_file() or items[0].is_symlink():
        return None
    file = items[0]
    if file.stat().st_size > 2_500_000:
        return None
    return file
