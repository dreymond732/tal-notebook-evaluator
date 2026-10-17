# Audit de gouvernance — restitution étudiante S1 et S3

Date : 16 octobre 2026. Branche : `code/rapports-pedagogiques-s1-s3`. Base examinée : `c81c38641ecddb66c5ea65c78eafbd2d8d3cbbc5`.

## Verdict

**CONFORME pour présentation au mainteneur.** Les revues indépendantes de code, de pédagogie et de rédaction sont favorables. Aucun constat bloquant ne reste ouvert. L'intégration, impliquée dans la production, relève de **MAINTAINER_REVIEW** ; ce rapport ne constitue ni une autorisation de fusion, ni une validation de déploiement. Aucune fusion ni mise en production n'a été réalisée dans cette mission.

## Mandat, périmètre et indépendance

L'utilisateur a demandé un plan complet et sa mise en œuvre prioritaire sur S1 et S3 : montrer le code et les sorties effectivement retrouvés, proposer des exemples de code à la demande et séparer les explications étudiantes des diagnostics internes.

Le lot couvre les 19 évaluateurs formatifs actifs : sept TD S1, TD0–TD7 S3, TD1B S3 et R0–R2 S3, soit 116 questions et autant d'exemples. Les douze futurs TD one/bis/ter des PR encore ouvertes ne sont pas déclarés couverts : leurs exemples devront être adaptés à leurs sujets stabilisés. Le moteur S1 sait déjà extraire leurs preuves sans leur attribuer les exemples historiques.

| Rôle / agent | Production ou revue constatée |
|---|---|
| Orchestration et intégration — parent | Branche, répartition, tests de routes, aperçus synthétiques, raccordement et préparation de livraison. Producteur : ne peut rendre `READY_TO_MERGE`. |
| TAL-Prof — `prof_plan` | Plan et matrice source → cible dans `docs/pedagogy/plan_restitution_etudiante_s1_s3.md`. Aucun notebook modifié. |
| TAL-Code-Architect — `s1_feedback` | Enrichissement S1, 45 exemples, intégration au moteur commun et au moteur TD2, tests dédiés. |
| TAL-Code-Architect — `s3_feedback` | Extraction inerte, enrichissement S3 et remédiations, 71 exemples et tests dédiés. |
| TAL-Code-Architect — `template_feedback` | Présentation commune, annexe étudiante et tests du gabarit. |
| TAL-Pedagogy-Reviewer — `review_pedagogy` | Relecture indépendante des 116 exemples et comparaison aux énoncés ; verdict `ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`. Aucun produit modifié. |
| TAL-Editorial-Reviewer — `prof_plan`, second mandat | Relecture des textes produits par les autres agents, des énoncés et des aperçus ; verdict `ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE`. Son propre plan est expressément exclu de sa revue. Preuves par question et empreintes dans `reports/editorial/rapports-s1-s3.md`. |
| TAL-Code-Auditor — `audit_code` | Revue indépendante du code, des exemples et de la sécurité ; exécution de la suite finale ; verdict `ACCEPT`. Aucun produit modifié. |
| TAL-Governance-Auditor — `audit_code`, second mandat | Présent audit après clôture des revues spécialisées. L'écriture de cet agent est limitée au présent fichier dans `reports/governance/`. |

Les deux cumuls de rôles restent des mandats de revue sur des productions tierces ; aucun producteur n'a validé son propre produit. Les verdicts spécialisés ont été transmis en session. La revue éditoriale est également conservée dans le dépôt. Aucun Étudiant-Modèle, aucune copie d'étudiant réel résolue et aucune revue GitHub déjà publiée ne sont revendiqués.

## Contrats et couverture

