"""Parcours élève du 02 sur un texte dont les effectifs se recomptent à la main."""
import json
from pathlib import Path

import spacy
from spacy.language import Language

from tal_toolkit import charger_corpus

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
    modele.add_pipe("sentencizer")
    modele.add_pipe("annoter_microcorpus_pt02", name="lemmatizer")
    fichier = tmp_path / "faguet_nettoye.txt"
    fichier.write_text("Femmes, 2 droits ! La femme a un droit.", encoding="utf-8")
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
    )] == [11, 8, 7]
    assert protocoles["alphabetiques"]["phrases"] == 2
    assert protocoles["alphabetiques"]["types"] == 7
    assert protocoles["alphabetiques · lemmes"]["types"] == 5
    assert protocoles["alphabetiques · lemmes"]["hapax"] == 3
    assert mesures["globales"]["sttr"] is None
    champs = {x["champ"]: x for x in mesures["champs"]}
    assert (champs["droit_institutions"]["formes"], champs["droit_institutions"]["lemmes"]) == (1, 2)
    assert len(mesures["annonces"]) == len(annonces["annonces"])
    preuve = mesures["preuve_champ"]
    assert contexte["corpus"].texte[preuve["debut"]:preuve["fin"]] == "droits"
    assert mesures["frequences_meme_entree"]["droit"] == {"formes": 1, "lemmes": 2, "écart": 1}
    assert mesures["ecarts_mesures"]["retrait de la ponctuation"]["N"] == -3
    assert mesures["preuve_vote"] is None
    travail = mesures["travail_03"]
    assert travail["studio"] == {"pivots": ["femme", "femmes"], "associes": ["homme", "hommes"],
                                "annonce_phrases": 208}
    assert travail["m4"] == {"pivot": "femme", "associe": "droit", "statut": "NON_CALCULE"}
    assert mesures["essais_personnels"]["annonce"]["statut_numerique"] == "MEME_VALEUR_A_L_ARRONDI"
