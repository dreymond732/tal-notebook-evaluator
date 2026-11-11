"""Réapplication des opérations et indicateurs réels du notebook 02."""
from __future__ import annotations

from hashlib import sha256

import pytest
import spacy

from tal_toolkit.analyse_pt02 import (
    CHAMPS_LEXICAUX, analyser_lexique_pt02, auditer_reapplication,
)
from tal_toolkit.pretraitements import OperationPretraitement, PlanPretraitement


def plan():
    return PlanPretraitement((
        OperationPretraitement("masquer_appels_notes", "Notes"),
        OperationPretraitement("recomposer_lignes", "Retours typographiques"),
    ), "test-reapplication")


def test_reapplication_noop_sur_texte_deja_propre():
    texte = "Le mariage existe.\n\nLe divorce est une question."
    verif = auditer_reapplication(texte, plan())
    assert verif["idempotent_sur_ce_texte"] is True
    assert verif["sha256_entree"] == sha256(texte.encode()).hexdigest()
    assert verif["total_modifications_operations"] == 0
    assert verif["premier_ecart_position"] is None


def test_reapplication_peut_changer_texte_incomplet():
    texte = "Le mariage[1] existe.\r\nLe divorce suit."
    verif = auditer_reapplication(texte, plan())
    assert verif["idempotent_sur_ce_texte"] is False
    assert verif["total_modifications_operations"] >= 1
    assert verif["sha256_entree"] != verif["sha256_reapplication"]
    assert verif["premier_ecart_position"] is not None


def test_mesures_lexicales_formes_premiere_personne_et_locutions():
    nlp = spacy.blank("fr")
    nlp.add_pipe("sentencizer")
    t = ("Je crois que la femme a un droit. La femme et l'homme "
         "ont des droits. Monsieur Turgeon et Charles Turgeon disent : "
         "il faut la division du travail. ")
    out = analyser_lexique_pt02(t, nlp, calculer_lemmes=True, taille_sttr=5)
    assert out["source_nettoyee_sha256"] == sha256(t.encode()).hexdigest()
    assert out["globales"]["tokens_lexicaux"] > 0
    assert out["globales"]["tokens_bruts_spacy"] >= out["globales"]["tokens_lexicaux"]
    assert out["globales"]["types_minuscules"] <= out["globales"]["tokens_lexicaux"]
    assert out["globales"]["sttr_nombre_blocs_complets"] > 0
    assert out["enonciation"]["premiere_personne_formes"]["je"] >= 1
    assert out["locutions"]["je_crois"]["occurrences"] == 1
    assert out["locutions"]["il_faut"]["occurrences"] == 1
    assert out["onomastique"]["Charles Turgeon"]["mentions"] == 2
    assert out["lemmatisation"]["statut"] == "NON_CALCULE"
    assert "Aucun lemmatiseur" in out["lemmatisation"]["raison"]
    assert all(out["controles"].values())
    assert "femme" in CHAMPS_LEXICAUX["genre_anthropologie"]


def test_mentions_longues_comptees_une_fois():
    from tal_toolkit.analyse_pt02 import _mentions
    x = "Charles Turgeon. M. Turgeon. Turgeon. Turgeonne n'est pas Turgeon."
    out = _mentions(x, ("Charles Turgeon", "M. Turgeon", "Turgeon"))
    assert out["mentions"] == 4
    assert out["variantes"]["Charles Turgeon"] == 1


def test_pipeline_et_sttr_preconditions():
    nlp = spacy.blank("fr")
    with pytest.raises(ValueError, match="Segmentateur"):
        analyser_lexique_pt02("Bonjour. Salut.", nlp)
    nlp.add_pipe("sentencizer")
    with pytest.raises(ValueError, match="positive"):
        analyser_lexique_pt02("Bonjour. Salut.", nlp, taille_sttr=0)
    assert analyser_lexique_pt02("", nlp)["globales"]["sttr"] is None
