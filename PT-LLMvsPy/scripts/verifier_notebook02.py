#!/usr/bin/env python3
"""Exécute les cahiers sur les fréquences, les cooccurrences et la vérification des affirmations sur Faguet dans des sessions distinctes."""
from __future__ import annotations

from hashlib import sha256
import json
import linecache
from pathlib import Path
from shutil import copy2
import subprocess
import sys
from tempfile import TemporaryDirectory

from tal_toolkit import charger_corpus, preparer_faguet_standard_td01

PROJET = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).resolve()
CAHIERS = (
    "02_comparer_les_frequences_des_formes_et_des_lemmes",
    "03_mesurer_les_cooccurrences_par_phrase_et_par_fenetre",
    "04_verifier_une_affirmation_par_le_calcul_et_la_lecture",
)
NUMERO_TEST = "00123456"


def executer_cellule(source: str, nom: str, contexte: dict) -> None:
    """Conserve le texte de la cellule pour inspect.getsource, comme dans IPython."""
    empreinte = sha256(source.encode("utf-8")).hexdigest()
    fichier = f"<{nom}-{empreinte}>"
    linecache.cache[fichier] = (len(source), None, source.splitlines(keepends=True), fichier)
    exec(compile(source, fichier, "exec"), contexte)


def executer_cahier(chemin: Path, numero_etudiant: str) -> None:
    cahier = json.loads(chemin.read_text(encoding="utf-8"))
    session = {"__name__": "__main__", "display": print}
    for cellule in cahier["cells"]:
        if cellule["cell_type"] == "code":
            source = "".join(cellule["source"])
            if cellule["id"] == "initialisation-pt":
                # Renseigner le champ de la copie, comme le ferait l’étudiant.
                champ = 'NUMERO_ETUDIANT = ""'
                assert source.count(champ) == 1
                source = source.replace(champ, f"NUMERO_ETUDIANT = {numero_etudiant!r}")
            executer_cellule(source, f"{chemin.name}/{cellule['id']}", session)


def verifier_parcours() -> None:
    original = PROJET.parent / "Notebooks TD/S3/ressources/faguet_source.txt"
    _, epure, _ = preparer_faguet_standard_td01(charger_corpus(original))
    with TemporaryDirectory() as temporaire:
        racine = Path(temporaire)
        personnel = racine / "S3-PythonVsLLM"
        personnel.mkdir()
        corpus_01 = personnel / f"faguet_nettoye_{NUMERO_TEST}.txt"
        corpus_01.write_bytes(epure.texte.encode("utf-8"))
        pieces = [corpus_01]

        for nom in CAHIERS:
            numero = nom[:2]
            seance = racine / f"session_{numero}"
            seance.mkdir()
            for piece in pieces:
                copy2(piece, seance / piece.name)
            chemin = PROJET / "notebooks" / f"{nom}.ipynb"
            subprocess.run(
                [sys.executable, str(SCRIPT), str(chemin), NUMERO_TEST],
                cwd=seance, check=True,
            )
            sortie = seance / f"resultats_{numero}_{NUMERO_TEST}.json"
            assert json.loads(sortie.read_text(encoding="utf-8"))["numero_etudiant"] == NUMERO_TEST
            # Rangement manuel simulé entre deux sessions indépendantes.
            sauvegarde = personnel / sortie.name
            copy2(sortie, sauvegarde)
            pieces.append(sauvegarde)
            print(f"{chemin.name} exécuté, {sortie.name} repris", flush=True)

        dossier_audit = json.loads(pieces[-1].read_text(encoding="utf-8"))
        resultat03 = json.loads(pieces[-2].read_text(encoding="utf-8"))
        principal = dossier_audit["studio"]["principal_03"]
        relation = dossier_audit["protocole_B"]["relation_03"]
        assert principal == resultat03["studio"]["principal"]
        assert relation == resultat03["relation"]
        assert principal["annonce"] == 208
        assert (relation["pivot"], relation["associe"]) == ("femme", "droit")
        for resultat in (principal, relation):
            assert len(resultat["passages"]) == 2, "Deux passages à relire sur Faguet intégral."
            for passage in resultat["passages"]:
                assert epure.texte[passage["debut"]:passage["fin"]] == passage["texte"]


if __name__ == "__main__":
    if len(sys.argv) == 3:
        executer_cahier(Path(sys.argv[1]), sys.argv[2])
    else:
        verifier_parcours()
