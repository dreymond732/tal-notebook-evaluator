"""Une exploration personnelle ne doit pas remplacer les preuves communes reprises au 04."""
import json
from pathlib import Path

import spacy
from spacy.language import Language

from scripts.verifier_notebook02 import executer_cahier
from tal_toolkit import atelier


NOTEBOOKS = Path(__file__).resolve().parents[1] / "notebooks"


@Language.component("lemmes_essai_transfert")
def lemmes_essai_transfert(doc):
    for token in doc:
        token.lemma_ = {"femmes": "femme", "hommes": "homme"}.get(token.lower_, token.lower_)
    return doc


def test_couple_personnel_et_deux_questions_communes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    modele = spacy.blank("fr")
    modele.add_pipe("sentencizer")
    modele.add_pipe("lemmes_essai_transfert", name="lemmatizer")
    monkeypatch.setattr(atelier, "charger_modele_francais", lambda: modele)
    dossier = tmp_path
    numero = "00123456"
    texte = ("Une femme parle à un homme.\n\nLes femmes et les hommes lisent, 2 fois. "
             "Une femme revendique un droit. La loi prévoit une peine. "
             "Une loi modifie la peine. La peine relève de la loi.")
    (dossier / f"faguet_nettoye_{numero}.txt").write_text(texte, encoding="utf-8")
    executer_cahier(NOTEBOOKS / "02_mesures_lexicales.ipynb", numero)

    r2 = json.loads((dossier / f"resultats_02_{numero}.json").read_text(encoding="utf-8"))
    mesures = r2["mesures"]
    doc = modele(texte)
    assert r2["globales"]["tokens_bruts_spacy"] == len(doc)
    hors_espaces = mesures["tous_sans_espaces"]["tokens"]
    sans_ponctuation = mesures["sans_ponctuation"]["tokens"]
    assert r2["decompte_tokens"] == {
        "tokens_bruts_spacy": len(doc), "len_doc": len(doc),
        "tokens_is_space": 1, "tous_sans_espaces": hors_espaces,
    }
    assert r2["logiciel_formes"]["pipeline"] == ["sentencizer"]
    assert len(doc) - hors_espaces == 1  # Le double retour forme un token d'espacement.
    assert hors_espaces - sans_ponctuation == sum(t.is_punct for t in doc)
    assert sans_ponctuation - mesures["alphabetiques"]["tokens"] == 1  # Le chiffre 2.
    assert mesures["alphabetiques · lemmes"]["tokens"] == mesures["alphabetiques"]["tokens"]

    # L’étudiant saisit ses deux lemmes dans la copie personnelle du notebook.
    cahier = json.loads((NOTEBOOKS / "03_relations_lexicales.ipynb").read_text(encoding="utf-8"))
    cellule = next(c for c in cahier["cells"] if c.get("id") == "couple-perso")
    cellule["source"] = "".join(cellule["source"]).replace(
        'pivot_libre, associe_libre = "", ""', 'pivot_libre, associe_libre = "loi", "peine"'
    )
    suite = next(c for c in cahier["cells"] if c.get("id") == "micro-ngrammes")
    suite["source"] = "".join(suite["source"]).replace('ma_suite = "loi juste"', 'ma_suite = "les femmes"')
    copie = tmp_path / "03_personnel.ipynb"
    copie.write_text(json.dumps(cahier), encoding="utf-8")
    executer_cahier(copie, numero)
    executer_cahier(NOTEBOOKS / "04_audit_llm.ipynb", numero)

    r3 = json.loads((dossier / f"resultats_03_{numero}.json").read_text(encoding="utf-8"))
    r4 = json.loads((dossier / f"resultats_04_{numero}.json").read_text(encoding="utf-8"))
    assert r3["transfert"]["mesure"]["cooc"] == 3
    principal = r3["studio"]["principal"]
    assert (principal["annonce"], principal["calcule"]) == (208, 2)
    assert r3["agregations"]["essai"] == {"union": 2, "somme_paires": 3, "memes_indices": True}
    assert r3["statistiques_phrases"]["studio"]["n11"] == principal["calcule"]
    suites = {r["mode"]: (r["cible recherchée"], r["effectif"])
              for r in r3["sequences"] if r["tokens"] == "alphabetiques"}
    assert suites == {"forme": ("les femmes", 1), "lemme": ("les femme", 1)}
    assert r4["studio"]["principal_03"] == principal
    relation = r3["relation"]
    assert (relation["pivot"], relation["associe"], relation["mesure"]["cooc"]) == ("femme", "droit", 1)
    assert r4["protocole_B"]["relation_03"] == relation
    assert r4["protocole_B"]["valeur_annoncee"] is None
