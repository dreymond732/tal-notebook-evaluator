"""Exécuter les exemples fournis et l'essai personnel du notebook 01."""
import json
from pathlib import Path

from tal_toolkit import (
    OperationPretraitement, PlanPretraitement, executer_pretraitements,
    composer_texte_epure,
)


def _essayer(identifiant, **entrees):
    fichier = Path(__file__).resolve().parents[1] / "notebooks" / "01_preparer_le_corpus_et_mesurer_le_nettoyage.ipynb"
    cellules = {
        c["id"]: "".join(c["source"])
        for c in json.loads(fichier.read_text(encoding="utf-8"))["cells"]
    }
    contexte = {
        "OperationPretraitement": OperationPretraitement,
        "PlanPretraitement": PlanPretraitement,
        "executer_pretraitements": executer_pretraitements,
        "composer_texte_epure": composer_texte_epure,
        **entrees,
    }
    for etape in ("decrire-operation", identifiant):
        exec(compile(cellules[etape], f"notebook01:{etape}", "exec"), contexte)
    return contexte


def test_toutes_les_phrases_types_du_notebook_01():
    contexte = _essayer("exemples-fournis")
    assert len(contexte["EXEMPLES_FOURNIS"]) == 6
    assert {x["nom"] for x in contexte["EXEMPLES_FOURNIS"]} == {
        "retours typographiques",
        "apostrophes courbes",
        "appel et contenu de note",
        "séparateur d'astérisques",
        "titre conservé",
        "césure approuvée",
    }


def test_une_prevision_personnelle_inexacte_permet_d_observer_le_resultat():
    exemple = "Je relis le chapitre.\n\n[Note 2: Une référence à écarter.]\n\nJe poursuis."
    contexte = _essayer("essai-personnel", MON_TEXTE=exemple, MA_PREVISION=exemple)
    assert contexte["mon_journal"].original == exemple
    assert contexte["mon_resultat"] == "Je relis le chapitre.\n\nJe poursuis."
    assert contexte["MA_PREVISION"] != contexte["mon_resultat"]
