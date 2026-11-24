"""Entrées et sorties communes aux cahiers d'analyse de Faguet."""
from __future__ import annotations

import json
import re
from functools import partial
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

from .io_corpus import Corpus, charger_corpus, corpus_depuis_texte

DOSSIER_COLAB = Path("/content")


def valider_numero_etudiant(numero: str) -> str:
    """Conserve le numéro tel qu’il apparaît sur la carte, zéros initiaux compris."""
    if not isinstance(numero, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", numero):
        raise ValueError("Complétez NUMERO_ETUDIANT avec votre numéro étudiant : 1 à 64 lettres non accentuées, chiffres, tirets ou tirets bas, sans espace.")
    return numero


def _nom_sans_doublon(chemin: Path) -> str:
    """Un navigateur peut ajouter « (1) » juste avant l’extension."""
    return re.sub(r" \(\d+\)$", "", chemin.stem) + chemin.suffix


def _archive_de(source: Path, etudiant: str) -> bool:
    # Date et étiquette de session occupent les deux derniers champs du ZIP.
    prefixe = _nom_sans_doublon(source).removesuffix(".zip").rsplit("_", 2)[0]
    return source.suffix == ".zip" and prefixe == f"FAGUET_01_{etudiant}"


def _signaler_import_anonyme(source: Path, etudiant: str) -> None:
    for fichier in source.parent.iterdir():
        if not fichier.is_file():
            continue
        nom = _nom_sans_doublon(fichier)
        identite = re.fullmatch(r"(?:resultats_0[234]_(.+)\.json|faguet_nettoye_(.+)\.txt)", nom)
        autre = identite is not None and etudiant not in identite.groups()
        if autre or (nom.startswith("FAGUET_01_") and nom.endswith(".zip") and not _archive_de(fichier, etudiant)):
            raise ValueError(f"{source.name} ne porte aucun numéro et la session contient un export "
                             "d’un autre étudiant. Importez uniquement vos propres fichiers dans une nouvelle session.")
    print(f"Ancien export sans numéro : {source.name}. Vérifiez qu’il provient de votre dossier personnel.")


def _corpus_importe(source: Path, etudiant: str) -> Corpus:
    if source.suffix.lower() == ".txt":
        nom = _nom_sans_doublon(source)
        if nom not in ("faguet_nettoye.txt", f"faguet_nettoye_{etudiant}.txt"):
            raise ValueError(f"{source.name} : choisissez le TXT nettoyé du 01 portant votre numéro étudiant.")
        if nom == "faguet_nettoye.txt":
            _signaler_import_anonyme(source, etudiant)
        return charger_corpus(source)

    if source.suffix.lower() != ".zip":
        raise ValueError("Choisissez le TXT nettoyé ou le ZIP du notebook 01.")
    if source.name.startswith("FAGUET_01_") and not _archive_de(source, etudiant):
        raise ValueError(f"{source.name} : le numéro du ZIP ne correspond pas à votre numéro étudiant.")
    with ZipFile(source) as archive:
        if "faguet_nettoye.txt" not in archive.namelist():
            raise ValueError(f"{source.name} ne contient pas le texte nettoyé du notebook 01.")
        texte = archive.read("faguet_nettoye.txt").decode("utf-8")
        meta = (json.loads(archive.read("metadonnees_analyse.json"))
                if "metadonnees_analyse.json" in archive.namelist() else {})
    if meta.get("numero_etudiant", etudiant) != etudiant:
        raise ValueError(f"{source.name} : le numéro enregistré dans le ZIP ne correspond pas au vôtre.")
    if "numero_etudiant" not in meta and not _archive_de(source, etudiant):
        _signaler_import_anonyme(source, etudiant)
    corpus = corpus_depuis_texte(texte, origine=f"{source}!faguet_nettoye.txt")
    if meta.get("sha256_nettoye", corpus.sha256) != corpus.sha256:
        raise ValueError(f"{source.name} : l’empreinte du texte ne correspond pas aux métadonnées du 01.")
    return corpus


def _charger_import_01(dossier: Path, source_01: str, etudiant: str) -> Corpus:
    if source_01:
        return _corpus_importe(dossier / Path(source_01).expanduser(), etudiant)
    fichiers = sorted(p for p in dossier.iterdir() if p.is_file())
    sources = [p for p in fichiers if
               _nom_sans_doublon(p) == f"faguet_nettoye_{etudiant}.txt"
               or _archive_de(p, etudiant)]
    if not sources:
        sources = [p for p in fichiers if _nom_sans_doublon(p) == "faguet_nettoye.txt"
                   or (p.name.startswith("FAGUET_v") and p.suffix == ".zip")]
    if not sources:
        raise FileNotFoundError(f"Importez votre TXT nettoyé ou le ZIP du notebook 01 dans {dossier}, puis relancez la cellule.")
    corpus = _corpus_importe(sources[0], etudiant)
    for autre in sources[1:]:
        if _corpus_importe(autre, etudiant).sha256 != corpus.sha256:
            raise ValueError(f"Plusieurs textes du 01 diffèrent dans {dossier}. Gardez dans la session la version retenue en revue.")
    return corpus


def ouvrir_corpus_atelier(dossier: Path, source_01: str = "") -> Corpus:
    """Réutilise le texte nettoyé du 01, seul ou dans son archive."""
    dossier.mkdir(parents=True, exist_ok=True)
    copie = dossier / "faguet_nettoye.txt"
    if copie.is_file() and not source_01:
        return charger_corpus(copie)
    if source_01:
        source = Path(source_01).expanduser()
    else:
        archives = sorted(dossier.glob("*.zip"))
        if len(archives) > 1:
            raise ValueError("Plusieurs archives dans le dossier. Indiquez celle du notebook 01 dans SOURCE_01.")
        source = archives[0] if archives else Path.cwd() / "analyse_faguet_v2_0_0" / copie.name
    if not source.is_file():
        raise FileNotFoundError(
            f"Placez le fichier {copie.name} ou l’archive ZIP du notebook 01 dans {dossier}, "
            "ou indiquez son chemin dans SOURCE_01, puis relancez la cellule."
        )
    if source.suffix.lower() == ".zip":
        with ZipFile(source) as archive:
            contenu = archive.read(copie.name)
    else:
        contenu = source.read_bytes()
    if copie.is_file() and copie.read_bytes() != contenu:
        raise ValueError("Ce dossier contient déjà un autre texte nettoyé. Choisissez un nouveau dossier pour cette analyse.")
    if not copie.exists():
        copie.write_bytes(contenu)
    return charger_corpus(copie)


def enregistrer_resultats(dossier: Path, numero: str, contenu: dict, *,
                          numero_etudiant: str | None = None, sha256_corpus: str | None = None) -> Path:
    if numero_etudiant is None:
        chemin = dossier / f"resultats_{numero}.json"
    else:
        numero_etudiant = valider_numero_etudiant(numero_etudiant)
        chemin = dossier / f"resultats_{numero}_{numero_etudiant}.json"
        contenu = {**contenu, "numero_etudiant": numero_etudiant, "numero_notebook": numero}
        if sha256_corpus is not None:
            contenu["sha256_corpus"] = sha256_corpus
    donnees = json.dumps(contenu, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    sortie = NamedTemporaryFile(mode="w", dir=dossier, encoding="utf-8", delete=False)
    temporaire = Path(sortie.name)
    try:
        with sortie:
            sortie.write(donnees)
        temporaire.replace(chemin)
    finally:
        temporaire.unlink(missing_ok=True)
    print("Résultats enregistrés dans", chemin)
    return chemin


def lire_resultats(dossier: Path, numero: str, *, numero_etudiant: str | None = None,
                   sha256_corpus: str | None = None) -> dict:
    nom_ancien = f"resultats_{numero}.json"
    nom = nom_ancien
    if numero_etudiant is not None:
        numero_etudiant = valider_numero_etudiant(numero_etudiant)
        nom = f"resultats_{numero}_{numero_etudiant}.json"
    fichiers = sorted(dossier.glob(f"resultats_{numero}*.json"))
    copies = [p for p in fichiers if _nom_sans_doublon(p) == nom]
    if not copies and numero_etudiant is not None:
        copies = [p for p in fichiers if _nom_sans_doublon(p) == nom_ancien]
    if not copies:
        raise FileNotFoundError(f"Importez {nom}, exporté par le notebook {numero}, dans {dossier}, puis relancez la cellule.")
    contenu = json.loads(copies[0].read_text(encoding="utf-8"))
    if any(json.loads(p.read_text(encoding="utf-8")) != contenu for p in copies[1:]):
        raise ValueError(f"Plusieurs versions du résultat {numero} diffèrent dans {dossier}. Gardez uniquement votre version à reprendre.")
    if not isinstance(contenu, dict):
        raise ValueError(f"{copies[0].name} ne contient pas un résultat de notebook.")
    if numero_etudiant is not None and contenu.get("numero_etudiant", numero_etudiant) != numero_etudiant:
        raise ValueError(f"{copies[0].name} : le numéro étudiant du résultat ne correspond pas au vôtre.")
    if (numero_etudiant is not None and "numero_etudiant" not in contenu
            and _nom_sans_doublon(copies[0]) == nom_ancien):
        _signaler_import_anonyme(copies[0], numero_etudiant)
    if contenu.get("numero_notebook", numero) != numero:
        raise ValueError(f"{copies[0].name} : ce résultat provient d’un autre notebook.")
    if sha256_corpus is not None and contenu.get("sha256_corpus", sha256_corpus) != sha256_corpus:
        raise ValueError(f"{copies[0].name} : le texte utilisé pour cette mesure diffère du texte importé du 01.")
    return contenu


def charger_modele_francais():
    """Même découpage par ponctuation pour comparer les formes et leurs lemmes."""
    import spacy
    from spacy.cli import download

    modele = "fr_core_news_sm"
    if not spacy.util.is_package(modele):
        download(modele)
    nlp = spacy.load(modele, exclude=["parser", "senter", "ner"])
    nlp.add_pipe("sentencizer")
    return nlp


def lire_annonces_globales() -> dict:
    """Tableau du rapport Studio transcrit le 10 novembre 2026."""
    chemin = Path(__file__).resolve().parents[2] / "data" / "annonces_globales_gemini.json"
    if chemin.is_file():
        return json.loads(chemin.read_text(encoding="utf-8"))
    from urllib.request import urlopen

    url = ("https://raw.githubusercontent.com/dreymond732/tal-notebook-evaluator/"
           "51c355fd026d68a5bfada8e8cfa57687e5a57fd6/PT-LLMvsPy/data/annonces_globales_gemini.json")
    with urlopen(url, timeout=30) as reponse:
        return json.load(reponse)


def preparer_atelier(source_01: str = "", dossier_personnel: str = "", *,
                     numero_etudiant: str | None = None):
    """Ouvre les fichiers importés dans la session et prépare la reprise des résultats."""
    if numero_etudiant is not None:
        numero_etudiant = valider_numero_etudiant(numero_etudiant)
    try:
        from google.colab import files
    except ImportError:
        files = None
    if files is not None:
        dossier = DOSSIER_COLAB
        if dossier_personnel and Path(dossier_personnel).resolve() != dossier:
            raise ValueError("Dans Colab, importez vos fichiers dans /content via le volet Fichiers.")
    elif dossier_personnel:
        dossier = Path(dossier_personnel).expanduser()
    else:
        dossier = Path.cwd() if numero_etudiant is not None else Path.cwd() / "PT-Faguet"

    if numero_etudiant is None:
        corpus = ouvrir_corpus_atelier(dossier, source_01)
    else:
        corpus = _charger_import_01(dossier, source_01, numero_etudiant)
    identite = {"numero_etudiant": numero_etudiant,
                "sha256_corpus": corpus.sha256 if numero_etudiant is not None else None}

    def sauvegarder(numero: str, contenu: dict) -> Path:
        chemin = enregistrer_resultats(dossier, numero, contenu, **identite)
        if files is not None:
            try:
                files.download(str(chemin))
            except Exception:
                print(f"Pour récupérer {chemin.name}, ouvrez le volet Fichiers de Colab et choisissez Télécharger.")
        return chemin

    print("Dossier de la séance :", dossier)
    return corpus, dossier, partial(lire_resultats, dossier, **identite), sauvegarder
