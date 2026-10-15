"""TD5-bis — Paramètres, défauts et portée: analyse des seules traces enregistrées."""
from s1_expansion import CHECKS
from s1_revision import check_saved_notebook

EVAL_ID = 'td5-bis-s1'
MAX_SCORE_TOTAL = 6.0

def check_notebook(content_str, filename):
    return check_saved_notebook(content_str, filename, EVAL_ID, CHECKS[EVAL_ID])
