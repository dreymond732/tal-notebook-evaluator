# Audit de gouvernance — Métadonnées, dépôt unique et distribution TAL

## Verdict et périmètre

**CONFORME**, le 26 septembre 2026, pour la migration examinée sur la branche
`integration/tal-metadata-submit`, comparée à la référence
`2a367529963f66a186dff1658b5951d0dbc27642`. L'audit porte sur les modifications
locales présentées avant leur commit : catalogue, métadonnées de 32 sujets,
résolution des réponses, entrée `/submit`, préparation des copies distribuables,
documentation et gardes de non-régression. Il ne vaut ni fusion ni déploiement.

Ce verdict concerne la conformité de cette migration et de son processus ; il
ne certifie pas la correction de tous les barèmes historiques. Les limites
précises sont consignées ci-dessous. Aucun actif normatif n'a été modifié.

## Autorisation et séparation des rôles

L'enseignant demande de poursuivre la transposition du parcours TQR à TAL après
présentation du plan. La réalisation conserve les activités, les barèmes et les
instructions du tuteur ; elle n'introduit aucune nouvelle compétence évaluée.

Sources normatives consultées : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`,
`docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et le rôle gouvernance.

- TAL-Prof a établi `docs/pedagogy/metadata_migration_coverage.md` avant l'édition
  des notebooks ; cet ordre a été confirmé dans le relais de l'orchestrateur.
- TAL-Pedagogy-Designer a effectué les ajouts de métadonnées aux 32 sujets.
- TAL-Code-Architect et l'agent de résolution ont produit catalogue, contrat,
  routage, adaptations des moteurs et tests techniques. L'orchestrateur, dans
  son rôle Architecte, a produit le générateur, `deploy.sh`, les exclusions Git,
  les tests de distribution et la documentation technique correspondante.
- TAL-Integration-Master a produit les preuves d'intégrité, la CI et sa note
  d'intégration ; il est donc producteur et ne peut s'auto-déclarer indépendant.
- `/root/consolidation_code_review`, TAL-Code-Auditor indépendant, a confirmé
  directement **CONFORME**, avec revue en lecture seule et aucune écriture produit.
- `/root/consolidation_pedagogy_review`, TAL-Pedagogy-Reviewer indépendant, a
  confirmé directement **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**, avec aucune
  écriture produit.
- `/root/consolidation_governance` a examiné les preuves et écrit uniquement
  le présent rapport, sans modification du produit ou des règles auditées.

Le routage et la localisation des réponses constituent un
`CHANGEMENT_DE_CONTRAT` : la double revue requise est obtenue. Les verdicts
rapportés sont des preuves explicites de session, non des reviews GitHub
supposées publiées. Aucune réduction pédagogique n'ayant été constatée, aucun
arbitrage de suppression n'est requis pour cette migration.

## Preuves examinées

