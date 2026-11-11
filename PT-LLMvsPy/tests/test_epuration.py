"""Microcorpus adversariaux : transformations approuvables, source jamais perdue."""
from __future__ import annotations

import gzip
import hashlib
import json

import pytest

from tal_toolkit import (
    OperationPretraitement, PlanPretraitement, composer_texte_epure,
    executer_pretraitements, exporter_texte_approuve, recenser_elements,
)


def plan(*noms, cibles_titres=(), cibles_cesures=()):
    operations = []
    for nom in noms:
        cibles = (
            tuple(cibles_titres) if nom == "masquer_lignes_exactes" else
            tuple(cibles_cesures) if nom == "raccorder_cesures_validees" else ()
        )
        operations.append(OperationPretraitement(nom, "Vérification contrôlée", cibles))
    return PlanPretraitement(tuple(operations), identifiant="exemples-v1")


def test_recensement_non_destructif():
    texte = "Le Féminisme\r\n\r\nIDÉES GÉNÉRALES\r\n[1]\r\n[Note 2: x]\r\n* * * * *\r\nmot-\r\ntrès"
    res = recenser_elements(texte)
    assert res["retours_crlf"] == 7
    assert res["categories"]["appels_notes"]["nombre"] == 1
    assert res["categories"]["blocs_notes"]["nombre"] == 1
    assert res["categories"]["separateurs"]["nombre"] == 1
    assert res["categories"]["cesures_candidates"]["nombre"] == 1
    assert res["categories"]["titres_potentiels"]["nombre"] >= 1


def test_notes_appels_et_blocs_distincts():
    source = "Faguet[1] parle.\r\n\r\n[Note 2: plusieurs\r\nlignes.] \r\n\r\nConclusion."
    r = executer_pretraitements(
        source, plan=plan("masquer_appels_notes", "masquer_blocs_notes")
    )
    assert len(r.original) == len(r.analyse)
    assert r.execution[0]["modifications"] == 1
    assert r.execution[1]["modifications"] == 1
    assert "[1]" not in composer_texte_epure(r).texte
    assert "plusieurs" not in composer_texte_epure(r).texte
    assert "Faguet" in composer_texte_epure(r).texte
    assert "Conclusion" in composer_texte_epure(r).texte
    assert source == r.original


def test_separateurs_et_titres_seulement_sur_lignes():
    source = (
        "Le Féminisme\r\n\r\nIDÉES GÉNÉRALES\r\n\r\n"
        "On calcule 2 * 3 * 4 dans une phrase.\r\n"
        "*       *       *       *       *\r\n\r\n"
        "IDÉES GÉNÉRALES ne désigne pas ici une ligne entière."
    )
    r = executer_pretraitements(
        source, plan=plan("masquer_separateurs", "masquer_lignes_exactes",
                          cibles_titres=("Le Féminisme", "IDÉES GÉNÉRALES"))
    )
    assert r.execution[0]["modifications"] == 1
    assert r.execution[1]["modifications"] == 2
    epure = composer_texte_epure(r).texte
    assert not epure.startswith("Le Féminisme")
    assert "2 * 3 * 4" in epure
    assert "IDÉES GÉNÉRALES ne désigne" in epure
    assert len(epure) < len(source)


def test_titres_conserves_sans_autorisation():
    source = "IDÉES GÉNÉRALES\r\n\r\nLe passage s'ouvre."
    r = executer_pretraitements(source, plan=plan("masquer_separateurs"))
    assert "IDÉES GÉNÉRALES" in composer_texte_epure(r).texte


def test_cesure_explicitement_validee_recollee_sans_deplacer_la_source():
    source = "Un impor-\r\ntant détail. Un lui-même reste composé."
    r = executer_pretraitements(
        source, plan=plan("raccorder_cesures_validees", "recomposer_lignes",
                          cibles_cesures=("impor-\r\ntant",))
    )
    epure = composer_texte_epure(r)
    assert "important détail" in epure.texte
    assert "lui-même" in epure.texte
    assert "impor-\r\ntant" in r.original
    assert r.execution[0]["modifications"] == 1
    k = epure.texte.index("important")
    assert r.original[epure.position_originale(k):].startswith("impor-")
    assert r.original[epure.position_originale(k+5):].startswith("tant")


def test_cesure_non_autorisee_non_touchee():
    source = "Un traîne-\r\nsavates n'est pas automatiquement une césure."
    # Sans entrée explicite aucune réparation silencieuse n'est permise.
    r = executer_pretraitements(source)
    assert r.original == r.analyse
    with pytest.raises(ValueError):
        OperationPretraitement("raccorder_cesures_validees", "test")


