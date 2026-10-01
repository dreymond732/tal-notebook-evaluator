# Gouvernance — Revue de progression des TD du S3

## Mission et verdict

Revue indépendante du 1er octobre 2026, branche `pedagogy/s3-progression-review`, référence `933b0df6565fbd7d64f02db941eda5e8358eb16e`, après fusion des PR 19 et 20. L’enseignant demande de transposer la revue S1 au S3, sans réduire les supports déjà étayés.

**Verdict : CONFORME**, pour le périmètre et les preuves ci-dessous. Les critères statiques de certaines révisions et la collecte des productions à relire évoluent : le flux mixte de **CHANGEMENT_DE_CONTRAT** a été appliqué, avec double revue indépendante, même si la version de notebook reste 2. Les onze noms de fichiers, les identifiants évaluateurs, les 67 questions, leurs marqueurs et barèmes restent stables. Les sept contrôles S3 ne sont pas modifiés.

## Séparation des responsabilités

| Rôle | Production ou contrôle | Résultat |
|---|---|---|
| TAL-Prof (`s3review_prof`) | Matrice préalable, spécification et périmètres du tuteur dans `docs/pedagogy/` | Validation de la matrice par l’orchestrateur avant conception ; aucune réduction autorisée |
| TAL-Pedagogy-Designer (`s3review_designer_early`, `s3review_designer_late`) | Onze notebooks, métadonnées, restitution et bilans pédagogiques | Production soumise à revue indépendante |
| TAL-Code-Architect (`s3review_architect`, orchestrateur pour la distribution) | Révisions, collecte des preuves, critères de présence de textes, tests techniques ; contrôle de la cellule canonique S3 et instructions techniques de distribution | Production soumise à revue indépendante |
| TAL-Code-Auditor (`s1v2_governance`, rôle affecté à cette seule revue S3) | Revue technique et sondes indépendantes, produit en lecture seule | ACCEPT après clôture de quatre constats |
| TAL-Pedagogy-Reviewer (`s3review_pedagogy_audit`) | Comparaison des supports, couverture et progression, produit en lecture seule | ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE |
| TAL-Integration-Master (`s3review_integration`) | Fixture de conservation, tests et documentation technique | Producteur : MAINTAINER_REVIEW, jamais auto-validation READY_TO_MERGE |
| TAL-Governance-Auditor (`s3review_governance`) | Permissions, provenance, contrats et preuves ; présent rapport uniquement | CONFORME |

Le nom de session conservé par l’auditeur code provient d’une mission antérieure ; il n’a produit ni code, ni tests, ni documentation de cette PR S3. Les deux réviseurs et la gouvernance n’ont pas modifié les produits qu’ils valident. La branche est dédiée ; `AGENTS.md`, la matrice des permissions, le contrat normatif et `docs/agents/` restent inchangés. Aucune fusion ni mise en production n’est effectuée.

## Conservation et pédagogie

La matrice `docs/pedagogy/s3_progression_review_coverage.md` précède la conception et a été explicitement validée par l’orchestrateur. La spécification et les bilans `docs/s3_review_early_coverage.md` et `docs/s3_review_late_coverage.md` explicitent les ajouts, les prérequis et l’autonomie conservée. Aucun arbitrage de réduction n’est nécessaire : aucune activité n’est supprimée, externalisée ou rendue optionnelle.

La gouvernance a comparé les onze objets de `tests/fixtures/s3_progression_review_source_baseline.json` aux notebooks obtenus par `git show` au commit parent : ils sont identiques. Les sept empreintes de contrôles correspondent aux fichiers du parent et aux fichiers actuels, identiques octet pour octet. La fixture historique de migration reste figée ; la nouvelle preuve est reliée à cette référence, sans effacement des garanties précédentes.

La revue pédagogique indépendante confirme **263 cellules originales** avec les mêmes identifiants et le même ordre, **252 sources hors tuteur identiques**, les **67 réponses et cellules d’identité strictement inchangées**, et les racines v2 conservées. Les 32 repères ciblés utilisent des exemples distincts, avant la notion mobilisée. Ils renforcent le parcours Python, annotations, fréquences, passages, cooccurrences, dénominateurs, visualisations et audit de Faguet. Les figures, interprétations, tests personnels et transferts restent à produire par l’étudiant.

La réserve `TAL-PED-S3-001` a été clôturée : `None` et le taux indéfini figurent désormais dans les périmètres fermés TD6 Q2/Q3, alignés avec les repères du sujet. La synchronisation finale des 34 profils est vérifiée. Les instructions du tuteur restent en première cellule et en métadonnées ; les contrôles gardent leur interdiction d’assistance. Aucune nouvelle bibliothèque n’est introduite.

