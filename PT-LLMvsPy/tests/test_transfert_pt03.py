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
    dossier = tmp_path / "PT-Faguet"
    dossier.mkdir()
    texte = ("Une femme parle à un homme. Les femmes et les hommes lisent. "
             "Une femme revendique un droit. La loi prévoit une peine. "
             "Une loi modifie la peine. La peine relève de la loi.")
    (dossier / "faguet_nettoye.txt").write_text(texte, encoding="utf-8")
    executer_cahier(NOTEBOOKS / "02_mesures_lexicales.ipynb")

    # L’étudiant saisit ses deux lemmes dans la copie personnelle du notebook.
    cahier = json.loads((NOTEBOOKS / "03_relations_lexicales.ipynb").read_text(encoding="utf-8"))
    cellule = next(c for c in cahier["cells"] if c.get("id") == "couple-perso")
    cellule["source"] = "".join(cellule["source"]).replace(
        'pivot_libre, associe_libre = "", ""', 'pivot_libre, associe_libre = "loi", "peine"'
    )
    copie = tmp_path / "03_personnel.ipynb"
    copie.write_text(json.dumps(cahier), encoding="utf-8")
    executer_cahier(copie)
    executer_cahier(NOTEBOOKS / "04_audit_llm.ipynb")

    r3 = atelier.lire_resultats(dossier, "03")
    r4 = atelier.lire_resultats(dossier, "04")
    assert r3["transfert"]["mesure"]["cooc"] == 3
    principal = r3["studio"]["principal"]
    assert (principal["annonce"], principal["calcule"]) == (208, 2)
    assert r4["studio"]["principal_03"] == principal
    relation = r3["relation"]
    assert (relation["pivot"], relation["associe"], relation["mesure"]["cooc"]) == ("femme", "droit", 1)
    assert r4["protocole_B"]["relation_03"] == relation
    assert r4["protocole_B"]["valeur_annoncee"] is None
