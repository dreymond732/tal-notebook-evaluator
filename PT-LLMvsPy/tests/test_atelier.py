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
    with pytest.raises(FileNotFoundError, match="Préparer un corpus et mesurer l’effet du nettoyage"):
        ouvrir_corpus_atelier(tmp_path)
    with pytest.raises(FileNotFoundError, match=r"resultats_02\.json"):
        lire_resultats(tmp_path, "02")


def test_reprise_identifiee_seances_distinctes(tmp_path, monkeypatch):
    from shutil import copy2
    from tal_toolkit.atelier import preparer_atelier

    etudiant = "00_A-7"
    texte = "Lois.\r\nLois et droits."
    s2, s3, s4 = [tmp_path / nom for nom in ("02", "03", "04")]
    for dossier in (s2, s3, s4):
        dossier.mkdir()
    fichier = s2 / f"FAGUET_01_{etudiant}_20261125T090000Z_123456789.zip"
    with ZipFile(fichier, "w") as archive:
        archive.writestr("faguet_nettoye.txt", texte)
        archive.writestr("metadonnees_analyse.json", json.dumps({"numero_etudiant": etudiant}))
    # Ces deux dossiers ont une autre identité, une partie de leur numéro est commune.
    voisin = s2 / f"FAGUET_01_{etudiant}_suite_20261125T090000Z_123456789.zip"
    with ZipFile(voisin, "w") as archive:
        archive.writestr("faguet_nettoye.txt", "Autre texte.")
    monkeypatch.chdir(s2)
    corpus, dossier, _, sauver = preparer_atelier(numero_etudiant=etudiant)
    assert dossier == s2 and corpus.texte == texte
    json02 = sauver("02", {"observations": ["essai 02"]})
    assert json02.name == "resultats_02_00_A-7.json"
    assert json.loads(json02.read_text()) == {
        "observations": ["essai 02"], "numero_etudiant": etudiant,
        "numero_notebook": "02", "sha256_corpus": corpus.sha256,
    }
    for destination in (s3, s4):
        copy2(fichier, destination)
        copy2(json02, destination)
    monkeypatch.chdir(s3)
    _, _, lire, sauver = preparer_atelier(numero_etudiant=etudiant)
    assert lire("02")["observations"] == ["essai 02"]
    json03 = sauver("03", {"passage": texte[:5]})
    copy2(json03, s4)
    monkeypatch.chdir(s4)
    _, _, lire, sauver = preparer_atelier(numero_etudiant=etudiant)
    assert lire("02")["numero_etudiant"] == etudiant and lire("03")["passage"] == "Lois."
    assert sauver("04", {"conclusion": "ok"}).name == "resultats_04_00_A-7.json"


def test_reprise_fichiers_anciens_et_controles_de_coherence(tmp_path, monkeypatch):
    from tal_toolkit.atelier import preparer_atelier

    monkeypatch.chdir(tmp_path)
    (tmp_path / "faguet_nettoye.txt").write_text("Texte.")
    ancien = tmp_path / "resultats_02.json"
    ancien.write_text('{"mesure": 1}')
    _, _, lire, sauver = preparer_atelier(numero_etudiant="001")
    assert lire("02") == {"mesure": 1}
    ancien.write_text('{"numero_etudiant":"002"}')
    with pytest.raises(ValueError, match="numéro étudiant"):
        lire("02")
    fichier = sauver("02", {"mesure": 2})
    assert lire("02")["mesure"] == 2
    copies = tmp_path / "resultats_02_001 (1).json"
    copies.write_text(fichier.read_text())
    assert lire("02")["mesure"] == 2
    copies.write_text('{}')
    with pytest.raises(ValueError, match="Plusieurs versions"):
        lire("02")
    copies.unlink()
    fichier.write_text('{"numero_notebook":"03"}')
    with pytest.raises(ValueError, match="autre notebook"):
        lire("02")
    fichier.write_text('{"sha256_corpus":"empreinte différente"}')
    with pytest.raises(ValueError, match="texte utilisé"):
        lire("02")


