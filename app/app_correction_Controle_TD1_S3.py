"""Contrôle cumulatif S3 : rapport technique privé, relecture humaine requise."""
from s3_controls import check_control
import s3_controls_linguistic as check

EVAL_ID = 'controle-td1-s3'
MAX_SCORE_TOTAL = 20.0
CHECKS = [
    {"label": 'Mesures Python du texte', "validate": check.c1q1, "feedback": 'Longueur exacte, split en minuscules, dictionnaire des fréquences et nombre de formes.'},
    {"label": 'Annotations localisées', "validate": lambda v, ctx: check.annot_value(v, check.C1["texte_musee"]), "feedback": 'Tous les tokens retrouvent leurs positions ; les catégories et lemmes restent à relire humainement.'},
    {"label": 'Phrases et tailles cohérentes', "validate": check.c1q3, "feedback": 'Couverture du texte et tailles cohérentes avec Q2 ; frontières linguistiques à relire.'},
    {"label": 'Filtres liés aux annotations', "validate": check.c1q4, "feedback": 'Listes dérivées exactement des annotations Q2 selon les filtres annoncés.'},
    {"label": 'Repères de dépendance', "validate": check.c1q5, "feedback": 'Deux tokens localisés dans la deuxième phrase ; relation et figure displaCy à relire humainement.'},
    {"label": 'Transfert au transport', "validate": check.c1q6, "feedback": 'Annotations localisées et comptages cohérents sur le texte du transport.'},
    {"label": 'Fonction de bilan et cas vide', "validate": check.c1q7, "feedback": 'Quatre corpus dont le vide ; longueurs et tailles exactes/cohérentes. Segmentation à relire.'},
]

def check_notebook(content_str, filename):
    return check_control(content_str, filename, 1, CHECKS)
