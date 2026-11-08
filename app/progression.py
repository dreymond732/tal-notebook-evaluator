"""Consolidation privée des soumissions TAL, sans réécrire les journaux sources.

Chaque ligne valide du CSV constitue un essai. Les noms seuls ne sont jamais
utilisés comme identifiant, sauf après validation explicite d'une correspondance.
Le verrou interprocessus est partagé avec l'écriture des nouvelles soumissions.
"""
from __future__ import annotations

import argparse
import csv
import fcntl
import os
import re
import tempfile
import unicodedata
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

import outils
from notebook_contract import CONTRACT_VERSIONS, load_catalog
from storage_layout import GRADE_COLUMNS, storage_id

SEMESTERS = ("S1", "S2", "S3")
# Les synthèses TD3–TD6 sont des travaux réellement réalisés : elles restent
# des évaluations distinctes de leurs approfondissements one/bis/ter.
# Seul l'ancien contrôle S1 sans journal exploitable est exclu du suivi.
HISTORICAL = frozenset({"Controletilt-s1"})
IDENTITY_HEADER = ("Nom", "Prénom", "Classe", "Numéro étudiant")
ANOMALY_HEADER = ("Source", "Ligne", "Motif", "Détail")
NUMBER_RE = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")


def _key(*parts):
    return tuple(" ".join(unicodedata.normalize("NFKC", str(p)).split()).casefold()
                 for p in parts)


def _safe(value):
    value = str(value)
    return "'" + value if value.lstrip().startswith(("=", "+", "-", "@")) else value


def _score(value):
    try:
        result = Decimal(str(value).strip().replace(",", "."))
        return result if result.is_finite() and result >= 0 else None
    except InvalidOperation:
        return None


def _date(value):
    try:
        return datetime.strptime(value.strip(), "%d/%m/%Y %H:%M")
    except (ValueError, AttributeError):
        return None


def _academic_start(value):
    if not value:
        return None
    match = re.fullmatch(r"(\d{4})-(\d{4})", value)
    if not match or int(match.group(2)) != int(match.group(1)) + 1:
        raise ValueError("TAL_ACADEMIC_YEAR attendu sous la forme 2026-2027")
    return int(match.group(1))


@contextmanager
def progression_lock(root=None):
    """Verrou Linux sur le volume persistant, partagé entre workers Flask."""
    directory = Path(root if root is not None else outils.BASE_DIR) / "suivi"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(directory, 0o700)
    fd = os.open(directory / ".consolidation.lock", os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _write_csv(path, header, rows):
    """Remplacement atomique d'un seul export, jamais d'un journal source."""
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                         dir=path.parent, prefix=".suivi-",
                                         delete=False) as stream:
            tmp = Path(stream.name)
            writer = csv.writer(stream, delimiter=";", lineterminator="\n")
            writer.writerow(header)
            writer.writerows([_safe(v) for v in row] for row in rows)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)


def _load_mapping(path, errors):
    """Seule la table explicitement validée peut attribuer un numéro manquant."""
    mapping = {}
    if not path.exists():
        return mapping
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter=";")
            if not reader.fieldnames or not set(IDENTITY_HEADER) <= set(reader.fieldnames):
                errors.append((path.name, "", "correspondances_invalides", "En-têtes attendus absents"))
                return {}
            for line, item in enumerate(reader, 2):
                if None in item or any(item.get(k) is None for k in IDENTITY_HEADER):
                    errors.append((path.name, line, "correspondance_incomplete", "Nombre de colonnes incorrect"))
                    continue
                number = item["Numéro étudiant"].strip()
                key = _key(*(item[k] for k in IDENTITY_HEADER[:3]))
                if not all(key) or not NUMBER_RE.fullmatch(number):
                    errors.append((path.name, line, "correspondance_invalide", "Identité ou numéro incorrect"))
                    continue
                if key in mapping and mapping[key] != number:
                    errors.append((path.name, line, "correspondance_conflictuelle",
                                   "Deux numéros pour le même nom, prénom et classe"))
                    mapping[key] = None
                elif key not in mapping:
                    mapping[key] = number
    except (OSError, UnicodeError, csv.Error) as exc:
        errors.append((path.name, "", "correspondances_illisibles", type(exc).__name__))
    return mapping


