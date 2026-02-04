# Fichier: app_correction_Controle_S2.py
from engine import run_evaluation

EVAL_ID = "controle-s2"
MAX_SCORE_TOTAL = 20.0

# --- CALCUL DES RÉPONSES (DÉTERMINISTE) ---
# Le corpus contient 60 blocs de 10 lignes = 600 lignes.
# Les lignes vides sont aux indices 4 et 9 de chaque bloc de 10.
# 2 lignes vides par bloc * 60 blocs = 120 lignes vides.
# Lignes non vides = 600 - 120 = 480.

# Q5 : "Nature" est dans la ligne 0 de chaque bloc. 60 blocs = 60 lignes.
# Q7 : Nombre de mots. Bloc de base (nettoyé) :
# "la nature est un temple où de vivants piliers" (9 mots)
# ... calcul total basé sur le texte exact = 2880 mots.

CORRECT_ANSWERS = {
    # Partie 1 : Algo
    'Q1': [3, 6, 12, 15, 21, 24, 30, 33, 39, 42, 48],
    'Q2': {'a': 10, 'b': 25, 'c': 40, 'd': 40},
    'Q3': 0.5, # Intersection {le, chat, mange, la, souris} (5) vs {fromage...} -> Inter=3, Union=6 -> 0.5
    
    # Partie 2 : Fichiers Lecture
    'Q4': 480, # 600 lignes tot - 120 vides
    'Q5': 60,  # 1 occurrence par bloc de 10, 60 blocs
    
    # Partie 3 : Nettoyage
    'Q6': "salut  ça va  ", 
    'Q7': 2880, # Calculé sur la base exacte des strophes fournies
    'Q8': {'nature': 60}, # On teste juste une clé spécifique pour valider la structure
    'Q9': 0, # Vu que tout est répété 60 fois, il n'y a aucun Hapax.
    
    # Partie 4 : Écriture
    'Q10': ['a;60', 'avec;60', 'aux;0'], # On vérifie le format "mot;count" (ex: 'a' est le 1er alphabétique)
    # Note: 'a' (verbe avoir ou préposition) apparait 1 fois par bloc ("passe à travers") -> 60 fois.
    
    'Q11': 240 
    # Lignes commençant par 'L' dans le bloc :
    # 0: "La Nature..." (OK)
    # 1: "Laissent..." (OK)
    # 2: "L'homme..." (OK)
    # 8: "Les parfums..." (OK)
    # -> 4 lignes par bloc * 60 blocs = 240 lignes.
}

POINTS_BREAKDOWN = {
    'Q1': 1.0, 'Q2': 2.0, 'Q3': 2.0, # Algo (5 pts)
    'Q4': 1.0, 'Q5': 2.0,            # Lecture (3 pts)
    'Q6': 2.0, 'Q7': 2.0, 'Q8': 2.0, 'Q9': 1.0, # Traitement (7 pts)
    'Q10': 2.0, 'Q11': 3.0           # Écriture (5 pts)
}

def check_notebook(content_str, filename):
    return run_evaluation(
        content_str, 
        filename, 
        CORRECT_ANSWERS, 
        POINTS_BREAKDOWN, 
        MAX_SCORE_TOTAL,
        EVAL_ID
    )