| Exigence | Preuve et résultat |
|---|---|
| Branche et permissions | Gouvernance : branche dédiée et référence vérifiées ; aucun diff sur `AGENTS.md`, la matrice, `docs/agents/` ou `docs/EVALUATOR_CONTRACT.md`. Répartition des écritures confirmée par les relais. |
| Cadrage préalable | Matrice du Prof : correspondance des 33 profils, détail des activités et invariants, statut inactif de `ControleFinalS2.ipynb`, exclusions et règles de résolution explicités. |
| Intégrité des sujets | Réviseur pédagogique : comparaison profonde des 32 JSON à la référence, après retrait des seules nouvelles clés `metadata.tal` ; sources, sorties, compteurs, pièces jointes, IDs, ordre et métadonnées antérieures identiques. |
| Affectation des cellules | Réviseur pédagogique : 313 cellules de réponse et 28 cellules d'identification rapprochées des marqueurs et des titres ; aucun décalage constaté, aucun contexte tuteur évalué comme réponse. |
| Exclusions | Réviseur pédagogique : neuf corrigés et le sujet inactif identiques octet par octet ; aucune distribution ou activation implicite de ces supports. |
| Preuves de référence | Auditeur code : recalcul indépendant des 42 empreintes de la fixture depuis les objets Git de la référence ; correspondance exacte. La CI ne régénère pas ces références. |
| Tuteurs | Vérification propre de la gouvernance : `python app/tutor_metadata.py --check`, 33 profils conformes. La revue pédagogique confirme les règles S1 sans code et le refus absolu des contrôles, conservés dans les deux emplacements. |
| Catalogue et modes | Catalogue validé contre les registres actifs. `td2-S2` et `td4-S2` demeurent des contrôles. Les métadonnées téléversées ne déterminent ni le mode ni un module à importer librement. |
| Routage et confidentialité | Revue technique : reconnaissance indépendante du nom de fichier, refus des identités incohérentes et doublons, compatibilité des anciennes routes ; traitement de persistance commun et rapport détaillé des contrôles réservé à l'enseignant. |
| Non-exécution des copies | Lecture du contrat, du routage et de la résolution par la gouvernance ; confirmation de l'auditeur code : code source et sorties enregistrées uniquement, aucun code étudiant exécuté. |
| Non-régression des moteurs | Auditeur code : sept copies de référence avec sorties injectées, sans exécution étudiante, couvrant six moteurs S2 et le contrôle S1 ; scores, détails, maxima et erreurs identiques avant/après métadonnées. Suite couvrant notamment sous-sorties TD2 S1 et fonctions auxiliaires S3. |
| Distribution | Réviseur pédagogique : génération et vérification indépendantes des 32 copies ; chacune égale à la source plus une seule cellule de dépôt fournie, sans sortie enregistrée. Sources inchangées après génération. Gouvernance : `prepare_student_notebooks.py check`, 32 succès. |
| Adresse du serveur | Inspection du générateur : lecture de `TAL_PUBLIC_URL` sans exécuter le fichier `.env`, injection dans les copies hors Git, contrôle des sources incluant sorties ; adresse réelle absente des nouveaux fichiers inspectés. L'adresse reste visible dans les copies distribuées, ce qui est documenté. |
| Remplacement de distribution | Auditeur code : garde par manifeste et refus des fichiers étrangers/liens symboliques examinés et retestés ; génération complète vérifiée avant remplacement. |
| Tests et CI | Auditeur code : 143 tests exécutés indépendamment, aucun échec ni saut ; CI, preuve d'intégrité et fixture examinées sans anomalie bloquante. Gouvernance : journal distinct de l'orchestrateur lu, également 143 tests réussis sans saut. |
| Qualité du diff | Gouvernance : `git diff --check`, succès sans diagnostic. |

## Limites et relais

Docker, Colab et le proxy réel de production sont **NOT_TESTED localement**.
Le workflow prépare un contrôle Docker avec simulation du préfixe de proxy,
mais son résultat GitHub Actions n'était pas observé lors du verdict. Il faut
vérifier ce résultat avant décision de fusion, puis le parcours public lors du
déploiement. Les vérifications locales ne sont pas présentées comme une preuve
de fonctionnement en production.

Le contrôle S1 peut déjà attribuer 36 points pour un maximum déclaré de 35 :
cette dette préexistante est reproduite par les essais comparatifs et documentée.
Elle n'est ni corrigée ni approuvée par ce verdict. Un arbitrage séparé de
l'enseignant est nécessaire avant modification de ce barème. De même, les quatre
sujets dépourvus de cellule d'identification — TD5 S2 et R0–R2 S3 — restent
inchangés ; l'identification technique du sujet ne crée pas une identité étudiante.

Les modifications de CI et de tests ont été produites par l'intégration : le
statut de relais est **MAINTAINER_REVIEW**, jamais `READY_TO_MERGE`. Aucun veto de
gouvernance sur cette migration. À la date de cet audit, l'orchestrateur signale
la création de la branche distante dédiée ; le lot audité n'est pas encore
committé. Aucune fusion ni aucun déploiement n'est effectué. La fusion et la production restent sous décision
du mainteneur ; le déploiement compatible doit précéder la distribution des
nouveaux supports. Toute modification substantielle ultérieure du lot nécessite
la réévaluation des preuves concernées.
