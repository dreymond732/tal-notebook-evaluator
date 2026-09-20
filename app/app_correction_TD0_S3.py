"""Diagnostic texte : résultats déterministes, sans exécution côté serveur."""
from collections import Counter
from s3_audit import check_audit, same, keys
from s3_audit_data import TEXT0

EVAL_ID = 'td0-s3'
MAX_SCORE_TOTAL = 7.0
EXPECTED = [
    {'caracteres': len(TEXT0)}, {'mots': TEXT0.split()}, {'occurrences': len(TEXT0.split())},
    {'formes': len(set(TEXT0.split()))}, {'frequences': dict(Counter(TEXT0.split()))},
    {'frequences': dict(Counter(TEXT0.lower().split()))},
]
LABELS = ['Lecture UTF-8', 'Découpage brut', 'Occurrences', 'Formes distinctes', 'Fréquences brutes', 'Fréquences minuscules']
CHECKS = [{'label': label, 'validate': lambda value, expected=expected: same(value, expected),
           'feedback': 'Résultat du texte fixé : ' + repr(expected)} for label, expected in zip(LABELS, EXPECTED)]
CHECKS.append({'label': 'Preuve du découpage et limites à relire',
               'validate': lambda value: keys(value, ['split', 'limites']) and same(value['split'], ['L’analyse,', 'c’est', 'utile', '!']) and isinstance(value['limites'], str),
               'feedback': 'Le point porte sur la liste exacte issue du découpage du microcas. La synthèse limites est à relire humainement, sans note automatique de qualité.'})


def check_notebook(content_str, filename):
    return check_audit(content_str, filename, 0, CHECKS)
