"""Identifiants physiques stables, indépendants de la classe et du contrat notebook.

L'identifiant de route reste inchangé ; le nom de dossier correspond au suffixe
du module correcteur, par exemple td2-s1 -> TD2_S1.
"""


def storage_id(evaluator):
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
