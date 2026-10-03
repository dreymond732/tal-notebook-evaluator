# TAL — Contrat partagé des agents

Le dépôt est maintenu par neuf rôles : `TAL-Code-Architect`, `TAL-Code-Auditor`, `TAL-Étudiant-Modèle`, `TAL-Prof`, `TAL-Pedagogy-Designer`, `TAL-Pedagogy-Reviewer`, `TAL-Editorial-Reviewer`, `TAL-Governance-Auditor` et `TAL-Integration-Master`.

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
12. Chaque passage visible d'un support pédagogique s'adresse à l'étudiant, y compris les commentaires du code fourni. La seule exception de destinataire concerne les corrigés de devoirs maison destinés à l'enseignant. Les notes de conception, de maintenance et les justifications pour les agents vont dans la documentation du projet. Les instructions cachées du tuteur restent adressées au LLM et ne remplacent jamais l'explication destinée à l'étudiant.
13. Toute révision d'un TD, d'une révision, d'un contrôle ou d'un devoir passe par une revue indépendante de rédaction française (`TAL-Editorial-Reviewer`), en plus de la revue pédagogique. Distinguer explicitement cours, exemple, exercice guidé, problème autonome et vérification, sans imposer un gabarit répétitif. Une validation technique ne vaut pas validation de lisibilité.
14. Conserver le tuteur en double : contexte complet et identique dans les métadonnées Colab et dans le commentaire HTML de la première cellule Markdown. En TD, il guide dans le périmètre des notions et bibliothèques déjà étudiées ou introduites avant la question ; en contrôle, il ne fournit aucune aide. Voir `docs/pedagogy/TUTORING_POLICY.md` et le contrôle éditorial détaillé dans `docs/agents/TAL-Editorial-Reviewer.md`.

## Contexte TAL

Les supports sont dans `Notebooks TD/` et `Notebooks contrôles finaux/`. Un évaluateur est l'ensemble cohérent du notebook, de son module `app_correction_*.py`, de son entrée dans `app/routes.py`, de son template et de sa persistance dans `soumissions/`.

Le parcours progresse des bases Python vers le TAL. Toute nouvelle bibliothèque ou compétence est d'abord cadrée par `TAL-Prof` et validée par l'enseignant. Les comparaisons entre bibliothèques ou avec les LLM précisent tâche, langues, données, versions et contexte d'exécution.

## Handoff

Tout relais contient : mission, branche/PR, objectif, fichiers modifiés, contrat affecté, tests, résultats, risques, critères d'acceptation et verdict demandé.

Pour les supports, ajouter les références historiques et techniques comparées, les cellules relues, les preuves par question, les verdicts pédagogique et éditorial distincts, ainsi que ce qui reste non vérifié. L'inventaire de reprise est `docs/pedagogy/editorial_revision_inventory.md` ; il ne constitue pas une validation des contenus.
