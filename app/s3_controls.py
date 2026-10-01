"""Mesures techniques privées des contrôles S3, sans exécution des copies."""
import re

from s3_audit import collect, read_notebook, grade_traces
from notebook_contract import ContractError, s3_contract_identity
from s3_review import review_evidence

TRACE_RE = re.compile(r'^S3_C([1-7])_Q([1-9][0-9]*):\s*(.*)$')
WEIGHTS = (2.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0)
SCORE_KIND = 'technique_provisoire'
HUMAN_REVIEW = (
    'Relecture humaine requise : raisonnement, validité des annotations linguistiques, '
    'interprétation, qualité des figures, autonomie et respect du protocole. '
    'Le score technique sur 20 ne constitue pas une note globale. '
    'Le serveur analyse uniquement les traces enregistrées, sans exécuter le code ; '
    'il ne certifie ni leur authenticité ni leur fraîcheur.'
)


def check_control(content_str, filename, number, checks):
    """Contrat commun ; aucune mesure de qualité par longueur ou mots-clés."""
    if len(checks) != len(WEIGHTS):
        raise ValueError('Un contrôle S3 comporte exactement sept vérifications.')
    maximum = sum(WEIGHTS)
    try:
        nb = read_notebook(content_str)
        info = s3_contract_identity(nb, f'controle-td{number}-s3')
        displays, records = collect(nb['cells'], number, trace_re=TRACE_RE)
    except ContractError as exc:
        return 0.0, [], maximum, {}, str(exc)
    except (ValueError, TypeError, RecursionError, OverflowError) as exc:
        return 0.0, [], maximum, {}, 'Erreur JSON/notebook : ' + str(exc)
    score, details, deferred = grade_traces(displays, records, checks, WEIGHTS, contextual=True)
    info.update(score_brut=score, score_nature=SCORE_KIND,
                relecture_humaine='requise', score_max=maximum, contract_version=2,
                points_a_reexaminer=deferred, review_evidence=review_evidence(nb, len(checks)))
    return score, details, maximum, info, None
