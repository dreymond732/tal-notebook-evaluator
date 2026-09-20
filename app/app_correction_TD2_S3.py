"""Fréquences spaCy : invariants et cohérence, pas vérité linguistique."""
from s3_audit import check_audit
from s3_audit_data import TEXT2
import s3_audit_linguistic as check

EVAL_ID = 'td2-s3'
MAX_SCORE_TOTAL = 7.0
NOTE = 'Contrôle de structure/cohérence uniquement : annotations et interprétations sont à relire humainement.'
CHECKS = [
    {'label': 'Synthèse et dix annotations', 'validate': lambda v: check.summary_td2(v, TEXT2),
     'feedback': 'Longueur exacte du texte ; dix annotations dans l’ordre et comptages bornés. ' + NOTE},
    {'label': 'Fréquences de noms et verbes', 'validate': lambda v: check.two_frequencies(v, TEXT2),
     'feedback': 'Dictionnaires non vides à effectifs entiers positifs, total borné. ' + NOTE},
    {'label': 'Effet exact des exclusions', 'validate': check.exclusions, 'contextual': True,
     'feedback': 'avant reprend Q2 ; apres retire exactement les lemmes exclus. ' + NOTE},
    {'label': 'Distribution des POS', 'validate': lambda v: check.pos_counts(v, TEXT2),
     'feedback': 'Catégories valides, ni PUNCT ni SPACE ; top3 ordonné et cohérent. ' + NOTE},
    {'label': 'Cinq contrôles manuels documentés', 'validate': lambda v: check.linguistic_review(v, TEXT2),
     'feedback': 'Cinq formes présentes dans le texte ; champs d’annotation présents. Les jugements ne sont pas notés automatiquement. ' + NOTE},
    {'label': 'Données des figures', 'validate': check.chart_data, 'contextual': True,
     'feedback': 'Le dictionnaire des figures reprend les noms filtrés en Q3. La présence et la qualité des figures sont vérifiées humainement. ' + NOTE},
    {'label': 'Cohérence des fonctions généralisées', 'validate': check.generalization, 'contextual': True,
     'feedback': 'Versions spécialisées et générales retrouvent Q2 ; combinaison = somme des deux dictionnaires. ' + NOTE},
]


def check_notebook(content_str, filename):
    return check_audit(content_str, filename, 2, CHECKS)
