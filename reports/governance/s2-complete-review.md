# Gouvernance — Révision complète du semestre 2

## Mission et verdict

Revue du 1er octobre 2026, branche `pedagogy/s2-complete-review`, base `b7650e3d035846a67014b94e463a08cd43b67fb5` après fusion de la PR 21. L’enseignant demande une révision complète du S2 dans des dossiers dédiés, avec progression explicite, métadonnées, tuteur, restitution HTML et consolidations récentes, sans réduction des activités existantes.

**Verdict : CONFORME**, pour le périmètre et les preuves ci-dessous. Le passage des six correcteurs S2 actifs au contrat v2 constitue un **CHANGEMENT_DE_CONTRAT** : double revue spécialisée, puis gouvernance. Les 140 questions des sept sujets sont conservées ; 122 relèvent des six correcteurs actifs. Le contrôle final reste inactif et hors distribution, comme avant la révision : son ancien module ne correspond pas au sujet et son barème par question n’est pas validé.

## Responsabilités et indépendance

| Rôle | Intervention | Verdict ou relais |
|---|---|---|
| TAL-Prof — `s2review_prof` | Matrice avant conception, progression, contrat des réponses, périmètres du tuteur | Matrice validée par l’orchestrateur avant conception ; aucune réduction |
| TAL-Pedagogy-Designer — `s2review_designer_td`, `s2review_designer_controls` | Trois TD, quatre évaluations, métadonnées, tuteurs, HTML et bilans | Produits soumis à revue indépendante |
| TAL-Code-Architect — `s2review_engine`, `s2review_checks` | Contrats, moteur partagé, six correcteurs, catalogue, routes, distribution et tests techniques | Produits soumis à revue indépendante |
| TAL-Integration-Master — `s2review_integration` | Fixture de conservation, tests d’intégration et documentation technique | Producteur : `MAINTAINER_REVIEW` |
| TAL-Code-Auditor — `s2review_code_auditor` | Revue technique, sondes et tests indépendants ; produits en lecture seule | `ACCEPT` après clôture des constats |
| TAL-Pedagogy-Reviewer — orchestrateur | Lecture des sept sujets, progression, couverture et tuteurs ; produits en lecture seule | `ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` |
| TAL-Governance-Auditor — `s2review_code_auditor`, mission distincte après les deux verdicts | Permissions, provenance, contrats et preuves ; présent rapport uniquement | `CONFORME` |

La limite de sessions a conduit à deux cumuls explicites : le Designer TD a reçu les derniers ajustements de périmètre du tuteur relevant du rôle Prof ; l’auditeur code assure ensuite la gouvernance. Aucun de ces producteurs ne valide ses propres produits : l’orchestrateur n’a modifié aucun produit de cette PR et assure la revue pédagogique ; l’auditeur code et gouvernance n’a modifié ni application, ni tests, ni notebooks, ni documentation pédagogique. Son unique écriture est le présent rapport.

La branche est dédiée. `AGENTS.md`, la matrice de permissions, `docs/EVALUATOR_CONTRACT.md` et `docs/agents/` restent inchangés. Aucune fusion ni mise en production n’est effectuée.

## Conservation et pédagogie

La matrice `docs/pedagogy/s2_complete_review_coverage.md` précède la conception ; elle indique les sept déplacements, les 140 questions et les exceptions techniques bornées. Les bilans `docs/s2_review_td_coverage.md` et `docs/s2_review_controls_coverage.md` décrivent les apports. Chaque déplacement possède son équivalent intégral immédiat : les TD sont dans `Notebooks TD/S2/`, les évaluations dans `Notebooks contrôles finaux/S2/`.

La gouvernance a comparé directement les sept objets de `tests/fixtures/s2_complete_review_source_baseline.json` aux sources obtenues par `git show` au commit parent : identité exacte. Les 37 autres notebooks correspondent aussi au parent et à leurs empreintes actuelles, notamment S1, S3, corrigés et archive historique exclue. Les fixtures historiques restent inchangées et la nouvelle preuve s’y rattache. Les tests vérifient l’ordre des cellules et les préfixes des sources conservées, avec exceptions explicites pour tuteur, identité, titre erroné « Contrôle S3 » et affichages canoniques. Données et calculs étudiants ne sont pas réduits.

La revue pédagogique indépendante confirme les 140 questions, les prérequis, les transferts et les 71 exemples avec 71 essais, complétés par trois synthèses. Les trois supports formatifs couvrent cinq séances accompagnées de deux heures : deux pour TD3, deux pour TD5, une pour TD6. **Ces durées sont des hypothèses de conception, non des temps mesurés.** Aucune activité obligatoire n’est rendue optionnelle ni externalisée pour tenir artificiellement dans deux heures. La numérotation historique reste visible, mais l’ordre suit les acquis : TD3, contrôle TD2, TD5, contrôle TD4 et devoir maison, puis TD6.

