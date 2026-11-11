"""Tests pédagogiques sur microcorpus indépendants du corpus Faguet."""
import hashlib
import pytest

from tal_toolkit import (
    DocCache, charger_corpus, corpus_depuis_texte, tokeniser_phrases,
    frequences, concordances_exactes, contient_expression, mesurer,
    table_contingence, proportion, pour_mille, pmi_phrase,
    couverture_pivots, verifier_citation, champs_manquants,
    comparer_intervalle, evaluer_affirmation,
)


def test_corpus_preserve_les_octets(tmp_path):
    fichier = tmp_path / "texte.txt"
    original = "L’archive.\r\nDeux lignes.\n".encode("utf-8")
    fichier.write_bytes(original)
    objet = charger_corpus(fichier, sha256_attendu=hashlib.sha256(original).hexdigest())
    assert objet.texte == original.decode("utf-8")
    assert objet.sha256 == hashlib.sha256(original).hexdigest()


def test_corpus_refuse_empreinte_fausse(tmp_path):
    f = tmp_path / "texte.txt"
    f.write_text("Texte", encoding="utf-8")
    with pytest.raises(ValueError):
        charger_corpus(f, sha256_attendu="0" * 64)


def test_microcorpus_sha256():
    assert corpus_depuis_texte("abc").sha256 == hashlib.sha256(b"abc").hexdigest()


def test_frequences_deterministes():
    lignes = frequences(["chat", "livre", "chat", "arbre"])
    assert [(r["terme"], r["effectif"]) for r in lignes] == [
        ("chat", 2), ("arbre", 1), ("livre", 1)
    ]
    assert lignes[0]["total"] == 4
    assert lignes[0]["pour_mille"] == 500


def test_concordances_positions_et_non_chevauchement():
    source = "aaaa"
    resultats = concordances_exactes(source, "aa", largeur=2)
    assert [(r["debut"], r["fin"]) for r in resultats] == [(0, 2), (2, 4)]
    assert all(source[r["debut"]:r["fin"]] == r["pivot"] for r in resultats)


@pytest.mark.parametrize("motif,largeur", [("", 1), ("x", -1)])
def test_concordances_refuse_parametres_invalides(motif, largeur):
    with pytest.raises(ValueError):
        concordances_exactes("abc", motif, largeur)


def test_expression_contigue():
    assert contient_expression(["grande", "salle", "ouverte"], ["grande", "salle"])
    assert not contient_expression(["grande", "porte", "salle"], ["grande", "salle"])


def test_expression_vide_refusee():
    with pytest.raises(ValueError):
        contient_expression(["chat"], [])


def test_union_par_phrase_et_marges():
    m = mesurer(
        [["chat", "livre", "chat"], ["livre"], ["chat", "plume"], ["plume"]],
        [["chat"]], [["livre"]],
    )
    assert (m["N"], m["cooc"], m["marge_pivot"], m["marge_associe"]) == (4, 1, 2, 2)
    assert m["indices_cooc"] == [0]
    assert table_contingence(m) == {"n11": 1, "n10": 1, "n01": 1, "n00": 1}


def test_somme_paires_nequivaut_pas_union():
    corpus = [["chat", "livre", "plume"], ["chat", "livre"], ["plume"]]
    uni = mesurer(corpus, [["chat"]], [["livre"], ["plume"]], "union")
    somme = mesurer(corpus, [["chat"]], [["livre"], ["plume"]], "somme_paires")
    assert uni["cooc"] == 2
    assert somme["cooc"] == 3
    assert somme["indices_cooc"] == [0, 1]
    with pytest.raises(ValueError):
        table_contingence(somme)


def test_agregation_invalide_et_expression_vide():
    with pytest.raises(ValueError):
        mesurer([["chat"]], [], [["chat"]])
    with pytest.raises(ValueError):
        mesurer([["chat"]], [["chat"]], [["chat"]], "inconnu")


