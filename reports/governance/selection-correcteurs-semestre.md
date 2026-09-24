# Audit de gouvernance — sélection des correcteurs par semestre

## Verdict et référence

**CONFORME**, le 24 septembre 2026, pour le changement technique au commit
`f4f6827977affc3807c9435f01ecf8b5e58ae11e`, branche
`code/selection-correcteurs-semestre`, comparé à `origin/main`
`8ee3954d3a4ba96fb5d21058376e56dd740a9844`.

La demande enseignante autorise le parcours accueil → S1/S2/S3 → correcteurs
du semestre après vérification du classement. Le présent audit ne vaut ni
fusion, ni déploiement, ni verdict `READY_TO_MERGE`. L'intégration impliquée
dans la production doit présenter le lot en `MAINTAINER_REVIEW`.

## Sources et séparation des rôles

Sources normatives lues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`,
`docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et
`docs/agents/TAL-Governance-Auditor.md`.

- Producteur : `/root`, mandat TAL-Code-Architect ; code, tests et documentation
  technique dans les zones autorisées.
- Réviseur indépendant : `/root/semester_code_audit`, TAL-Code-Auditor ;
  verdict **ACCEPT** transmis dans le handoff de session. Cette preuve n'est pas
  présentée comme une review GitHub déjà publiée.
- Présent auditeur : `/root/semester_governance`, TAL-Governance-Auditor ;
  lecture seule du produit, écriture limitée à ce rapport.

Le flux technique s'applique. Les onze fichiers du diff concernent l'application,
ses templates, trois fichiers de tests, le README et
`docs/SEMESTER_NAVIGATION.md`. Aucun notebook ni objectif, activité, barème,
marqueur ou méthode de validation n'est modifié. Il n'y a pas de
`CHANGEMENT_DE_CONTRAT` ni d'adaptation pédagogique : la matrice source → cible
et la revue pédagogique ne sont pas requises pour ce lot.

## Preuves examinées

| Exigence | Preuve et constat |
|---|---|
| Branche dédiée | Branche, HEAD et base contrôlés directement ; espace de travail propre avant création de ce rapport. Aucun changement direct de `main` observé. |
| Classement complet préalable | Audit code : concordance des modules, supports et manifeste pour les 32 correcteurs actifs, soit 8 en S1, 6 en S2 et 18 en S3. Inventaire consigné dans la documentation technique. Deux modules historiques S2 non enregistrés restent inactifs. |
| Aucun correcteur silencieusement omis | Lecture directe : `EVALUATOR_SEMESTERS` doit contenir exactement les clés de `EVALUATORS` et seulement S1, S2 ou S3 ; validation appelée à la création de l'application. |
| Parcours et accès historiques | Lecture directe : accueil à trois choix, filtrage par semestre, anciennes routes `/eval/<identifiant>` conservées, retours vers le semestre et changement de semestre dans les formulaires, résultats et reçus. |
| Modes et confidentialité | Badges fondés sur `EVALUATOR_MODES`, y compris les deux anciennes URL S2 commençant par `td` en mode contrôle. Aucun changement du traitement des résultats privés ; revue technique favorable. |
| Proxy | Liens générés avec `url_for` ; tests des listes, accès directs et retours avec `/universite/tal`. La configuration du proxy reste inchangée. |
| Contrat et sécurité | Lecture du diff intégral : aucune modification des modules correcteurs, de la persistance, des dépendances ou de l'infrastructure ; aucun ajout d'exécution de code étudiant ni de secret. |
| Tests | Journal `/tmp/tal-semesters-tests.log` lu : **103 tests, OK**. Le handoff de l'auditeur code rapporte également une exécution indépendante à **103/103**. Les tests de navigation vérifient les 32 accès GET, les listes sans omission, les retours POST représentatifs TD/contrôle, les modes, les erreurs et le proxy. Les suites S3 existantes restent incluses. |
| Qualité du diff | `git diff --check origin/main...HEAD` exécuté par la gouvernance : succès, sans diagnostic. |
| Hypothèses, risques et acceptation | Documentés dans `docs/SEMESTER_NAVIGATION.md` : omission future, mélange des niveaux, liens historiques, retours de dépôt et préfixe proxy. |

La gouvernance n'a pas relancé la suite de tests : elle a examiné son journal,
le diff et les preuves attribuées au réviseur indépendant. Aucun fichier de
produit ou de règles n'a été modifié par le présent auditeur.

## Limites et relais

- **Docker : NOT_TESTED** ; commande Docker absente de cet environnement.
- **Déploiement sur le serveur enseignant et vérification publique : NOT_TESTED**.
  Les tests Flask avec en-tête de proxy ne prouvent pas le fonctionnement d'un
  déploiement de production.
- Le classement concerne le registre actif vérifié à ce commit. Les deux modules
  historiques S2 exclus du registre ne sont pas activés par cette évolution.

Aucun veto de gouvernance. Relais à l'intégration avec le verdict technique,
ce rapport et les limites explicites ; fusion et production sous décision du
mainteneur.
