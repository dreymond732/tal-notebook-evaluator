"""Exécuter les deux parcours de décision du notebook sur un microcorpus.

La décision « reviser » n'interrompt pas les calculs ; aucun export approuvé
ne doit être produit sur cette branche. Les contrôles sont réalisés sans Colab.
"""
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
    executer_pretraitements, exporter_texte_approuve,
    preparer_archive_td01, verifier_standardisation_td01,
    valider_inspection, charger_corpus,
)


def _cellules():
    chemin = (
        Path(__file__).resolve().parents[1]
        / "notebooks" / "01_corpus_protocole.ipynb"
    )
    nb = json.loads(chemin.read_text(encoding="utf-8"))
    return ["".join(c["source"]) for c in nb["cells"]]


class _Frame:
    """Juste le DataFrame nécessaire pour tester la sauvegarde CSV."""

    def __init__(self, lignes):
        self.lignes = lignes

    def to_csv(self, chemin, *, index, encoding):
        assert not index and encoding == "utf-8"
        with Path(chemin).open("w", encoding="utf-8", newline="") as stream:
            ecrivain = csv.DictWriter(
                stream, fieldnames=self.lignes[0].keys()
            )
            ecrivain.writeheader()
            ecrivain.writerows(self.lignes)


@pytest.mark.parametrize(
    ("decision", "statut"),
    [
        ("conserver", "retenu"),
        ("reviser", "provisoire_a_reviser"),
    ],
)
def test_notebook_continue_les_mesures_et_archive_selon_decision(
    tmp_path, monkeypatch, decision, statut,
):
    textes = _cellules()
    source = corpus_depuis_texte(
        "Ce texte[1] décrit une première idée.\r\n\r\n"
        "[Note 1: Exemple de note.]\r\n\r\nCette idée est reprise."
    )
    plan = PlanPretraitement(
        (
            OperationPretraitement(
                "masquer_appels_notes", "Retirer les appels de notes"
            ),
            OperationPretraitement(
                "masquer_blocs_notes", "Retirer les blocs éditoriaux"
            ),
        ),
        "test-continuation",
    )
    resultat = executer_pretraitements(source, plan=plan)
    vue = composer_texte_epure(resultat)
    apercu = tmp_path / "faguet_nettoye.txt"
    with apercu.open("w", encoding="utf-8", newline="") as out:
        out.write(vue.texte)

    journal = {
        "decision": decision,
        "methode_inspection": (
            "Lecture du texte complet et vérification des zones de notes."
        ),
        "justification_decision": (
            "La préparation est conservée pour la comparaison des mesures."
            if decision == "conserver" else
            "Les appels de notes méritent une vérification supplémentaire."
        ),
        "anomalies": [],
    }
    fichier_inspection = tmp_path / "inspection.json"
    fichier_inspection.write_text(json.dumps(journal), encoding="utf-8")

    # Le code des métriques n'impose pas pandas en tant que dépendance Python
    # du noyau commun ; on simule ici uniquement l'affichage/écriture du tableau.
    faux_pandas = types.SimpleNamespace(DataFrame=_Frame)
    monkeypatch.setitem(sys.modules, "pandas", faux_pandas)

    # La vérification des sources standard est indépendante de cette simulation.
    import tal_toolkit.protocole_td01 as protocole
    monkeypatch.setattr(protocole, "SHA_FAGUET_TD01", source.sha256)

    environnement = {
        "DECISION_SUITE": decision,
        "journal_inspection": journal,
        "valider_inspection": valider_inspection,
        "FICHIER_APERCU": apercu,
        "FICHIER_INSPECTION": fichier_inspection,
        "DOSSIER_TRAVAIL": tmp_path,
        "source": source,
        "corpus_source": source,
        "vue_epuree": vue,
        "resultat_global": resultat,
        "SHA256_SOURCE": source.sha256,
        "REVISION_GIT_RESOLUE": "c" * 40,
        "VERSION_NOTEBOOK": "2.0.1",
        "VERSION_BIBLIOTHEQUE": "0.3.0",
        "MODE_REVISION": "exploration",
        "METRIQUES_TD01": METRIQUES_TD01,
        "spacy": spacy,
        "charger_corpus": charger_corpus,
        "comparer_corpus_td01": comparer_corpus_td01,
        "exporter_texte_approuve": exporter_texte_approuve,
        "verifier_standardisation_td01": verifier_standardisation_td01,
        "preparer_archive_td01": preparer_archive_td01,
        "preuve_standardisation": None,
        "JUSTIFICATION_DECISION": journal["justification_decision"],
        "json": json,
        "Path": Path,
        "display": lambda x: None,
    }
    for identifiant in (20, 22, 23):
        exec(compile(textes[identifiant], f"notebook:{identifiant}", "exec"),
             environnement)

    assert environnement["STATUT_ANALYSE"] == statut
    assert environnement["FICHIER_COMPARAISON"].is_file()
    suivi = json.loads(environnement["FICHIER_SUIVI"].read_text("utf-8"))
    assert suivi["decision_nettoyage"] == decision
    assert suivi["statut"] == statut
    assert suivi["sha256_texte_prepare"] == vue.sha256_texte_utf8
    assert suivi["revision_git"] == "c" * 40
    assert len(environnement["resultat_comparaison"]["comparaison"]) == 7

    # Les mêmes cellules finales produisent un livrable différent selon
    # la décision, et le dossier à réviser ne se déclare jamais approuvé.
    code_livrable = textes[25].replace(
        'MON_IDENTIFIANT = ""', 'MON_IDENTIFIANT = "test987"'
    ).replace(
        'BILAN_PERSONNEL = """\n"""',
        'BILAN_PERSONNEL = """Les effets du nettoyage et des notes '
        'doivent être comparés sur les mêmes unités de comptage."""'
    ).replace(
        "VALIDATION_ANALYSE = False", "VALIDATION_ANALYSE = True"
    )
    exec(compile(code_livrable, "notebook:25", "exec"), environnement)
    livrable = environnement["livrable"]
    assert Path(livrable["archive"]).is_file()
    with zipfile.ZipFile(livrable["archive"]) as archive:
        if decision == "reviser":
            assert environnement["export_epuration"] is None
            assert "faguet_nettoye_provisoire.txt" in archive.namelist()
            assert "fiche_suivi.json" in archive.namelist()
            assert "manifeste.json" not in archive.namelist()
            assert livrable["statut"] == "provisoire_a_reviser"
        else:
            assert environnement["export_epuration"] is not None
            assert "manifeste.json" in archive.namelist()
            assert "inspection.json" in archive.namelist()
            assert "faguet_epure.txt" in archive.namelist()
