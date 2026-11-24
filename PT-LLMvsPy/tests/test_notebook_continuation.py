"""Le projet produit et conserve ses résultats sans validation manuelle forcée."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import types
import zipfile

import pytest
import spacy

from tal_toolkit import (
    METRIQUES_TD01, OperationPretraitement, PlanPretraitement,
    comparer_corpus_td01, composer_texte_epure, corpus_depuis_texte,
    executer_pretraitements, charger_corpus,
)


def _cellules():
    p = Path(__file__).resolve().parents[1] / "notebooks/01_preparer_le_corpus_et_mesurer_le_nettoyage.ipynb"
    return {
        c["id"]: "".join(c["source"])
        for c in json.loads(p.read_text(encoding="utf-8"))["cells"]
        if c["cell_type"] == "code"
    }


class _DataFrame:
    def __init__(self, records):
        self.records = records

    def to_csv(self, path, *, index=False, encoding="utf-8"):
        assert index is False and encoding == "utf-8"
        with Path(path).open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(self.records[0]))
            writer.writeheader()
            writer.writerows(self.records)


def test_mesures_sans_decision_et_archive_automatique(tmp_path, monkeypatch):
    codes = _cellules()
    source = corpus_depuis_texte(
        "Un passage[1] à nettoyer.\r\n\r\n"
        "[Note 1: Une référence.]\r\n\r\nAutre passage."
    )
    plan = PlanPretraitement(
        (
            OperationPretraitement("masquer_appels_notes", "Appels éditoriaux"),
            OperationPretraitement("masquer_blocs_notes", "Notes éditoriales"),
        ), identifiant="test-corpus",
    )
    monkeypatch.setitem(
        sys.modules, "pandas", types.SimpleNamespace(DataFrame=_DataFrame)
    )

    contexte = dict(
        corpus_source=source, EST_COLAB=True,
        DOSSIER_TRAVAIL=tmp_path, plan_standard_td01=lambda: plan,
        executer_pretraitements=executer_pretraitements, composer_texte_epure=composer_texte_epure,
        SHA256_SOURCE=source.sha256,
        METRIQUES_TD01=METRIQUES_TD01,
        spacy=spacy, charger_corpus=charger_corpus,
        comparer_corpus_td01=comparer_corpus_td01,
        json=json, Path=Path, display=lambda x: None,
        NUMERO_ETUDIANT="00Ab_7-9", NUMERO_SESSION="123456789",
        DATE_SESSION="20261111T124200Z",
        VERSION_NOTEBOOK="2.1.0",
        REVISION_GIT_RESOLUE="d" * 40,
        VERSION_BIBLIOTHEQUE="0.3.0",
        NOTES_INSPECTION="",
        COMMENTAIRES_ANALYSE="",
    )

    telechargements = []
    fichiers_colab = types.SimpleNamespace(download=telechargements.append)
    monkeypatch.setitem(sys.modules, "google.colab", types.SimpleNamespace(files=fichiers_colab))

    for etape in (
        "nettoyer-livre", "telecharger-texte", "noter-inspection",
        "verifier-texte", "preparer-mesures", "mesurer-corpus", "enregistrer-metadonnees",
        "commenter-analyse", "preparer-archive", "telecharger-archive",
    ):
        exec(compile(codes[etape], f"notebook:{etape}", "exec"), contexte)

    assert contexte["FICHIER_INSPECTION"].is_file()
    assert contexte["FICHIER_COMPARAISON"].is_file()
    assert contexte["FICHIER_COMPARAISON_JSON"].is_file()
    assert contexte["FICHIER_METADONNEES"].is_file()
    assert contexte["FICHIER_ARCHIVE"].is_file()
    assert len(contexte["resultat_comparaison"]["comparaison"]) == 7

    meta = json.loads(contexte["FICHIER_METADONNEES"].read_text(encoding="utf-8"))
    assert meta["numero_etudiant"] == "00Ab_7-9"
    assert meta["numero_session"] == "123456789"
    assert meta["version_notebook"] == "2.1.0"
    assert meta["revision_git"] == "d" * 40
    assert meta["sha256_nettoye"] == contexte["vue_epuree"].sha256_texte_utf8
    assert meta["sha256_source"] == source.sha256

    assert contexte["FICHIER_APERCU"].name == "faguet_nettoye_00Ab_7-9.txt"
    assert contexte["FICHIER_ARCHIVE"].name == "FAGUET_01_00Ab_7-9_20261111T124200Z_123456789.zip"
    assert telechargements == [str(contexte["FICHIER_APERCU"]), str(contexte["FICHIER_ARCHIVE"])]
    with zipfile.ZipFile(contexte["FICHIER_ARCHIVE"]) as archive:
        assert archive.read("faguet_nettoye.txt") == contexte["FICHIER_APERCU"].read_bytes()
        assert json.loads(archive.read("metadonnees_analyse.json")) == meta
        assert archive.testzip() is None
        assert set(archive.namelist()) == {
            "faguet_nettoye.txt", "observations_nettoyage.txt",
            "comparaison_metriques.csv", "comparaison_metriques.json",
            "metadonnees_analyse.json", "commentaires_analyse.txt",
        }


@pytest.mark.parametrize("numero", ["", "../001", "0 01", "é01", "x" * 65])
def test_numero_invalide_refuse_avant_preparation(numero, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", lambda question: numero)
    with pytest.raises(ValueError, match="Numéro étudiant"):
        exec(compile(_cellules()["identification"], "notebook:identification", "exec"), {})
    assert not list(tmp_path.iterdir())
