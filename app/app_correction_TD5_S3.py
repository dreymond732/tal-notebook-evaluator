"""TD5 S3 : contrôle de microcas, aucune exécution de code soumis."""
from s3_audit import check_audit, same

EVAL_ID = "td5-s3"
MAX_SCORE_TOTAL = 7.0
EXPECTED = [{'conditionnelle': 0.666667, 'base': 0.5}, {'A': 0.75, 'B': 0.5, 'base_A': 0.75, 'base_B': 0.166667}, {'court': 40.0, 'long': 20.0}, {'associe_sachant_pivot': 0.666667, 'pivot_sachant_associe': 0.5}, {'sans_pivot': None, 'sans_associe': 0.0}, {'k1': 0.5, 'k3': 1.0}, {'effectif': 2, 'denominateur': 3, 'proportion': 0.666667}]
LABELS = ['Proportion conditionnelle', 'Association et fréquence de base', 'Normalisation par longueur', 'Asymétrie conditionnelle', 'Dénominateur nul', 'Sensibilité à la fenêtre', 'Effectif et dénominateur']
CHECKS = [
    {"label": label, "validate": lambda value, expected=expected: same(value, expected),
     "feedback": "Microcas déterministe : " + repr(expected) + ". Les transferts au corpus et les interprétations restent à relire avec l’enseignant."}
    for label, expected in zip(LABELS, EXPECTED)
]

def check_notebook(content_str, filename):
    return check_audit(content_str, filename, 5, CHECKS)
