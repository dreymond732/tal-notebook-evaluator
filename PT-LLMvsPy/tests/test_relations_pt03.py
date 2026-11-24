"""Contrats des mesures comparées en classe, sur des phrases dénombrables."""
import pytest

from tal_toolkit import compter_paires_fenetre, couverture_pivots, extraire_ngrammes, frequences
from tal_toolkit.linguistic import tokeniser_phrases
from tal_toolkit.textometry import bilan_fenetres, frequences_ngrammes


def test_fenetres_couverture_paires_et_frontieres():
    phrases = [["loi", ",", "droit", "droit"], ["loi"]]
    assert bilan_fenetres(phrases, "loi", "droit", 2) == {
        "pivots": 2, "pivots_couverts": 1, "paires": 1,
    }
    assert bilan_fenetres(phrases, "loi", "droit", 3)["paires"] == 2
    assert bilan_fenetres(phrases, "loi", "droit", 3)["pivots_couverts"] == 1
    assert bilan_fenetres(phrases, "loi", "droit", 0)["paires"] == 0


def test_paires_distinguent_repetitions_et_frontieres():
    phrases = [["droit", ",", "loi", "droit"], ["loi"]]
    premiere, seconde = phrases
    assert compter_paires_fenetre(premiere, "loi", "droit", 0) == 0
    assert compter_paires_fenetre(premiere, "loi", "droit", 1) == 1
    assert compter_paires_fenetre(premiere, "loi", "droit", 2) == 2
    assert couverture_pivots(premiere, "loi", "droit", 2)["effectif"] == 1
    assert compter_paires_fenetre(seconde, "loi", "droit", 2) == 0
    assert compter_paires_fenetre(premiere + seconde, "loi", "droit", 2) == 3
    with pytest.raises(ValueError):
        compter_paires_fenetre(premiere, "loi", "loi", 1)
    with pytest.raises(ValueError):
        compter_paires_fenetre(premiere, "loi", "droit", -1)


def test_extraction_ngrammes_conserve_ordre_ponctuation_et_repetitions():
    phrases = [["loi", ",", "droit"], [], ["loi", ","]]
    bigrammes = extraire_ngrammes(phrases, 2)
    assert bigrammes == ["loi ,", ", droit", "loi ,"]
    assert frequences(bigrammes) == frequences_ngrammes(phrases, 2)
    assert extraire_ngrammes(phrases, 3) == ["loi , droit"]
    assert extraire_ngrammes(phrases, 4) == []
    with pytest.raises(ValueError):
        extraire_ngrammes(phrases, 0)


def test_ngrammes_comptent_les_repetitions_et_respectent_les_phrases():
    phrases = [["loi", "et", "loi", "et"], ["droit"]]
    bigrammes = frequences_ngrammes(phrases, 2)
    assert [(r["terme"], r["effectif"]) for r in bigrammes] == [("loi et", 2), ("et loi", 1)]
    assert {r["terme"] for r in frequences_ngrammes(phrases, 3)} == {"loi et loi", "et loi et"}


def test_filtres_portent_sur_la_forme_et_preservent_les_indices():
    spacy = pytest.importorskip("spacy")
    from spacy.tokens import Doc

    vocab = spacy.blank("fr").vocab
    doc = Doc(vocab, words=["3", "lois", ".", "!"], sent_starts=[True, False, False, True],
              lemmas=["trois", "loi", ".", "!"])
    assert tokeniser_phrases(doc, mode="lemme", tokens="sans_ponctuation") == [
        ["trois", "loi"], [],
    ]
    assert tokeniser_phrases(doc, mode="lemme", tokens="alphabetiques") == [["loi"], []]
