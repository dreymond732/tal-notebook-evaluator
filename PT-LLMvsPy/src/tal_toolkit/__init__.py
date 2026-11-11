"""PT-LLMvsPy : fonctions communes des analyses textométriques du S3."""
from .audit_llm import (
    champs_manquants, comparer_intervalle, evaluer_affirmation, verifier_citation,
)
from .metriques_globales import (ProtocoleGlobal, preparer_texte_pour_analyse, calculer_metriques_globales, comparer_annonces)
from .pretraitements import (
    OperationPretraitement, PlanPretraitement, ResultatPretraitement,
    executer_pretraitements, recenser_elements,
)
from .epuration import (
    TexteEpure, composer_texte_epure, exporter_texte_approuve,
)
from .inspection_td01 import (
    localiser_dans_original, fonctions_ayant_modifie_zone,
    compter_motif, valider_inspection,
)
from .comparaison_td01 import comparer_corpus_td01, INDICATEURS_TD01
from .soumission_td01 import (
    preparer_archive_td01, verifier_archive_td01, deposer_archive_drive,
    deposer_archive_drive_api,
    verifier_tests_personnels,
)
from .protocole_td01 import (
    SHA_FAGUET_TD01, SHA_FAGUET_EPURE_TD01,
    IDENTIFIANT_PROFIL_TD01, METRIQUES_TD01,
    plan_standard_td01, verifier_corpus_standard_td01,
    preparer_faguet_standard_td01, verifier_standardisation_td01,
)
from .io_corpus import Corpus, charger_corpus, corpus_depuis_texte
from .linguistic import DocCache, tokeniser_phrases
from .textometry import (
    concordances_exactes, contient_expression, couverture_pivots, frequences,
    mesurer, pmi_phrase, pour_mille, proportion, table_contingence,
)

__version__ = "0.3.0"
__all__ = [
    "ProtocoleGlobal", "preparer_texte_pour_analyse", "calculer_metriques_globales", "comparer_annonces",
    "OperationPretraitement", "PlanPretraitement", "ResultatPretraitement",
    "executer_pretraitements", "recenser_elements",
    "TexteEpure", "composer_texte_epure", "exporter_texte_approuve",
    "localiser_dans_original", "fonctions_ayant_modifie_zone",
    "compter_motif", "valider_inspection",
    "comparer_corpus_td01", "INDICATEURS_TD01",
    "preparer_archive_td01", "verifier_archive_td01",
    "deposer_archive_drive", "deposer_archive_drive_api", "verifier_tests_personnels",
    "SHA_FAGUET_TD01", "SHA_FAGUET_EPURE_TD01",
    "IDENTIFIANT_PROFIL_TD01", "METRIQUES_TD01",
    "plan_standard_td01", "verifier_corpus_standard_td01",
    "preparer_faguet_standard_td01", "verifier_standardisation_td01",
    "Corpus", "DocCache", "charger_corpus", "corpus_depuis_texte",
    "tokeniser_phrases", "frequences", "concordances_exactes",
    "contient_expression", "mesurer", "table_contingence",
    "proportion", "pour_mille", "pmi_phrase", "couverture_pivots",
    "verifier_citation", "champs_manquants", "comparer_intervalle",
    "evaluer_affirmation",
]
