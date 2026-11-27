"""Une exploration personnelle ne doit pas remplacer les preuves communes reprises dans le cahier de vérification des affirmations."""
import json
from pathlib import Path

import pytest
import spacy
from spacy.language import Language

from scripts.verifier_notebook02 import executer_cahier
from tal_toolkit import atelier, verifier_citation
from tal_toolkit.audit_llm import concordances_expression


NOTEBOOKS = Path(__file__).resolve().parents[1] / "notebooks"


@Language.component("lemmes_essai_transfert")
def lemmes_essai_transfert(doc):
    for token in doc:
        token.lemma_ = {"femmes": "femme", "hommes": "homme"}.get(token.lower_, token.lower_)
    return doc


@pytest.mark.parametrize("variante", [False, True], ids=["consignes-du-cahier", "consignes-du-json"])
def test_couple_personnel_et_deux_questions_communes(tmp_path, monkeypatch, capsys, variante):
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
    executer_cahier(NOTEBOOKS / "02_comparer_les_frequences_des_formes_et_des_lemmes.ipynb", numero)

    fichier_frequences = dossier / f"resultats_02_{numero}.json"
    r2 = json.loads(fichier_frequences.read_text(encoding="utf-8"))
    travail = r2["travail_03"]
    if variante:
        # Des valeurs différentes de l'exemple distinguent la lecture du JSON d'un calcul figé.
        travail["studio"] = {"pivots": ["loi", "lois"], "associes": ["peine", "peines"], "annonce_phrases": 17}
        travail["m4"].update(pivot="femme", associe="homme")
        travail["regle_phrase"] = "Compter chaque phrase commune une seule fois."
        # Les exports du 02 antérieurs à l'introduction du filtre personnel restent lisibles.
        del r2["variante_personnelle"]
        # La mesure commune provient de la même ligne alphabétique que les ratios.
        r2["globales"]["tokens_lexicaux"] += 1
        fichier_frequences.write_text(json.dumps(r2, ensure_ascii=False), encoding="utf-8")
    else:
        assert travail["studio"] == {"pivots": ["femme", "femmes"], "associes": ["homme", "hommes"], "annonce_phrases": 208}
        assert travail["m4"] == {"pivot": "femme", "associe": "droit", "statut": "NON_CALCULE"}
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
    cahier = json.loads((NOTEBOOKS / "03_mesurer_les_cooccurrences_par_phrase_et_par_fenetre.ipynb").read_text(encoding="utf-8"))
    cellules = {c["id"]: c for c in cahier["cells"]}
    cellule = cellules["couple-perso"]
    cellule["source"] = "".join(cellule["source"]).replace(
        'pivot_libre, associe_libre = "", ""', 'pivot_libre, associe_libre = "loi", "peine"'
    )
    suite = cellules["micro-ngrammes"]
    suite["source"] = "".join(suite["source"]).replace('ma_suite = "loi juste"', 'ma_suite = "les femmes"')
    if variante:
        cellule["source"] = cellule["source"].replace('filtre_libre = "sans_ponctuation"', 'filtre_libre = "personnel"')
        filtre = cellules["filtre-personnel"]
        filtre["source"] = "".join(filtre["source"]).replace("len(t.text) >= 5", "len(t.text) >= 60")
        rayons = cellules["choisir-rayons"]
        rayons["source"] = "".join(rayons["source"]).replace("= 5, 10", "= 3, 10")
        fenetre = cellules["micro-fenetre"]
        fenetre["source"] = "".join(fenetre["source"]).replace(
            '["loi", ",", "droit", "droit"]', '["droit", ",", "loi", "droit"]'
        )
        # L'étudiant prépare un nouvel essai après le calcul, puis exporte les mesures précédentes.
        export = cellules["exporter"]
        export["source"] = 'def filtrer_phrase(phrase):\n    return list(phrase)\n\n' + "".join(export["source"])
    copie = tmp_path / "03_personnel.ipynb"
    copie.write_text(json.dumps(cahier), encoding="utf-8")
    capsys.readouterr()
    executer_cahier(copie, numero)
    affichage = capsys.readouterr().out
    assert "def mesurer(" in affichage
    if variante:
        assert "[(2, 0), (2, 3)]" in affichage
        assert "[(1, 0), (1, 2)]" in affichage
    else:
        assert "[(0, 2)]" in affichage
        assert "[(0, 1), (0, 2)]" in affichage
    executer_cahier(NOTEBOOKS / "04_verifier_une_affirmation_par_le_calcul_et_la_lecture.ipynb", numero)

    r3 = json.loads((dossier / f"resultats_03_{numero}.json").read_text(encoding="utf-8"))
    r4 = json.loads((dossier / f"resultats_04_{numero}.json").read_text(encoding="utf-8"))
    assert r3["transfert"]["mesure"]["cooc"] == (0 if variante else 3)
    personnel = r4["lectures_personnelles"]
    assert personnel["cooccurrences_03"] == r3["transfert"]
    if variante:
        assert personnel["frequences_02"] is None
        assert personnel["condition_filtre_03"] == r3["filtre_personnel"]
    else:
        vue_02 = r2["variante_personnelle"]
        for cle in ("filtre", "selection", "comptage", "mesures_livre"):
            assert personnel["frequences_02"][cle] == vue_02[cle]
    seuil = 60 if variante else 5
    assert f"len(t.text) >= {seuil}" in r3["filtre_personnel"]
    unites_personnelles = {r["mode"]: (r["phrases"], r["positions"])
                           for r in r3["unites"] if r["tokens"] == "personnel"}
    n_phrases = sum(any(t.is_alpha for t in phrase) for phrase in doc.sents)
    n_positions = sum(t.is_alpha and len(t.text) >= seuil for t in doc)
    assert unites_personnelles == {"forme": (n_phrases, n_positions), "lemme": (n_phrases, n_positions)}
    for tableau in ("fenetres", "fenetres_continues"):
        assert {r["rayon"] for r in r3[tableau]} == ({3, 10} if variante else {5, 10})
        pivots = {r["mode"]: r["pivots"] for r in r3[tableau] if r["tokens"] == "personnel"}
        assert pivots == ({"forme": 0, "lemme": 0} if variante else {"forme": 2, "lemme": 3})
    principal = r3["studio"]["principal"]
    studio = travail["studio"]
    assert principal["conventions"]["pivots"] == studio["pivots"]
    assert principal["conventions"]["associes"] == studio["associes"]
    assert all(forme in principal["ligne"] for forme in studio["pivots"] + studio["associes"])
    assert principal["annonce"] == studio["annonce_phrases"]
    assert principal["calcule"] == (3 if variante else 2)
    assert principal["ecart"] == principal["calcule"] - studio["annonce_phrases"]
    assert r3["regle_02"] == travail["regle_phrase"]
    assert r3["agregations"]["essai"] == {"union": 2, "somme_paires": 3, "memes_indices": True}
    assert r3["statistiques_phrases"]["studio"]["n11"] == principal["calcule"]
    suites = {r["mode"]: (r["cible recherchée"], r["effectif"])
              for r in r3["sequences"] if r["tokens"] == "alphabetiques"}
    assert suites == {"forme": ("les femmes", 1), "lemme": ("les femme", 1)}
    assert r4["studio"]["principal_03"] == principal
    relation = r3["relation"]
    assert (relation["pivot"], relation["associe"]) == (travail["m4"]["pivot"], travail["m4"]["associe"])
    assert relation["mesure"]["cooc"] == (2 if variante else 1)
    assert r4["protocole_B"]["statut_source"] == relation["statut_source"] == travail["m4"]["statut"]
    assert r4["protocole_B"]["relation_03"] == relation
    assert r4["protocole_B"]["valeur_annoncee"] is None

    reference = r2["mesures"]["alphabetiques"]
    assert r4["annonce_A"]["mesure_02"] == reference["tokens"]
    ratios = r4["ratios_A"]["mesures"]
    assert ratios["ttr"]["ratio sur votre texte"] == reference["unites_distinctes"] / reference["tokens"]
    assert ratios["mots_par_phrase"]["ratio sur votre texte"] == reference["tokens"] / reference["phrases"]
    assert all(r["verdict"] == "INSUFFISAMMENT_DEFINI" for r in ratios.values())
    temoins = r4["concordance_mot"]["temoins"]
    assert [texte[t["debut"]:t["fin"]] for t in temoins] == ["droit"]

    if variante:
        # Un export 03 ancien contient ses résultats communs sans la rubrique de transfert.
        del r3["transfert"], r3["filtre_personnel"]
        (dossier / f"resultats_03_{numero}.json").write_text(json.dumps(r3), encoding="utf-8")
        audit = executer_04_avec_recherches_personnelles(dossier, numero)
        assert audit["lectures_personnelles"]["cooccurrences_03"] is None
        assert audit["protocole_B"]["relation_03"] == relation
        assert audit["effectifs"] == {"droit": 1, "la peine": 2, "illustration": 0}
        assert audit["protocole_enquete"]["largeur_extrait"] == 4
        assert audit["protocole_enquete"]["largeur_concordance"] == 2
        assert {passage["forme"] for passage in audit["passages"]} == {"droit", "la peine"}
        for passage in audit["passages"]:
            assert passage["debut"] == max(0, passage["debut_occurrence"] - 4)
            assert passage["fin"] == min(len(texte), passage["fin_occurrence"] + 4)
            assert passage["texte"] == texte[passage["debut"]:passage["fin"]]
            assert texte[passage["debut_occurrence"]:passage["fin_occurrence"]].lower() == passage["forme"]
        candidate = audit["citation_C"]
        assert candidate["statut"] == "CANDIDAT_APPROCHE"
        assert candidate["demarche"]["ancre"] == "la peine"
        assert candidate["demarche"]["nombre_pistes"] == 2
        assert candidate["demarche"]["numero_piste"] == 2
        assert candidate["demarche"]["statut_recherche"] == "NON_RETROUVEE"
        assert candidate["passage_source"] == texte[candidate["debut"]:candidate["fin"]]
        debut_piste = texte.lower().rindex("la peine")
        assert candidate["debut"] == debut_piste - 3
        assert candidate["fin"] == debut_piste + len("la peine") + 3