def test_taux_denominateurs_nuls():
    assert proportion(0, 0) is None
    assert proportion(0, 5) == 0
    assert pour_mille(4, 100) == 40
    with pytest.raises(ValueError):
        proportion(3, 2)


def test_pmi_en_phrases_et_zero():
    m = mesurer([["a", "b"], ["a"], ["b"], ["autre"]], [["a"]], [["b"]])
    assert pmi_phrase(m) == 0.0
    absent = mesurer([["a"], ["b"]], [["a"]], [["b"]])
    assert pmi_phrase(absent) is None


def test_couverture_fenetre_positions():
    tokens = ["chat", "lit", "un", "livre", "chat", "lit"]
    assert couverture_pivots(tokens, "chat", "livre", 1)["effectif"] == 1
    assert couverture_pivots(tokens, "chat", "livre", 3)["effectif"] == 2


def test_citation_exacte_conserve_span():
    source = "La preuve vient du texte."
    r = verifier_citation(source, "preuve vient")
    assert r["statut"] == "EXACTE"
    assert source[r["debut"]:r["fin"]] == "preuve vient"


def test_citation_normalisee_et_positions_originales():
    source = "L’archive   décrit."
    r = verifier_citation(source, "l'archive décrit.")
    assert r["statut"] == "NORMALISEE"
    assert source[r["debut"]:r["fin"]] == source


def test_citation_candidate_jamais_validee():
    source = "La mer traverse la ville."
    r = verifier_citation(source, "La mer longe la ville.", candidat=(0, len(source)))
    assert r["statut"] == "CANDIDAT_APPROCHE"
    assert r["passage_source"] == source


def test_citation_absente():
    r = verifier_citation("La rivière traverse la ville.", "mer lointaine")
    assert r["statut"] == "NON_RETROUVEE"
    assert (r["debut"], r["fin"]) == (-1, -1)


def test_citation_candidat_invalide():
    with pytest.raises(ValueError):
        verifier_citation("abc", "x", candidat=(3, 4))


def test_audit_protocole_incomplet():
    a = {"unite": None, "fenetre": None, "normalisation": None}
    assert champs_manquants(a) == ["unite", "fenetre", "normalisation", "agregation"]
    assert evaluer_affirmation(a, 3, protocole_comparable=True) == "INSUFFISAMMENT_DEFINI"


def test_audit_champs_complets_non_comparables():
    a = {"unite": "phrase", "fenetre": "phrase", "normalisation": "forme",
         "agregation": "union", "intervalle": [2, 4]}
    assert evaluer_affirmation(a, 3, protocole_comparable=False) == "NON_COMPARABLE"
    assert evaluer_affirmation(a, 3, protocole_comparable=True) == "compatible selon le protocole"
    assert evaluer_affirmation(a, 5, protocole_comparable=True) == "contredit selon le protocole"


def test_intervalle_bornes_inclusives():
    assert comparer_intervalle(2, 2, 4) == "compatible selon le protocole"
    assert comparer_intervalle(4, 2, 4) == "compatible selon le protocole"
    with pytest.raises(ValueError):
        comparer_intervalle(3, 4, 2)


def test_cache_spacy_et_tokenisation():
    spacy = pytest.importorskip("spacy")
    nlp = spacy.blank("fr")
    nlp.add_pipe("sentencizer")
    cache = DocCache(capacite=1)
    a = cache.analyser(nlp, "Une grande salle. Un livre.")
    assert cache.analyser(nlp, "Une grande salle. Un livre.") is a
    assert tokeniser_phrases(a, mode="forme") == [
        ["une", "grande", "salle", "."], ["un", "livre", "."]
    ]
    cache.analyser(nlp, "Autre texte.")
    assert cache.analyser(nlp, "Une grande salle. Un livre.") is not a


def test_lemmes_absents_sont_refuses():
    spacy = pytest.importorskip("spacy")
    nlp = spacy.blank("fr")
    nlp.add_pipe("sentencizer")
    with pytest.raises(ValueError):
        tokeniser_phrases(nlp("Une salle."), mode="lemme")
