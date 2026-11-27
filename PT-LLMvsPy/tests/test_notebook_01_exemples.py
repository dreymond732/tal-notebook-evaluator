"""Vérifier ce que les cellules du cahier 01 affichent aux étudiants."""
from inspect import getsource
import json
from pathlib import Path
import re

import pytest

from scripts.verifier_notebook02 import executer_cellule


@pytest.fixture
def cellules():
    fichier = Path(__file__).resolve().parents[1] / "notebooks" / "01_preparer_le_corpus_et_mesurer_le_nettoyage.ipynb"
    return {
        c["id"]: "".join(c["source"])
        for c in json.loads(fichier.read_text(encoding="utf-8"))["cells"]
        if c["cell_type"] == "code"
    }


def _executer(cellules, *etapes):
    contexte = {"re": re}
    for etape in ("fonctions-nettoyage", *etapes):
        executer_cellule(cellules[etape], f"notebook01:{etape}", contexte)
    return contexte


def test_six_effets_du_nettoyage(cellules, capsys):
    _executer(cellules, "exemples-fournis")
    assert capsys.readouterr().out.splitlines() == [
        "Lignes réunies : Une phrase continue.",
        "Apostrophe : L'homme",
        "Note et appel : " + repr("Un propos.\n\nLa suite."),
        "Séparateur : " + repr("Texte un.\n\nTexte deux."),
        "Titre conservé : " + repr("IDÉES GÉNÉRALES\n\nLe chapitre commence."),
        "Césure choisie : Une information.",
    ]


def test_lecture_du_filtre_et_de_la_transformation(cellules, capsys):
    contexte = _executer(cellules, "lire-filtre", "lire-transformation")
    sortie = capsys.readouterr().out
    for nom in ("retirer_appels_notes", "recomposer_lignes"):
        assert getsource(contexte[nom]) in sortie
    assert "Avant _Féminisme français_[1]\nAprès _Féminisme français_" in sortie
    assert repr("le livre le plus complet\n\nUn autre paragraphe.") in sortie


def test_ordre_des_deux_instructions_sur_le_meme_passage(cellules, capsys):
    contexte = _executer(cellules, "ordre-des-traitements")
    assert contexte["passage"] == "_Féminisme français_[1]"
    assert capsys.readouterr().out.splitlines() == [
        "Titre traité en premier : « Féminisme français »[1]",
        "Signes retirés en premier : Féminisme français[1]",
    ]


def test_le_traitement_personnel_est_insere_dans_la_suite(cellules, capsys):
    contexte = _executer(cellules, "suite-reference", "definir-nettoyage", "essai-personnel")
    assert contexte["texte"] == "Le _chapitre_ commence."
    assert contexte["mon_resultat"] == "Le chapitre commence."
    assert contexte["MON_TEXTE"] == contexte["exemple"]

    # Essayer la variante proposée dans la consigne : conserver les appels sauf [1].
    essais = dict(cellules)
    essais["definir-nettoyage"] = essais["definir-nettoyage"].replace(
        "texte = retirer_appels_notes(texte)", 'texte = texte.replace("[1]", "")'
    )
    essais["essai-personnel"] = re.sub(
        r"^MON_TEXTE = .*$", 'MON_TEXTE = "Un renvoi[1], puis un autre[2]."',
        essais["essai-personnel"], flags=re.MULTILINE,
    )
    capsys.readouterr()
    variante = _executer(essais, "definir-nettoyage", "essai-personnel")
    assert variante["MON_TEXTE"] == "Un renvoi[1], puis un autre[2]."
    assert variante["mon_resultat"] == "Un renvoi, puis un autre[2]."
    assert "Prévision vérifiée : False" in capsys.readouterr().out
