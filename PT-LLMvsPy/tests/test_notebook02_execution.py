"""Exécution de la chaîne du notebook 02 sur un corpus nettoyé simulé."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import secrets
import sys
import zipfile
from datetime import datetime, timezone
from urllib.request import urlopen

import pandas as pd
import spacy

from tal_toolkit import (
    charger_corpus, recenser_elements, OperationPretraitement,
    PlanPretraitement, ProtocoleGlobal,
    calculer_metriques_globales, comparer_annonces,
    corpus_depuis_texte, executer_pretraitements, composer_texte_epure,
)
from tal_toolkit.analyse_pt02 import (
    auditer_reapplication, analyser_lexique_pt02, CHAMPS_LEXICAUX,
)


def test_code_du_notebook_02_dans_l_ordre_sur_microcorpus(tmp_path):
    notebook = json.loads(
        (Path(__file__).resolve().parents[1] /
         "notebooks/02_mesures_lexicales.ipynb").read_text(encoding="utf-8")
    )
    textes = ["".join(c["source"]) for c in notebook["cells"]]
    brut = corpus_depuis_texte(
        "M. Charles Turgeon écrit. La femme[1] a un droit.\r\n\r\n"
        "[Note 1: Exemple.]\r\n\r\nJe crois qu'il faut des droits aux femmes."
    )
    plan = PlanPretraitement((
        OperationPretraitement("masquer_blocs_notes", "Masquer les notes"),
        OperationPretraitement("masquer_appels_notes", "Masquer les appels"),
        OperationPretraitement("recomposer_lignes", "Retours typographiques"),
    ), "test-second")
    traitement = executer_pretraitements(brut, plan=plan)
    vue = composer_texte_epure(traitement)
    n1 = tmp_path / "analyse_faguet_v2_0_0"
    n2 = tmp_path / "analyse_faguet_n2_v1_0_0"
    n1.mkdir()
    n2.mkdir()
    (n1 / "faguet_nettoye.txt").write_text(vue.texte, encoding="utf-8")
    (n1 / "metadonnees_analyse.json").write_text(
        json.dumps({
            "sha256_nettoye": vue.sha256_texte_utf8,
            "version_notebook": "2.0.0",
            "revision_git": "a" * 40,
            "plan_pretraitement": traitement.plan,
            "operations": list(traitement.execution),
        }), encoding="utf-8",
    )

    def display(_):
        pass

    contexte = {
        "__builtins__": __builtins__,
        "Path": Path, "DOSSIER_N1": n1, "DOSSIER_N2": n2,
        "json": json, "hashlib": hashlib, "re": re,
        "secrets": secrets, "zipfile": zipfile,
        "datetime": datetime, "timezone": timezone,
        "urlopen": urlopen,
        "spacy": spacy, "pd": pd, "display": display,
        "DEPOT_LIB": "dreymond732/tal-notebook-evaluator",
        "COMMIT_LIB": "main",
        "VERSION_NOTEBOOK_02": "1.0.0",
        "charger_corpus": charger_corpus,
        "recenser_elements": recenser_elements,
        "OperationPretraitement": OperationPretraitement,
        "PlanPretraitement": PlanPretraitement,
        "ProtocoleGlobal": ProtocoleGlobal,
        "calculer_metriques_globales": calculer_metriques_globales,
        "comparer_annonces": comparer_annonces,
        "auditer_reapplication": auditer_reapplication,
        "analyser_lexique_pt02": analyser_lexique_pt02,
        "CHAMPS_LEXICAUX": CHAMPS_LEXICAUX,
    }
    # La cellule 2 ne sert qu'à installer et localiser les dépendances :
    # le test injecte les mêmes références sans requête d'installation.
    # La cellule 24 ne monte Drive que dans Colab.
    for i in (3, 5, 7, 9, 11, 12, 14, 16, 18, 20, 22):
        exec(compile(textes[i], f"nb02:{i}", "exec"), contexte)
    assert contexte["resultats_pt02"]["globales"]["tokens_lexicaux"] > 0
    assert contexte["corpus"].sha256 == vue.sha256_texte_utf8
    assert contexte["bilan_idempotence"]["idempotent_sur_ce_texte"]
    assert contexte["ARCHIVE_N2"].is_file()
    with zipfile.ZipFile(contexte["ARCHIVE_N2"]) as archive:
        assert archive.testzip() is None
        assert "resultats_et_preuves.json" in archive.namelist()
        assert "faguet_nettoye.txt" in archive.namelist()
        assert "metadonnees_analyse.json" in archive.namelist()
