import json
from zipfile import ZipFile

import pytest

from tal_toolkit.atelier import ouvrir_corpus_atelier, lire_resultats, enregistrer_resultats


def test_reprendre_archive_01_dans_une_nouvelle_session(tmp_path):
    texte = "Lois.\r\nLois et droits."
    with ZipFile(tmp_path / "FAGUET.zip", "w") as archive:
        archive.writestr("faguet_nettoye.txt", texte)
        archive.writestr("observations_nettoyage.txt", "Notes personnelles.")
    corpus = ouvrir_corpus_atelier(tmp_path)
    assert corpus.texte == texte
    assert not (tmp_path / "observations_nettoyage.txt").exists()
    (tmp_path / "FAGUET.zip").unlink()
    assert ouvrir_corpus_atelier(tmp_path).texte == texte
    numero = "03"
    preuve = {"debut": 7, "fin": 11, "extrait": "Lois"}
    enregistrer_resultats(tmp_path, numero, preuve)
    sauvegarde = lire_resultats(tmp_path, numero)
    assert corpus.texte[sauvegarde["debut"]:sauvegarde["fin"]] == sauvegarde["extrait"]
    assert json.loads((tmp_path / "resultats_03.json").read_text()) == preuve


def test_expliquer_reprise_necessaire(tmp_path):
    with pytest.raises(FileNotFoundError, match="notebook 01"):
        ouvrir_corpus_atelier(tmp_path)
    with pytest.raises(FileNotFoundError, match="notebook 02"):
        lire_resultats(tmp_path, "02")
