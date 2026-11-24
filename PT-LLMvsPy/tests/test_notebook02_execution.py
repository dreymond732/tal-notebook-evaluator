"""Parcours élève du 02 sur un texte dont les effectifs se recomptent à la main."""
import json
from pathlib import Path

import spacy
from spacy.language import Language

from tal_toolkit import charger_corpus, corpus_depuis_texte

PT = Path(__file__).resolve().parents[1]


# Cette annotation déterministe teste l'effet du regroupement sans nécessiter
# un téléchargement de modèle pendant la CI. Elle ne mesure pas sa qualité.
@Language.component("annoter_microcorpus_pt02")
def annoter_microcorpus(doc):
    for token in doc:
        token.lemma_ = {"femmes": "femme", "droits": "droit"}.get(token.lower_, token.lower_)
    return doc


def test_cahier_complet_sur_microcorpus(tmp_path):
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
    source = (PT / "notebooks/02_comparer_les_frequences_des_formes_et_des_lemmes.ipynb").read_text(encoding="utf-8")
    for cellule in json.loads(source)["cells"]:
        if cellule["cell_type"] == "code" and cellule["id"] != "initialisation-pt":
            exec(compile("".join(cellule["source"]), cellule["id"], "exec"), contexte)
    mesures = json.loads(sortie.read_text(encoding="utf-8"))
    protocoles = mesures["mesures"]
    assert [protocoles[f]["tokens"] for f in (
        "tous_sans_espaces", "sans_ponctuation", "alphabetiques",
    )] == [15, 10, 9]
    assert protocoles["alphabetiques"]["phrases"] == 3
    assert protocoles["alphabetiques"]["types"] == 8
    assert protocoles["alphabetiques · lemmes"]["types"] == 5
    assert protocoles["alphabetiques · lemmes"]["hapax"] == 3
    assert mesures["globales"]["sttr"] is None
    assert mesures["globales"]["ttr"] == 1
    assert mesures["globales_formes"]["ttr"] == 8 / 9
    champs = {x["champ"]: x for x in mesures["champs"]}
    assert (champs["droit_institutions"]["formes"], champs["droit_institutions"]["lemmes"]) == (1, 2)
    assert len(mesures["annonces"]) == len(annonces["annonces"])
    preuve = mesures["preuve_champ"]
    assert contexte["corpus"].texte[preuve["debut"]:preuve["fin"]] == "droits"
    assert mesures["frequences_meme_entree"]["droit"] == {"formes": 1, "lemmes": 2, "écart": 1}
    assert mesures["ecarts_mesures"]["retrait de la ponctuation"]["N"] == -5
    assert mesures["preuve_vote"] is None
    travail = mesures["travail_03"]
    assert travail["studio"] == {"pivots": ["femme", "femmes"], "associes": ["homme", "hommes"],
                                "annonce_phrases": 208}
    assert travail["m4"] == {"pivot": "femme", "associe": "droit", "statut": "NON_CALCULE"}
    assert mesures["essais_personnels"]["annonce"]["statut_numerique"] == "MEME_VALEUR_A_L_ARRONDI"


def test_annotation_absente_ou_elargie_au_token():
    (chemin,) = (PT / "notebooks").glob("02_*.ipynb")
    source = chemin.read_text(encoding="utf-8")
    cellule = next(c for c in json.loads(source)["cells"] if c["id"] == "annotation-faguet")
    code = "".join(cellule["source"])
    corpus = corpus_depuis_texte("Je vote aux élections.")
    modele = spacy.blank("fr")
    modele.add_pipe("sentencizer")
    contexte = {"corpus": corpus, "document": modele("")}
    exec(code, contexte)
    assert contexte["preuve_vote"] is None

    modele.tokenizer.add_special_case("vote aux", [{"ORTH": "vote aux"}])
    contexte["document"] = modele(corpus.texte)
    exec(code, contexte)
    preuve = contexte["preuve_vote"]
    assert preuve["forme"] == "vote aux"
    assert corpus.texte[preuve["debut"]:preuve["fin"]] == preuve["forme"]
