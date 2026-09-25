# Audit de gouvernance — TD S3 et préparation du nettoyage historique

## Verdict et périmètre

**CONFORME**, le 25 septembre 2026, pour les commits `6a7665f` et `9b779f2`,
branche `pedagogy/td-s3-sans-consigne-depot`, comparés à `origin/main`
`5f7a736`. Ce verdict porte sur le retrait des consignes actuelles des TD S3
et sur l'outil de préparation/publication contrôlée de l'historique. Il ne
vaut ni fusion, ni publication de l'historique réécrit, ni déploiement.

## Autorisation et séparation des rôles

Sources normatives lues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`,
`docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et le rôle
`TAL-Governance-Auditor`.

L'enseignant demande explicitement de poursuivre sur les TD S3 et l'historique
Git le retrait des adresses de dépôt. Cette autorisation couvre la préparation
technique et le retrait logistique ; aucune activité pédagogique n'est réduite.

- `/root/td3_deposit_prof`, TAL-Prof, a produit avant édition la matrice
  `docs/pedagogy/S3_TD_DEPOSIT_REMOVAL.md` et précisé le périmètre du README.
- `/root`, TAL-Pedagogy-Designer, a modifié huit TD et leur README.
- `/root/history_architect`, TAL-Code-Architect, a produit l'utilitaire,
  ses tests et sa documentation technique.
- `/root/td3_deposit_review`, TAL-Pedagogy-Reviewer indépendant, a transmis
  directement **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**.
- `/root/history_code_audit`, TAL-Code-Auditor indépendant, a rendu
  **ACCEPT** sur les trois fichiers techniques finalisés.
- `/root/td3_history_governance` a contrôlé les preuves et écrit uniquement
  le présent rapport.

La double revue est obtenue pour ce lot code et pédagogie. Le contrat de
correction, les routes, les barèmes, les sorties évaluées et la persistance
des copies restent inchangés. Les verdicts cités sont des preuves de session,
pas des reviews GitHub supposées publiées.

## Preuves examinées

| Exigence | Preuve et résultat |
|---|---|
| Branche dédiée | HEAD `9b779f2` et branche contrôlés ; espace de travail propre avant rédaction du présent rapport. Aucun changement direct de `main` observé. |
| Cadrage préalable | Matrice source → cible lue intégralement, avec arbitrage logistique autorisé et distinction explicite entre dépôt de copie, sauvegarde et dépôt de code. |
| Conservation des supports | Comparaison JSON indépendante de la gouvernance : huit TD, une seule source Markdown modifiée par TD ; code, sorties, métadonnées et structure conservés. Le réviseur confirme la conservation intégrale des trois remédiations R0–R2. |
| Couverture pédagogique | Revue indépendante : objectifs, exercices, ressources et liens, exports, sauvegardes, durées, réemploi des fonctions, bilans méthodologiques et limites des vérifications automatiques conservés. Aucune consigne de transmission ni domaine serveur restant dans les onze supports audités. |
| Tuteur | Journaux `/tmp/tal-td3-tutor-tests.log` et `/tmp/tal-td3-tutor-check.log` lus : 22 tests réussis et 33 profils conformes. La gouvernance ne les a pas relancés. |
| Utilitaire historique | Auditeur code : sept tests relancés avec succès ; trois vérifications indépendantes supplémentaires couvrent le rejet atomique serveur, une référence avancée entre vérification et publication, et le refus des tags annotés. |
| Préparation réelle | Manifeste local lu : six branches, aucun tag, 111 commits, 283 versions de blobs, 15 signatures retirées. Auditeur code : bundles valides, empreinte conforme, conservation des 111 commits et ressources identiques en chemins, modes et contenus. |
| Graphe et ressources | Le script compare parents, auteurs, committers, dates, messages et arborescences ; seules les substitutions de domaines et du pin des ressources sont autorisées. Nouveau pin vérifié : `b92e92b6c216014283056c83aa545881a447b3a5`. |
| Publication encadrée | `prepare` ne publie rien ; `publish` vérifie l'empreinte du bundle et les références, puis utilise des références explicites, `--atomic` et un bail par référence, sans demande de suppression ni contournement des protections. |
| Données privées et serveur | Sauvegarde originale hors du dépôt de travail ; paramètres privés non versionnés. Aucune adresse personnelle reproduite dans les nouveaux fichiers techniques ou ce rapport. Aucun code de notebook étudiant exécuté, aucune copie étudiante transmise. |
| Qualité du diff | `git diff --check origin/main...HEAD` exécuté par la gouvernance : succès sans diagnostic. |

## Limites et statut réel

L'historique nettoyé a été **préparé et vérifié localement uniquement**. Les
références distantes restent dans leur état antérieur : l'authentification
Git permettant leur publication n'est pas disponible dans cet environnement.
Une publication ordinaire de la branche de PR n'est pas une publication de
l'historique réécrit.

La création de cette branche distante et sa fusion rendent la préparation
locale actuelle obsolète pour la publication. Le mainteneur doit préparer
de nouveau depuis son poste authentifié après fusion, comme indiqué dans
`docs/HISTORY_CLEANUP.md`. Les signatures des commits modifiés ne peuvent
être conservées ; le script les compte et refuse les tags annotés.

Les baux protègent les références existantes. Une nouvelle branche créée
après le contrôle préalable n'est détectée qu'au contrôle final : le gel
des contributions doit couvrir toute l'opération. Les copies, forks, caches
et références de PR peuvent conserver d'anciens objets ; aucun effacement
mondial n'est revendiqué. La documentation explique ces limites et la
préservation préalable des soumissions, configurations et volumes Docker
avant le reclonage du serveur.

Publication historique distante, exécution de notebooks, suite Flask complète
et déploiement : **NOT_TESTED / NON_EFFECTUÉS** pour ce lot. Le serveur
applicatif n'est pas modifié. Le script futur d'injection de cellule de dépôt
par variable d'environnement reste hors périmètre.

Aucun veto de gouvernance. Relais à l'Integration-Master indépendant ; fusion
et production restent sous décision du mainteneur. La gouvernance ne rend
pas `READY_TO_MERGE`.
