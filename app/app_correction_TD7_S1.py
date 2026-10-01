"""TD7 S1: versioned, inert formative evaluation."""
from s1_revision import check_s1
from s1_reference import CHECKS as REFERENCE_CHECKS

EVAL_ID = 'td7-s1'
CHECKS = REFERENCE_CHECKS[7]
MAX_SCORE_TOTAL = 7.0

def check_notebook(content_str, filename):
    return check_s1(content_str, filename, 7, CHECKS)
