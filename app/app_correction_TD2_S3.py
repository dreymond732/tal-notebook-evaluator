"""Fréquences spaCy : invariants et cohérence, pas vérité linguistique."""
from s3_audit import check_audit
from s3_audit_data import TEXT2
import s3_audit_linguistic as check

EVAL_ID = 'td2-s3'
MAX_SCORE_TOTAL = 7.0
REFERENCE = check.SPACY_REFERENCE['td2']
NOTE = 'Référence technique : spaCy 3.8.7 / fr_core_news_sm 3.8.0 sur le corpus fixé, sans garantie de vérité linguistique. Les critiques et interprétations ne sont pas autocorrigées.'
CHECKS = [
    {'label': 'Synthèse et dix annotations', 'validate': lambda v: check.summary_td2(v, TEXT2, REFERENCE),
     'feedback': 'Longueur, phrases, tokens et dix premières annotations non ponctuation conformes au pipeline fixé. ' + NOTE},
    {'label': 'Fréquences de noms et verbes', 'validate': lambda v: check.two_frequencies(v, TEXT2, REFERENCE['frequencies']),
     'feedback': 'Dictionnaires complets conformes au pipeline fixé, avec effectifs entiers positifs (aucun booléen). ' + NOTE},
    {'label': 'Effet exact des exclusions', 'required_text_fields': ['justification'], 'validate': lambda v: check.exclusions(v, {2: REFERENCE['frequencies']}),
     'feedback': 'avant reprend les noms de référence ; apres retire exactement les lemmes exclus. ' + NOTE},
    {'label': 'Distribution des POS', 'required_text_fields': ['limite'], 'validate': lambda v: check.pos_counts(v, TEXT2, REFERENCE['pos']),
     'feedback': 'Distribution exacte du pipeline hors ponctuation et espaces ; top3 décroissant, ex æquo libres. ' + NOTE},
    {'label': 'Cinq contrôles manuels documentés', 'required_text_fields': ['limite_modele'], 'validate': lambda v: check.linguistic_review(v, TEXT2, REFERENCE),
     'feedback': 'Liste de lemmes conforme au pipeline ; cinq occurrences annotées sélectionnées librement, sans répétition artificielle. Les jugements ne sont pas notés automatiquement. ' + NOTE},
    {'label': 'Données des figures', 'required_text_fields': ['hypothese', 'verification'], 'validate': check.chart_data, 'contextual': True,
     'dependencies': {3: lambda v: check.keys(v, ['apres']) and check.frequencies(v['apres'])},
     'feedback': 'Le dictionnaire des figures reprend les noms filtrés en Q3. Si tous les noms ont été retirés, adaptez le filtre et réexécutez Q3 puis Q6, comme demandé dans le sujet. Vérifiez la présence et la qualité des figures avec les critères du TD ; le score ne les certifie pas. ' + NOTE},
    {'label': 'Cohérence des fonctions généralisées', 'required_text_fields': ['comparaison'], 'validate': lambda v: check.generalization(v, {2: REFERENCE['frequencies']}),
     'feedback': 'Versions spécialisées et générales retrouvent les fréquences de référence indépendamment de Q2 ; combinaison = somme des deux dictionnaires. ' + NOTE},
]


def check_notebook(content_str, filename):
    return check_audit(content_str, filename, 2, CHECKS)
