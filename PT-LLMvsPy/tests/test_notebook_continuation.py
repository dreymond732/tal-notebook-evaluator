"""Le projet produit et conserve ses résultats sans validation manuelle forcée."""
from __future__ import annotations

import csv
from hashlib import sha256
from inspect import getsource
import json
from pathlib import Path
import re
import sys
import types
import zipfile

import pytest
import spacy

from scripts.verifier_notebook02 import executer_cellule
from tal_toolkit import (
    METRIQUES_TD01, __version__, charger_corpus, comparer_corpus_td01,
    composer_texte_epure, compter_motif, corpus_depuis_texte,
    executer_pretraitements, plan_standard_td01,
)


def _cellules():
    p = Path(__file__).resolve().parents[1] / "notebooks/01_preparer_le_corpus_et_mesurer_le_nettoyage.ipynb"
    return {
        c["id"]: "".join(c["source"])
        for c in json.loads(p.read_text(encoding="utf-8"))["cells"]
        if c["cell_type"] == "code"
    }


def test_mesures_sans_decision_et_archive_automatique(tmp_path, monkeypatch, capsys):
    codes = _cellules()
    original = (
        "Il a publié sur le _Féminisme français_[1], le plus complet.\r\n\r\n"
        "[Note 1: Une référence.]\r\n\r\n"
        "[Note 2: Autre référence.]\r\n\r\nAutre passage."
    )
    source = corpus_depuis_texte(original)
    contexte = dict(
        corpus_source=source, EST_COLAB=True,
        DOSSIER_TRAVAIL=tmp_path, plan_standard_td01=plan_standard_td01,
        executer_pretraitements=executer_pretraitements, composer_texte_epure=composer_texte_epure,
        SHA256_SOURCE=source.sha256,
        METRIQUES_TD01=METRIQUES_TD01,
        spacy=spacy, charger_corpus=charger_corpus,
        comparer_corpus_td01=comparer_corpus_td01,
        re=re, json=json, display=lambda x: None, compter_motif=compter_motif,
        NUMERO_ETUDIANT="00Ab_7-9", NUMERO_SESSION="123456789",
        DATE_SESSION="20261111T124200Z",
        VERSION_NOTEBOOK="version-test",
        VERSION_BIBLIOTHEQUE=__version__,
        NOTES_INSPECTION="",
        COMMENTAIRES_ANALYSE="",
    )

    telechargements = []
    fichiers_colab = types.SimpleNamespace(download=telechargements.append)
    monkeypatch.setitem(sys.modules, "google.colab", types.SimpleNamespace(files=fichiers_colab))

    for etape in ("fonctions-nettoyage", "definir-nettoyage", "nettoyer-livre"):
        executer_cellule(codes[etape], f"notebook01:{etape}", contexte)
    filtre_execute = contexte["retirer_appels_notes"]

    # Redéfinir le filtre pour un prochain essai avant d'exporter le précédent.
    executer_cellule(
        "def retirer_appels_notes(texte):\n    return texte\n",
        "notebook01:filtre-modifie", contexte,
    )
    assert contexte["nettoyer"](original) != contexte["texte_nettoye"]

    for etape in (
        "ecrire-texte", "telecharger-texte", "localiser-passage", "choisir-motif-reference",
        "reperer-occurrence-reference", "compter-motif", "noter-inspection",
        "verifier-texte", "preparer-mesures", "mesurer-corpus", "enregistrer-metadonnees",
        "commenter-analyse", "preparer-archive", "telecharger-archive",
    ):
        executer_cellule(codes[etape], f"notebook01:{etape}", contexte)

    assert source.texte == original
    assert contexte["texte_nettoye"] == (
        "Il a publié sur le Féminisme français, le plus complet.\n\nAutre passage."
    )
    sortie = capsys.readouterr().out
    for version, extrait in (
        ("Source", " _Féminisme français_[1], "),
        ("Référence", " _Féminisme français_, "),
        ("Votre traitement", " Féminisme français, "),
    ):
        assert f"{version} : {extrait!r}" in sortie
    zone = contexte["zone"]
    assert zone["occurrence_choisie"] == 2
    assert zone["debut"] == original.rindex("[Note")
    assert f"Original : {zone['fenetre_originale']!r}" in sortie
    assert any(
        ligne.startswith("Référence :") and ligne.endswith("Autre passage.'")
        for ligne in sortie.splitlines()
    )
    assert "masquer_blocs_notes · caractères modifiés :" in sortie
    assert contexte["decompte"]["occurrences_original"] == 2
    assert contexte["decompte"]["occurrences_epure"] == 0
    assert contexte["FICHIER_INSPECTION"].is_file()
    assert contexte["FICHIER_COMPARAISON"].is_file()
    assert contexte["FICHIER_COMPARAISON_JSON"].is_file()
    assert contexte["FICHIER_METADONNEES"].is_file()
    assert contexte["FICHIER_ARCHIVE"].is_file()
    assert len(contexte["resultat_comparaison"]["comparaison"]) == 7

    meta = json.loads(contexte["FICHIER_METADONNEES"].read_text(encoding="utf-8"))
    assert meta["numero_etudiant"] == "00Ab_7-9"
    assert meta["numero_session"] == "123456789"
    assert meta["version_notebook"] == "version-test"
    assert meta["version_bibliotheque"] == __version__
    assert meta["revision_git"] == "main"
    assert meta["sha256_source"] == sha256(original.encode("utf-8")).hexdigest()
    plan = meta["plan_pretraitement"]
    assert plan["instructions"] == getsource(contexte["nettoyer"])
    assert plan["fonctions"]["retirer_appels_notes"] == getsource(filtre_execute)
    for nom in ("retirer_blocs_notes", "retirer_separateurs", "recomposer_lignes"):
        assert plan["fonctions"][nom] == getsource(contexte[nom])

    assert contexte["FICHIER_APERCU"].name == "faguet_nettoye_00Ab_7-9.txt"
    assert contexte["FICHIER_ARCHIVE"].name == "FAGUET_01_00Ab_7-9_20261111T124200Z_123456789.zip"
    assert telechargements == [str(contexte["FICHIER_APERCU"]), str(contexte["FICHIER_ARCHIVE"])]
    with zipfile.ZipFile(contexte["FICHIER_ARCHIVE"]) as archive:
        texte_archive = archive.read("faguet_nettoye.txt")
        assert texte_archive == contexte["FICHIER_APERCU"].read_bytes()
        assert texte_archive.decode("utf-8") == contexte["texte_nettoye"]
        assert sha256(texte_archive).hexdigest() == meta["sha256_nettoye"]
        mesures = json.loads(archive.read("comparaison_metriques.json"))
        assert mesures["source_epuree_sha256"] == meta["sha256_nettoye"]
        assert mesures["source_originale_sha256"] == meta["sha256_source"]
        assert mesures["protocole_commun"] == meta["protocole_mesures"]
        contenu_csv = archive.read("comparaison_metriques.csv").decode("utf-8")
        lignes = csv.DictReader(contenu_csv.splitlines())
        assert [ligne["id"] for ligne in lignes] == [
            ligne["id"] for ligne in mesures["comparaison"]
        ]
        assert json.loads(archive.read("metadonnees_analyse.json")) == meta
        assert archive.testzip() is None
        assert set(archive.namelist()) == {
            "faguet_nettoye.txt", "observations_nettoyage.txt",
            "comparaison_metriques.csv", "comparaison_metriques.json",
            "metadonnees_analyse.json", "commentaires_analyse.txt",
        }

    contexte["FICHIER_APERCU"].write_text("Texte modifié après la mesure.", encoding="utf-8")
    with pytest.raises(ValueError, match="essais différents"):
        executer_cellule(codes["preparer-archive"], "notebook01:preparer-archive", contexte)


@pytest.mark.parametrize("numero", ["", "../001", "0 01", "é01", "x" * 65])
def test_numero_invalide_refuse_avant_preparation(numero, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", lambda question: numero)
    with pytest.raises(ValueError, match="Numéro étudiant"):
        exec(compile(_cellules()["identification"], "notebook:identification", "exec"), {})
    assert not list(tmp_path.iterdir())
