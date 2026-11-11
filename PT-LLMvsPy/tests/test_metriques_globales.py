"""Contrats de métriques globales : tests indépendants des estimations Gemini."""
import hashlib
import json
from pathlib import Path

import pytest

from tal_toolkit import (
    ProtocoleGlobal, calculer_metriques_globales, comparer_annonces,
    corpus_depuis_texte, preparer_texte_pour_analyse,
)


@pytest.fixture()
def nlp():
    spacy = pytest.importorskip("spacy")
    pipeline = spacy.blank("fr")
    pipeline.add_pipe("sentencizer")
    return pipeline


def test_cas_manuel_minimal(nlp):
    source = corpus_depuis_texte("Chat chat. Chien.")
    out = calculer_metriques_globales(source, nlp)
    m = out["metriques"]
    assert (m["tokens"], m["types"], m["hapax"], m["phrases"]) == (3, 2, 1, 2)
    assert m["ttr"] == pytest.approx(2 / 3)
    assert m["ttr_pourcent"] == pytest.approx(200 / 3)
    assert m["hapax_types_pourcent"] == pytest.approx(50)
    assert m["mots_par_phrase"] == 1.5
    assert all(out["controles"].values())
    assert out["provenance"]["sha256_utf8_original"] == hashlib.sha256(
        source.texte.encode("utf-8")
    ).hexdigest()


def test_choix_formes_exactes_change_les_types(nlp):
    texte = "Chat chat. Chien."
    m = calculer_metriques_globales(texte, nlp, protocole=ProtocoleGlobal(
        formes="exactes"
    ))["metriques"]
    assert (m["tokens"], m["types"], m["hapax"]) == (3, 3, 3)


def test_ponctuation_change_l_unite_de_compte(nlp):
    texte = "Chat, chien."
    alphas = calculer_metriques_globales(texte, nlp)["metriques"]
    tous = calculer_metriques_globales(texte, nlp, protocole=ProtocoleGlobal(
        tokens="tous_sans_espaces"
    ))["metriques"]
    assert alphas["tokens"] == 2
    assert tous["tokens"] == 4
    assert tous["types"] >= alphas["types"]


def test_retours_typographiques_recomposes_sans_decalage(nlp):
    texte = "Chat et chien\r\nregardent. \r\n\r\nChat dort."
    analyse = preparer_texte_pour_analyse(texte, "recomposer_lignes")
    assert len(analyse) == len(texte)
    assert analyse.startswith("Chat et chien  regardent.")
    assert "\r\n\r\n" in analyse
    m = calculer_metriques_globales(
        corpus_depuis_texte(texte), nlp,
        protocole=ProtocoleGlobal(retours="recomposer_lignes")
    )
    assert m["metriques"]["tokens"] > 0
    for t in m["traces"]["tokens"]:
        assert texte[t["debut"]:t["fin"]] == t["forme_originale"]
    for p in m["traces"]["phrases"]:
        assert texte[p["debut"]:p["fin"]] == p["extrait_original"]


def test_phrases_et_mots_sur_texte_vide(nlp):
    out = calculer_metriques_globales("", nlp)["metriques"]
    assert (out["tokens"], out["types"], out["hapax"], out["phrases"]) == (0, 0, 0, 0)
    assert out["ttr"] is None
    assert out["ttr_pourcent"] is None
    assert out["hapax_types_pourcent"] is None
    assert out["mots_par_phrase"] is None


def test_pas_de_segmentation_invalide(nlp):
    nlp.remove_pipe("sentencizer")
    with pytest.raises(ValueError, match="segmenter les phrases"):
        calculer_metriques_globales("Un exemple.", nlp)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"tokens": "ponctuation_seule"},
        {"formes": "famille_lexicale"},
        {"retours": "supprimer_les_lignes"},
    ],
)
def test_protocoles_invalides(kwargs):
    with pytest.raises(ValueError):
        ProtocoleGlobal(**kwargs)


def test_lemme_sans_modele_refuse(nlp):
    with pytest.raises(ValueError, match="lemme"):
        calculer_metriques_globales(
            "Chat et chien.", nlp, protocole=ProtocoleGlobal(formes="lemmes")
        )


def test_provenance_du_texte_change_si_corpus_change(nlp):
    a = calculer_metriques_globales("Un livre.", nlp)
    b = calculer_metriques_globales("Deux livres.", nlp)
    assert a["provenance"]["sha256_utf8_original"] != b["provenance"]["sha256_utf8_original"]


def test_confrontation_numerique_n_est_pas_validation_de_gemini(nlp):
    m = calculer_metriques_globales("Chat chat. Chien.", nlp)
    a = [
        {"cle": "tokens", "valeur": 3, "decimales": 0, "unite": "mots"},
        {"cle": "ttr", "valeur": 0.667, "decimales": 3, "unite": "ratio"},
        {"cle": "hapax", "valeur": 3, "decimales": 0, "unite": "types"},
    ]
    comparaisons = comparer_annonces(m, a)
    assert [r["statut_numerique"] for r in comparaisons] == [
        "MEME_VALEUR_A_L_ARRONDI", "MEME_VALEUR_A_L_ARRONDI", "ECART"
    ]
    assert all(r["protocole_reference"] == "INCONNU" for r in comparaisons)
    assert all(r["origine_reference"] == "gemini" for r in comparaisons)
    manuel = comparer_annonces(m, a, origine_reference="comptage_manuel")
    assert all(r["origine_reference"] == "comptage_manuel" for r in manuel)
    assert all(r["protocole_reference"] == "DECLARATION_A_VERIFIER" for r in manuel)


def test_comparaison_inconnue_rejetee(nlp):
    m = calculer_metriques_globales("Chat.", nlp)
    with pytest.raises(KeyError):
        comparer_annonces(m, [{"cle": "complexite", "valeur": 2,
                                "decimales": 0, "unite": "indice"}])


def test_annonces_fournies_arithmetiquement_coherentes():
    """Ces affirmations testent l'arithmétique du tableau, pas l'exactitude corpus."""
    # Les valeurs sont indépendamment reprises du tableau transmis par l'enseignant.
    n, v, h, s = 79540, 8633, 4609, 3829
    assert round(v / n, 4) == 0.1085
    assert round(100 * v / n, 2) == 10.85
    assert round(100 * h / v, 2) == 53.39
    assert round(n / s, 2) == 20.77
