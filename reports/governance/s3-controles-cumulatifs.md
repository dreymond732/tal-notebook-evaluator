# Audit de gouvernance — contrôles cumulatifs S3

## Verdict et périmètre

**CONFORME pour présentation au mainteneur.** L’intégration ayant participé à la préparation du lot, son statut est **MAINTAINER_REVIEW**, et non `READY_TO_MERGE`. La PR est à ouvrir **prête pour revue**, conformément à la décision enseignante en session ; aucun brouillon supplémentaire n’est requis. La fusion et le déploiement restent à la décision du mainteneur.

Branche observée : `pedagogy/s3-controles-cumulatifs`, base `affb1b47d0e2c6b408dc9be37a5fd66de94b3779`. La demande porte sur une série consistante de contrôles centrés sur le TD précédent et réinvestissant les acquis antérieurs dans d’autres contextes, avec un premier contrôle après TD1. Le lot ajoute sept sujets C1–C7, sept évaluateurs, leur intégration aux routes et à la persistance, les profils du tuteur, les tests et les documents associés. Aucun TD ni ancien contrôle n’est remplacé.

Sources normatives relues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md`, rôles Pedagogy-Reviewer et Governance-Auditor. Le changement de contrat suit le flux mixte.

## Séparation des rôles

| Rôle / agent | Production ou contrôle |
|---|---|
| TAL-Prof — `controls_prof` | Matrice préalable, spécification, manifeste du tuteur et documentation pédagogique dans sa zone autorisée. |
| TAL-Pedagogy-Designer — `controls_designer_a` | Sujets C1–C3 et sommaire des contrôles ; corrections demandées par les revues. |
| TAL-Pedagogy-Designer — `controls_designer_b` | Sujets C4–C7, données et contrats de résultats ; corrections demandées par les revues. |
| TAL-Code-Architect — `controls_architect` | Évaluateurs, intégration, tests et documentation technique ; aucune auto-validation. |
| TAL-Code-Auditor — `controls_review_code` | Revue indépendante en lecture seule ; **ACCEPT** et campagne de **97 tests réussis** transmis à l’intégration. |
| TAL-Pedagogy-Reviewer — `controls_review_pedagogy` | Validation préalable de la matrice, lecture indépendante des sept sujets et des TD sources ; **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE** après clôture des constats. |
| TAL-Governance-Auditor — même agent, second mandat | Écriture limitée au présent rapport. Cet agent n’a produit ni sujet, ni correcteur, ni spécification ; la séparation producteur/réviseur est conservée. |
| Orchestration / intégration — parent | Répartition, collecte des preuves, vérification complémentaire et publication ; intégration impliquée, donc `MAINTAINER_REVIEW`. |

Les verdicts spécialisés sont des handoffs explicites de session. Ils ne sont pas présentés comme des reviews GitHub déjà publiées. Aucun Étudiant modèle n’a été mobilisé et aucune copie corrigée n’est livrée.

## Preuves et résultats

| Exigence | Preuve examinée et résultat |
|---|---|
| Branche dédiée | Observation propre de la branche et de sa base ; aucun changement direct de `main`, fusion ou déploiement dans ce mandat. |
| Matrice avant conception | `S3_CONTROLES_COVERAGE_MATRIX.md` lue et acceptée avant le GO de conception. Le repérage final lie les objectifs des TD aux questions des contrôles. Les supports TD existants sont inchangés. |
| Couverture cumulative | Lecture propre : C1 annotations, positions, phrases, filtres, dépendances et acquis Python ; C2 fréquences, exclusions, POS, WordCloud/barres et fonctions généralisées ; C3 concordances, formes/lemmes/expressions, citations et preuves ; C4 unités, marges, union/somme, fenêtres et frontières ; C5 proportions, dénominateurs, table 2×2 et sensibilité ; C6 dispersion, segmentation, cartes de chaleur, matrices et retour au texte ; C7 audit paramétrable, citations, cas indépendant et rapport. |
| Transfert substantiel | Lecture propre : corpus indépendants et réutilisation effective des fonctions. C1 musée/transport/météo ; C2 réparation/table portuaire/alimentation ; C3 patrimoine/radio ; C4 mobilité/archives sonores ; C5 médiation muséale/littoral ; C6 exposition/ateliers ; C7 médiathèque/jardin. Les annonces C7 sont explicitement synthétiques, sans attribution à un modèle réel. |
| Charge et autonomie | Sept exercices par contrôle, plusieurs productions liées par exercice, soit 49 exercices et 49 traces. Chaque budget totalise 120 minutes. Les notes et fonctions personnelles de TD sont autorisées, les corrigés et assistants interdits. Aucun ancien fichier n’est techniquement requis. Le tableau et les notes du C7 sont constitués progressivement. La durée reste prévisionnelle. |
| Pas de notion anticipée | C1 n’impose pas Counter ; C2 n’impose pas un moteur d’expressions ; C4 ne demande pas d’association statistique ; PMI et recherche approchée ne sont pas exigées. La comparaison moyenne des taux/taux global est réservée à C6, après apprentissage au TD6. |
| Absence d’aide dans les contrôles | Lecture propre des sujets : données, conventions, formats et imports sont fournis, mais aucune fonction solution, valeur résultat ni exemple résolu. Le tuteur refuse code, indices, quiz, explications, validation et exécution de cellules. Instructions dans la première cellule Markdown et les métadonnées. |
| Cohérence des profils | Intégration : `app/tutor_metadata.py --check` réussit pour **33 profils** ; les 26 profils antérieurs et les exclusions sont inchangés. Les contrôles sont classés `controle`, les TD gardent leur guidage. |
| Changement de contrat | Déclaré dans les spécifications et `docs/S3_CONTROLS_EVALUATION.md`. Sept routes `controle-td1-s3` à `controle-td7-s3`, traces `S3_Cn_Qm`, barème technique 2 + 6 × 3 = 20, signature et tuple de retour conservés. Double revue favorable. |
| Portée de l’évaluation | Lecture propre du contrat et du moteur : score technique provisoire distinct d’une note globale. La grille humaine examine code, transfert, annotations, preuves, figures et interprétations. Aucun score de qualité fondé sur la longueur du texte. Le rapport privé et le CSV désignent explicitement le caractère technique provisoire et la relecture requise. |
| Non-exécution serveur | Lecture propre : parse JSON/AST et sorties enregistrées, aucun lancement des fonctions soumises. La vérification linguistique se limite aux positions, à la couverture et à la cohérence des annotations ; elle n’est pas présentée comme une certification linguistique. |
| Mesures et données | Les données contractuelles sont rapprochées statiquement des littéraux des sujets. Les contrôles déterministes portent sur comptes, indices, expressions contiguës, marges, agrégation et dénominateurs. Les proportions indéfinies restent `null` ; une annonce incomplète reste insuffisamment définie malgré un recomptage exploratoire. |
| Revue technique | Code-Auditor : **ACCEPT**, **97/97 tests**, dont 20 nouveaux tests ; moteur, corpus, traces invalides, modules, routes, proxy, persistance, confidentialité du reçu, CSV spécialisé et échappement HTML. Intégration : second passage complet également **97/97**. Les campagnes existantes restent incluses. |
| Faisabilité linguistique | Code-Auditor : calcul indépendant des 14 traces C1–C2 avec spaCy 3.8.7 et modèle français 3.8.0, acceptées à 20/20 ; alignement des deux flux C6 vérifié. Il s’agit de traitements d’audit propres au réviseur, sans exécution de cellules étudiantes. |
| État des sujets | Intégration : nbformat et AST conformes pour les sept sujets ; sorties vides et compteurs d’exécution nuls. Observation propre des cellules : espaces de réponse vierges. |
| Non-régression de périmètre | Observation propre du diff : aucun sujet TD existant, corrigé modèle, contrôle historique, règle d’agent, workflow, Dockerfile ou Compose modifié. Les modifications communes du moteur et du CSV sont couvertes par la campagne de non-régression. |

## Constats clos

- **TAL-PED-001 — conditions de réemploi ambiguës.** Les introductions précisent désormais la reprise autorisée des notes et fonctions personnelles, l’adaptation requise et l’interdiction des corrigés et assistants. Charge et autonomie deviennent interprétables.
- **TAL-PED-002 — anticipation au C5.** La comparaison moyenne des taux/taux global, enseignée au TD6, a été retirée du C5 et de son contrat. Elle reste au C6, à sa place dans la progression.
- **Faisabilité de C1 Q5.** La première phrase n’offrait pas la relation verbale attendue avec le modèle figé. Le sujet cible la deuxième phrase ; le Code-Auditor a vérifié `observe` racine et `visiteuse` dépendant `nsubj`. La réserve pédagogique a été rouverte puis clôturée sur cette preuve technique.
- **TAL-AUD-001 — casse du découpage C1 Q1.** Le correcteur attendait un découpage en minuscules alors que le sujet demandait celui du texte original. Le Code-Auditor confirme la séparation corrigée entre découpage original et fréquences normalisées, avec test de régression. Le défaut de dépendance C1 Q5 correspond à son constat **TAL-AUD-002**, également clos.
- **Consistance de C2.** Les deux corpus textuels ont été enrichis à douze phrases chacun, avec des répétitions et contrastes utiles aux fréquences et figures, au lieu d’un ensemble dominé par des occurrences uniques.
- **Sommaire des contrôles.** Les titres et contextes provisoires C4–C7 ont été remplacés par ceux des sujets définitifs ; aucun notebook n’a été modifié lors de cet alignement documentaire.

## Empreintes des sujets audités

| Sujet | SHA-256 |
|---|---|
| Controle_TD1_S3.ipynb | `9254cf50a03003ab01cef350e0679904202b9650c058f3916a362c846aca292d` |
| Controle_TD2_S3.ipynb | `8880f987290ad5aba7b44a3d9fd3f4517aa0413f432ee6bce3e100af118028d2` |
| Controle_TD3_S3.ipynb | `d9148c1a9c531039940e9348ec27508b9d3651d0c5c6875d20785535e887f5d5` |
| Controle_TD4_S3.ipynb | `833316e47c088fe6644038c9246e965c2c1bce4ccd0bd8f146ddcaf3d0cceb64` |
| Controle_TD5_S3.ipynb | `b9a9cfa6b2aa55d117e529821a4d8e114eef77a6970b39657c6f0de7c0593a4e` |
| Controle_TD6_S3.ipynb | `2b82586b325acc64a426a6137987ae6d93f1a15d235af0d1b47ce72a04d6525a` |
| Controle_TD7_S3.ipynb | `8268ecce4e174ce5c18cf5e7a8c76bf104d59d5d48c499af19d792674ee176df` |

## Limites et relais

- Exécution intégrale dans **Colab : NOT_TESTED**. Le comportement effectif du service tiers face aux instructions de refus n’est pas garanti par leur présence dans le fichier.
- **Passation en classe : NOT_TESTED**. Les deux heures sont un budget de conception ; administrer les sept sujets intégralement représente quatorze heures à organiser séparément des huit TD.
- **Docker et déploiement : NOT_TESTED** dans cette mission. Les tests Flask/proxy ne constituent pas un déploiement de production.
- Une sortie enregistrée peut être fabriquée ou périmée. Le serveur ne certifie ni l’autonomie, ni l’existence effective d’une fonction généralisable, ni la validité scientifique d’une interprétation. La relecture humaine demeure nécessaire.
- Le barème /20 est un indicateur technique proposé, pas une note globale déjà arrêtée par l’enseignant.

Le présent auditeur n’a pas relancé la suite technique : les preuves de tests et d’environnement sont attribuées à leurs auteurs. Aucun veto de gouvernance restant. Relais à l’intégration : publier la PR prête pour revue, avec ce rapport, les deux verdicts spécialisés et les limites, puis laisser la fusion au mainteneur.
