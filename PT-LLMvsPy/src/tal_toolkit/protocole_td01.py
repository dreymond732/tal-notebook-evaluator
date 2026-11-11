"""Contrat commun de prétraitement de Faguet pour le TD01 (version S3).

Aucune adaptation automatique aux résultats de Gemini. Le plan est identique
pour toute étudiante ; seules les études de microcas et les commentaires
diffèrent. Les décisions scientifiques restent soumises à l'enseignant.
"""
from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256

from .epuration import TexteEpure, composer_texte_epure
from .io_corpus import Corpus
from .metriques_globales import ProtocoleGlobal
from .pretraitements import (
    OperationPretraitement, PlanPretraitement, ResultatPretraitement,
    executer_pretraitements, recenser_elements,
)

SHA_FAGUET_TD01 = "c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa"
SHA_FAGUET_EPURE_TD01 = "0885496f4abf4ca9112a3c303f8dc69cb887ffaa34033371aa7c49bad9e38fc2"
LONGUEUR_FAGUET_EPURE_TD01 = 446289
IDENTIFIANT_PROFIL_TD01 = "faguet-td01-standard-v1"
OPERATIONS_TD01 = (
    ("masquer_blocs_notes", "Écarter les trois blocs de notes éditoriales"),
    ("masquer_appels_notes", "Écarter les quatre renvois bibliographiques entre crochets"),
    ("masquer_separateurs", "Écarter les lignes d'astérisques purement visuelles"),
    ("recomposer_lignes", "Réunir les lignes typographiques sans effacer les paragraphes"),
)
ATTENDUS_STRUCTURAUX_TD01 = {
    "blocs_notes": 3,
    "appels_notes": 4,
    "separateurs": 20,
    "cesures_candidates": 0,
    "apostrophes_courbes": 0,
}
METRIQUES_TD01 = ProtocoleGlobal(
    tokens="alphabetiques",
    formes="minuscules",
    retours="conserver",
    ignorer_phrases_sans_mots=True,
)


def plan_standard_td01() -> PlanPretraitement:
    """Plan entièrement déterminé, sans arbitrage individuel des traitements."""
    return PlanPretraitement(
        tuple(OperationPretraitement(nom, raison) for nom, raison in OPERATIONS_TD01),
        identifiant=IDENTIFIANT_PROFIL_TD01,
    )


def verifier_corpus_standard_td01(corpus: Corpus) -> dict:
    """Refuse une autre édition ou des transformations cachées de la source."""
    if not isinstance(corpus, Corpus) or corpus.sha256 != SHA_FAGUET_TD01:
        raise ValueError("Corpus Faguet différent du commit figé du TD01")
    inventaire = recenser_elements(corpus)
    observes = {
        cle: inventaire["categories"][cle]["nombre"]
        for cle in ATTENDUS_STRUCTURAUX_TD01
    }
    if observes != ATTENDUS_STRUCTURAUX_TD01:
        raise ValueError("Structure du corpus Faguet inattendue : vérifier la source")
    return {"sha256": corpus.sha256, "inventaire": observes}


def preparer_faguet_standard_td01(
    corpus: Corpus,
) -> tuple[ResultatPretraitement, TexteEpure, dict]:
    """Exécute et vérifie le même plan de traitement sur le même corpus."""
    reference = verifier_corpus_standard_td01(corpus)
    plan = plan_standard_td01()
    resultat = executer_pretraitements(corpus, plan=plan, max_exemples=50)
    attendus_modifications = (3, 4, 20, 6479)
    observes_modifications = tuple(
        ligne["modifications"] for ligne in resultat.execution
    )
    if observes_modifications != attendus_modifications:
        raise ValueError("Nombre de transformations incompatible avec Faguet standard")
    vue = composer_texte_epure(resultat)
    if (not resultat.indices_conserves
            or resultat.sha256_original != corpus.sha256
            or vue.sha256_source != corpus.sha256
            or sha256(vue.texte.encode("utf-8")).hexdigest() != vue.sha256_texte_utf8
            or len(vue.indices_source) != len(vue.texte)
            or len(vue.texte) != LONGUEUR_FAGUET_EPURE_TD01
            or vue.sha256_texte_utf8 != SHA_FAGUET_EPURE_TD01):
        raise ValueError("Texte épuré non standard : empreinte ou longueur différente")
    return resultat, vue, {
        "schema": "standardisation-td01-v1",
        "profil": IDENTIFIANT_PROFIL_TD01,
        "source": reference,
        "transformations": [
            {"nom": ligne["operation"], "modifications": ligne["modifications"]}
            for ligne in resultat.execution
        ],
        "sha256_epure": vue.sha256_texte_utf8,
        "politique_mesures": asdict(METRIQUES_TD01),
        "statut": "CALCULE_ET_CONTROLE_LOCAL",
        "validation_enseignante": "A_CONFIRMER_APRES_REVUE",
    }


def verifier_standardisation_td01(
    standardisation: dict, manifeste: dict, comparaison: dict,
) -> None:
    """Vérifie les preuves standardisées avant de constituer une soumission."""
    if standardisation.get("schema") != "standardisation-td01-v1":
        raise ValueError("Contrat de standardisation manquant")
    if standardisation.get("profil") != IDENTIFIANT_PROFIL_TD01:
        raise ValueError("Plan d'épuration hors protocole commun")
    if standardisation.get("source", {}).get("sha256") != SHA_FAGUET_TD01:
        raise ValueError("Empreinte source hors protocole commun")
    if manifeste["source"]["plan"]["identifiant"] != IDENTIFIANT_PROFIL_TD01:
        raise ValueError("Manifeste incohérent avec le plan commun")
    if (tuple(o["nom"] for o in manifeste["source"]["plan"]["operations"])
            != tuple(n for n, _ in OPERATIONS_TD01)):
        raise ValueError("L'ordre des opérations ne suit pas le profil commun")
    if (standardisation.get("sha256_epure") != manifeste["export"]["sha256_texte_utf8"]
            or standardisation.get("sha256_epure") != SHA_FAGUET_EPURE_TD01):
        raise ValueError("Empreinte du texte épuré incohérente")
    if comparaison.get("protocole_commun") != asdict(METRIQUES_TD01):
        raise ValueError("Protocole de métriques non standard")
    if (comparaison["source_originale_sha256"] != SHA_FAGUET_TD01
            or comparaison["source_epuree_sha256"] != standardisation["sha256_epure"]):
        raise ValueError("Comparaison non conforme à la source et au texte épuré")
