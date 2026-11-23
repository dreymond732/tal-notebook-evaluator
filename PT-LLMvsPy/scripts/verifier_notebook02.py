#!/usr/bin/env python3
"""Exécute le 02 sur Faguet puis ses deux cahiers utilisateurs dans des sessions distinctes."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from tal_toolkit import charger_corpus, preparer_faguet_standard_td01

PROJET = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).resolve()
CAHIERS = ("02_mesures_lexicales", "03_relations_lexicales", "04_audit_llm")


def executer_cahier(chemin: Path) -> None:
    cahier = json.loads(chemin.read_text(encoding="utf-8"))
    session = {"__name__": "__main__", "display": print}
    for cellule in cahier["cells"]:
        if cellule["cell_type"] == "code":
            source = "".join(cellule["source"])
            exec(compile(source, f"{chemin.name}/{cellule['id']}", "exec"), session)


def verifier_parcours() -> None:
    original = PROJET.parent / "Notebooks TD/S3/ressources/faguet_source.txt"
    _, epure, _ = preparer_faguet_standard_td01(charger_corpus(original))
    with TemporaryDirectory() as temporaire:
        dossier = Path(temporaire) / "PT-Faguet"
        dossier.mkdir()
        (dossier / "faguet_nettoye.txt").write_text(epure.texte, encoding="utf-8")
        for nom in CAHIERS:
            chemin = PROJET / "notebooks" / f"{nom}.ipynb"
            subprocess.run([sys.executable, str(SCRIPT), str(chemin)], cwd=temporaire, check=True)
            print(f"{chemin.name} exécuté", flush=True)
        dossier_audit = json.loads((dossier / "resultats_04.json").read_text(encoding="utf-8"))
        passages = dossier_audit["protocole_B"]["relation_03"]["passages"]
        assert passages, "Le couple par défaut doit fournir des passages à relire."
        for passage in passages:
            assert epure.texte[passage["debut"]:passage["fin"]] == passage["texte"]


if __name__ == "__main__":
    if len(sys.argv) == 2:
        executer_cahier(Path(sys.argv[1]))
    else:
        verifier_parcours()
