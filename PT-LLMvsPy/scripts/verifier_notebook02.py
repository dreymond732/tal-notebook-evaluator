#!/usr/bin/env python3
"""Contrôle d'intégration sur le Faguet réel, sans chiffres Gemini attendus."""
from __future__ import annotations

from urllib.parse import quote
from urllib.request import urlopen

import spacy

from tal_toolkit import (
    charger_corpus, calculer_metriques_globales, ProtocoleGlobal,
    preparer_faguet_standard_td01,
)
from tal_toolkit.analyse_pt02 import auditer_reapplication, analyser_lexique_pt02


COMMIT = "b92e92b6c216014283056c83aa545881a447b3a5"
CHEMIN = "Notebooks TD/S3/ressources/faguet_source.txt"
SHA = "c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa"
URL = (
    f"https://raw.githubusercontent.com/dreymond732/tal-notebook-evaluator/"
    f"{COMMIT}/{quote(CHEMIN, safe='/')}"
)


def main():
    with urlopen(URL, timeout=60) as response:
        donnees = response.read()
    from tempfile import TemporaryDirectory
    from pathlib import Path

    with TemporaryDirectory() as temp:
        fichier = Path(temp) / "faguet_source.txt"
        fichier.write_bytes(donnees)
        corpus = charger_corpus(fichier, sha256_attendu=SHA)
        resultat, epure, preuve = preparer_faguet_standard_td01(corpus)
        from tal_toolkit.pretraitements import PlanPretraitement, OperationPretraitement
        operations = tuple(
            OperationPretraitement(
                item["nom"], item["justification"],
                tuple(item.get("cibles", ()))
            ) for item in resultat.plan["operations"]
        )
        plan = PlanPretraitement(operations, resultat.plan["identifiant"])
        audit = auditer_reapplication(epure.texte, plan)
        nlp = spacy.blank("fr")
        nlp.add_pipe("sentencizer")
        nlp.max_length = len(epure.texte) + 1000
        resultats = analyser_lexique_pt02(
            epure.texte, nlp, calculer_lemmes=True, taille_sttr=1000
        )
        controle = calculer_metriques_globales(
            epure.texte, nlp,
            protocole=ProtocoleGlobal(
                tokens="alphabetiques", formes="minuscules",
                retours="conserver", ignorer_phrases_sans_mots=True
            ), max_exemples=2
        )
        assert all(resultats["controles"].values())
        correspondances = {
            "tokens": "tokens_lexicaux",
            "types": "types_minuscules",
            "hapax": "hapax",
            "phrases": "phrases_non_vides",
        }
        for cle, autre in correspondances.items():
            assert controle["metriques"][cle] == resultats["globales"][autre]
        assert resultats["lemmatisation"]["statut"] == "NON_CALCULE"
        assert resultats["source_nettoyee_sha256"] == epure.sha256_texte_utf8
        assert len(resultats["champs_lexicaux"]) == 5
        assert len(resultats["onomastique"]) >= 5
        print("Faguet épuré SHA-256 :", epure.sha256_texte_utf8)
        print("Idempotence réapplication :", audit["idempotent_sur_ce_texte"])
        print("Modifications réapplication :", audit["operations"])
        print("Tokens lexicaux :", resultats["globales"]["tokens_lexicaux"])
        print("Types :", resultats["globales"]["types_minuscules"])
        print("Hapax :", resultats["globales"]["hapax"])
        print("Phrases :", resultats["globales"]["phrases_non_vides"])
        print("STTR blocs :", resultats["globales"]["sttr_nombre_blocs_complets"])
        print("Égalité des quatre comptes avec le moteur du semestre : OK")


if __name__ == "__main__":
    main()
