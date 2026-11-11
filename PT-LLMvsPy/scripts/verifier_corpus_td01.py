#!/usr/bin/env python3
"""Contrôle du profil sur le VRAI texte Faguet figé, avant diffusion Colab."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

import spacy

from tal_toolkit import (
    SHA_FAGUET_TD01, SHA_FAGUET_EPURE_TD01, METRIQUES_TD01, charger_corpus,
    comparer_corpus_td01, preparer_faguet_standard_td01,
)

SOURCE_URL = (
    "https://raw.githubusercontent.com/dreymond732/tal-notebook-evaluator/"
    "b92e92b6c216014283056c83aa545881a447b3a5/"
    "Notebooks%20TD/S3/ressources/faguet_source.txt"
)


def main() -> None:
    with urlopen(SOURCE_URL, timeout=30) as response:
        octets = response.read()
    assert sha256(octets).hexdigest() == SHA_FAGUET_TD01
    with TemporaryDirectory() as tmp:
        p = Path(tmp) / "faguet_source.txt"
        p.write_bytes(octets)
        corpus = charger_corpus(p, sha256_attendu=SHA_FAGUET_TD01)
        resultat, epure, standardisation = preparer_faguet_standard_td01(corpus)
        assert resultat.sha256_original == SHA_FAGUET_TD01
        assert len(epure.texte) == len(epure.indices_source)
        assert epure.sha256_texte_utf8 == standardisation["sha256_epure"]
        assert epure.sha256_texte_utf8 == SHA_FAGUET_EPURE_TD01
        print("CRLF =", corpus.texte.count("\r\n"))
        print("Caractères original/épuré =", len(corpus.texte), len(epure.texte))
        print("Source SHA-256 =", corpus.sha256)
        print("Épuré SHA-256 =", epure.sha256_texte_utf8)
        print("Opérations =", standardisation["transformations"])
        nlp = spacy.blank("fr")
        nlp.add_pipe("sentencizer")
        comparaison = comparer_corpus_td01(
            corpus, epure.texte, nlp, protocole=METRIQUES_TD01
        )
        assert comparaison["source_epuree_sha256"] == epure.sha256_texte_utf8
        assert len(comparaison["comparaison"]) == 7
        assert comparaison["controles"]["meme_protocole"]
        assert comparaison["controles"]["meme_pipeline"]
        print("Les sept métriques ont été calculées sur les deux versions.")


if __name__ == "__main__":
    main()
