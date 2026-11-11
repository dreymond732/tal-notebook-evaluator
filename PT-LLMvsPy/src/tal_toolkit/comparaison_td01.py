"""Comparaison homogène des métriques du corpus original et de la vue épurée.

Ne change ni les réglages spaCy, ni les filtres, ni les formules entre les corpus.
Les conventions de prétraitement ont déjà été approuvées hors de ce module.
"""
from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from typing import TYPE_CHECKING

from .io_corpus import Corpus
from .metriques_globales import ProtocoleGlobal, calculer_metriques_globales

if TYPE_CHECKING:
    from spacy.language import Language


INDICATEURS_TD01 = (
    ("tokens", "Tokens lexicaux", "tokens"),
    ("types", "Types distincts", "types"),
    ("hapax", "Hapax legomena", "types"),
    ("ttr", "TTR", "ratio"),
    ("hapax_types_pourcent", "Hapax parmi les types", "%"),
    ("phrases", "Phrases", "phrases"),
    ("mots_par_phrase", "Longueur moyenne", "tokens/phrase"),
)


def comparer_corpus_td01(
    original: Corpus,
    epure: Corpus | str,
    nlp: Language,
    *,
    protocole: ProtocoleGlobal | None = None,
) -> dict:
    """Recalcule chaque indicateur avec une politique identique.

    La politique retours='conserver' est obligatoire : la vue épurée doit
    être mesurée telle qu'approuvée, sans nettoyage silencieux supplémentaire.
    Les écarts relatifs sont rapportés à la mesure du texte original ; ils
    valent None lorsque la valeur d'origine est nulle.
    """
    protocole = protocole or ProtocoleGlobal()
    if protocole.retours != "conserver":
        raise ValueError("Mesurer chaque version exactement telle que fournie")
    if not isinstance(original, Corpus):
        raise TypeError("L'original doit être un Corpus avec SHA-256 des octets")
    if not isinstance(epure, (Corpus, str)):
        raise TypeError("L'épuré doit être un Corpus ou un texte")
    result_original = calculer_metriques_globales(
        original, nlp, protocole=protocole, max_exemples=4
    )
    result_epure = calculer_metriques_globales(
        epure, nlp, protocole=protocole, max_exemples=4
    )
    a, b = result_original["metriques"], result_epure["metriques"]
    lignes = []
    for cle, libelle, unite in INDICATEURS_TD01:
        avant, apres = a[cle], b[cle]
        ecart = None if avant is None or apres is None else apres - avant
        variation = None if ecart is None or not avant else ecart / avant * 100
        lignes.append({
            "id": cle, "indicateur": libelle, "unite": unite,
            "original": avant, "epure": apres, "ecart": ecart,
            "variation_relative_pourcent": variation,
        })
    return {
        "schema": "comparaison-td01-v1",
        "protocole_commun": asdict(protocole),
        "logiciel": result_original["logiciel"],
        "source_originale_sha256": original.sha256,
        "source_epuree_sha256": (
            epure.sha256 if isinstance(epure, Corpus)
            else sha256(epure.encode("utf-8")).hexdigest()
        ),
        "comparaison": lignes,
        "controles": {
            "original": result_original["controles"],
            "epure": result_epure["controles"],
            "meme_protocole": result_original["protocole"] == result_epure["protocole"],
            "meme_pipeline": result_original["logiciel"] == result_epure["logiciel"],
        },
    }
