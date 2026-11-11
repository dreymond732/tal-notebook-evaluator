#!/usr/bin/env python3
"""Synthèse des archives Faguet déposées sur Drive.

À utiliser depuis un clone autorisé du dépôt ou un poste de l'enseignant :
    python scripts/collecter_td01.py /chemin/vers/depots --sortie bilan_td01.csv

Ne dépend pas d'une API Drive : le dossier peut être synchronisé ou téléchargé.
Ne décompresse jamais les ZIP sur disque, ne modifie aucun travail étudiant.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
import sys
import zipfile

from tal_toolkit.soumission_td01 import verifier_archive_td01


SHA_FAGUET = "c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa"


def collecter(dossier: Path) -> tuple[list[dict], list[dict]]:
    import json
    valides: list[dict] = []
    anomalies: list[dict] = []
    archives = sorted(set(dossier.glob("TD01_*.zip"))
                      | set(dossier.glob("FAGUET_*.zip")))
    for archive in archives:
        try:
            manifeste = verifier_archive_td01(archive)
            if manifeste["sha256_source"] != SHA_FAGUET:
                raise ValueError("Empreinte différente du corpus Faguet figé")
            with zipfile.ZipFile(archive, "r") as z:
                comparaisons = list(csv.DictReader(
                    z.read("comparaison_metriques.csv").decode("utf-8").splitlines()
                ))
                if "inspection.json" in z.namelist():
                    from tal_toolkit.inspection_td01 import valider_inspection
                    inspection = json.loads(z.read("inspection.json"))
                    valider_inspection(inspection)
                    tests = inspection["anomalies"]
                    type_suivi = "inspection"
                else:
                    tests = json.loads(z.read("tests_personnels.json"))
                    if len(tests) < 2:
                        raise ValueError("Tests personnels incomplets")
                    type_suivi = "tests_anterieurs"
            valeurs = {x["id"]: x for x in comparaisons}
            if len(valeurs) != 7:
                raise ValueError("Comparaison lexicale incomplète")
            ligne = {
                "fichier": archive.name,
                "identifiant": manifeste["identifiant"],
                "date_utc": manifeste["utc"],
                "version_bibliotheque": manifeste["version_bibliotheque"],
                "sha256_source": manifeste["sha256_source"],
                "sha256_epure": manifeste["sha256_epure"],
                "nombre_tests": len(tests),
                "type_suivi": type_suivi,
                "mode_revision": manifeste.get("mode_revision", "reference"),
                "revision_git": manifeste.get("revision_git", ""),
                "version_notebook": manifeste.get("version_notebook", ""),
            }
            for cle in ("tokens", "types", "hapax", "ttr",
                        "hapax_types_pourcent", "phrases", "mots_par_phrase"):
                for colonne, suffixe in (
                    ("original", "_original"),
                    ("epure", "_epure"),
                    ("ecart", "_ecart"),
                ):
                    ligne[cle + suffixe] = valeurs[cle][colonne]
            valides.append(ligne)
        except (ValueError, KeyError, UnicodeDecodeError, zipfile.BadZipFile,
                OSError, TypeError) as exc:
            anomalies.append({"fichier": archive.name,
                              "erreur": f"{type(exc).__name__}: {exc}"})
    derniere_par_login: dict[str, dict] = {}
    for ligne in valides:
        identifiant = ligne["identifiant"]
        if (identifiant not in derniere_par_login
                or ligne["date_utc"] > derniere_par_login[identifiant]["date_utc"]):
            derniere_par_login[identifiant] = ligne
    for ligne in valides:
        ligne["derniere_soumission"] = (
            ligne is derniere_par_login[ligne["identifiant"]]
        )
    return valides, anomalies


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dossier", type=Path)
    parser.add_argument("--sortie", type=Path, default=Path("bilan_td01.csv"))
    args = parser.parse_args()
    if not args.dossier.is_dir():
        parser.error("Dossier de dépôts inaccessible")
    valides, anomalies = collecter(args.dossier)
    if valides:
        args.sortie.parent.mkdir(parents=True, exist_ok=True)
        with args.sortie.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(valides[0]))
            w.writeheader()
            w.writerows(valides)
    import json
    path_anomalies = args.sortie.with_suffix(".anomalies.json")
    path_anomalies.write_text(
        json.dumps(anomalies, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{len(valides)} archives valides, {len(anomalies)} anomalies.")
    print(f"Tableau : {args.sortie if valides else 'Aucun tableau (zéro archive valide)'}")
    print(f"Anomalies : {path_anomalies}")
    return 0 if not anomalies else 1


if __name__ == "__main__":
    sys.exit(main())
