"""Comparaison et dépôt Drive testés sans compte Google ni accès réseau."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import spacy

from tal_toolkit import (
    Corpus, OperationPretraitement, PlanPretraitement,
    executer_pretraitements, exporter_texte_approuve,
)
from tal_toolkit.comparaison_td01 import comparer_corpus_td01
from tal_toolkit.metriques_globales import ProtocoleGlobal
from tal_toolkit.soumission_td01 import (
    preparer_archive_td01, deposer_archive_drive,
    verifier_archive_td01, verifier_tests_personnels,
)


def _environnement(tmp_path):
    original = "L'été[1] arrive.\r\n\r\n[Note 1: Une précision.]\r\n\r\nL'été arrive."
    from tal_toolkit.io_corpus import corpus_depuis_texte
    corpus = corpus_depuis_texte(original, origine="microcorpus-test")
    plan = PlanPretraitement(
        (OperationPretraitement("masquer_appels_notes", "Retrait de l'appel"),
         OperationPretraitement("masquer_blocs_notes", "Retrait du contenu")),
        identifiant="test-labo",
    )
    traite = executer_pretraitements(corpus, plan=plan)
    approuve = exporter_texte_approuve(
        traite, tmp_path / "export",
        decisions={
            "masquer_appels_notes": "approuve",
            "masquer_blocs_notes": "approuve",
        },
        confirmation_sha256=corpus.sha256,
        justification_globale="Les effets ont été examinés et approuvés sur le corpus.",
        approbation_compaction=True,
    )
    nlp = spacy.blank("fr")
    nlp.add_pipe("sentencizer")
    comparaison = comparer_corpus_td01(
        corpus, Path(approuve["texte"]).read_text("utf-8"), nlp,
        protocole=ProtocoleGlobal(
            tokens="alphabetiques", formes="minuscules", retours="conserver"
        ),
    )
    tests = [
        {"debut": 0, "fin": 11, "operation": "masquer_appels_notes",
         "type_cas": "positif", "attendu": "L'été  ", "observe": "L'été  ",
         "justification": "L'appel bibliographique ne fait pas partie du texte."},
        {"debut": 12, "fin": 19, "operation": "masquer_appels_notes",
         "type_cas": "contre-exemple", "attendu": "arrive.",
         "observe": "arrive.",
         "justification": "Aucun appel de note dans ce segment ne doit disparaître."},
    ]
    return corpus, approuve, comparaison, tests


def test_comparaison_conditions_identiques(tmp_path):
    _, _, comp, _ = _environnement(tmp_path)
    assert comp["schema"] == "comparaison-td01-v1"
    assert len(comp["comparaison"]) == 7
    assert all(v for d in comp["controles"].values()
               for v in (d.values() if isinstance(d, dict) else [d]))
    assert comp["source_originale_sha256"] != comp["source_epuree_sha256"]
    assert comp["comparaison"][0]["original"] > comp["comparaison"][0]["epure"]
    assert comp["comparaison"][0]["variation_relative_pourcent"] < 0


def test_comparaison_interdit_second_nettoyage(tmp_path):
    from tal_toolkit.io_corpus import corpus_depuis_texte
    nlp = spacy.blank("fr")
    nlp.add_pipe("sentencizer")
    with pytest.raises(ValueError, match="telle que fournie"):
        comparer_corpus_td01(
            corpus_depuis_texte("Bonjour."), "Bonjour.", nlp,
            protocole=ProtocoleGlobal(retours="recomposer_lignes"),
        )


def test_soumission_zip_et_drive_monte(tmp_path, monkeypatch):
    corpus, approuve, comp, tests = _environnement(tmp_path)
    out = preparer_archive_td01(
        "etu012", approuve, tests, comp,
        "Les notes ont été exclues de ce microcorpus ; la perte des mentions "
        "bibliographiques est explicite. La comparaison n'est pas une preuve "
        "d'un protocole identique au modèle Gemini.",
        tmp_path / "local",
        version_bibliotheque="0.2.0",
    )
    fichier = Path(out["archive"])
    assert fichier.is_file()
    assert out["sha256"] == hashlib.sha256(fichier.read_bytes()).hexdigest()
    registre = verifier_archive_td01(fichier)
    assert registre["sha256_source"] == corpus.sha256
    drive = tmp_path / "drive"
    drive.mkdir()
    with pytest.raises(ValueError, match="non confirmé"):
        deposer_archive_drive(fichier, drive, confirmation_explicite=False)
    deposer = deposer_archive_drive(fichier, drive, confirmation_explicite=True)
    assert deposer["verification"] == "SHA256_ET_ZIP_OK"
    assert Path(deposer["depot"]).read_bytes() == fichier.read_bytes()
    with pytest.raises(FileExistsError):
        deposer_archive_drive(fichier, drive, confirmation_explicite=True)

    from scripts import collecter_td01
    monkeypatch.setattr(collecter_td01, "SHA_FAGUET", corpus.sha256)
    releves, anomalies = collecter_td01.collecter(drive)
    assert len(releves) == 1 and anomalies == []
    assert releves[0]["identifiant"] == "etu012"
    assert releves[0]["derniere_soumission"] is True
    assert releves[0]["nombre_tests"] == 2


def test_depôt_inaccessible_et_copie_secours_preservee(tmp_path):
    _, approuve, comp, tests = _environnement(tmp_path)
    out = preparer_archive_td01(
        "etu456", approuve, tests, comp,
        "Cette expérience vérifie les deux versions du texte avec un même "
        "protocole et refuse tout dépôt en l'absence de droits sur le dossier.",
        tmp_path / "local", version_bibliotheque="0.2.0",
    )
    chemin = Path(out["archive"])
    with pytest.raises(FileNotFoundError):
        deposer_archive_drive(chemin, tmp_path / "drive-absent",
                             confirmation_explicite=True)
    assert chemin.exists()


@pytest.mark.parametrize("identifiant", ["a", "../admin", "Jean Dupont", ""])
def test_identifiant_invalide_refuse(tmp_path, identifiant):
    _, export, comp, tests = _environnement(tmp_path)
    with pytest.raises(ValueError, match="Identifiant"):
        preparer_archive_td01(
            identifiant, export, tests, comp,
            "Observations documentées de la chaîne de prétraitements et de mesure.",
            tmp_path / "local", version_bibliotheque="0.2.0",
        )


def test_soumission_rejette_tests_incomplets(tmp_path):
    _, export, comp, tests = _environnement(tmp_path)
    cases = [tests[:1], [dict(t, type_cas="positif") for t in tests],
             [dict(tests[0], attendu="faux"), tests[1:][0]]]
    for spec in cases:
        with pytest.raises(ValueError):
            preparer_archive_td01(
                "etu012", export, spec, comp,
                "Justification des choix et effets globaux dans cette expérience.",
                tmp_path / "local", version_bibliotheque="0.2.0",
            )


def test_soumission_rejette_metriques_incoherentes(tmp_path):
    _, export, comp, tests = _environnement(tmp_path)
    comp["source_originale_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="Empreinte"):
        preparer_archive_td01(
            "etu012", export, tests, comp,
            "Une justification suffisamment longue des traitements choisis.",
            tmp_path / "local", version_bibliotheque="0.2.0",
        )


def test_soumission_rejette_secret(tmp_path):
    _, export, comp, tests = _environnement(tmp_path)
    with pytest.raises(ValueError, match="Secret"):
        preparer_archive_td01(
            "etu012", export, tests, comp,
            "Rapport avec secret github_pat_123456789 et une justification méthodologique.",
            tmp_path / "local", version_bibliotheque="0.2.0",
        )