Les huit TD conservent une planification de 120 minutes et les révisions R0–R2 leurs formats de 25, 25 et 30 minutes. **Ces durées sont des hypothèses de conception, non des temps mesurés.** TD7 suppose les fonctions antérieures et l’environnement prêts. Cette limite ne justifie aucune réduction des activités existantes.

## Contrat technique et sécurité

- Les contrats restent en v2, avec identité littérale comprenant nom, prénom, classe et numéro étudiant. Les anciennes versions restent refusées par « mauvaise version du notebook » avant correction et persistance. Une copie v2 antérieure reste compatible ; elle n’acquiert pas les nouveaux appuis par simple dépôt.
- Les cellules sont classées selon leur fonction. Les entraînements, exemples, préparations et restitutions ne peuvent fournir la réponse notée. Les 28 anciennes cellules d’interprétation TD4–TD7 et la reprise personnelle TD7 restent rattachées à une question pour la relecture humaine, sans attribution de points.
- Les révisions acceptent des constructions autonomes R1/R2 sans échec en cascade depuis Q1, ainsi que des variantes valides d’exclusion. Les contrôles statiques refusent les sélections POS inversées et le code placé après un retour inconditionnel utilisé comme preuve. La collecte du rapport supporte les sorties malformées sans transformer leur diagnostic local en erreur globale.
- Les champs rédigés manquants sont signalés sans prétendre noter leur qualité. Le filtrage retirant tous les noms peut être observé en TD2 Q3 ; la réalisation de figures Q6 exige la reprise du filtre et des données, conformément au sujet conservé.
- Le serveur analyse uniquement sources et sorties enregistrées ; il n’exécute aucun code étudiant. La gouvernance a vérifié que les onze sources ne contiennent ni exécution ni sortie préremplie. Les sondes des réviseurs utilisent des traces synthétiques, sans exécution de notebook étudiant.
- Les onze sources se terminent par la cellule HTML canonique contenant uniquement `__TAL_PUBLIC_URL__`, sans adresse de dépôt réelle. Le déploiement remplace cette cellule dans la copie distribuée ; il ne modifie pas la source et ne crée pas de doublon. Les vérifications utilisent une URL neutre.

L’auditeur code a clôturé ses quatre constats `TAL-AUD-S3-001` à `TAL-AUD-S3-004` après sondes indépendantes : exclusions, autonomie des réponses R1, direction des filtres POS et conservation des observations dans le rapport. Les vrais gabarits R0–R2 complétés par des fixtures conformes obtiennent 4/4, avec observations visibles. Son verdict final est **ACCEPT**.

Les limites demeurent explicites : l’analyse statique ne reconnaît pas tout Python valide, n’authentifie pas les traces et ne démontre pas la généralité des fonctions. Les scores sont techniques et provisoires ; la pertinence des figures, interprétations et jugements linguistiques nécessite une relecture humaine. La cohérence des règles du tuteur ne prouve pas l’obéissance du service Colab.

## Gates et relais

| Vérification | Preuve |
|---|---|
| Suite complète après corrections techniques | **254 tests PASS**, sans saut ; exécutée par l’intégration et indépendamment par l’auditeur code, puis relancée par l’orchestrateur après toutes les mutations (4,219 s) |
| Compilation de `app` et `tests`, `git diff --check` | PASS |
| Tuteurs synchronisés après l’ajustement TD6 | **34/34 PASS** |
| Conservation et distribution ciblées | **5 tests PASS**, revue pédagogique indépendante |
| Régressions S3 ciblées | **13 tests PASS**, revue pédagogique indépendante |
| Vérification des sources | **33/33 PASS** |
| Génération et vérification de la distribution | **33/33 PASS**, également vérifiées indépendamment par l’auditeur code avec empreintes des sources inchangées |
| Santé et proxy | `/health` : 33 évaluateurs ; formulaires `/` et `/submit` sous `X-Forwarded-Prefix: /universite/tal` : PASS |
| Contrôles S3 | **7/7 identiques octet pour octet**, comparaison indépendante de gouvernance |

**Docker local : NOT_TESTED. CI distante : à clôturer après publication sur le commit exact de la PR.** La réussite distante, dont le build et le contrôle de santé Docker, doit être consignée dans le relais de PR avant fusion ; elle n’est pas présumée par ce rapport.

L’intégration reste **MAINTAINER_REVIEW**, puisqu’elle produit des tests et la documentation. Le mainteneur décide de la fusion et du déploiement. Après fusion et `bash deploy.sh`, redistribuer les onze notebooks S3 depuis `dist/Notebooks TD/S3/` pour diffuser les appuis et la restitution HTML. Les copies v2 antérieures restent évaluables ; les copies v1 demeurent refusées.
