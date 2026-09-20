"""Contrôle cumulatif S3 : rapport technique privé, relecture humaine requise."""
from s3_controls import check_control
import s3_controls_linguistic as check

EVAL_ID = 'controle-td2-s3'
MAX_SCORE_TOTAL = 20.0
CHECKS = [
    {"label": 'Corpus et annotations', "validate": check.c2q1, "feedback": 'Longueur exacte et couverture du texte par les annotations localisées.'},
    {"label": 'Fréquences des noms et verbes', "validate": check.c2q2, "feedback": 'Fréquences calculées à partir des annotations Q1 ; qualité linguistique à relire.'},
    {"label": 'Exclusion documentée', "validate": check.c2q3, "feedback": 'Exclusion atelier appliquée aux fréquences des noms, sans suppression supplémentaire.'},
    {"label": 'Catégories et classement', "validate": check.c2q4, "feedback": 'Comptages POS exacts par rapport à Q1 ; trois premiers décroissants, ex aequo libres.'},
    {"label": 'Calcul sur annotation de référence', "validate": check.c2q5, "feedback": 'Comptages exacts sur la table du port, exclusion et cas vide.'},
    {"label": 'Données des représentations', "validate": check.c2q6, "feedback": 'Données exactes des fréquences filtrées ; rendu et interprétation des figures à relire.'},
    {"label": 'Réutilisation sur un autre corpus', "validate": check.c2q7, "feedback": 'Couverture du nouveau corpus et fréquences cohérentes ; fonction et expression à relire.'},
]

def check_notebook(content_str, filename):
    return check_control(content_str, filename, 2, CHECKS)