def _catalog():
    entries = []
    for item in load_catalog():
        evaluator = item.get("evaluator")
        if not item["active"] or not evaluator or evaluator in HISTORICAL:
            continue
        version = CONTRACT_VERSIONS.get(evaluator)
        if version is not None and version != item["version"]:
            raise ValueError("Contrat incohérent : " + evaluator)
        storage = storage_id(evaluator)
        kind = ("DM" if evaluator.startswith("dm-") or "DevoirMaison" in evaluator
                else "Contrôle" if item["mode"] == "controle" else "TD")
        entries.append(dict(item, storage=storage, kind=kind))
    return entries


def _read_records(root, entries, first_year, errors):
    """Consomme exclusivement les journaux fusionnés à schéma stable."""
    records = []
    for item in entries:
        path = root / item["storage"] / ("notes_" + item["storage"] + ".csv")
        if not path.exists():
            continue
        try:
            with path.open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream, delimiter=";")
                fields = reader.fieldnames or []
                if fields != list(GRADE_COLUMNS):
                    errors.append((str(path.relative_to(root)), "", "schema_invalide",
                                   "Lancer la migration pour obtenir le schéma canonique"))
                    continue
                for line, row in enumerate(reader, 2):
                    origin = str(path.relative_to(root))
                    if None in row or any(v is None for v in row.values()):
                        errors.append((origin, line, "ligne_invalide", "Nombre de colonnes incorrect"))
                        continue
                    version = row.get("Version du contrat", "").strip()
                    if version != str(item["version"]):
                        # Les essais des précédents contrats sont archivés dans
                        # le même journal mais exclus du suivi courant.
                        if not version.isdecimal():
                            errors.append((origin, line, "version_invalide", "Contrat non identifié"))
                        continue
                    value = _score(row.get("Score", ""))
                    if value is None:
                        errors.append((origin, line, "score_invalide", "Valeur absente ou non numérique"))
                        continue
                    date = _date(row.get("Date", ""))
                    if date is None:
                        errors.append((origin, line, "date_invalide", "Date illisible"))
                        if first_year is not None:
                            continue
                    elif first_year is not None and not (
                        datetime(first_year, 9, 1) <= date < datetime(first_year + 1, 9, 1)
                    ):
                        continue
                    identity = tuple((row.get(k) or "").strip() for k in IDENTITY_HEADER[:3])
                    if not all(identity):
                        errors.append((origin, line, "identite_incomplete", "Nom, prénom ou classe manquant"))
                        continue
                    number = (row.get("Numéro étudiant") or "").strip()
                    if number and not NUMBER_RE.fullmatch(number):
                        errors.append((origin, line, "numero_invalide", "Numéro étudiant mal formé"))
                        continue
                    nature = row.get("Nature du score", "").strip()
                    if nature not in {"note", "technique_provisoire"}:
                        errors.append((origin, line, "nature_invalide", "Nature de score inconnue"))
                        continue
                    records.append({
                        "item": item, "number": number, "identity": identity,
                        "date": date, "score": value,
                        "nature": "Score technique provisoire" if nature == "technique_provisoire" else "Note",
                        "source": origin, "line": line
                    })
        except (OSError, UnicodeError, csv.Error) as exc:
            errors.append((str(path.relative_to(root)), "", "lecture_impossible", type(exc).__name__))
    return records


def _format(value):
    return f"{value:.2f}".replace(".", ",")


