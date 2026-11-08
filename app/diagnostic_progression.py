"""Diagnostic en lecture seule d'un journal d'évaluation TAL.

N'affiche aucun numéro, nom ou score personnel. Ne déduit pas le nombre
d'essais du nombre de fichiers nb/ ou rapport/ et ne réécrit aucun export.
"""
import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

import outils
from progression import (
    _catalog, _academic_start, _date, _score, NUMBER_RE, IDENTITY_HEADER,
)
from storage_layout import GRADE_COLUMNS


def diagnostic(evaluator="td4-s1", root=None, academic_year="2026-2027"):
    root = Path(root if root is not None else outils.BASE_DIR)
    entry = next((item for item in _catalog()
                  if item["evaluator"] == evaluator), None)
    if entry is None:
        raise ValueError("Évaluateur absent du catalogue de progression : " + evaluator)
    year = _academic_start(academic_year)
    storage = entry["storage"]
    base = root / storage
    journal = base / ("notes_" + storage + ".csv")
    counters = Counter()
    numbers = set()
    natures = set()
    if journal.exists():
        with journal.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            if reader.fieldnames != list(GRADE_COLUMNS):
                raise ValueError("En-tête non canonique : " + str(journal))
            for row in reader:
                counters["lignes_csv"] += 1
                if None in row or any(value is None for value in row.values()):
                    counters["colonnes_incorrectes"] += 1
                    continue
                if row["Version du contrat"].strip() != str(entry["version"]):
                    counters["contrat_ancien_ou_different"] += 1
                    continue
                if _score(row["Score"]) is None:
                    counters["score_invalide"] += 1
                    continue
                date = _date(row["Date"])
                if date is None:
                    counters["date_illisible"] += 1
                    continue
                if year is not None and not (
                    datetime(year, 9, 1) <= date < datetime(year + 1, 9, 1)
                ):
                    counters["hors_annee"] += 1
                    continue
                if not all((row[k] or "").strip() for k in IDENTITY_HEADER[:3]):
                    counters["identite_incomplete"] += 1
                    continue
                number = row["Numéro étudiant"].strip()
                if number and not NUMBER_RE.fullmatch(number):
                    counters["numero_invalide"] += 1
                    continue
                if row["Nature du score"] not in {"note", "technique_provisoire"}:
                    counters["nature_invalide"] += 1
                    continue
                natures.add(row["Nature du score"])
                if not number:
                    counters["sans_numero"] += 1
                    continue
                counters["essais_valides_identifies"] += 1
                numbers.add(number)

    progression_file = root / "suivi" / ("progression_" + entry["semester"] + ".csv")
    counted = None
    progress_numbers = set()
    if progression_file.exists():
        with progression_file.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter=";")
            column = evaluator + "__essais"
            if column not in (reader.fieldnames or []):
                counted = "COLONNE_ABSENTE"
            else:
                counted = 0
                for record in reader:
                    try:
                        value = int(record.get(column) or 0)
                    except (TypeError, ValueError) as exc:
                        raise ValueError("Nombre d'essais illisible dans le suivi") from exc
                    counted += value
                    if value:
                        progress_numbers.add(record.get("Numéro étudiant", ""))

    def artifact_count(folder, extension):
        path = base / folder
        return sum(1 for file in path.iterdir()
                   if file.is_file() and file.suffix.lower() == extension) if path.is_dir() else 0

    return {
        "evaluation": evaluator, "dossier": storage,
        "journal_present": journal.is_file(),
        "annee": academic_year,
        "fichiers_nb": artifact_count("nb", ".ipynb"),
        "fichiers_rapport": artifact_count("rapport", ".html"),
        "lignes_csv": counters["lignes_csv"],
        "essais_valides_identifies": counters["essais_valides_identifies"],
        "etudiants_distincts_csv": len(numbers),
        "essais_du_suivi": counted,
        "etudiants_distincts_suivi": len(progress_numbers),
        "natures_observees": sorted(natures),
        "lignes_non_retenues": {
            key: value for key, value in sorted(counters.items())
            if key not in {"lignes_csv", "essais_valides_identifies"} and value
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evaluation", default="td4-s1")
    parser.add_argument("--root", default=outils.BASE_DIR)
    parser.add_argument("--annee", default="2026-2027")
    args = parser.parse_args()
    print(json.dumps(
        diagnostic(args.evaluation, args.root, args.annee),
        ensure_ascii=False, indent=2,
    ))


if __name__ == "__main__":
    main()
