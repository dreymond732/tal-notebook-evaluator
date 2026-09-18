from formative_s1 import check_formative_notebook

EVAL_ID = 'td7-s1'
MAX_SCORE_TOTAL = 7.0
CHECKS = [{'label': 'Recherche insensible à la casse', 'source': ['re.search', 're.IGNORECASE'], 'output': 'Résultat Q1 :', 'points': 1.0, 'feedback': 'Reprendre : recherche insensible à la casse.'}, {'label': 'Extraction de nombres', 'source': ['re.findall', '\\d+'], 'output': 'Résultat Q2 :', 'points': 1.0, 'feedback': 'Reprendre : extraction de nombres.'}, {'label': 'Extraction de mots', 'source': ['re.findall'], 'output': 'Résultat Q3 :', 'points': 1.0, 'feedback': 'Reprendre : extraction de mots.'}, {'label': 'Remplacement de date', 'source': ['re.sub', '\\d{2}/\\d{2}/\\d{4}'], 'output': 'Résultat Q4 :', 'points': 1.0, 'feedback': 'Reprendre : remplacement de date.'}, {'label': 'Nettoyage paramétré', 'source': ['def nettoyer_texte', 're.sub', '.lower('], 'output': 'Résultat Q5 :', 'points': 1.0, 'feedback': 'Reprendre : nettoyage paramétré.'}, {'label': 'Pipeline', 'source': ['def analyser_texte', 'nettoyer_texte', 'frequences'], 'output': 'Résultat Q6 :', 'points': 1.0, 'feedback': 'Reprendre : pipeline.'}, {'label': 'Limite interprétée', 'source': [], 'output': 'Résultat Q7 :', 'points': 1.0, 'feedback': 'Reprendre : limite interprétée.'}]

def check_notebook(content_str, filename):
    return check_formative_notebook(content_str, CHECKS, MAX_SCORE_TOTAL)
