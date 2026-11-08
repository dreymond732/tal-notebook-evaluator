"""Audite les 34 TD du catalogue TAL et leur intégration aux relevés S1/S2/S3.

Option --toutes-evaluations : inclure les DM et contrôles (45 évaluations).
Lecture seule, jamais d'identité ou de score personnel dans la sortie.
Le script ne régénère pas les CSV ; il compare la source au suivi existant.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from collections import Counter
from contextlib import contextmanager
from pathlib import Path

import outils
from diagnostic_progression import diagnostic
from progression import _catalog, _academic_start, SEMESTERS

SEVERE = ("schema_invalide", "journal_illisible", "colonnes_incorrectes",
          "numero_invalide", "score_invalide", "date_illisible",
          "nature_invalide", "nature_incompatible")


@contextmanager
def read_only_snapshot(root):
    """Verrou partagé sur un verrou existant, sans créer ni modifier de fichier."""
    lock = root / "suivi" / ".consolidation.lock"
    if lock.is_file() and not lock.is_symlink():
        with lock.open("rb") as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_SH)
            try:
                yield
            finally:
                fcntl.flock(file.fileno(), fcntl.LOCK_UN)
    else:
        yield


def audit(root=None, academic_year=None, semester=None, all_evaluations=False):
    root = Path(root if root is not None else outils.BASE_DIR)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Volume soumissions introuvable ou invalide")
    if academic_year is None:
        academic_year = os.getenv("TAL_ACADEMIC_YEAR", "").strip()
    _academic_start(academic_year)  # Valide la période sans modifier les données.
    if semester is not None and semester not in SEMESTERS:
        raise ValueError("Semestre inconnu")
    entries = [e for e in _catalog()
               if (semester is None or e["semester"] == semester)
               and (all_evaluations or e["kind"] == "TD")]

    rows = []
    with read_only_snapshot(root):
        for entry in entries:
            evaluator = entry["evaluator"]
            try:
                d = diagnostic(evaluator, root=root, academic_year=academic_year)
            except (OSError, UnicodeError, ValueError) as exc:
                # Ne pas afficher un message d'exception potentiellement nominatif.
                rows.append({
                    "semestre": entry["semester"], "type": entry["kind"],
                    "evaluation": evaluator, "dossier": entry["storage"],
                    "statut": "ECART", "erreur": type(exc).__name__,
                })
                continue

            problems = d["lignes_non_retenues"]
            missing = d["essais_du_suivi"]
            issues = {}
            if d["journal_present"] and any(problems.get(k) for k in SEVERE):
                issues["lignes_invalides"] = sum(problems.get(k, 0) for k in SEVERE)
            if d["journal_present"] and problems.get("contrat_ancien_ou_different"):
                issues["versions_anterieures"] = problems["contrat_ancien_ou_different"]
            if d["journal_present"] and problems.get("hors_annee"):
                issues["hors_annee"] = problems["hors_annee"]
            if d["journal_present"] and problems.get("sans_numero"):
                issues["sans_numero"] = problems["sans_numero"]

            if not d["journal_present"] and (d["fichiers_nb"] or d["fichiers_rapport"]):
                issues["archives_sans_journal"] = 1
            if not d["journal_present"] and d["ancien_dossier_present"]:
                issues["ancien_dossier_sans_journal_canonique"] = 1
            if d["erreurs_correspondances"]:
                issues["correspondances_invalides"] = d["erreurs_correspondances"]

            if isinstance(missing, str):
                issues["colonne_suivi_absente"] = 1
            if missing is None:
                issues["suivi_absent"] = 1
            if type(d["ecarts_individuels"]) is int and d["ecarts_individuels"] > 0:
                issues["divergences_par_etudiant"] = d["ecarts_individuels"]

            if any(key in issues for key in (
                "archives_sans_journal", "ancien_dossier_sans_journal_canonique",
                "colonne_suivi_absente", "suivi_absent", "divergences_par_etudiant",
                "correspondances_invalides",
            )):
                status = "ECART"
            elif issues:
                status = "A_VERIFIER"
            elif d["journal_present"]:
                status = "OK"
            else:
                status = "SANS_DEPOT"

            rows.append({
                "semestre": entry["semester"],
                "type": entry["kind"],
                "evaluation": evaluator,
                "dossier": d["dossier"],
                "statut": status,
                "journal": d["journal_present"],
                "nb": d["fichiers_nb"],
                "rapports": d["fichiers_rapport"],
                "lignes_csv": d["lignes_csv"],
                "essais_eligibles": d["essais_valides_identifies"],
                "etudiants_eligibles": d["etudiants_distincts_csv"],
                "essais_suivi": d["essais_du_suivi"],
                "etudiants_suivi": d["etudiants_distincts_suivi"],
                "versions": d["versions_presentes"],
                "motifs": dict(sorted(issues.items())),
            })
    return {
        "annee": academic_year or "non_filtree",
        "perimetre": "toutes" if all_evaluations else "TD",
        "evaluations": len(rows),
        "semestres": dict(sorted(Counter(x["semestre"] for x in rows).items())),
        "statuts": dict(sorted(Counter(x["statut"] for x in rows).items())),
        "resultats": rows,
    }


def format_report(report):
    output = [
        f"Audit TAL {report['annee']} : {report['evaluations']} évaluations "
        f"({report['perimetre']}; "
        + ", ".join(f"{k}={v}" for k, v in report["semestres"].items()) + ")",
        "Sem Évaluation             Dossier                CSV  NB Rap Essais(CSV/suivi) Étudiants(CSV/suivi) Statut",
        "-" * 111,
    ]
    for row in report["resultats"]:
        if "erreur" in row:
            output.append(
                f"{row['semestre']:3} {row['evaluation']:22} {row['dossier']:22} "
                f"ERREUR({row['erreur']})"
            )
            continue
        output.append(
            f"{row['semestre']:3} {row['evaluation']:22} {row['dossier']:22} "
            f"{row['lignes_csv']:3}  {row['nb']:2} {row['rapports']:3} "
            f"{row['essais_eligibles']:5}/{str(row['essais_suivi']):<5}  "
            f"{row['etudiants_eligibles']:5}/{row['etudiants_suivi']:<5}  "
            f"{row['statut']}"
        )
        if row["motifs"]:
            output.append("    " + ", ".join(
                f"{key}={value}" for key, value in row["motifs"].items()
            ))
    output.append("Statuts : " + ", ".join(
        f"{key}={value}" for key, value in report["statuts"].items()))
    output.append(
        "Aucun nom, numéro étudiant ou score individuel n'est affiché. "
        "Le nombre de copies et de rapports n'est pas le nombre d'essais."
    )
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=outils.BASE_DIR)
    parser.add_argument("--annee", default=None)
    parser.add_argument("--semestre", choices=SEMESTERS)
    parser.add_argument("--toutes-evaluations", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit(args.root, args.annee, args.semestre, args.toutes_evaluations)
    print(json.dumps(report, ensure_ascii=False, indent=2)
          if args.json else format_report(report))
    if report["statuts"].get("ECART"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
