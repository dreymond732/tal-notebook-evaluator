"""Contrats des mesures comparées en classe, sur des phrases dénombrables."""
import pytest

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
