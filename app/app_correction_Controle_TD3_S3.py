"""Contrôle cumulatif S3 : rapport technique privé, relecture humaine requise."""
from s3_controls import check_control
import s3_controls_linguistic as check

EVAL_ID = 'controle-td3-s3'
MAX_SCORE_TOTAL = 20.0
CHECKS = [
    {"label": 'Périmètre du corpus', "validate": check.c3q1, "feedback": 'Mesures exactes du corpus synthétique et identifiants des quatre citations.'},
    {"label": 'Concordances exhaustives', "validate": check.c3q2, "feedback": 'Toutes les sous-chaînes plan, indices et contextes de douze caractères ; recherche absente vide.'},
    {"label": 'Fragment, forme, lemme et expression', "validate": check.c3q3, "feedback": 'Occurrences exactes de fragments/formes/expression ; les lemmes ont des positions vérifiables, leur pertinence relève de la relecture.'},
    {"label": 'Citations exactes', "validate": check.c3q4, "feedback": 'Premier indice et booléen exact pour chaque citation, sans normalisation.'},
    {"label": 'Normalisation et passages candidats', "validate": check.c3q5, "feedback": 'Recherche normalisée exacte ; candidats présents dans le texte. Leur pertinence est à relire.'},
    {"label": 'Tests de concordance', "validate": check.c3q6, "feedback": 'Cas répété, fragment inclus dans un mot, texte vide et motif vide avec erreur annoncée.'},
    {"label": 'Transfert au bulletin radio', "validate": check.c3q7, "feedback": 'Occurrences, formes et vérification exacte des citations sur le second corpus.'},
]

def check_notebook(content_str, filename):
    return check_control(content_str, filename, 3, CHECKS)
