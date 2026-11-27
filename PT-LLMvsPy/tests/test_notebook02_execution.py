"""Parcours du cahier sur les fréquences, avec des effectifs vérifiables à la main."""
import json
from collections import Counter
from pathlib import Path

import pytest
import spacy
from spacy.language import Language

from scripts.verifier_notebook02 import executer_cellule
from tal_toolkit import charger_corpus, corpus_depuis_texte

PT = Path(__file__).resolve().parents[1]
CAHIER = PT / "notebooks/02_comparer_les_frequences_des_formes_et_des_lemmes.ipynb"


# Cette annotation déterministe teste l'effet du regroupement sans nécessiter
# un téléchargement de modèle pendant la CI. Elle ne mesure pas sa qualité.
@Language.component("annoter_microcorpus_pt02")
def annoter_microcorpus(doc):
    for token in doc:
        token.lemma_ = {"femmes": "femme", "droits": "droit"}.get(token.lower_, token.lower_)
    return doc


@pytest.mark.parametrize("personnaliser", [False, True], ids=["version-fournie", "filtre-et-unite-modifies"])
def test_cahier_complet_sur_microcorpus(tmp_path, personnaliser):
    modele = spacy.blank("fr")
    # Deux découpages réellement distincts rendent observable l'origine du TTR exporté.
    modele.tokenizer.add_special_case("Femme-médecin", [{"ORTH": "Femme-médecin"}])
    modele.add_pipe("sentencizer")
    modele.add_pipe("annoter_microcorpus_pt02", name="lemmatizer")
    fichier = tmp_path / "faguet_nettoye.txt"
    fichier.write_text("Femmes, 2 droits ! La femme a un droit. Femme-médecin.", encoding="utf-8")
    annonces = json.loads((PT / "data/annonces_globales_gemini.json").read_text(encoding="utf-8"))
    sortie = tmp_path / "resultats_02.json"

    def enregistrer(numero, resultats):
        assert numero == "02"
        sortie.write_text(json.dumps(resultats, ensure_ascii=False), encoding="utf-8")

    contexte = {
        "corpus": charger_corpus(fichier),
        "dossier": tmp_path,
        "lire_annonces_globales": lambda: annonces,
        "charger_modele_francais": lambda: modele,
        "enregistrer_resultats": enregistrer,
        "display": lambda tableau: None,
    }
    for cellule in json.loads(CAHIER.read_text(encoding="utf-8"))["cells"]:
        if cellule["cell_type"] == "code" and cellule["id"] != "initialisation-pt":
            source = "".join(cellule["source"])
            if personnaliser and "def filtrer(document):" in source:
                source = source.replace("    return selections", (
                    '    selections["terminaison_s"] = [t for t in document if t.lower_.endswith("s")]\n'
                    '    return selections'
                ))
            if personnaliser and "def compter_ma_version(tokens):" in source:
                source = source.replace('filtre_choisi = "personnel"', 'filtre_choisi = "terminaison_s"')
                source = source.replace("[t.text for t in tokens]", "[t.lemma_.lower() for t in tokens]")
            executer_cellule(source, cellule["id"], contexte)
    mesures = json.loads(sortie.read_text(encoding="utf-8"))
    protocoles = mesures["mesures"]
    assert [protocoles[f]["tokens"] for f in (
        "tous_sans_espaces", "sans_ponctuation", "alphabetiques",
    )] == [13, 9, 7]
    assert protocoles["alphabetiques"]["phrases"] == 2  # « Femme-médecin. » n'a aucun token alphabétique.
    assert protocoles["alphabetiques"]["unites_distinctes"] == 7
    assert protocoles["alphabetiques · lemmes"]["tokens"] == 7
    assert protocoles["alphabetiques · lemmes"]["phrases"] == 2
    assert protocoles["alphabetiques · lemmes"]["unites_distinctes"] == 5
    assert protocoles["alphabetiques · lemmes"]["hapax"] == 3
    assert mesures["formes_comparables"] == protocoles["alphabetiques"]
    assert mesures["meme_decoupage"] is False
    assert mesures["globales"]["sttr"] is None
    assert mesures["globales"]["ttr"] == 1
    assert mesures["globales_formes"]["ttr"] == 8 / 9
    champs = {x["champ"]: x for x in mesures["champs"]}
    assert (champs["droit_institutions"]["formes"], champs["droit_institutions"]["lemmes"]) == (1, 2)
    assert len(mesures["annonces"]) == len(annonces["annonces"])
    preuve = mesures["preuve_champ"]
    assert contexte["corpus"].texte[preuve["debut"]:preuve["fin"]] == "droits"
    assert mesures["frequences_meme_entree"]["droit"] == {"formes": 1, "lemmes": 2, "écart": 1}
    assert mesures["ecarts_mesures"]["retrait de la ponctuation"]["N"] == -4
    assert mesures["preuve_vote"] is None
    travail = mesures["travail_03"]
    assert travail["studio"] == {"pivots": ["femme", "femmes"], "associes": ["homme", "hommes"],
                                "annonce_phrases": 208}
    assert travail["m4"] == {"pivot": "femme", "associe": "droit", "statut": "NON_CALCULE"}
    assert mesures["essais_personnels"]["annonce"]["statut_numerique"] == "MEME_VALEUR_A_L_ARRONDI"

    variante = mesures["variante_personnelle"]
    if personnaliser:
        assert variante["filtre"] == "terminaison_s"
        assert variante["frequences_exemple"] == {"ces": 1, "femme": 1}
        assert variante["frequences_livre"] == {"femme": 1, "droit": 1}
        assert 'selections["terminaison_s"]' in variante["selection"]
        assert "t.lemma_.lower()" in variante["comptage"]
    else:
        assert variante["filtre"] == "personnel"
        assert variante["frequences_exemple"] == {"femmes": 1, "votent": 1, "femme": 1}
        assert variante["frequences_livre"] == {"Femmes": 1, "droits": 1, "femme": 1, "droit": 1}
    assert variante["mesures_livre"]["N"] == sum(variante["frequences_livre"].values())


