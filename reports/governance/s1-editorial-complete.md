# Gouvernance — reprise éditoriale des sept TD S1

## Verdict et périmètre

**CONFORME — 4 octobre 2026**, sur les sept TD S1 révisés et leurs retours automatiques. La demande enseignante « Reprends les TD du S1 », dans la continuité des règles éditoriales et du principe d'absence de relecture individuelle systématique, autorise ce lot. Les contrôles, DM, corrigés et archives ne sont pas validés par ce verdict.

Branche dédiée vérifiée : `pedagogy/s1-editorial-complete`. Base exacte vérifiée par Git : `670e6c104a6d0228fcad8a91cfc8776117b038bb`. Le présent auditeur indépendant a seulement écrit ce rapport ; aucun notebook, code, test ou règle audités n'a été modifié par lui. Aucun changement des actifs normatifs n'est présent. Pas de fusion ni de déploiement.

L'intégration a produit des tests et de la documentation : son verdict de livraison doit donc être **MAINTAINER_REVIEW**, jamais `READY_TO_MERGE`. La décision de fusion et de production appartient au mainteneur.

## Séparation des rôles et preuves de contenu

La matrice `docs/pedagogy/s1_editorial_complete_coverage.md` distingue le parent technique, l'historique Git `2a36752` et les originaux retrouvés (cours de 212 cellules et six notebooks). La chronologie rapportée par le cadrage et les handoffs est : lecture des sources originales, validation indépendante `ACCEPT_SUR_PÉRIMÈTRE_COURANT`, puis feu vert aux Designers. Le rapport éditorial a corrigé une formulation contradictoire qui attribuait cette validation au Prof et plaçait les retrouvailles après celle-ci. Cette chronologie n'est pas une déduction des dates de fichiers.

Les Designers ont rédigé les supports ; les réviseurs pédagogique et éditorial sont distincts des producteurs. Leurs verdicts finaux et ceux de l'auditeur technique ont été consultés dans les statuts des agents et confrontés aux rapports déposés.

| Revue indépendante | Verdict et preuve | Limite |
|---|---|---|
| TAL-Pedagogy-Reviewer | `ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`, 45 questions et tous les essais actuels ; bilan détaillé par question et matrice finale | Couverture exhaustive des originaux 2025 `NON_DÉMONTRÉE` |
| TAL-Editorial-Reviewer | `ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE`, 293 cellules finales, rapport `reports/editorial/s1-editorial-complete.md` | Pas d'observation en classe ni de preuve de comportement Colab |
| Étudiant-Modèle | Lecture des 45 questions favorable, `Corrigés modèles/TD/s1-editorial-complete/lecture_etudiante.md` | Lecture sans résolution ni exécution, accès limité aux sujets et ressources autorisées |
| TAL-Code-Auditor | `ACCEPT`, invariants et portée des retours S1 confirmés, 79 tests ciblés reproduits | Avis technique distinct des avis d'apprentissage |

**TAL-PED-S1-01 est clos** : onze vérifications dépendant de fonctions sont réellement placées après les réponses concernées (TD5 Q1–Q6, TD6 Q4–Q5, TD7 Q4–Q6). Une simple étiquette « après exercice » n'était pas une correction suffisante. Les essais restent livrés.

Les lacunes historiques ne sont ni restaurées implicitement ni présentées comme de nouvelles suppressions. La matrice documente notamment les activités sur les mots de deux lettres, la distinction texte brut/normalisé, certaines compositions et un panorama d'API plus large. Ce lot conserve le parcours actuellement distribué ; il ne prétend pas reconstituer tout le cours de 2025. Une extension curriculaire demeure distincte. L'inventaire marque uniquement les sept TD S1 `REVU`, en laissant leurs contrôles et DM à reprendre.

## Vérifications directement réalisées par la gouvernance

