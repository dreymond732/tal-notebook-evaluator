# Gouvernance — R1 ciblé et autonomie des TD spaCy

## Verdict

**CONFORME**, le 3 octobre 2026, pour la branche `pedagogy/s3-r1-remediation`, issue de `2c7dc3c696ef0f5f70046a2c6ef005f7e21cc1ac`.

Audit indépendant par `/root/r1_governance` dans le rôle TAL-Governance-Auditor. Le présent rôle n’a modifié ni supports, ni code, ni tests, ni règles ; son unique production est ce rapport. Ce verdict ne vaut ni fusion ni déploiement. L’intégration est productrice : statut attendu **MAINTAINER_REVIEW**, jamais `READY_TO_MERGE`.

## Autorisation et séparation des rôles

L’enseignant a autorisé la reprise de R1 comme remédiation ciblée après TD1, transmis des retouches marginales de TD1 et demandé que les TD n’entraînent pas une relecture individuelle massive. Le lot conserve les exercices, les interprétations et leurs contrats ; il distingue retour technique, vérification personnelle et absence d’autocorrection linguistique. L’ajustement de TD1B retire une promesse de relecture systématique sans supprimer les quatre activités ni le dépôt.

| Travail | Rôle / agent | Séparation constatée |
|---|---|---|
| Cadrage préalable, couverture, périmètre du tuteur et suivi pédagogique | TAL-Prof, `/root/r1_prof` | Documentation pédagogique et manifeste, sans auto-validation de contenu |
| Supports R1, TD1, TD1B et README | TAL-Pedagogy-Designer, `/root` | Producteur distinct des trois réviseurs spécialisés |
| Messages applicatifs, tests de conservation et documentation technique | TAL-Code-Architect, `/root/r1_architect` | Audit technique indépendant demandé |
| Revue de couverture avant conception puis finale | TAL-Pedagogy-Reviewer, `/root/r1_pedagogy_review` | Aucun support modifié ; confirmation finale directe à la gouvernance |
| Revue exhaustive du français et des fonctions des passages | TAL-Editorial-Reviewer, `/root/r1_editorial_review` | Rapport seul dans `reports/editorial/` |
| Lecture des consignes sans résolution | TAL-Étudiant-Modèle | Sujet et ressources autorisées seulement, note dans `Corrigés modèles/` |
| Audit technique | TAL-Code-Auditor, `/root/r1_code_audit` | Verdict ACCEPT indépendant confirmé directement à la gouvernance |
| Gouvernance | TAL-Governance-Auditor, `/root/r1_governance` | Écriture limitée au présent rapport |

Les actifs normatifs `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md` et `docs/agents/` sont inchangés dans le diff. La mission n’a pas modifié ses propres règles de validation. La branche courante est dédiée ; aucune modification de `main` n’a été effectuée par cet audit.

## Couverture et lisibilité : preuves exigées

La matrice `docs/pedagogy/s3_r1_remediation_coverage.md` a été établie par TAL-Prof puis validée par TAL-Pedagogy-Reviewer **avant conception**, conformément au handoff confirmé directement par ce dernier. Elle compare les états historiques disponibles de R1 (`2a36752`, `c649cfe`, `4fe2e48`), le parent technique `2c7dc3c`, TD1/TD1B et le fichier fourni par l’enseignant. Aucune référence indisponible n’est présentée comme examinée.

- **Pédagogie : ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**, sur les 98 cellules et 14 questions, plus le README. Le réviseur a confirmé son verdict après l’ultime précision de l’introduction de R1 : R2 n’exige pas d’avoir refait R1.
- **Éditorial : ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE**, dans `reports/editorial/s3-r1-remediation.md`. Lecture exhaustive, preuves par question, destinataire étudiant et distinction cours/exemple/consigne/vérification sont documentés. Les deux templates de dépôt ont aussi été relus.
- **Lecture étudiante :** `Corrigés modèles/TD/s3-r1-remediation/lecture_etudiante.md` décrit les 98 cellules et les 14 tâches, sans résoudre ni exécuter une cellule. Elle distingue les limites de sa lecture des défauts constatés. Le point mineur sur l’indépendance R1/R2 a été corrigé puis relu.

Les quatre exercices R1, les six exercices TD1 et les quatre exercices TD1B restent livrés. R1 devient conditionnel selon la décision enseignante ; ses activités ne sont pas réduites. Aucune activité n’est déclarée couverte par un support futur absent. Le lot ne vaut pas validation des autres supports du cours.

L’audit a comparé indépendamment le fichier TD1 joint au parent : ses différences de source touchent uniquement les cellules `f1c4b87024c7` et `94811d622eb5`. Les suppressions demandées sont reprises ; la mention Q6 et le séparateur, demandés dans le message mais absents du différentiel joint, sont ajoutés. Aucun code de réponse n’est supprimé pour alléger la charge de lecture.

## Contrats et sécurité

