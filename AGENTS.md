# TAL — Contrat partagé des agents

Le dépôt est maintenu par huit rôles : `TAL-Code-Architect`, `TAL-Code-Auditor`, `TAL-Étudiant-Modèle`, `TAL-Prof`, `TAL-Pedagogy-Designer`, `TAL-Pedagogy-Reviewer`, `TAL-Governance-Auditor` et `TAL-Integration-Master`.

Les règles détaillées sont dans `docs/agents/`. Les sources normatives sont ce fichier, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md` et `docs/agents/WORKFLOW.md`.

## Règles communes

1. Toute mission utilise une branche dédiée ; jamais `main`.
2. Un producteur ne valide jamais son propre travail.
3. Toute modification indique fichiers, hypothèses, tests, risques et critères d'acceptation.
4. Une conformité exige une preuve explicite.
5. Le serveur n'exécute jamais le code d'un notebook étudiant.
6. Aucun secret n'est exposé.
7. Un changement mixte code + pédagogie exige les deux revues spécialisées.
8. Un `NON_CONFORME` de gouvernance bloque le workflow.
9. L'Integration-Master ne rend `READY_TO_MERGE` que s'il est indépendant de la PR ; sinon, `MAINTAINER_REVIEW`.
10. La fusion et la production restent sous décision du mainteneur.
11. L'adaptation d'un support existant ne peut réduire sa couverture pédagogique sans décision explicite de l'enseignant. Une matrice source → cible, validée avant conception, est obligatoire ; une simplification de forme n'est acceptable que si l'objectif, l'activité étudiante et le niveau d'autonomie visés restent couverts.

## Contexte TAL

Les supports sont dans `Notebooks TD/` et `Notebooks contrôles finaux/`. Un évaluateur est l'ensemble cohérent du notebook, de son module `app_correction_*.py`, de son entrée dans `app/routes.py`, de son template et de sa persistance dans `soumissions/`.

Le parcours progresse des bases Python vers le TAL. Toute nouvelle bibliothèque ou compétence est d'abord cadrée par `TAL-Prof` et validée par l'enseignant. Les comparaisons entre bibliothèques ou avec les LLM précisent tâche, langues, données, versions et contexte d'exécution.

## Handoff

Tout relais contient : mission, branche/PR, objectif, fichiers modifiés, contrat affecté, tests, résultats, risques, critères d'acceptation et verdict demandé.
