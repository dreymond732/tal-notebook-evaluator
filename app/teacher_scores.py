"""Présentation des scores, sans modification des notes ou CSV sources.

Le maximum brut provient uniquement du correcteur Python enregistré
dans le dictionnaire EVALUATORS (liste de confiance). Une éventuelle
métadonnée étudiante ne peut pas choisir le module ni le dénominateur.
"""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from functools import lru_cache
from importlib import import_module

from routes import EVALUATORS


@lru_cache(maxsize=None)
def max_raw_score(evaluator):
    if evaluator not in EVALUATORS:
        raise ValueError("Évaluateur inconnu")
    # Le journal DM historique contient des copies notées /20. Les nouveaux
    # essais /17,75 figurent à part dans dm_hybride.sqlite3. Le CSV consolidé
    # ne stocke pas la génération du barème : NE JAMAIS recalculer les anciens
    # scores avec le dénominateur 17,75.
    if evaluator == "dm-intermediaire-s1":
        return Decimal("20")
    module_name = EVALUATORS[evaluator][1]
    module = import_module(module_name)
    try:
        value = Decimal(str(module.MAX_SCORE_TOTAL))
    except (AttributeError, TypeError, InvalidOperation) as exc:
        raise ValueError("Barème brut absent ou invalide : " + evaluator) from exc
    if not value.is_finite() or value <= 0:
        raise ValueError("Barème brut non positif : " + evaluator)
    return value


def scaled_score(raw_score, evaluator, target):
    """Arrondi /10 TD ou /20 DM-contrôle ; jamais de plafonnement arbitraire."""
    if raw_score is None or str(raw_score).strip() == "":
        return ""
    if target not in (10, 20):
        raise ValueError("Échelle de présentation invalide")
    try:
        value = Decimal(str(raw_score).strip().replace(",", "."))
    except (InvalidOperation, TypeError) as exc:
        raise ValueError("Score brut invalide") from exc
    if not value.is_finite() or value < 0:
        raise ValueError("Score brut non fini ou négatif")
    converted = value * Decimal(target) / max_raw_score(evaluator)
    return f"{converted.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}".replace(".", ",")
