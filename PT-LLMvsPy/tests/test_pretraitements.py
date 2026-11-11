"""Tests d'un contrat de prétraitement AVANT le comptage."""
from hashlib import sha256
import pytest

from tal_toolkit import charger_corpus
from tal_toolkit.pretraitements import (
    OperationPretraitement, PlanPretraitement, executer_pretraitements,
)


def plan(*noms):
    return PlanPretraitement(
        identifiant="test-v1",
        operations=tuple(OperationPretraitement(n, "Cas de test") for n in noms),
    )


def test_par_defaut_aucune_transformation():
    source = "L’archive\r\nmontre deux lignes.\r\n\r\nUn titre."
    r = executer_pretraitements(source)
    assert r.analyse == r.original == source
    assert r.execution == ()
    assert r.sha256_original == r.sha256_analyse_utf8
    assert r.indices_conserves


def test_recomposer_retours_isoles_et_preserver_paragraphes():
    src = "Un mot\r\nsuivant.\r\n\r\nDeuxième phrase.\nSuite."
    r = executer_pretraitements(src, plan=plan("recomposer_lignes"))
    assert r.analyse == "Un mot  suivant.\r\n\r\nDeuxième phrase. Suite."
    assert len(r.analyse) == len(src)
    assert r.execution[0]["statut"] == "EXECUTEE"
    assert r.execution[0]["modifications"] == 2
    assert r.execution[0]["exemples"][0]["avant"] == "\r\n"
    assert r.execution[0]["exemples"][0]["apres"] == "  "
    assert r.execution[0]["exemples"][0]["debut"] == src.index("\r\n")


def test_recomposition_ne_traite_pas_decesures_silencieusement():
    r = executer_pretraitements("pro-\r\nfession", plan=plan("recomposer_lignes"))
    assert r.analyse == "pro-  fession"
    assert "profession" not in r.analyse


def test_normaliser_apostrophes_ne_change_ni_le_debut_ni_le_taille():
    src = "L’archive et ‘l’histoire’."
    r = executer_pretraitements(src, plan=plan("apostrophes_droites"))
    assert r.analyse == "L'archive et 'l'histoire'."
    assert len(r.analyse) == len(src)
    assert r.execution[0]["modifications"] == 4
    assert r.original == src


def test_ordre_operations_et_preuve_sha256_du_fichier(tmp_path):
    f = tmp_path / "corpus.txt"
    octets = "L’archive\r\ncontinue.\r\n\r\nFin.".encode("utf-8")
    f.write_bytes(octets)
    original = charger_corpus(f)
    r = executer_pretraitements(
        original, plan=plan("recomposer_lignes", "apostrophes_droites")
    )
    assert r.original == octets.decode("utf-8")
    assert r.analyse == "L'archive  continue.\r\n\r\nFin."
    assert r.sha256_original == sha256(octets).hexdigest()
    assert r.sha256_analyse_utf8 == sha256(r.analyse.encode("utf-8")).hexdigest()
    assert r.sha256_original != r.sha256_analyse_utf8
    manifest = r.manifeste()
    assert manifest["indices_conserves"] is True
    assert len(manifest["execution"]) == 2
    assert manifest["execution"][0]["operation"] == "recomposer_lignes"
    assert manifest["execution"][1]["operation"] == "apostrophes_droites"
    assert manifest["execution"][0]["modifications"] == 1


def test_non_transformations_non_effectuees_ne_sont_pas_annoncees():
    r = executer_pretraitements(
        "[1] L’archive et des mots vides.",
        plan=plan("apostrophes_droites"),
        max_exemples=0,
    )
    assert "[1]" in r.analyse  # notes non supprimées
    assert "des" in r.analyse  # stopwords non supprimés
    assert r.execution[0]["exemples"] == []
    assert r.execution[0]["modifications"] == 1


def test_operation_inconnue_ou_sans_justification_interdite():
    with pytest.raises(ValueError):
        OperationPretraitement("supprimer_notes", "Non valide")
    with pytest.raises(ValueError):
        OperationPretraitement("recomposer_lignes", "")


def test_plan_duplique_refuse():
    with pytest.raises(ValueError):
        plan("recomposer_lignes", "recomposer_lignes")


def test_plan_id_vide_refuse():
    with pytest.raises(ValueError):
        PlanPretraitement(identifiant=" ")


def test_max_exemples_negatifs_refuses():
    with pytest.raises(ValueError):
        executer_pretraitements("Texte", max_exemples=-1)


def test_recomposer_et_apostrophes_idempotents():
    src = "L’archive\r\nparle de l’histoire."
    p = plan("recomposer_lignes", "apostrophes_droites")
    a = executer_pretraitements(src, plan=p).analyse
    b = executer_pretraitements(a, plan=p)
    assert a == b.analyse
    assert all(x["modifications"] == 0 for x in b.execution)