def test_cesure_texte_invalide_et_ordre_invalide():
    with pytest.raises(ValueError):
        OperationPretraitement("raccorder_cesures_validees", "test", ("mot-à-mot",))
    with pytest.raises(ValueError):
        plan("recomposer_lignes", "raccorder_cesures_validees",
             cibles_cesures=("impor-\r\ntant",))


def test_pas_de_masque_sans_cibles_pour_titres():
    with pytest.raises(ValueError):
        OperationPretraitement("masquer_lignes_exactes", "Aucun titre")


def test_manifeste_et_index_source(tmp_path):
    source = "Texte [1]\r\nsuite.\r\n\r\n[Note 2: contenu]\r\n\r\nDernier paragraphe."
    r = executer_pretraitements(
        source, plan=plan(
            "masquer_appels_notes", "masquer_blocs_notes",
            "recomposer_lignes",
        ),
    )
    rendu = composer_texte_epure(r)
    assert len(rendu.texte) == len(rendu.indices_source)
    assert all(
        source[j] == rendu.texte[i] for i, j in enumerate(rendu.indices_source)
        if rendu.texte[i].isalpha()
    )
    assert r.sha256_original == hashlib.sha256(source.encode("utf-8")).hexdigest()
    assert r.manifeste()["zones_masquees"]
    with pytest.raises(ValueError):
        exporter_texte_approuve(
            r, tmp_path, decisions={"masquer_appels_notes": "approuve"},
            confirmation_sha256=r.sha256_original,
            justification_globale="Tous les effets ont été vérifiés avec un échantillon",
            approbation_compaction=True,
        )
    assert not (tmp_path / "faguet_epure.txt").exists()
    with pytest.raises(ValueError):
        exporter_texte_approuve(
            r, tmp_path,
            decisions={op["nom"]: "approuve" for op in r.plan["operations"]},
            confirmation_sha256="0" * 64,
            justification_globale="Tous les effets ont été vérifiés avec un échantillon",
            approbation_compaction=True,
        )

    bilan = exporter_texte_approuve(
        r, tmp_path,
        decisions={op["nom"]: "approuve" for op in r.plan["operations"]},
        confirmation_sha256=r.sha256_original,
        justification_globale="Les sorties ont été contrôlées sur un extrait, puis globalement.",
        approbation_compaction=True,
    )
    assert (tmp_path / "faguet_epure.txt").read_bytes() == rendu.texte.encode("utf-8")
    manifeste = json.loads((tmp_path / "faguet_epure.manifest.json").read_text("utf-8"))
    assert manifeste["source"]["sha256_original"] == r.sha256_original
    with gzip.open(bilan["correspondance"], "rt", encoding="utf-8") as f:
        offsets = json.load(f)
    assert offsets == list(rendu.indices_source)
    assert bilan["sha256_epure"] == rendu.sha256_texte_utf8


def test_epuration_preserve_paragraphes_meme_sans_operations():
    source = "Un mot\r\nà suivre.\r\n\r\nSecond paragraphe."
    r = executer_pretraitements(source)
    epure = composer_texte_epure(r)
    assert epure.texte == "Un mot à suivre.\n\nSecond paragraphe."


def test_rapports_sans_contenu_modifie_mais_operation_executee():
    r = executer_pretraitements("Un texte déjà propre.", plan=plan("apostrophes_droites"))
    assert r.execution[0]["statut"] == "EXECUTEE"
    assert r.execution[0]["modifications"] == 0
    assert r.analyse == r.original


def test_note_faguet_crochets_imbriques_non_tronquee():
    # Faguet contient une note [Note 3: ... sexe [féminin] ... suite.]
    source = (
        "Texte introductif.\r\n\r\n"
        "[Note 3: Dans le sexe [féminin] un texte plus long, et la suite.]\r\n\r\n"
        "Le texte reprend."
    )
    repere = recenser_elements(source)
    assert repere["categories"]["blocs_notes"]["nombre"] == 1
    note = repere["categories"]["blocs_notes"]["exemples"][0]
    assert note["texte"].endswith("et la suite.]")
    resultat = executer_pretraitements(
        source, plan=plan("masquer_blocs_notes")
    )
    assert resultat.execution[0]["modifications"] == 1
    assert resultat.zones_masquees == ((note["debut"], note["fin"]),)
    rendu = composer_texte_epure(resultat)
    assert "féminin" not in rendu.texte
    assert "la suite.]" not in rendu.texte
    assert "Le texte reprend." in rendu.texte
    assert resultat.original == source


def test_note_non_fermee_est_refusee():
    texte = "Une phrase. [Note 7: propos [annexe] pas de fermeture"
    with pytest.raises(ValueError, match="non fermé"):
        recenser_elements(texte)
    with pytest.raises(ValueError, match="non fermé"):
        executer_pretraitements(texte, plan=plan("masquer_blocs_notes"))