- Lecture des sources normatives, de la matrice préalable et du bilan final, du rapport éditorial complet, de la lecture étudiante, du bilan technique et de l'inventaire.
- Concordance calculée des sept SHA-256 avec les empreintes finales du rapport éditorial ; fichiers totalisant 293 cellules. Ces empreintes ancrent le présent verdict aux mêmes versions.
- Lecture JSON et contrôle du contexte complet identique dans `metadata.colab.aiContexts` et le commentaire HTML de première cellule des sept TD. La règle « Au S1 : langage naturel seulement, aucun code » est présente. La modification du manifest se limite à `None` dans TD5 Q1, expliqué avant le premier exemple d'après les revues indépendantes.
- Lecture du diff des trois modules concernés : les conditions de validation, marqueurs, points et versions v2 ne changent pas. Le changement porte sur les messages et `relecture_humaine='facultative'`, limité aux sept identifiants TD S1. Les explications restent disponibles ; leur sens n'est pas validé par le score. Aucun ajout d'exécution de code soumis.
- Absence de diff des notebooks S2/S3 et des contrôles ; absence de modification des actifs normatifs ; `git diff --check` réussi.
- Aucun original privé ajouté à la liste des fichiers du lot ; la matrice contient seulement références et empreintes. Aucun ajout d'URL ou d'adresse électronique dans les diffs des sept notebooks, ni dans les rapports examinés. Les données pédagogiques déjà distribuées restent inchangées selon les contrôles d'AST ; ce constat n'est pas un audit exhaustif de secrets de tout l'historique Git.
- Lecture du journal final `/tmp/s1-editorial-full-tests-final.log` : **295 tests, OK**. La gouvernance n'a pas elle-même réexécuté cette suite.

## Vérifications techniques rapportées et examinées

Le Code-Auditor a reproduit indépendamment 79 tests (34 S1, 16 TD2, 29 S2), l'exécution de 44 exemples et de deux préparations, le contrôle de 35 profils tuteur et de 34 sources actives. L'intégration rapporte également `check`, `render` et `verify` sur 34 supports avec adresse neutre, ainsi que nbformat et analyse syntaxique des sept sources. Aucune réponse étudiante n'a été exécutée. Ces validations sont décrites dans `docs/s1_editorial_correctors.md` ; elles ne sont pas présentées comme une exécution propre de la gouvernance.

Les sept snapshots de la nouvelle fixture ont été comparés au parent exact, en JSON et octet par octet, par l'auditeur technique. Les tests de conservation protègent IDs, ordre historique, métadonnées, AST des anciennes cellules, affichages fournis et restitution canonique. L'exception TD6 Q6 autorise seulement la suppression du `print` commenté précisément identifié ; l'affichage `repr(...)` du contrat reste protégé. Les exemples Markdown TD2 deviennent exécutables sans réponses ajoutées.

**TAL-AUD-001 est clos** : le test S2 utilisait encore les anciennes empreintes des sept TD S1. Il continue à vérifier ces empreintes contre les snapshots exacts du parent, sans régénérer les hashes historiques ni élargir les chemins exemptés ; les versions courantes S1 font l'objet des contrôles distincts ci-dessus. L'auditeur technique a accepté cette adaptation produite par l'intégration. Aucun assouplissement général du contrôle des fichiers S2 n'est rapporté ou visible dans le diff.

Les sept évaluateurs existaient déjà : aucun nouveau correcteur, changement de route, barème ou contrat de réponse n'est nécessaire. La restitution HTML canonique est conservée avec séparateur. Les cours, exemples, exercices et autoévaluations s'adressent à l'étudiant ; le double contexte caché reste destiné au tuteur. Les notices ne promettent plus de correction individuelle systématique.

## Limites de livraison

Les validations locales ne prouvent ni une CI distante réussie ni un démarrage Docker distant : à vérifier après publication. La durée de deux heures reste une cible non mesurée, particulièrement pour TD3 Q4, TD6 Q5–Q6 et TD7 Q5–Q6. Le comportement réel du tuteur Colab, la compréhension et l'authenticité des sorties étudiantes ne sont pas certifiés. Les contrôles et DM demandent leur propre revue de prérequis et de rédaction. Ces limites explicites n'invalident pas la conservation et la révision du lot courant, mais interdisent de le présenter comme une restauration exhaustive ou une validation de tout S1.