def test_import_txt_et_zip_verifie_la_version_du_corpus(tmp_path, monkeypatch):
    from tal_toolkit.atelier import preparer_atelier

    monkeypatch.chdir(tmp_path)
    (tmp_path / "faguet_nettoye_00.txt").write_text("Première lecture.")
    archive = tmp_path / "FAGUET_01_00_20261125T090000Z_12.zip"
    with ZipFile(archive, "w") as z:
        z.writestr("faguet_nettoye.txt", "Autre lecture.")
    with pytest.raises(ValueError, match="Plusieurs textes"):
        preparer_atelier(numero_etudiant="00")
    with ZipFile(archive, "w") as z:
        z.writestr("faguet_nettoye.txt", "Première lecture.")
        z.writestr("metadonnees_analyse.json", '{"numero_etudiant":"01"}')
    with pytest.raises(ValueError, match="numéro enregistré"):
        preparer_atelier(numero_etudiant="00")
    with pytest.raises(FileNotFoundError, match="Préparer un corpus et mesurer l’effet du nettoyage"):
        preparer_atelier(numero_etudiant="0")


@pytest.mark.parametrize("valeur", ["", "../001", "0 01", ".01", "à", "A"*65, 123])
def test_numero_etudiant_invalide(valeur):
    from tal_toolkit.atelier import valider_numero_etudiant

    with pytest.raises(ValueError, match="NUMERO_ETUDIANT"):
        valider_numero_etudiant(valeur)


def test_colab_import_local_et_telechargement_avec_recours(tmp_path, monkeypatch, capsys):
    import sys
    from types import ModuleType, SimpleNamespace
    from tal_toolkit import atelier

    # Les deux copies sont dans le disque de session. Seule la copie du navigateur est simulée.
    colab = ModuleType("google.colab")
    telecharges = []
    colab.files = SimpleNamespace(download=telecharges.append)
    monkeypatch.setitem(sys.modules, "google.colab", colab)
    monkeypatch.setattr(atelier, "DOSSIER_COLAB", tmp_path)
    (tmp_path / "sample_data").mkdir()
    (tmp_path / "faguet_nettoye_A01.txt").write_text("Bonjour.")
    _, dossier, _, sauver = atelier.preparer_atelier(numero_etudiant="A01")
    export = sauver("02", {"observations": ["vérifié"]})
    assert dossier == tmp_path
    assert telecharges == [str(export)] and export.parent == tmp_path

    def echec_navigateur(_):
        raise RuntimeError("Téléchargement indisponible")
    colab.files.download = echec_navigateur
    sauver("02", {"observations": ["revu"]})
    assert json.loads(export.read_text())["observations"] == ["revu"]
    assert "volet Fichiers" in capsys.readouterr().out
    with pytest.raises(ValueError, match="dans /content"):
        atelier.preparer_atelier(dossier_personnel="/content/drive/MyDrive", numero_etudiant="A01")


def test_reprise_anonyme_isolee_refuse_la_session_melangee(tmp_path, monkeypatch, capsys):
    from tal_toolkit.atelier import preparer_atelier

    monkeypatch.chdir(tmp_path)
    ancien = tmp_path / "FAGUET_v2_0_0_20261125T090000Z_123456789.zip"
    with ZipFile(ancien, "w") as archive:
        archive.writestr("faguet_nettoye.txt", "Texte commun.")
    (tmp_path / "resultats_02.json").write_text('{"mesure":1}')
    _, _, lire, _ = preparer_atelier(numero_etudiant="001")
    assert lire("02") == {"mesure": 1}
    avis = capsys.readouterr().out
    assert ancien.name in avis and "Ancien export sans numéro : resultats_02.json" in avis
    (tmp_path / "resultats_02_002 (1).json").write_text('{"numero_etudiant":"002"}')
    with pytest.raises(ValueError, match="autre étudiant"):
        preparer_atelier(numero_etudiant="001")
    with pytest.raises(ValueError, match="autre étudiant"):
        lire("02")
