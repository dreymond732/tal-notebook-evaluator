"""Dépôt individuel du TD01 : archive contrôlée et envoi via Drive API.

Ce module n'utilise ni GitHub, ni jeton, ni API Google. Colab monte le Drive
sous le compte Google de l'étudiante ; le dossier de dépôt est configuré
explicitement. Aucune soumission sans confirmation humaine.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import shutil
import zipfile


_IDENTIFIANT = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{2,49}\Z")
_NOMS_EXPORT = ("faguet_epure.txt", "faguet_epure.manifest.json",
                "faguet_epure.offsets.json.gz")
_EXIGES = ("tests_personnels.json", "protocole.json",
           "comparaison_metriques.csv", "rapport.md",
           "faguet_epure.txt", "manifeste.json", "offsets.json.gz",
           "livrable.json")
_EXIGES_INSPECTION = tuple(
    "inspection.json" if nom == "tests_personnels.json" else nom
    for nom in _EXIGES
)
_SIGNATURES_SECRETS = ("github_pat_", "ghp_", "gho_", "Bearer ")


def _hash(octets: bytes) -> str:
    return sha256(octets).hexdigest()


def _serialiser(obj: object) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n").encode("utf-8")


def verifier_tests_personnels(tests: list[dict]) -> None:
    """Refuse les cas incomplets et exige un cas positif et un contre-exemple."""
    if not isinstance(tests, list) or len(tests) < 2:
        raise ValueError("Deux tests personnels documentés au minimum")
    categories: set[str] = set()
    for i, t in enumerate(tests):
        if not isinstance(t, dict):
            raise ValueError(f"Test {i} mal formé")
        for champ in ("debut", "fin", "operation", "type_cas",
                      "attendu", "observe", "justification"):
            if champ not in t:
                raise ValueError(f"Test {i} : champ manquant {champ}")
        if not (isinstance(t["debut"], int) and not isinstance(t["debut"], bool)
                and isinstance(t["fin"], int) and t["fin"] > t["debut"] >= 0):
            raise ValueError(f"Test {i} : offsets invalides")
        if t["type_cas"] not in ("positif", "contre-exemple"):
            raise ValueError(f"Test {i} : type de cas non reconnu")
        if (not isinstance(t["justification"], str)
                or len(t["justification"].strip()) < 15):
            raise ValueError(f"Test {i} : justification insuffisante")
        if (not isinstance(t["operation"], str) or not t["operation"].strip()
                or not isinstance(t["attendu"], str)
                or not isinstance(t["observe"], str)):
            raise ValueError(f"Test {i} : contenu invalide")
        if t["attendu"] != t["observe"]:
            raise ValueError(f"Test {i} : écart non résolu ; analyser avant dépôt")
        categories.add(t["type_cas"])
    if categories != {"positif", "contre-exemple"}:
        raise ValueError("Il faut un cas positif et un contre-exemple")


def _controle_comparaison(comparaison: dict, sha_orig: str, sha_epure: str) -> None:
    if comparaison.get("schema") != "comparaison-td01-v1":
        raise ValueError("Comparaison de mesures invalide")
    if (comparaison.get("source_originale_sha256") != sha_orig
            or comparaison.get("source_epuree_sha256") != sha_epure):
        raise ValueError("Empreinte de la comparaison incohérente")
    controles = comparaison.get("controles", {})
    if not controles or not all(
        isinstance(v, bool) and v
        for d in controles.values()
        for v in (d.values() if isinstance(d, dict) else (d,))
    ):
        raise ValueError("Contrôles des métriques non validés")
    lignes = comparaison.get("comparaison", [])
    attendus = {
        "tokens", "types", "hapax", "ttr",
        "hapax_types_pourcent", "phrases", "mots_par_phrase",
    }
    if {x.get("id") for x in lignes} != attendus or len(lignes) != 7:
        raise ValueError("Sept indicateurs obligatoires")


def preparer_archive_td01(
    identifiant: str,
    export_epuration: dict,
    tests_personnels: list[dict],
    comparaison: dict,
    observations: str,
    dossier_local: str | Path,
    *,
    version_bibliotheque: str,
    standardisation_td01: dict | None = None,
    inspection: dict | None = None,
    revision_git: str = "",
    version_notebook: str = "",
    mode_revision: str = "reference",
) -> dict:
    """Prépare l'archive sans la soumettre. Vérifie l'origine de chaque fichier.

    Ne télécharge ni ne publie rien. Les trois fichiers d'épuration restent
    locaux et seront encapsulés après vérification de leurs empreintes.
    """
    if not isinstance(identifiant, str) or not _IDENTIFIANT.fullmatch(identifiant):
        raise ValueError("Identifiant alphanumérique (3-50 caractères) requis")
    if inspection is None:
        verifier_tests_personnels(tests_personnels)
    else:
        from .inspection_td01 import valider_inspection
        valider_inspection(inspection)
    if mode_revision not in {"reference", "exploration"}:
        raise ValueError("Mode de révision non reconnu")
    if inspection is not None:
        if not revision_git.strip() or not version_notebook.strip():
            raise ValueError("Version du notebook et révision Git nécessaires")
        if mode_revision == "reference" and standardisation_td01 is None:
            raise ValueError("La référence exige une preuve de standardisation")
        if mode_revision == "exploration":
            if standardisation_td01 is not None:
                raise ValueError("Une exploration ne doit pas se déclarer standardisée")
            from .protocole_td01 import SHA_FAGUET_TD01, METRIQUES_TD01
            from dataclasses import asdict
            if (comparaison["source_originale_sha256"] != SHA_FAGUET_TD01
                    or comparaison["protocole_commun"] != asdict(METRIQUES_TD01)):
                raise ValueError("Une exploration conserve le texte initial et les paramètres de mesure")
    if not isinstance(observations, str) or len(observations.strip()) < 50:
        raise ValueError("Un bilan interprétatif de 50 caractères minimum est requis")
    if not isinstance(version_bibliotheque, str) or not version_bibliotheque.strip():
        raise ValueError("Version de la bibliothèque manquante")

    fichiers = {k: Path(export_epuration[k]) for k in
                ("texte", "manifeste", "correspondance")}
    if [fichiers[k].name for k in ("texte", "manifeste", "correspondance")] != list(_NOMS_EXPORT):
        raise ValueError("Exports inattendus : noms de fichiers non conformes")
    for fichier in fichiers.values():
        if not fichier.is_file():
            raise FileNotFoundError(f"Export d'épuration manquant : {fichier}")

    manifeste = json.loads(fichiers["manifeste"].read_text(encoding="utf-8"))
    source = manifeste["source"]["sha256_original"]
    epure = manifeste["export"]["sha256_texte_utf8"]
    if (_hash(fichiers["texte"].read_bytes()) != epure
            or manifeste["validation"]["confirmation_sha256"] != source
            or not all(x == "approuve"
                       for x in manifeste["validation"]["decisions"].values())
            or manifeste["validation"].get("compaction_blancs_approuvee") is not True):
        raise ValueError("Le corpus épuré n'est pas approuvé ou son empreinte diffère")
    _controle_comparaison(comparaison, source, epure)
    if standardisation_td01 is not None:
        from .protocole_td01 import verifier_standardisation_td01
        verifier_standardisation_td01(standardisation_td01, manifeste, comparaison)

    import csv
    sortie_csv = io.StringIO(newline="")
    champs = ("id", "indicateur", "unite", "original", "epure",
              "ecart", "variation_relative_pourcent")
    writer = csv.DictWriter(sortie_csv, fieldnames=champs, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(comparaison["comparaison"])

    contenus = {
        **({
            "tests_personnels.json": _serialiser(tests_personnels)
        } if inspection is None else {
            "inspection.json": _serialiser(inspection)
        }),
        "protocole.json": _serialiser({
            "protocole_comparaison": comparaison["protocole_commun"],
            "logiciel": comparaison["logiciel"],
            "version_bibliotheque": version_bibliotheque,
            "source_originale_sha256": source,
            "source_epuree_sha256": epure,
            "standardisation_td01": standardisation_td01,
            "revision_git": revision_git,
            "version_notebook": version_notebook,
            "mode_revision": mode_revision,
        }),
        "comparaison_metriques.csv": sortie_csv.getvalue().encode("utf-8"),
        "rapport.md": (
            ("# Analyse du corpus Faguet" if inspection is not None else "# TD01")
            + f" — {identifiant}\n\n" + observations.strip() + "\n"
        ).encode("utf-8"),
        "faguet_epure.txt": fichiers["texte"].read_bytes(),
        "manifeste.json": fichiers["manifeste"].read_bytes(),
        "offsets.json.gz": fichiers["correspondance"].read_bytes(),
    }
    for nom in ("inspection.json" if inspection is not None
                else "tests_personnels.json", "protocole.json", "rapport.md"):
        if any(m in contenus[nom].decode("utf-8") for m in _SIGNATURES_SECRETS):
            raise ValueError("Secret probable détecté dans la contribution")
    registre = {
        "schema": "livrable-td01-v1",
        "identifiant": identifiant,
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version_bibliotheque": version_bibliotheque,
        "sha256_source": source,
        "sha256_epure": epure,
        "profil_standardise": (
            standardisation_td01["profil"] if standardisation_td01 is not None else None
        ),
        "mode_revision": mode_revision,
        "revision_git": revision_git,
        "version_notebook": version_notebook,
        "fichiers_sha256": {k: _hash(v) for k, v in contenus.items()},
    }
    contenus["livrable.json"] = _serialiser(registre)

    destination = Path(dossier_local)
    destination.mkdir(parents=True, exist_ok=True)
    maintenant = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    prefixe = "FAGUET" if inspection is not None else "TD01"
    version_fichier = (
        "v" + version_notebook.replace(".", "-") + "_"
        if inspection is not None else ""
    )
    chemin = destination / f"{prefixe}_{identifiant}_{version_fichier}{maintenant}.zip"
    with zipfile.ZipFile(chemin, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for nom, octets in contenus.items():
            archive.writestr(nom, octets)
    verifier_archive_td01(chemin)
    return {
        "archive": str(chemin),
        "sha256": _hash(chemin.read_bytes()),
        "identifiant": identifiant,
        "fichiers": sorted(contenus),
    }


def verifier_archive_td01(chemin: str | Path) -> dict:
    """Vérifie le ZIP et les empreintes internes sans exécuter ni extraire de code."""
    with zipfile.ZipFile(chemin, "r") as archive:
        fichiers = set(archive.namelist())
        if (archive.testzip() is not None
                or fichiers not in (set(_EXIGES), set(_EXIGES_INSPECTION))):
            raise ValueError("Archive incomplète ou endommagée")
        registre = json.loads(archive.read("livrable.json"))
        for nom, empreinte in registre["fichiers_sha256"].items():
            if nom not in archive.namelist() or _hash(archive.read(nom)) != empreinte:
                raise ValueError(f"Empreinte incorrecte dans l'archive : {nom}")
        return registre


def deposer_archive_drive(
    archive_locale: str | Path,
    dossier_drive_monte: str | Path,
    *,
    confirmation_explicite: bool,
) -> dict:
    """Copie et relit le ZIP sur le Drive monté ; ne remplace jamais un dépôt.

    Ne crée pas implicitement le dossier partagé. L'identification du dossier
    et les droits sont vérifiés séparément par l'utilisateur dans Colab.
    """
    if confirmation_explicite is not True:
        raise ValueError("Dépôt non confirmé")
    source = Path(archive_locale)
    destination = Path(dossier_drive_monte)
    if not source.is_file():
        raise FileNotFoundError("Archive locale absente")
    if not destination.is_dir():
        raise FileNotFoundError("Dossier Drive non accessible : vérifier partage et raccourci")
    if not source.name.startswith(("TD01_", "FAGUET_")) or source.suffix != ".zip":
        raise ValueError("Archive de résultats attendue")
    verifier_archive_td01(source)
    cible = destination / source.name
    if cible.exists():
        raise FileExistsError("Un dépôt porte déjà ce nom ; rien n'a été écrasé")
    # On copie seulement après validation ; une interruption laisse l'archive
    # locale disponible. La relecture doit confirmer le transfert.
    shutil.copyfile(source, cible)
    if _hash(cible.read_bytes()) != _hash(source.read_bytes()):
        raise IOError("Dépôt Drive incomplet : conserve la copie locale")
    verifier_archive_td01(cible)
    return {
        "depot": str(cible),
        "sha256": _hash(cible.read_bytes()),
        "verification": "SHA256_ET_ZIP_OK",
    }


_ID_DOSSIER = re.compile(r"[A-Za-z0-9_-]{10,128}\Z")


def deposer_archive_drive_api(
    archive_locale: str | Path,
    service: object,
    dossier_id: str,
    *,
    confirmation_explicite: bool,
) -> dict:
    """Charge le ZIP vers un ID Drive précis, puis relit les octets pour SHA-256.

    service : client Google Drive API v3 authentifié via Colab, avec les droits
    de l'étudiante. Ne crée aucun dossier et ne remplace aucune archive.
    """
    if confirmation_explicite is not True:
        raise ValueError("Dépôt Google Drive non confirmé")
    if not isinstance(dossier_id, str) or not _ID_DOSSIER.fullmatch(dossier_id):
        raise ValueError("Identifiant du dossier Drive invalide")
    source = Path(archive_locale)
    if not source.is_file():
        raise FileNotFoundError("Archive locale manquante")
    if not source.name.startswith(("TD01_", "FAGUET_")) or source.suffix != ".zip":
        raise ValueError("Une archive de résultats ZIP est requise")
    verifier_archive_td01(source)
    empreinte_locale = _hash(source.read_bytes())

    dossier = service.files().get(
        fileId=dossier_id, fields="id,name,mimeType,capabilities(canAddChildren)",
        supportsAllDrives=True,
    ).execute()
    if (dossier.get("id") != dossier_id
            or dossier.get("mimeType") != "application/vnd.google-apps.folder"):
        raise ValueError("La destination n'est pas le dossier Drive attendu")
    if dossier.get("capabilities", {}).get("canAddChildren") is not True:
        raise PermissionError("Le compte Google ne peut pas déposer dans ce dossier")

    nom_echappe = source.name.replace("\\", "\\\\").replace("'", "\\'")
    deja = service.files().list(
        q=f"'{dossier_id}' in parents and name = '{nom_echappe}' and trashed = false",
        pageSize=10,
        fields="files(id,name),nextPageToken",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
    if deja.get("files"):
        raise FileExistsError("Un dépôt du même nom existe déjà : aucun écrasement")

    from googleapiclient.http import MediaFileUpload
    media = MediaFileUpload(str(source), mimetype="application/zip", resumable=False)
    distant = service.files().create(
        body={"name": source.name, "parents": [dossier_id],
              "mimeType": "application/zip"},
        media_body=media,
        fields="id,name,md5Checksum,size,webViewLink,parents",
        supportsAllDrives=True,
    ).execute()
    identifiant = distant.get("id")
    if not identifiant or dossier_id not in distant.get("parents", []):
        raise IOError("Upload sans preuve du dossier de destination")

    octets_distants = service.files().get_media(
        fileId=identifiant, supportsAllDrives=True,
    ).execute()
    if not isinstance(octets_distants, bytes):
        raise IOError("Impossible de relire les octets sur Google Drive")
    if _hash(octets_distants) != empreinte_locale:
        raise IOError("SHA-256 Drive différent de l'archive locale")
    if distant.get("size") is not None and int(distant["size"]) != source.stat().st_size:
        raise IOError("Taille de l'archive distante incorrecte")
    if distant.get("md5Checksum"):
        from hashlib import md5
        if md5(octets_distants).hexdigest() != distant["md5Checksum"]:
            raise IOError("Somme MD5 Google Drive incorrecte")
    with zipfile.ZipFile(io.BytesIO(octets_distants), "r") as archive:
        fichiers = set(archive.namelist())
        if (archive.testzip() is not None
                or fichiers not in (set(_EXIGES), set(_EXIGES_INSPECTION))):
            raise IOError("Archive distante corrompue ou incomplète")
    return {
        "depot": distant.get("webViewLink") or (
            f"https://drive.google.com/file/d/{identifiant}/view"
        ),
        "fichier_id": identifiant, "dossier_id": dossier_id,
        "nom": source.name, "sha256": empreinte_locale,
        "verification": "SHA256_ET_ZIP_OK",
    }
