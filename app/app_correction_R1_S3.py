from revision_s3 import check_revision

EVAL_ID = "td-r1-s3"
MAX_SCORE_TOTAL = 4.0

def check_notebook(content_str, filename):
    return check_revision(content_str, EVAL_ID)
