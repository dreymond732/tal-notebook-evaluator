"""S2 v2: typed recorded traces and static dependencies, never execution."""
from s1_revision import check_saved_notebook


def check_s2(content_str, filename, evaluator, checks):
    return check_saved_notebook(content_str, filename, evaluator, checks)
