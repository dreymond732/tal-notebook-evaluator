# Gouvernance — Revue et distribution des TD S1

## Mission et périmètre

Revue du 1er octobre 2026 sur la branche `pedagogy/s1-review-distribution`, référence `b12b40f`. La demande enseignante autorise la revue des sept TD S1, leur dénomination selon le contenu, les métadonnées de notebook et de cellule, et une restitution HTML dont l’adresse est injectée au déploiement. Le gabarit conserve seulement `__TAL_PUBLIC_URL__` dans Git. La protection concerne le dépôt : l’adresse réelle demeure nécessairement lisible dans la copie distribuée.

**Verdict : CONFORME**, pour ce périmètre et l’état relu. Aucun changement de barème, de réponse attendue, de version S1 ou d’activité n’est réalisé. Les limites préexistantes des correcteurs et de l’étayage sont distinguées des corrections apportées.

## Séparation des responsabilités

| Rôle | Production ou contrôle | Résultat |
|---|---|---|
| TAL-Prof (`s1_prof_review`) | Matrice `docs/pedagogy/s1_td_review_distribution.md`, chemin des profils et renvois pédagogiques | Matrice validée par l’orchestrateur avant conception ; aucune réduction autorisée ou réalisée |
| TAL-Pedagogy-Designer | Sept notebooks renommés, métadonnées ajoutées, sept cellules finales ; README et relais pédagogique | Production décrite dans `docs/s1_notebook_review.md` |
| TAL-Code-Architect (`s1_distribution_architect`) | Catalogue, génération, déploiement, tests de distribution, documentation technique | Production soumise à revue indépendante |
| TAL-Code-Auditor (`s1_code_review`) | Relecture technique et vérifications indépendantes, sans écriture produit/tests | ACCEPT |
| TAL-Pedagogy-Reviewer (`s1_pedagogy_review`) | Lecture intégrale et comparaison des sept supports, sans écriture produit | ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE |
| TAL-Integration-Master (`s1_integration`) | Adaptation ciblée des tests d’intégrité et de résolution ; tests supplémentaires S1 | MAINTAINER_REVIEW, car producteur de tests |
| TAL-Governance-Auditor (`s1_governance`) | Contrôle des règles, des preuves et du relais ; écriture du présent rapport uniquement | CONFORME |

Les actifs normatifs `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md` et `docs/agents/` sont inchangés. La fixture historique `tests/fixtures/notebook_migration_baseline.json` n’est pas régénérée. Aucune modification directe de `main`, fusion ou mise en production n’est réalisée dans cette mission.

## Preuves et critères d’acceptation

- La matrice source → cible couvre les sept supports et leurs 45 questions principales, avec les sept compléments du TD2. La comparaison indépendante confirme les 123 cellules historiques conservées, dans le même ordre, avec sources, types, sorties et identifiants préexistants identiques. Les 130 cellules finales disposent de métadonnées et d’identifiants cohérents.
- Les racines `metadata.tal`, les identités et les réponses conservent leurs contrats ; les sept versions restent à 1. Les règles S1 du tuteur et la première cellule sont inchangées. Le chemin de session suit le nouveau nom ; 34 profils passent le contrôle du tuteur.
- Le gabarit final est unique, fourni, hors évaluation, sans sortie ni exécution enregistrée. La génération remplace le gabarit S1 et ajoute une unique cellule pour les autres supports. Les imports de restitution ne deviennent pas des notions autorisées pour résoudre les exercices.
- La distribution de 33 copies est générée et vérifiée ; une seule restitution résolue par copie, aucun substitut résiduel. Les sept nouveaux noms S1 et les 18 contrats S3 v2 sont conservés dans leur catalogue respectif. Les empreintes des 33 sources restent identiques avant et après génération.
- Les anciens chemins distribués sont retirés uniquement dans le périmètre du manifeste géré. Les sources, copies étrangères et soumissions ne sont pas réécrites par cette opération. `dist/` et `.env` restent ignorés par Git.
- L’URL HTML est échappée et le lien utilise `rel="noopener noreferrer"`. Le fichier d’environnement est lu comme données, jamais exécuté. Le déploiement vérifie les sources, génère et vérifie la distribution avant Docker ; un échec interrompt la suite. Les tests utilisent des commandes factices pour vérifier cet ordre.
- Le serveur n’exécute aucun code de notebook étudiant. L’exécution de contrôle du rendu concerne uniquement le gabarit de confiance. Les sondes comparent les résultats des sept moteurs sur traces positives et négatives, vérifient que la restitution ne contribue ni à l’identité ni au score, et soumettent les sept sujets avec des noms de fichier arbitraires au bon évaluateur.
- La suite finale d’intégration, également exécutée indépendamment par l’auditeur code, compte **209 tests réussis** (journal examiné : `/tmp/tal-s1-integration-tests.log`). Compilation Python, contrôle des espaces Git, 33 sources et génération/vérification des 33 copies passent. Les tests historiques maintiennent la fixture gelée et limitent explicitement la normalisation des sept renommages S1.

## Limites et suite

Le renommage ne fiabilise pas les six anciens correcteurs génériques : leurs vérifications par marqueurs ou fragments syntaxiques peuvent accepter une preuve faible ou rejeter une variante valide. Les identités S1 n’ont toujours pas de numéro étudiant obligatoire. Ces réserves, ainsi que l’étayage inégal et les ambiguïtés de certains exercices, sont documentées dans la revue pédagogique et le relais technique ; elles ne doivent pas être présentées comme résolues. La durée réelle de deux heures n’est pas mesurée. La relecture du contrôle final historique relève également des arguments par défaut et un `range` décroissant insuffisamment préparés explicitement dans les TD ; le présent verdict ne certifie pas la préparation exhaustive à ce contrôle.

**Docker local : NOT_TESTED. CI distante : en attente de publication au moment de ce rapport.** La validation Docker de la CI doit être constatée sur le commit de la PR avant de l’annoncer comme acquise. Les résultats locaux n’attestent pas d’un déploiement sur le serveur ni d’une séance Colab réelle.

Après les revues et la CI, le relais reste **MAINTAINER_REVIEW** : le mainteneur décide de la fusion et du déploiement. Après fusion, `bash deploy.sh` produit les fichiers à distribuer dans `dist/Notebooks TD/S1/`. Les anciennes copies S1 compatibles ne sont pas rejetées du seul fait du renommage.