Le diff applicatif concerne les formulations de retour et de réception. Les validateurs et barèmes restent identiques. Q6 conserve son point technique dans un total de six : « non autocorrigé sur le fond linguistique » n’annonce donc pas l’absence de tout contrôle. TD1B conserve le type interne `human_review`, la persistance et l’absence de note automatique ; le reçu n’annonce plus de retour individuel systématique. Il n’y a pas de nouveau changement de contrat dans ce lot ; le changement historique introduisant ce type de dépôt reste documenté.

La fixture `tests/fixtures/s3_r1_editorial_source_baseline.json` a été contrôlée indépendamment : ses octets UTF-8 sont exactement ceux de R1 au parent annoncé, SHA-256 `d75faed85c6000beeac1354330e6d32ce79672d26da1df17b08d877e5ce93e9e`. Elle ne remplace pas l’ancien état par le nouveau. Les tests relient cet état figé aux empreintes antérieures et contrôlent les cellules, identifiants, métadonnées, ordre et AST des sources actuelles. Les autres supports ne reçoivent pas d’exception générale de réécriture. La couverture de la prose relève des revues indépendantes, pas d’une comparaison textuelle artificielle.

Les trois notebooks conservent le double contexte du tuteur, complet dans le commentaire HTML initial et les métadonnées Colab. Le manifeste n’élargit pas les notions ou bibliothèques autorisées ; il harmonise les titres de R1. Le tuteur guide en TD avec les acquis disponibles avant chaque question. Aucun contrôle n’est modifié.

Aucun code étudiant n’est exécuté sur le serveur. L’architecture de lecture des copies et de persistance est inchangée. Les seules exécutions de notebook déclarées pour ce lot portent sur trois exemples fournis de R1, localement, sans réponse étudiante. Les notebooks sources n’enregistrent aucune sortie exécutée. L’Étudiant-Modèle n’a exécuté aucun exercice et n’a consulté ni correcteur ni test.

Les cellules finales contiennent le placeholder `__TAL_PUBLIC_URL__`, pas une adresse de serveur réel. L’examen des domaines présents dans les fichiers suivis modifiés ne relève que documentation, ressources publiques et URL neutre de test. L’audit n’a exposé aucun secret. Le commentaire technique canonique de restitution est conservé conformément au format explicitement demandé par l’enseignant ; les instructions visibles précédentes s’adressent à l’étudiant.

## Vérifications et état exact

| Preuve | Résultat et provenance |
|---|---|
| Suite complète | 292 tests PASS ; fin du journal `/tmp/tal-r1-full-tests.log` lue directement par la gouvernance |
| Audit code indépendant | ACCEPT, 49 tests ciblés PASS et 35 profils tuteur vérifiés ; handoff reçu directement du réviseur |
| Exemples fournis R1 | 3 exemples exécutés avec spaCy 3.8.7 / modèle sm 3.8.0 ; preuve transmise par l’intégration, non réexécutée par la gouvernance |
| Structure des notebooks | nbformat et AST des trois supports PASS selon l’intégration ; 26 + 40 + 32 cellules vérifiées directement |
| Distribution | 34 notebooks générés puis vérifiés avec URL neutre selon l’intégration ; aucun déploiement réel dans ce lot |
| Diff | `git diff --check` PASS ; actifs normatifs inchangés, fixture parent byte-identique vérifiés directement |

Empreintes finales vérifiées par la gouvernance et concordantes avec les revues de contenu :

| Support | SHA-256 |
|---|---|
| R1 | `f7d2a865ece47f3c679476cbb164fa6dcc0329871c125480cc137785c374fcbd` |
| TD1 | `9de9c90179b5ff99e477a7e8dc8abd99c6089cfd614a5f92aba4788bb46deed1` |
| TD1B | `abb86418ddcfcab29b1be7b18ac063a228196d0a74d01af5c690a867fee24069` |
| README S3 | `41d57d399b0c439d797fee52df16be12ebc1b979d78a33cd388842fac01d9c04` |

## Limites et relais

Durée réelle, efficacité de la remédiation en classe, rendu dans une session Colab et obéissance effective du LLM ne sont pas mesurés. Les critères personnels ne garantissent pas la justesse de toutes les interprétations ; le dépôt sans note ne la valide pas davantage. Le nombre de phrases de Q6 reste une trace déclarée dont le serveur ne recalcule pas la segmentation. Les limites existantes de stockage sur fichiers ne sont pas corrigées par ce lot.

Les réserves non bloquantes de la lecture étudiante restent visibles dans sa note. Aucun résultat de CI distante n’est revendiqué par ce rapport ; l’intégration doit vérifier la publication et les contrôles de la PR. Une modification ultérieure de contenu visible ou de contrat exige une relecture adaptée avant de réutiliser ces verdicts.

Relais à l’intégration pour **MAINTAINER_REVIEW**, puis au mainteneur pour décider fusion et déploiement. Aucun déploiement ou engagement de correction individuelle n’est implicite dans ce verdict.
