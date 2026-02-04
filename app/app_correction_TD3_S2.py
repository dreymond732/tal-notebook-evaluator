from engine import run_evaluation

EVAL_ID = "td3-S2"
MAX_SCORE_TOTAL = 30.0

CORRECT_ANSWERS = {
    'Q1': 300.0, 
    'Q2': {'deb': 13, 'fin': 19}, 
    'Q3': True, 
    'Q4': 'python tal', 
    'Q5': 2, 
    'Q6': ['tal', 'spacy', 'nlp'], 
    'Q7': 3, 
    'Q8': [0, 4, 16, 36, 64], 
    'Q9': {'tal': 2, 'est': 1, 'cool': 1, 'python': 1}, 
    'Q10': [3, 2, 1], 
    'Q11': 'tal', 
    'Q12': 17, 
    'Q13': [('annotation', 10), ('python', 6), ('tal', 3), ('nlp', 3)], 
    'Q14': {'intersection': {3}, 'union': {1, 2, 3, 4}}, 
    'Q15': None, 
    'Q16': 120, 
    'Q17': {'max': 10, 'index': 1}, 
    'Q18': [('tal', 'est'), ('est', 'cool')], 
    'Q19': {'a': 1, 'b': 2, 'c': 3}, 
    'Q20': [1, 2, 4, 5, 7, 8], 
    'Q21': 1, 
    'Q22': {'moyenne': 5.0, 'ecart_type': 2.0}, 
    'Q23': 4, 
    'Q24': True, 
    'Q25': 15, 
    'Q26': {'tal': 3, 'python': 6, 'spacy': 5}, 
    'Q27': [9, 7], 
    'Q28': ['tal', 'et', 'python'], 
    'Q29': [('analyser', 'corpus'), ('analyser', 'termes'), ('analyser', 'tokens'), ('extraire', 'corpus'), ('extraire', 'termes'), ('extraire', 'tokens')], 
    'Q30': 6
}

POINTS_BREAKDOWN = {f"Q{i}": 1.0 for i in range(1, 31)}

def check_notebook(content_str, filename):
    return run_evaluation(content_str, filename, CORRECT_ANSWERS, POINTS_BREAKDOWN, MAX_SCORE_TOTAL, EVAL_ID)