Les constats pédagogiques sont clôturés : les 74 cellules de pratique et synthèse sont collectées dans le rapport humain sans points ; le gabarit incorrect utilisant `or` en TD3 Q3 ne reçoit plus de crédit ; les périmètres du tuteur couvrent les prérequis d’anagrammes et les opérations de fichier réellement nécessaires ; les cas limites des bigrammes sont explicités ; le nouvel essai d’anagrammes utilise des données distinctes du contrôle. Les quatre évaluations ne reçoivent aucun nouveau guidage ; leurs consignes et indices historiques sont conservés conformément à la règle de non-réduction.

Le tuteur est synchronisé en métadonnées et en première cellule Markdown. Les TD guident par dialogue et exemples distincts ; contrôles, devoir maison et final interdisent toute assistance. Aucune nouvelle bibliothèque n’est introduite. Cette cohérence ne garantit pas l’obéissance d’un service LLM externe.

## Contrat technique et sécurité

- Les identifiants publics et leur casse sont conservés. Six évaluateurs actifs passent en v2, avec 122 questions et maxima historiques de 20, 30, 40, 25, 20 et 40 points. Le final conserve 18 questions et son statut inactif.
- Métadonnées racine et cellules identifient explicitement le correcteur, les questions et les rôles. Les quatre champs d’identité sont littéraux ; le numéro étudiant distingue les homonymes. Les anciennes versions sont refusées avec « mauvaise version du notebook », avant correction ou persistance, sur dépôt automatique et route historique.
- Les valeurs enregistrées sont comparées avec leurs types et les variantes autorisées ; les constructions demandées sont recherchées dans leurs dépendances syntaxiques. Exemples, pratiques, préparations, commentaires et restitution ne valent pas réponse.
- Les fichiers sont évalués au moyen des traces relues et enregistrées : corpus multiligne, espaces significatifs, dernière ligne, CSV complet, en-tête et ordre décroissant. Les égalités de fréquence admettent plusieurs ordres. Une écriture du premier CSV ne suffit pas à prouver celle du second.
- Le serveur n’exécute aucun code étudiant et n’ouvre aucun chemin fourni par la copie. Les tests utilisent des sources et sorties synthétiques inertes. L’analyse littérale est bornée ; les critères et barèmes appartiennent à l’application.
- Les contrôles et le devoir maison ne montrent qu’un accusé de dépôt ; les détails restent dans le rapport enseignant, avec HTML étudiant échappé. Les résultats v2 vont dans `soumissions/<identifiant>-v2/<classe>/`, sans réécriture des historiques.
- Chaque source S2 se termine par la cellule HTML canonique contenant `__TAL_PUBLIC_URL__`, sans adresse réelle ni sortie exécutée. L’injection concerne les copies distribuées ; le final inactif reste hors `dist`. Les contrôles utilisent une URL neutre.

Les constats techniques sont clôturés après contre-épreuves indépendantes : `TAL-AUD-S2-001` casse des identifiants ; `002` indices négatifs équivalents ; `003` constructions explicitement demandées ; `004` condition composée du TD3 Q3 ; `005` confusion entre les écritures des deux CSV du TD6. Les vrais wrappers et les vrais sujets complétés par des traces synthétiques font partie des tests.

Le résultat reste un **score technique provisoire**. L’analyse statique ne reconnaît pas tout programme Python valide, ne démontre pas sa généralité et n’authentifie ni l’auteur ni la fraîcheur des sorties. Les explications, choix et interprétations nécessitent une relecture humaine.

## Preuves et relais

Le premier passage d’intégration comptait 281 tests ; les contrôles ajoutés pendant la revue portent le total final à 284. Le résultat de publication à retenir est celui de la suite finale.

| Vérification | Résultat |
|---|---|
| Suite complète finale, relancée indépendamment après le correctif CSV | **284 tests PASS**, aucun saut, 5,189 s |
| Résultats S2 ciblés | **18 tests PASS**, 122 références indépendantes, six vrais wrappers et six sujets réels |
| Préservation, métadonnées et distribution S2 | PASS dans la suite complète |
| Tuteurs synchronisés | **34/34 PASS** |
| Vérification des sources | **33/33 PASS** |
| Comparaison directe à la base Git | Sept sources de fixture exactes ; 37 autres notebooks identiques |
| `git diff --check` | PASS |
| Revue technique | **ACCEPT**, auditeur indépendant des produits |
| Revue pédagogique | **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**, orchestrateur indépendant des produits |

**Docker local : NOT_TESTED. CI distante : à clôturer sur le commit exact de la PR après publication.** Le résultat distant, notamment construction et santé Docker, doit figurer dans le relais de PR avant fusion ; il n’est pas présumé ici.

L’Integration-Master reste **MAINTAINER_REVIEW**, puisqu’il produit des tests et la documentation. Le mainteneur décide de la fusion et du déploiement. Après fusion et déploiement, redistribuer les **six nouveaux notebooks S2 actifs** depuis les dossiers S2 de `dist` : les anciennes copies v1 ne sont ni migrées automatiquement ni corrigées. Le contrôle final nécessite une mission explicite sur son correcteur et son barème avant activation et distribution.
