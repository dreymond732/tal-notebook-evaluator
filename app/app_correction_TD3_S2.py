"""S2 v2 : critères par question, traces typées et constructions inertes."""
from s2_revision import check_s2
from s2_reference import CHECKS, REFERENCES, WEIGHTS

EVAL_ID = 'td3-S2'
CORRECT_ANSWERS = REFERENCES[3]
POINTS_BREAKDOWN = WEIGHTS[3]
MAX_SCORE_TOTAL = sum(POINTS_BREAKDOWN.values())
HUMAN_REVIEW = 'Le score technique porte sur les traces enregistrées et les constructions repérées. La correction générale des algorithmes et les explications demandent une relecture humaine.'
HUMAN_REVIEW_DIMENSIONS = ['Conformité de la démarche aux consignes', 'Traitement des cas limites', 'Explications et justification des choix']


def check_notebook(content_str, filename):
    return check_s2(content_str, filename, EVAL_ID, CHECKS[3])
