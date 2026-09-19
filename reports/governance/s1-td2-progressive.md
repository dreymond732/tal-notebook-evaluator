# Audit de gouvernance — TD2 du S1

## Verdict et périmètre

**CONFORME pour la présentation de ce lot au mainteneur.** Ce verdict ne vaut ni `READY_TO_MERGE`, ni autorisation de fusion ou de déploiement. Il ne certifie pas le comportement réel de Colab, la durée vécue en classe ou les résultats d'une exécution du corrigé modèle.

Branche auditée : `pedagogy/s1-td2-progressive`. Base de comparaison : `ad28d093cd807729aaefa30aa8261f8e0d6947ca`, sur la branche S1 après fusion du pilote de tutorat. La PR doit cibler la branche S1 correspondante et isoler ce lot des changements antérieurs. Le sujet final contrôlé possède le SHA256 `df8be0b6b1da0b8427368bb23b1279fff50cba6e74ad737ca335cb9cf1d445df`.

Le passage au TD2 est explicitement demandé par l'enseignant après validation de la politique de tutorat : accompagnement progressif, quiz après demande de solution, mini-cours si nécessaire, aucun code fourni par le tuteur au S1, instructions dans les métadonnées seules. Le lot renforce les sept groupes existants et leur correcteur formatif. Aucun contrôle ni TD ultérieur n'est révisé.

Sources normatives relues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et `docs/agents/TAL-Governance-Auditor.md`.

## Séparation des rôles et relais

| Rôle | Production ou contrôle | Preuve et limites |
|---|---|---|
| TAL-Prof — `td2_prof` | Spécification et matrice avant adaptation, fiche TD2 dans le manifeste, documentation pédagogique | `docs/pedagogy/TD2_S1_SPECIFICATION.md`, `S1_COVERAGE_MATRIX.md`, `tutor_sessions.json`, `README.md` ; antériorité du cadrage transmise par l'orchestrateur |
| TAL-Pedagogy-Designer | Sujet TD2 et génération de ses métadonnées | Sept groupes et leurs activités maintenus ; aucune modification des autres sujets |
| TAL-Code-Architect | Correcteur TD2 dédié, tests et note technique | `app/app_correction_TD2_S1.py`, `tests/test_td2_s1.py`, `tests/test_s1_formative.py`, `docs/TD2_S1_EVALUATION.md` ; pas d'auto-validation |
| TAL-Étudiant-Modèle | Copie résolue et note indépendante | Écriture dans `Corrigés modèles/TD/td2-s1/` seulement ; accès déclaré limité aux sujets TD1/TD2 et consignes de rôle ; aucun correcteur, test ou autre corrigé consulté ; aucune exécution ni soumission |
| TAL-Pedagogy-Reviewer — `td2_review_pedagogy` | Revue indépendante de couverture, progression et copie modèle | Verdict final `ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`, transmis par l'orchestrateur après corrections |
| TAL-Code-Auditor — `td2_review_code` | Revue technique indépendante | Verdict final `ACCEPT`, transmis par l'orchestrateur après corrections et vérifications ciblées |
| TAL-Governance-Auditor — `td2_governance` | Règles, périmètre, preuves et relais | Écriture limitée au présent rapport ; aucune modification du produit audité |
| Orchestration — agent parent | Répartition, branche, collecte des relais et préparation de l'intégration | Aucun contenu pédagogique ou correcteur produit par l'orchestrateur dans ce lot, selon son relais |

Les verdicts spécialisés et leurs résultats sont des relais de session, transmis explicitement par l'orchestrateur à la Gouvernance ; ils ne sont pas présentés comme des revues GitHub déjà publiées. Les producteurs et réviseurs sont distincts. Le changement notebook/correcteur suit le flux mixte. L'Étudiant modèle n'est pas l'auditeur du correcteur et ne prétend pas l'avoir testé.

## Preuves examinées