Sources normatives relues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md`, fiches Code-Auditor, Governance-Auditor et Integration-Master.

La comparaison à la base confirme l'absence de modification des notebooks TD/contrôles, des tuteurs, du catalogue, des règles normatives, des routes, de la persistance, du Dockerfile et de la CI. Aucune activité étudiante n'est supprimée ou déplacée ; aucun arbitrage de réduction pédagogique n'est requis. La matrice du plan associe les défauts constatés aux corrections et critères d'acceptation.

Le contrat de notation est conservé : signatures `check_notebook(content_str, filename)`, tuple à cinq éléments, identités et versions, marqueurs, validateurs, scores et maxima. Les champs de présentation sont enrichis après la notation. Le `grade_traces` partagé avec les contrôles n'est pas enrichi de solutions formatives. Le raccordement S1 est sans effet pour les évaluateurs S2.

Le rapport sépare code retrouvé, sorties enregistrées, diagnostic, action et exemple. Les numéros de cellules suivent le fichier soumis. Les doublons, JSON mal formés, sorties stderr et erreurs restent visibles ; une preuve rejetée n'est pas reconstruite en réponse valide. Une trace plausible peut rester fabriquée ou périmée : l'extraction ne prétend pas en authentifier l'exécution.

L'ancien mélange « Observation Q4 » des remédiations est déplacé dans une portée non notée ; le code Q4 reste extrait dans sa propre réponse. Les états explicites prévalent sur les anciens symboles. Les productions personnelles et interprétations ne sont pas annoncées comme corrigées par les exemples de calcul.

## Preuves techniques indépendantes

| Contrôle | Résultat observé par Code-Auditor |
|---|---|
| Suite finale complète | `PATH=/root/.local/bin:$PATH python -m unittest discover -s tests -v` : **334 tests, 334 réussites**, 8,076 s. Journal de session : `/tmp/tal-audit-final.log`. |
| Syntaxe et diff | `python -m compileall -q app tests` et `git diff --check` : **PASS**. |
| Couverture des exemples | Inventaire indépendant du catalogue : **19 évaluateurs / 116 questions**, code non vide et AST valide pour chaque exemple. |
| Exécution des exemples auteurs | Tests applicatifs : **45 exemples S1 et 44 exemples déterministes S3**, soit **89/116**, exécutés localement avec résultats conformes aux critères existants. Les autres exemples ne sont pas annoncés comme exécutés. |
| Non-exécution du code soumis | Tests de sources sentinelles, erreurs, sorties fabriquées et patch de `exec` ; lecture du chemin AST/JSON : **PASS**. L'exécution des 89 exemples concerne seulement le code versionné des auteurs, dans les tests locaux. |
| Routes, proxy et persistance | Nouveau test : **38 POST** réels, 19 évaluateurs × dépôt automatique et route explicite, sous `/universite/tal/`. Code/sorties/erreurs synthétiques visibles et échappés, rapport HTML, notebook et CSV sauvegardés : **PASS**. Tests historiques des sélecteurs, identités et erreurs de persistance : **PASS**. |
| Contrôles sans divulgation | Tests historiques des reçus publics, rapport enseignant privé, erreurs, routes et proxy : **PASS** ; aucun exemple formatif dans le retour de `grade_traces`. |
| HTML inerte | Autoescape conservé pour code, sorties, diagnostics et solutions ; aucune sortie HTML/SVG soumise rendue comme HTML actif. Tests XSS et bascule locale sans dépendance externe : **PASS**. |
| Erreur de traceback atypique | Défaut initial `traceback=[None]` corrigé. Reproduction indépendante sur TD1 S1, TD2 S1, TD1 S3 et R0 : **4 POST PASS**, erreur locale visible, rapport sauvegardé, aucune exécution. Régression dédiée incluse dans la suite. |
| Tuteurs | `python app/tutor_metadata.py --check` : **PASS**, 36 contextes existants. Aucun contexte changé. |
| Distribution | `prepare_student_notebooks.py check`, puis `render` et `verify` avec URL neutre `https://example.test/universite/tal` : **PASS**, 34 notebooks. Sortie d'audit dans `/tmp/tal-audit-dist`, sources intactes. |

Les échecs intermédiaires ne sont pas présentés comme une validation : adaptation du libellé du score, maintien du champ historique `correct_answer` et correction du traceback ont été vérifiés avant la campagne finale. L'affichage explicite du nuage de mots, la séparation des diagnostics S2 et les états des remédiations ont également été repris. Aucun constat technique ouvert ne subsiste.

## Limites et relais

- **Exemples dépendants de spaCy : `NOT_TESTED` à l'exécution.** Les 27 exemples S3 restants ont été relus et compilés ; les paquets et modèles nécessaires ne sont pas installés dans cet environnement. Cela ne valide pas leurs prédictions réelles ni leur rendu graphique.
- **Rendu navigateur interactif : `NOT_TESTED`.** L'intégration rapporte un téléchargement Chromium vide ; les aperçus HTML synthétiques ont été relus sémantiquement et les conditions du gabarit testées, sans inspection visuelle effective du responsive ou du clic.
- **Docker : `NOT_TESTED`.** Docker n'est pas disponible localement. Le job existant `container-smoke` reste à exécuter dans la CI de la PR.
- **Colab, classe et déploiement : `NOT_TESTED`.** Aucune soumission étudiante réelle, exécution de notebook étudiant sur le serveur, fusion ou intervention en production.
- **Branches pédagogiques futures : hors verdict.** La compatibilité avec les TD one/bis/ter devra être relue après stabilisation et intégration des PR concernées ; ce lot ne les modifie pas.

Les aperçus `docs/examples/rapport_td1_s1.html` et `docs/examples/rapport_td1_s3.html` sont explicitement synthétiques et régénérables. Le plan, les tests, les revues et ces limites doivent accompagner la PR, qui reste soumise au mainteneur. **CONFORME ; intégration : MAINTAINER_REVIEW.**
