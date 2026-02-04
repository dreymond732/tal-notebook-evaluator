# Fichier: app_correction_TD5_S2.py
from engine import run_evaluation

# --- Configuration ---
EVAL_ID = "td5-S2"
MAX_SCORE_TOTAL = 25.0

# Réponses attendues pour les 25 exercices
CORRECT_ANSWERS = {
    'Q1': [0, 4, 16, 36, 64, 100, 144, 196, 256, 324, 400],
    'Q2': ['arbre', 'ecole', 'igloo', 'orange'],
    'Q3': {'le': 2, 'traitement': 10, 'automatique': 11, 'du': 2, 'langage': 7, 'est': 3, 'passionnant': 11},
    'Q4': 'passionnant est langage du automatique traitement le',
    'Q5': {'nom': 'Dupont', 'prenom': 'Jean', 'age': 25},
    'Q6': True,
    'Q7': True,
    'Q8': 2,
    'Q9': 'TAL',
    'Q10': 'bcd',
    'Q11': [1, 2, 3, 4, 5, 6],
    'Q12': {'a': 10, 'b': 25, 'c': 40, 'd': 40},
    'Q13': {'Maths': ['Alice', 'Bob'], 'Physique': ['Charlie']},
    # Q13 Note : pour les listes dans les valeurs, l'ordre n'importe pas si votre moteur gère les sets
    # Sinon, il faudra peut-être trier la réponse de l'étudiant dans engine.py ou ici.
    'Q14': [('Bob', 15), ('Alice', 12), ('Charlie', 10)],
    'Q15': 2,
    'Q16': ['bonjour', 'comment', 'ça', 'va'],
    'Q17': ['chat', 'noir', 'chien', 'dort'],
    'Q18': [('je', 'suis'), ('suis', 'content')],
    'Q19': [('un', 'deux', 'trois'), ('deux', 'trois', 'quatre')],
    'Q20': 0.5, # Intersection {chat,souris} (2) / Union {chat,chien,souris,oiseau} (4) = 0.5
    'Q21': 0.5, # 3/6
    'Q22': 32,
    'Q23': 'progr',
    'Q24': {'chat': 1, 'chien': 1},
    'Q25': ['python', 'est', 'super']
}

# Barème simple : 1 point par question
POINTS_BREAKDOWN = {f"Q{i}": 1.0 for i in range(1, 26)}

def check_notebook(content_str, filename):
    return run_evaluation(
        content_str, 
        filename, 
        CORRECT_ANSWERS, 
        POINTS_BREAKDOWN, 
        MAX_SCORE_TOTAL,
        EVAL_ID
    )