"""Archives de l'analyse Faguet versionnée : inspection sans anomalie possible."""
import json
from pathlib import Path
import zipfile

import pytest
import spacy

from tal_toolkit import (
    OperationPretraitement, PlanPretraitement, corpus_depuis_texte,
    executer_pretraitements, exporter_texte_approuve,
    comparer_corpus_td01,
    preparer_archive_td01, verifier_archive_td01, METRIQUES_TD01,
)


def _cas(tmp_path):
    corpus = corpus_depuis_texte(
        "Cette phrase[1] contient une note.\r\n\r\n"
        "[Note 1: une explication.]\r\n\r\nSuite."
    )
    plan = PlanPretraitement((
        OperationPretraitement("masquer_appels_notes", "Retirer les renvois"),
        OperationPretraitement("masquer_blocs_notes", "Retirer les notes"),
    ), "test-inspection")
    resultat = executer_pretraitements(corpus, plan=plan)
    export = exporter_texte_approuve(
        resultat, tmp_path / "epure",
        decisions={x.nom: "approuve" for x in plan.operations},
        confirmation_sha256=corpus.sha256,
        justification_globale="Les effets sont acceptables sur le document observé.",
        approbation_compaction=True,
    )
    nlp = spacy.blank("fr")
    nlp.add_pipe("sentencizer")
    comp = comparer_corpus_td01(
        corpus, Path(export["texte"]).read_text("utf-8"), nlp,
        protocole=METRIQUES_TD01,
    )
    inspection = {
        "decision": "conserver",
        "methode_inspection": "Lecture des paragraphes de début et de fin et recherche de notes.",
        "justification_decision": "Aucune anomalie relevée sur les passages inspectés.",
        "anomalies": [],
    }
    return corpus, export, comp, inspection


def test_archive_inspection_revision_et_collecte(tmp_path, monkeypatch):
    import tal_toolkit.protocole_td01 as protocole
    from scripts import collecter_td01
    corpus, export, comparaison, inspection = _cas(tmp_path)
    monkeypatch.setattr(protocole, "SHA_FAGUET_TD01", corpus.sha256)
    monkeypatch.setattr(collecter_td01, "SHA_FAGUET", corpus.sha256)
    archive = preparer_archive_td01(
        "test432", export, [], comparaison,
        "Deux paragraphes ont été vérifiés. Les renvois éditoriaux sont "
        "supprimés, et le nombre de tokens change sous le même protocole.",
        tmp_path / "archives", version_bibliotheque="0.3.0",
        inspection=inspection,
        revision_git="b" * 40,
        version_notebook="2.1.0",
        mode_revision="exploration",
    )
    assert Path(archive["archive"]).name.startswith("FAGUET_test432_v2-1-0_")
    registre = verifier_archive_td01(archive["archive"])
    assert registre["mode_revision"] == "exploration"
    assert registre["revision_git"] == "b" * 40
    assert registre["version_notebook"] == "2.1.0"
    with zipfile.ZipFile(archive["archive"]) as z:
        assert "inspection.json" in z.namelist()
        assert "tests_personnels.json" not in z.namelist()
        assert json.loads(z.read("inspection.json"))["anomalies"] == []
    lignes, erreurs = collecter_td01.collecter(tmp_path / "archives")
    assert len(lignes) == 1 and not erreurs
    assert lignes[0]["type_suivi"] == "inspection"
    assert lignes[0]["nombre_tests"] == 0
    assert lignes[0]["version_notebook"] == "2.1.0"


def test_exploration_ne_se_declare_pas_reference(tmp_path, monkeypatch):
    corpus, export, comparaison, inspection = _cas(tmp_path)
    import tal_toolkit.protocole_td01 as protocole
    monkeypatch.setattr(protocole, "SHA_FAGUET_TD01", corpus.sha256)
    base = dict(
        identifiant="test123", export_epuration=export,
        tests_personnels=[], comparaison=comparaison,
        observations="Recherche des notes et vérification de plusieurs lignes.",
        dossier_local=tmp_path / "archives",
        version_bibliotheque="0.3.0", inspection=inspection,
        revision_git="c" * 40, version_notebook="2.0.0",
    )
    with pytest.raises(ValueError, match="preuve de standardisation"):
        preparer_archive_td01(**base, mode_revision="reference")
    with pytest.raises(ValueError, match="ne doit pas"):
        preparer_archive_td01(
            **base, mode_revision="exploration", standardisation_td01={"profil": "X"}
        )