| Exigence | Résultat et provenance |
|---|---|
| Branche dédiée | Observation propre : branche courante `pedagogy/s1-td2-progressive`, distincte de `main`. Aucun commit, push, merge ou déploiement effectué par la Gouvernance |
| Matrice préalable | Spécification source → cible présente, déclarée préalable dans le cadrage et le relais d'orchestration ; sept groupes obligatoires, activités, productions, autonomie et charge explicités |
| Couverture conservée | Comparaison propre du sujet de base et de la cible : nettoyage, transformation, premier/dernier caractère et tranche, découpage avec troisième élément, reconstruction, traitement des trois chaînes et interprétation de `split()` conservés. Reviewer : `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` |
| Pas de réduction implicite | Q6 conserve les trois entrées. Le retrait de l'exigence `for` du correcteur corrige une anticipation absente du sujet source ; les indices et la liste littérale permettent l'activité sans boucle. Aucun déplacement sans équivalent immédiat ni suppression substantielle identifié |
| Changement de contrat déclaré | `CHANGEMENT_DE_CONTRAT` explicite dans la spécification ; Q1–Q7 conservés, sept traces complémentaires ajoutées, mêmes identifiant, signature à deux paramètres et retour à cinq éléments et plafond de 7 points. La répartition détaillée et la limite de Q7 sont documentées |
| Tutoriel et périmètre | Observation propre : `python app/tutor_metadata.py --check` réussit pour les quatre profils (3648, 4106, 955 et 3677 caractères). La fiche TD2 autorise seulement les notions introduites ; aucune bibliothèque ; instructions de tutorat exclusivement dans les métadonnées. Q6 inclut comparaison, égalité et booléen après correction finale |
| Non-régression des trois pilotes | Comparaison propre octet à octet avec la base : TD1 S1, TD0 S3 et DevoirS1 strictement identiques. Les trois fiches de manifeste préexistantes sont identiques également |
| Sujet et modèle non exécutés | Observation propre : 18 cellules chacun ; toutes les sorties vides, tous les compteurs d'exécution nuls. Markdown et métadonnées du modèle identiques au sujet final après synchronisation ; note modèle actualisée avec le SHA256 final. La copie est une solution statiquement relue, pas une preuve d'exécution réussie |
| Tests techniques indépendants | Code-Auditor : première campagne de 46 tests, 45 réussites et un échec de synchronisation des métadonnées ; après régénération, les 11 tests de métadonnées sont tous réussis. Les 46 cas sont ainsi couverts par la campagne initiale et la reprise ciblée, sans prétendre à une nouvelle campagne complète de 46 après régénération |
| Vérifications pédagogiques | Reviewer : revue finale sur le SHA256 ci-dessus, 15 tests TD2 exécutés indépendamment, verdict final favorable ; deux heures restent une prévision |
| Réserves corrigées | Indexations alternatives valides rétablies ; commentaire d'identification rétabli dans la cellule réelle du sujet, avec vérification indépendante de l'extraction et des chemins de persistance ; dérive des métadonnées supprimée par régénération |
| Absence d'exécution du code étudiant | Relecture propre du correcteur : JSON, AST, analyse des sorties et lecture de littéraux, sans appel d'exécution du code soumis. Code-Auditor : tests d'absence d'exécution et de route réelle avec persistance réussis. Aucun notebook étudiant ni copie modèle exécuté par la Gouvernance |
| Périmètre et gouvernance | Observation propre : aucun diff dans `AGENTS.md`, matrice de permissions, rôles, contrat partagé, routes ou workflows. Aucun secret ni donnée étudiante réelle identifié dans les ajouts audités ; identité du modèle explicitement fictive. `git diff --check` réussi |

La Gouvernance a exécuté les comparaisons de fichiers, le contrôle de génération et les inspections statiques ci-dessus. Elle n'a pas réexécuté la suite complète, les soumissions de test ou le code de réponse du modèle. Les résultats des tests spécialisés restent attribués à leurs auditeurs.

## Limites et relais d'intégration

- **Colab : `NOT_TESTED`.** L'activation, la conservation après copie et le comportement effectif du LLM nécessitent un essai réel. Les métadonnées ne constituent pas un verrou empêchant l'assistance.
- **Copie modèle : non exécutée.** La faisabilité statique est revue ; les sorties et l'ordre effectif d'exécution restent à vérifier humainement. Ne pas annoncer une note de 7/7 obtenue par cette copie.
- **Évaluation formative limitée.** Le correcteur ne certifie ni l'origine ni la fraîcheur des sorties, ni la pertinence sémantique du commentaire Q7. Il demande explicitement une relecture humaine. Ses contraintes syntaxiques et ses variantes reconnues sont décrites dans la note technique.
- **Charge de 120 minutes : prévisionnelle.** Le découpage n'a pas été mesuré auprès d'étudiants ; l'accompagnement requis dépend des acquis du TD1.
- **Progression globale : hors lot.** Ce verdict porte sur le TD2, pas sur l'ensemble des TD S1, leurs contrôles ou leur articulation complète avec S2/S3.

L'intégration doit conserver la cible S1, les deux verdicts spécialisés et ces limites dans la PR, puis contrôler la présence du sujet, du correcteur, de sa documentation et de la copie modèle. L'orchestrateur annonce une PR en brouillon et le verdict conservateur `MAINTAINER_REVIEW`, pour revue de l'enseignant et essai Colab réel. La fusion et la production restent sous décision du mainteneur. Aucun `READY_TO_MERGE` n'est émis par la Gouvernance.
