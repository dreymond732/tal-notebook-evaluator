"""Le contre-exemple est désormais une anomalie potentielle du texte déjà épuré."""
import pytest

from tal_toolkit import (
    OperationPretraitement, PlanPretraitement,
    executer_pretraitements, composer_texte_epure,
    localiser_dans_original, fonctions_ayant_modifie_zone,
    compter_motif, valider_inspection,
)


def test_localiser_et_attribuer_une_anomalie_sur_le_texte_original():
    source = (
        "Introduction.\r\n\r\n"
        "Un renvoi[1] au passage.\r\n"
        "Le paragraphe continue.\r\n\r\nConclusion."
    )
    plan = PlanPretraitement(
        (
            OperationPretraitement("masquer_appels_notes", "Masquer les renvois"),
            OperationPretraitement("recomposer_lignes", "Réunir les lignes"),
        ), "controle-v1"
    )
    resultat = executer_pretraitements(source, plan=plan)
    loc = localiser_dans_original(source, "renvoi[1]", contexte=50)
    assert source[loc["debut"]:loc["fin"]] == "renvoi[1]"
    assert loc["nombre_correspondances"] == 1
    fonctions = fonctions_ayant_modifie_zone(
        resultat, loc["fenetre_debut"], loc["fenetre_fin"]
    )
    noms = {x["operation"] for x in fonctions}
    assert "masquer_appels_notes" in noms
    assert "recomposer_lignes" in noms

    epure = composer_texte_epure(resultat).texte
    comptes = compter_motif(source, epure, "[1]")
    assert comptes["occurrences_original"] == 1
    assert comptes["occurrences_epure"] == 0


def test_frequence_literal_regex_et_ancre_ambiguë():
    original = "a...b abc a...b"
    nettoye = "a b abc a b"
    assert compter_motif(original, nettoye, "a...b")["occurrences_original"] == 2
    assert compter_motif(original, nettoye, "a.{3}b", mode="regex")["occurrences_original"] == 2
    with pytest.raises(ValueError, match="vide"):
        compter_motif(original, nettoye, "a*", mode="regex")
    loc = localiser_dans_original(original, "a...b", occurrence=2, contexte=0)
    assert loc["debut"] == original.rfind("a...b")
    with pytest.raises(ValueError, match="que 2"):
        localiser_dans_original(original, "a...b", occurrence=3)


def test_journal_sans_anomalie_admissible_mais_decision_motivée():
    journal = {
        "decision": "conserver",
        "methode_inspection": "Lecture du début, de la fin et de trois chapitres dans un éditeur",
        "justification_decision": "Pas de structure perdue parmi les passages examinés.",
        "anomalies": [],
    }
    valider_inspection(journal)
    journal["methode_inspection"] = ""
    with pytest.raises(ValueError, match="vérifications"):
        valider_inspection(journal)


def test_journal_avec_anomalie_chiffree():
    journal = {
        "decision": "reviser",
        "methode_inspection": "Lecture des intertitres et des passages comportant des renvois",
        "justification_decision": "L'effet sur les transitions entre paragraphes est trop important.",
        "anomalies": [{
            "ancre": "renvoi[1]", "debut": 12, "fin": 21,
            "fonction_suspectee": "masquer_appels_notes",
            "commentaire": "Le renvoi est supprimé, et la ponctuation doit être examinée.",
            "estimation": {"occurrences_original": 2, "occurrences_epure": 0},
        }],
    }
    valider_inspection(journal)
    journal["anomalies"][0]["estimation"] = {}
    with pytest.raises(ValueError, match="décompte"):
        valider_inspection(journal)
