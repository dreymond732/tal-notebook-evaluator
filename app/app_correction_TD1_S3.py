"""Annotations spaCy : conformité et recoupements, pas vérité linguistique."""
from s3_audit import check_audit
from s3_audit_data import TEXT0, TEXT1
import s3_audit_linguistic as check

EVAL_ID = 'td1-s3'
MAX_SCORE_TOTAL = 6.0
REFERENCE = check.SPACY_REFERENCE['td1']
NOTE = 'Conformité aux sorties du pipeline fixé spaCy 3.8.7 / fr_core_news_sm 3.8.0 sur le texte fourni, sans garantie de vérité linguistique. La justesse des critiques et interprétations n’est pas évaluée automatiquement.'
CHECKS = [
    {'label': 'Annotations traçables', 'validate': lambda v: check.q1_td1(v, TEXT1, REFERENCE['annotations']),
     'feedback': 'Les annotations non ponctuation, leur ordre et leurs positions doivent correspondre au pipeline fixé. ' + NOTE},
    {'label': 'Phrases et tailles', 'validate': lambda v: check.phrases(v, TEXT1, REFERENCE['phrases']),
     'feedback': 'Les phrases et leurs nombres de tokens correspondent au pipeline fixé. ' + NOTE},
    {'label': 'Filtres conformes au pipeline',
     'validate': lambda v: check.filters(v, {1: {'annotations': REFERENCE['annotations']}}, REFERENCE['filters']),
     'feedback': 'Les trois listes concordent avec le pipeline fixé ; ordre et répétitions sont conservés, mots vides exclus des mots pleins. ' + NOTE},
    {'label': 'Repères de dépendance', 'required_text_fields': ['interpretation'], 'validate': lambda v: check.dependency_td1(v, TEXT1),
     'feedback': 'Le point porte sur deux tokens distincts localisés dans la première phrase et une relation renseignée. La pertinence du verbe, de la relation et de son interprétation n’est pas évaluée automatiquement. ' + NOTE},
    {'label': 'Comparaison des découpages', 'required_text_fields': ['interpretation'], 'validate': lambda v: check.counts_td1(v, TEXT0, REFERENCE['counts']),
     'feedback': 'split vaut 47, tous les tokens 56 et les tokens hors ponctuation et espaces 41 pour le pipeline fixé. ' + NOTE},
    {'label': 'Transfert documenté', 'required_text_fields': ['question'], 'validate': check.transfer,
     'feedback': 'Extrait de 2–4 phrases ; cinq annotations couvrant le début du texte sans omission hors blancs, listes et question. La justesse de la segmentation, des annotations et de la question de corpus n’est pas évaluée automatiquement. ' + NOTE},
]


def check_notebook(content_str, filename):
    return check_audit(content_str, filename, 1, CHECKS)
