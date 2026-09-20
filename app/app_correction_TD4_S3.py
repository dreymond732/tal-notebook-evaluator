"""TD4 S3 : contrôle de microcas, aucune exécution de code soumis."""
from s3_audit import check_audit, same

EVAL_ID = "td4-s3"
MAX_SCORE_TOTAL = 7.0
EXPECTED = [{'chat': 2, 'livre': 2, 'N': 4}, {'chat_livre': 1, 'chat_plume': 1, 'livre_plume': 0}, {'somme_paires': 3, 'union': 2}, {'k1': 1, 'k3': 2}, {'sans_frontiere': 1, 'dans_phrase': 0}, {'formes_chat': 1, 'lemmes_chat': 2}, {'N': 4, 'cooc': 1, 'marge_pivot': 2, 'marge_associe': 2}]
LABELS = ['Marges de phrases', 'Cooccurrences de phrases', 'Somme et union', 'Fenêtres de mots', 'Frontières des phrases', 'Formes et lemmes', 'Invariants quantitatifs']
CHECKS = [
    {"label": label, "validate": lambda value, expected=expected: same(value, expected),
     "feedback": "Microcas déterministe : " + repr(expected) + ". Les transferts au corpus et les interprétations restent à relire avec l’enseignant."}
    for label, expected in zip(LABELS, EXPECTED)
]

def check_notebook(content_str, filename):
    return check_audit(content_str, filename, 4, CHECKS)
