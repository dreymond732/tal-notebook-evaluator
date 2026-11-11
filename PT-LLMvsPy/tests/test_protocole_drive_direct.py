"""Contrôles sans réseau du profil commun et du dépôt Drive par ID."""
from __future__ import annotations

from dataclasses import asdict
from hashlib import md5, sha256
from pathlib import Path
import json
import sys
import types
import zipfile

import pytest

from tal_toolkit.protocole_td01 import (
    ATTENDUS_STRUCTURAUX_TD01, IDENTIFIANT_PROFIL_TD01,
    METRIQUES_TD01, OPERATIONS_TD01, SHA_FAGUET_TD01,
    SHA_FAGUET_EPURE_TD01,
    plan_standard_td01, verifier_standardisation_td01,
)
from tal_toolkit.soumission_td01 import (
    deposer_archive_drive_api, verifier_archive_td01,
)


DRIVE_ID = "18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO"


def test_plan_faguet_commun_est_immuable_et_explicitement_identifie():
    p = plan_standard_td01()
    assert p.identifiant == IDENTIFIANT_PROFIL_TD01
    assert tuple(x.nom for x in p.operations) == tuple(n for n, _ in OPERATIONS_TD01)
    assert ATTENDUS_STRUCTURAUX_TD01 == {
        "blocs_notes": 3, "appels_notes": 4, "separateurs": 20,
        "cesures_candidates": 0, "apostrophes_courbes": 0,
    }


def test_normalisation_refuse_plan_ou_mesures_modifies():
    sha_epure = SHA_FAGUET_EPURE_TD01
    standard = {
        "schema": "standardisation-td01-v1",
        "profil": IDENTIFIANT_PROFIL_TD01,
        "source": {"sha256": SHA_FAGUET_TD01},
        "sha256_epure": sha_epure,
    }
    manifeste = {
        "source": {"plan": {
            "identifiant": IDENTIFIANT_PROFIL_TD01,
            "operations": [{"nom": x[0]} for x in OPERATIONS_TD01],
        }},
        "export": {"sha256_texte_utf8": sha_epure},
    }
    comparaisons = {
        "protocole_commun": asdict(METRIQUES_TD01),
        "source_originale_sha256": SHA_FAGUET_TD01,
        "source_epuree_sha256": sha_epure,
    }
    verifier_standardisation_td01(standard, manifeste, comparaisons)
    autre = dict(standard, profil="plan-personnel")
    with pytest.raises(ValueError, match="Plan d'épuration"):
        verifier_standardisation_td01(autre, manifeste, comparaisons)
    autre_mesure = dict(comparaisons, protocole_commun={"formes": "lemmes"})
    with pytest.raises(ValueError, match="Protocole de métriques"):
        verifier_standardisation_td01(standard, manifeste, autre_mesure)


def _archive_minimale(tmp_path):
    nom = tmp_path / "TD01_etu_test_20261110T153000Z.zip"
    noms = ("tests_personnels.json", "protocole.json",
            "comparaison_metriques.csv", "rapport.md",
            "faguet_epure.txt", "manifeste.json", "offsets.json.gz")
    corps = {n: (f"donnee {n}").encode() for n in noms}
    registre = {
        "schema": "livrable-td01-v1",
        "fichiers_sha256": {n: sha256(o).hexdigest() for n, o in corps.items()},
    }
    with zipfile.ZipFile(nom, "w") as z:
        for n, o in corps.items():
            z.writestr(n, o)
        z.writestr("livrable.json", json.dumps(registre).encode())
    verifier_archive_td01(nom)
    return nom


class _Request:
    def __init__(self, resultat):
        self.resultat = resultat

    def execute(self):
        return self.resultat


class _Files:
    def __init__(self, *, droit=True, doublon=False, corruption=False):
        self.droit = droit
        self.doublon = doublon
        self.corruption = corruption
        self.saved = None
        self.created = False

    def get(self, **kw):
        return _Request({
            "id": DRIVE_ID,
            "mimeType": "application/vnd.google-apps.folder",
            "capabilities": {"canAddChildren": self.droit},
        })

    def list(self, **kw):
        return _Request({"files": [{"id": "ancien"}] if self.doublon else []})

    def create(self, **kw):
        self.created = True
        self.saved = Path(kw["media_body"]).read_bytes()
        return _Request({
            "id": "remote-file-001", "parents": [DRIVE_ID],
            "size": str(len(self.saved)),
            "md5Checksum": md5(self.saved).hexdigest(),
            "webViewLink": "https://drive.google.com/file/d/remote-file-001/view",
        })

    def get_media(self, **kw):
        contenu = self.saved if not self.corruption else self.saved[:-1] + b"X"
        return _Request(contenu)


class _Service:
    def __init__(self, **options):
        self.fichiers = _Files(**options)

    def files(self):
        return self.fichiers


def _mock_google_lib(monkeypatch):
    paquet = types.ModuleType("googleapiclient")
    paquet.__path__ = []
    http = types.ModuleType("googleapiclient.http")
    http.MediaFileUpload = lambda path, **kwargs: path
    monkeypatch.setitem(sys.modules, "googleapiclient", paquet)
    monkeypatch.setitem(sys.modules, "googleapiclient.http", http)


def test_depot_direct_drive_dossier_id_et_integrite(tmp_path, monkeypatch):
    _mock_google_lib(monkeypatch)
    fichier = _archive_minimale(tmp_path)
    service = _Service()
    resultat = deposer_archive_drive_api(
        fichier, service, DRIVE_ID, confirmation_explicite=True,
    )
    assert resultat["dossier_id"] == DRIVE_ID
    assert resultat["verification"] == "SHA256_ET_ZIP_OK"
    assert resultat["sha256"] == sha256(fichier.read_bytes()).hexdigest()
    assert resultat["depot"].startswith("https://drive.google.com/")
    assert service.fichiers.created


@pytest.mark.parametrize("options,exc", [
    ({"droit": False}, PermissionError),
    ({"doublon": True}, FileExistsError),
    ({"corruption": True}, IOError),
])
def test_refus_droits_doublon_et_corruption(tmp_path, monkeypatch, options, exc):
    _mock_google_lib(monkeypatch)
    fichier = _archive_minimale(tmp_path)
    service = _Service(**options)
    with pytest.raises(exc):
        deposer_archive_drive_api(
            fichier, service, DRIVE_ID, confirmation_explicite=True,
        )
    if not options.get("corruption"):
        assert service.fichiers.created is False


def test_depot_drive_requires_confirmation(tmp_path):
    service = _Service()
    with pytest.raises(ValueError, match="non confirmé"):
        deposer_archive_drive_api(
            tmp_path / "absent.zip", service, DRIVE_ID,
            confirmation_explicite=False,
        )
