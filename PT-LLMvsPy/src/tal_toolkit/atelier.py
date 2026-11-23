"""Entrées et sorties communes aux cahiers d'analyse de Faguet."""
from __future__ import annotations

import json
from pathlib import Path
from zipfile import ZipFile

from .io_corpus import Corpus, charger_corpus


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


def enregistrer_resultats(dossier: Path, numero: str, contenu: dict) -> Path:
    chemin = dossier / f"resultats_{numero}.json"
    chemin.write_text(json.dumps(contenu, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print("Résultats enregistrés dans", chemin)
    return chemin


def lire_resultats(dossier: Path, numero: str) -> dict:
    chemin = dossier / f"resultats_{numero}.json"
    if not chemin.is_file():
        raise FileNotFoundError(f"Exécutez la dernière cellule du notebook {numero}, puis reprenez ce cahier dans le même dossier ({dossier}).")
    return json.loads(chemin.read_text(encoding="utf-8"))


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


def preparer_atelier(source_01: str = "", dossier_personnel: str = ""):
    """Monte Drive dans Colab et rattache les fichiers des trois séances au même dossier."""
    from functools import partial
    try:
        from google.colab import drive
    except ImportError:
        defaut = Path.cwd() / "PT-Faguet"
    else:
        drive.mount("/content/drive")
        defaut = Path("/content/drive/MyDrive/PT-Faguet")
    dossier = Path(dossier_personnel).expanduser() if dossier_personnel else defaut
    corpus = ouvrir_corpus_atelier(dossier, source_01)
    print("Votre dossier de travail :", dossier)
    return corpus, dossier, partial(lire_resultats, dossier), partial(enregistrer_resultats, dossier)
