"""Annotations spaCy : conformité et recoupements, pas vérité linguistique."""
from s3_audit import check_audit
from s3_audit_data import TEXT0, TEXT1
import s3_audit_linguistic as check

EVAL_ID = 'td1-s3'
MAX_SCORE_TOTAL = 6.0
NOTE = 'Conformité structurelle seulement ; catégories, lemmes, segmentation et interprétations restent à vérifier humainement.'
CHECKS = [
    {'label': 'Annotations traçables', 'validate': lambda v: check.q1_td1(v, TEXT1),
     'feedback': 'Toutes les formes non ponctuation doivent retrouver leur emplacement dans le texte. ' + NOTE},
    {'label': 'Phrases et tailles', 'validate': lambda v: check.phrases(v, TEXT1),
     'feedback': 'Les phrases reconstituent le texte dans l’ordre, avec des tailles plausibles. ' + NOTE},
    {'label': 'Filtres cohérents avec Q1', 'validate': check.filters, 'contextual': True,
     'feedback': 'Les listes NOUN/VERB concordent avec les annotations déclarées Q1. Les mots pleins en sont un sous-ensemble. ' + NOTE},
    {'label': 'Repères de dépendance', 'validate': lambda v: check.dependency(v, TEXT1),
     'feedback': 'Le point porte sur des positions et formes effectivement présentes. La relation et son sens nécessitent une relecture humaine. ' + NOTE},
    {'label': 'Comparaison des découpages', 'validate': lambda v: check.counts_td1(v, TEXT0),
     'feedback': 'split vaut 47 ; les autres comptages doivent respecter leurs bornes. ' + NOTE},
    {'label': 'Transfert documenté', 'validate': check.transfer,
     'feedback': 'Extrait de 2–4 phrases, cinq annotations localisées, listes et question. ' + NOTE},
]


def check_notebook(content_str, filename):
    return check_audit(content_str, filename, 1, CHECKS)
