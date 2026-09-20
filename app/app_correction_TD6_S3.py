"""TD6 S3 : contrôle de microcas, aucune exécution de code soumis."""
from s3_audit import check_audit, same

EVAL_ID = "td6-s3"
MAX_SCORE_TOTAL = 7.0
EXPECTED = [{'positions': [1, 3], 'relatives': [0.25, 0.75]}, {'effectifs': [2, 0, 0, 1], 'tailles': [2, 2, 2, 2]}, {'chat': [500.0, 250.0], 'plume': [0.0, 250.0]}, {'k': [1, 2, 3], 'cooc': [1, 2, 2]}, {'debut': 2, 'fin': 5, 'contexte': 'puis plume après'}, {'etiquettes': ['segment 1', 'segment 2'], 'valeurs': [500.0, 250.0]}, {'effectif': 2, 'taille': 6, 'pour_mille': 333.333333}]
LABELS = ['Dispersion des occurrences', 'Distribution par segments', 'Carte de chaleur normalisée', 'Sensibilité aux paramètres', 'Retour au contexte', 'Données du graphique', 'Transfert à un nouveau segment']
CHECKS = [
    {"label": label, "validate": lambda value, expected=expected: same(value, expected),
     "feedback": "Microcas déterministe : " + repr(expected) + ". Les transferts au corpus et les interprétations restent à relire avec l’enseignant."}
    for label, expected in zip(LABELS, EXPECTED)
]

def check_notebook(content_str, filename):
    return check_audit(content_str, filename, 6, CHECKS)
