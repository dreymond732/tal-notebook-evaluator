"""Le projet produit et conserve ses résultats sans validation manuelle forcée."""
from __future__ import annotations

import csv
import hashlib
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
    p = Path(__file__).resolve().parents[1] / "notebooks/01_corpus_protocole.ipynb"
    return ["".join(c["source"]) for c in json.loads(p.read_text(encoding="utf-8"))["cells"]]


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
    nettoyage = executer_pretraitements(source, plan=plan)
    epure = composer_texte_epure(nettoyage)
    fichier = tmp_path / "faguet_nettoye.txt"
    with fichier.open("w", encoding="utf-8", newline="") as stream:
        stream.write(epure.texte)

    monkeypatch.setitem(
        sys.modules, "pandas", types.SimpleNamespace(DataFrame=_DataFrame)
    )

    contexte = dict(
        corpus_source=source, FICHIER_APERCU=fichier,
        DOSSIER_TRAVAIL=tmp_path, vue_epuree=epure,
        resultat_global=nettoyage,
        SHA256_SOURCE=source.sha256,
        METRIQUES_TD01=METRIQUES_TD01,
        spacy=spacy, charger_corpus=charger_corpus,
        comparer_corpus_td01=comparer_corpus_td01,
        json=json, Path=Path, display=lambda x: None,
        NUMERO_SESSION="123456789",
        DATE_SESSION="20261111T124200Z",
        VERSION_NOTEBOOK="2.0.0",
        REVISION_GIT_RESOLUE="d" * 40,
        VERSION_BIBLIOTHEQUE="0.3.0",
        NOTES_INSPECTION="",
        COMMENTAIRES_ANALYSE="",
    )

    for i in [18, 20, 22, 23, 25]:
        exec(compile(codes[i], f"notebook:{i}", "exec"), contexte)

    assert contexte["FICHIER_INSPECTION"].is_file()
    assert contexte["FICHIER_COMPARAISON"].is_file()
    assert contexte["FICHIER_COMPARAISON_JSON"].is_file()
    assert contexte["FICHIER_METADONNEES"].is_file()
    assert contexte["FICHIER_ARCHIVE"].is_file()
    assert len(contexte["resultat_comparaison"]["comparaison"]) == 7

    meta = json.loads(contexte["FICHIER_METADONNEES"].read_text(encoding="utf-8"))
    assert meta["numero_session"] == "123456789"
    assert meta["version_notebook"] == "2.0.0"
    assert meta["revision_git"] == "d" * 40
    assert meta["sha256_nettoye"] == epure.sha256_texte_utf8
    assert meta["sha256_source"] == source.sha256

    with zipfile.ZipFile(contexte["FICHIER_ARCHIVE"]) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == {
            "faguet_nettoye.txt", "observations_nettoyage.txt",
            "comparaison_metriques.csv", "comparaison_metriques.json",
            "metadonnees_analyse.json", "commentaires_analyse.txt",
        }

    # Copier vers un dossier représentant le Drive monté.
    dossier_drive = tmp_path / "DrivePartage"
    dossier_drive.mkdir()
    cell28 = codes[28].replace(
        'DOSSIER_DEPOT_DRIVE = ""',
        f'DOSSIER_DEPOT_DRIVE = {str(dossier_drive)!r}'
    )
    exec(compile(cell28, "notebook:28", "exec"), contexte)
    fichier_depose = dossier_drive / contexte["FICHIER_ARCHIVE"].name
    assert fichier_depose.is_file()
    assert hashlib.sha256(fichier_depose.read_bytes()).digest() == hashlib.sha256(
        contexte["FICHIER_ARCHIVE"].read_bytes()
    ).digest()

    # Un dépôt du même fichier ne doit jamais être écrasé.
    with pytest.raises(FileExistsError):
        exec(compile(cell28, "notebook:28", "exec"), contexte)