def executer_04_avec_recherches_personnelles(dossier, numero):
    """Réutilise les deux résultats importés avec une locution et une piste choisies par l'étudiant."""
    (chemin,) = NOTEBOOKS.glob("04_*.ipynb")
    cahier = json.loads(chemin.read_text(encoding="utf-8"))
    cellules = {c["id"]: c for c in cahier["cells"]}
    reglages = [
        ("explorer-enquete", '["droit", "état"]', '["droit", "la peine", "illustration"]'),
        ("contextes-enquete", "largeur_concordance = 130", "largeur_concordance = 2"),
        ("retenir-passages", "largeur_extrait = 300", "largeur_extrait = 4"),
        ("localiser-candidat", "ANCRE = ancre_proposee", 'ANCRE = "la peine"'),
        ("localiser-candidat", "largeur_piste = 120", "largeur_piste = 3"),
        ("discuter-citation", "NUMERO_PISTE = None", "NUMERO_PISTE = 2"),
    ]
    for identifiant, avant, apres in reglages:
        cellule = cellules[identifiant]
        source = "".join(cellule["source"])
        assert avant in source
        cellule["source"] = source.replace(avant, apres)
    copie = dossier / "04_personnel.ipynb"
    copie.write_text(json.dumps(cahier, ensure_ascii=False), encoding="utf-8")
    executer_cahier(copie, numero)
    return json.loads((dossier / f"resultats_04_{numero}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("pivot,associe", [("droit civil", "femme"), ("femme", "droit civil")])
def test_couple_personnel_refuse_plusieurs_mots(pivot, associe):
    (chemin,) = NOTEBOOKS.glob("03_*.ipynb")
    cahier = json.loads(chemin.read_text(encoding="utf-8"))
    cellule = next(c for c in cahier["cells"] if c["id"] == "couple-perso")
    source = "".join(cellule["source"]).replace(
        'pivot_libre, associe_libre = "", ""', f"pivot_libre, associe_libre = {pivot!r}, {associe!r}"
    )
    with pytest.raises(ValueError, match="lemme"):
        exec(source, {})


def test_enquete_modalisation_avec_un_export_partiel(capsys):
    (chemin,) = NOTEBOOKS.glob("04_*.ipynb")
    cahier = json.loads(chemin.read_text(encoding="utf-8"))
    cellule = next(c for c in cahier["cells"] if c["id"] == "explorer-enquete")
    source = "".join(cellule["source"]).replace('ENQUETE = "polysémie"', 'ENQUETE = "modalisation"')
    exec(source, {"lexique": {"locutions": {"il_faut": {"occurrences": 0}}}})
    affichage = capsys.readouterr().out
    assert "il faut · 0" in affichage
    assert "il faudrait · non compté dans le cahier sur les fréquences" in affichage


@pytest.mark.parametrize("nouveau_choix", [1, 2], ids=["autre-citation-absente", "citation-exacte"])
def test_changer_de_citation_efface_les_pistes_precedentes(nouveau_choix):
    (chemin,) = NOTEBOOKS.glob("04_*.ipynb")
    cellules = {c["id"]: "".join(c["source"]) for c in json.loads(chemin.read_text(encoding="utf-8"))["cells"]}
    contexte = {"texte": "Elle peut être naturellement de même capacité intellectuelle.",
                "verifier_citation": verifier_citation, "concordances_expression": concordances_expression}
    chercher = cellules["chercher-citation"]
    retenir = cellules["discuter-citation"].replace("NUMERO_PISTE = None", "NUMERO_PISTE = 1")
    exec(chercher, contexte)
    exec(cellules["localiser-candidat"], contexte)
    exec(retenir, contexte)
    assert contexte["demarche_citation"]["nombre_pistes"] == 1
    assert contexte["audit_citation"]["statut"] == "CANDIDAT_APPROCHE"

    exec(chercher.replace("CHOIX_CITATION = 0", f"CHOIX_CITATION = {nouveau_choix}"), contexte)
    if nouveau_choix == 1:
        with pytest.raises(ValueError, match="piste"):
            exec(retenir, contexte)
    else:
        exec(retenir, contexte)
        assert contexte["audit_citation"]["statut"] == "EXACTE"
        assert contexte["demarche_citation"]["nombre_pistes"] == 0
        assert contexte["demarche_citation"]["numero_piste"] is None