def refresh_progression(root=None, academic_year=None):
    """Régénère S1/S2/S3 à partir des CSV, sous verrou progression_lock.

    Peut aussi être appelé seul en ligne de commande via le verrou. Aucune
    requête réseau, aucune exécution de cahier, aucun changement de barème.
    """
    root = Path(root if root is not None else outils.BASE_DIR)
    output = root / "suivi"
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(output, 0o700)
    if academic_year is None:
        academic_year = os.getenv("TAL_ACADEMIC_YEAR", "").strip()
    first_year = _academic_start(academic_year)
    errors = []
    entries = _catalog()
    mapping = _load_mapping(output / "correspondances_validees.csv", errors)
    records = _read_records(root, entries, first_year, errors)

    # Correspondance suggérée : seulement une identité exacte, avec même classe
    # et un numéro unique déjà observé. Elle n'est jamais appliquée d'office.
    known = defaultdict(set)
    for record in records:
        if record["number"]:
            known[_key(*record["identity"])].add(record["number"])

    unassigned = defaultdict(list)
    assigned = []
    for record in records:
        if not record["number"]:
            key = _key(*record["identity"])
            record["number"] = mapping.get(key) or ""
        if record["number"]:
            assigned.append(record)
        else:
            unassigned[_key(*record["identity"])].append(record)

    suggestions = []
    for key, group in sorted(unassigned.items()):
        candidates = known.get(key, set())
        candidate = next(iter(candidates)) if len(candidates) == 1 else ""
        reasons = sorted({r["item"]["evaluator"] for r in group})
        suggestions.append((*group[0]["identity"], candidate, len(group),
                            ", ".join(reasons),
                            "Candidat à valider" if candidate else "Ambigu" if candidates else "Sans candidat"))
        errors.append((";".join(reasons), "", "identite_non_resolue",
                       "Correspondance à valider dans correspondances_validees.csv"))

    grouped = {}
    names = defaultdict(list)
    natures = {}
    for record in assigned:
        evaluator = record["item"]["evaluator"]
        if evaluator in natures and natures[evaluator] != record["nature"]:
            errors.append((record["source"], record["line"], "nature_incompatible",
                           "Note et score technique ne doivent pas être mélangés"))
            continue
        natures[evaluator] = record["nature"]
        number = record["number"]
        names[number].append((record["date"] or datetime.min, record["identity"]))
        key = (record["item"]["semester"], evaluator, number)
        state = grouped.setdefault(key, [record["score"], record["score"], 0])
        state[0] = min(state[0], record["score"])
        state[1] = max(state[1], record["score"])
        state[2] += 1

    students = {}
    for number, observations in names.items():
        observations.sort(key=lambda p: p[0])
        names_seen = {_key(identity[0], identity[1]) for _, identity in observations}
        if len(names_seen) > 1:
            errors.append(("identite", "", "identite_contradictoire",
                           "Plusieurs noms/prénoms pour un même numéro étudiant : " + number))
        students[number] = observations[-1][1]

    for semester in SEMESTERS:
        semester_entries = [i for i in entries if i["semester"] == semester]
        semester_numbers = sorted(
            {number for sem, ev, number in grouped if sem == semester},
            key=lambda number: (_key(*students[number][:2]), number),
        )
        header = ["Numéro étudiant", "Nom", "Prénom"]
        for item in semester_entries:
            name = item["evaluator"]
            header += [name + "__min", name + "__max", name + "__essais"]
        rows = []
        for number in semester_numbers:
            identity = students[number]
            row = [number, identity[0], identity[1]]
            for item in semester_entries:
                state = grouped.get((semester, item["evaluator"], number))
                row += ([_format(state[0]), _format(state[1]), state[2]]
                        if state else ["", "", 0])
            rows.append(row)
        _write_csv(output / ("progression_" + semester + ".csv"), header, rows)

    _write_csv(output / "catalogue_evaluations.csv",
               ("Semestre", "Évaluation", "Intitulé", "Type", "Nature du score", "Version"),
               ((i["semester"], i["evaluator"], i.get("title", i["evaluator"]), i["kind"],
                 natures.get(i["evaluator"], "non_observee"), i["version"]) for i in entries))
    _write_csv(output / "correspondances_a_valider.csv",
               (*IDENTITY_HEADER[:3], "Numéro proposé", "Essais", "Évaluations", "Statut"),
               suggestions)
    _write_csv(output / "anomalies.csv", ANOMALY_HEADER, errors)
    return {"essais": len(assigned), "sans_numero": sum(map(len, unassigned.values())),
            "anomalies": len(errors), "etudiants": len(students)}


def main():
    parser = argparse.ArgumentParser(description="Consolidation privée des évaluations TAL")
    parser.add_argument("--root", default=outils.BASE_DIR)
    parser.add_argument("--annee", default=None, help="Année universitaire : 2026-2027")
    args = parser.parse_args()
    with progression_lock(args.root):
        result = refresh_progression(args.root, args.annee)
    print("Consolidation terminée :", result)


if __name__ == "__main__":
    main()
