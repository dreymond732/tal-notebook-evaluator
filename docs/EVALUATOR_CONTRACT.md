# TAL — Contrat des évaluateurs

## Unité fonctionnelle

Un évaluateur actif associe une entrée dans `EVALUATORS`, un notebook, un module `app_correction_*.py`, une route Flask, un template et la persistance dans `soumissions/`. Leur présence isolée ne suffit pas.

## Module

Le module expose `check_notebook(content_str, filename)` et retourne exactement :

```python
(score, details, max_score, student_info, error_msg)
```

Le score est numérique et borné par `max_score`; le barème annoncé correspond au barème appliqué ; `error_msg` vaut `None` en succès.

## Sécurité et contrat notebook

Le serveur n'exécute jamais le code étudiant. Il n'analyse que cellules, code source, marqueurs et sorties déjà enregistrées.

Les marqueurs, variables, sorties, méthodes de validation, types, formes, tolérances et barèmes font partie du contrat. Leur modification est un `CHANGEMENT_DE_CONTRAT`, soumis au flux mixte. Les solutions alternatives valides doivent être acceptées lorsque l'objectif pédagogique le permet.

## Web, proxy et persistance

Les routes GET/POST, templates et sélecteur restent cohérents. Les URL utilisent `url_for()`. L'application fonctionne sous `/universite/tal/` grâce à `ProxyFix` et aux en-têtes transmis par le proxy.

Une soumission acceptée persiste copie, rapport HTML et CSV de notes dans `soumissions/<évaluation>/<classe>/`. Une erreur de persistance ne vaut jamais succès silencieux.

Les TD peuvent être formatifs ; les contrôles restent sommatifs, sans divulgation du détail de correction.

## Validation

La CI vérifie progressivement : registre, import, signature, tuple de retour, barème, template, GET/POST, persistance, sélecteur, proxy, compatibilité notebook-correcteur et absence d'exécution de code étudiant. `NOT_TESTED` n'est jamais `PASS`.
