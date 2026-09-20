"""TD7 S3 : contrôle de microcas, aucune exécution de code soumis."""
from s3_audit import check_audit, same

EVAL_ID = "td7-s3"
MAX_SCORE_TOTAL = 7.0
EXPECTED = [{'mesurable': False, 'manquants': ['unite', 'fenetre', 'normalisation', 'agregation']}, {'N': 4, 'cooc': 1, 'marge_pivot': 2, 'marge_associe': 2}, {'exacte': True, 'debut': 3, 'fin': 15, 'alteree': False}, {'dans_intervalle': 'compatible selon le protocole', 'hors_intervalle': 'contredit selon le protocole'}, {'somme_paires': 3, 'union': 2}, {'N': 5, 'cooc': 2, 'marge_pivot': 3, 'marge_associe': 3}, {'indefini': 'insuffisamment défini', 'defini': 'compatible selon le protocole'}]
LABELS = ['Affirmation mesurable', 'Moteur de cooccurrences', 'Citation exacte et altérée', 'Verdict sous protocole', 'Ambiguïté de l’agrégation', 'Cas de transfert', 'Protocole absent ou explicite']
CHECKS = [
    {"label": label, "validate": lambda value, expected=expected: same(value, expected),
     "feedback": "Microcas déterministe : " + repr(expected) + ". Les transferts au corpus et les interprétations restent à relire avec l’enseignant."}
    for label, expected in zip(LABELS, EXPECTED)
]

def check_notebook(content_str, filename):
    return check_audit(content_str, filename, 7, CHECKS)
