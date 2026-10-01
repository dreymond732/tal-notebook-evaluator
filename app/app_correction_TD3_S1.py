"""TD3 S1: versioned, inert formative evaluation."""
from s1_revision import check_s1
from s1_reference import CHECKS as REFERENCE_CHECKS

EVAL_ID = 'td3-s1'
CHECKS = REFERENCE_CHECKS[3]
MAX_SCORE_TOTAL = 6.0

def check_notebook(content_str, filename):
    return check_s1(content_str, filename, 3, CHECKS)
