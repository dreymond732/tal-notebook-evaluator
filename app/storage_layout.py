"""Identifiants de stockage physiques ; routes et contrats notebooks inchangés.

Le nouveau format S1 correspond aux cahiers renommés en novembre 2026 :
  td4-s1 -> S1_TD4 ; td4-one-s1 -> S1_TD4_A.
Les chemins hérités restent disponibles uniquement pour la migration v2.
"""
import re


def legacy_storage_id(evaluator):
    """Nom du dossier de la migration #35, dérivé du module correcteur."""
    from routes import EVALUATORS

    try:
        module = EVALUATORS[evaluator][1]
    except KeyError as exc:
        raise ValueError("Évaluateur inconnu pour le stockage : " + evaluator) from exc
    prefix = "app_correction_"
    if not module.startswith(prefix):
        raise ValueError("Module correcteur inattendu pour " + evaluator)
    name = module[len(prefix):]
    if not name or not all(c.isalnum() or c == "_" for c in name):
        raise ValueError("Identifiant de stockage invalide pour " + evaluator)
    return name


def storage_id(evaluator):
    """Nouveau dossier : S1_TDn[_variante] pour tous les 19 TD du S1."""
    legacy = legacy_storage_id(evaluator)
    match = re.fullmatch(r"td([1-7])-s1", evaluator)
    if match:
        return f"S1_TD{match[1]}"
    match = re.fullmatch(r"td([3-6])-(one|bis|ter)-s1", evaluator)
    if match:
        number, part = match.groups()
        suffix = part if number == "3" else {"one": "A", "bis": "B", "ter": "C"}[part]
        return f"S1_TD{number}_{suffix}"
    return legacy


GRADE_COLUMNS = (
    "Date", "Nom", "Prénom", "Classe", "Score", "Bonus", "Nature du score",
    "Maximum technique", "Relecture humaine", "Numéro étudiant",
    "Version du contrat", "Origine", "Ligne origine",
)