def test_annotation_vote_exige_un_token_aux_bornes_exactes():
    cellules = json.loads(CAHIER.read_text(encoding="utf-8"))["cells"]
    cellule = next(c for c in cellules if c["id"] == "annotation-faguet")
    code = "".join(cellule["source"])
    modele = spacy.blank("fr")
    modele.add_pipe("sentencizer")
    corpus = corpus_depuis_texte("Je participe aux élections.")
    contexte = {"corpus": corpus, "document": modele(corpus.texte)}
    executer_cellule(code, cellule["id"], contexte)
    assert contexte["preuve_vote"] is None

    corpus = corpus_depuis_texte("Je vote aux élections.")
    document = modele(corpus.texte)
    # Une annotation témoin vérifie que la cellule rapporte bien la sortie du modèle injecté.
    document[1].pos_, document[1].lemma_ = "VERB", "voter"
    contexte.update(corpus=corpus, document=document, modele=modele, spacy=spacy,
                    freq_lemmes=Counter(t.lemma_ for t in document))
    executer_cellule(code, cellule["id"], contexte)
    assert contexte["preuve_vote"] == {
        "phrase": corpus.texte, "debut": 3, "fin": 7,
        "forme": "vote", "categorie": "VERB", "lemme": "voter",
    }

    modele.tokenizer.add_special_case("vote aux", [{"ORTH": "vote aux"}])
    contexte["document"] = modele(corpus.texte)
    executer_cellule(code, cellule["id"], contexte)
    assert contexte["preuve_vote"] is None

    modele = spacy.blank("fr")
    modele.tokenizer.add_special_case("vote", [{"ORTH": "vo"}, {"ORTH": "te"}])
    contexte["document"] = modele(corpus.texte)
    executer_cellule(code, cellule["id"], contexte)
    assert contexte["preuve_vote"] is None
