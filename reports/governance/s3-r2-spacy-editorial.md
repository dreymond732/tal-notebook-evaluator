# Gouvernance — pilotes éditoriaux R2, TD1 et TD1B S3

## Mission et périmètre

Audit indépendant du 3 octobre 2026, rôle `TAL-Governance-Auditor`, agent `pilot_governance`. Branche : `pedagogy/s3-r2-spacy-editorial`, base `553f3ada02c8ed93f1e04332a1c42ada5327eaa3`. Le présent rôle écrit uniquement ce rapport ; il n'a modifié ni les supports, ni le code, ni les tests, ni les règles auditées.

Le mandat initial de l'enseignant est de reprendre R2 et l'introduction à spaCy après fusion des règles éditoriales. L'arbitrage complémentaire explicite, relayé par le responsable et inscrit dans le cadrage, retient **deux TD de deux heures** : TD1 conservé et renforcé, puis TD1B consacré aux activités historiques manquantes, placé avant TD2 sans renumérotation générale. R2 reste une consolidation annoncée de 30 minutes. Ces durées sont des hypothèses de séance, non des mesures en classe.

Les règles lues sont `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et la fiche du Governance-Auditor. Aucun de ces actifs normatifs n'est modifié dans ce lot. La branche dédiée n'est pas `main` ; aucune fusion ni mise en production n'est effectuée par cet audit.

## Auteurs, permissions et indépendance

| Production ou contrôle | Responsable déclaré dans le handoff | Preuve / séparation |
|---|---|---|
| Cadrage, matrice, profils tuteur, inventaire | `pilot_prof`, TAL-Prof | `docs/pedagogy/s3_r2_spacy_editorial_coverage.md`, manifeste et inventaire ; validation préalable indépendante consignée avant conception |
| Réécriture R2 | `pilot_r2_designer` | Notebook R2 ; corrections rédactionnelles ciblées intégrées ensuite par `/root` en rôle Designer |
| Réécriture TD1 et README S3 | `/root`, rôle Designer | Notebook TD1 et README ; aucune auto-attribution de verdict pédagogique ou éditorial |
| TD compagnon | `pilot_companion_designer` | TD1B livré ; corrections lexicales ciblées intégrées par le responsable |
| Réception humaine, contrats, tests et documentation technique | `pilot_architect`, Code-Architect | Modification de contrat déclarée ; revue par un autre agent |
| Lecture comme étudiant | `pilot_student_reader`, Étudiant-Modèle | `Corrigés modèles/TD/s3-spacy-editorial/lecture_etudiante.md` ; questions lues sans accès aux correcteurs ou tests, sans exécution |
| Revue pédagogique | `pilot_pedagogy_review` | Indépendant des producteurs ; verdict final et preuves par question transmis dans le handoff |
| Revue éditoriale | `pilot_editorial_review` | `reports/editorial/s3-r2-spacy.md` ; lecture exhaustive et empreintes finales |
| Revue technique | `pilot_contract_audit` | Indépendant de l'Architecte ; verdict spécialisé transmis dans le handoff |
| Génération, essais des exemples fournis, intégration | `/root` | Ne peut rendre `READY_TO_MERGE` sur sa propre production : état d'intégration attendu `MAINTAINER_REVIEW` |

Le retour Étudiant-Modèle conserve ses limites : il ne remplace ni une classe novice réelle, ni la revue technique, ni les deux verdicts spécialisés. Sa seconde lecture ciblée lève le blocage syntaxique et les difficultés lexicales signalés, tout en conservant les hésitations non bloquantes sur TD1 Q1, Q4 et Q6.

## Conservation et destinataire

La matrice compare la version technique de départ et l'initiation spaCy historique fournie par l'enseignant, identifiée par son empreinte. Pour R2, aucune autre référence historique autonome n'est disponible ; le dossier ne prétend pas en restaurer une. Le cadrage indique sa validation préalable indépendante par `pilot_pedagogy_review`, avant les réécritures R2/TD1 puis avant TD1B.

Les quatre activités R2 et les six questions TD1, avec leur manipulation, leurs interprétations et l'autonomie finale de TD1 Q6, sont conservées. Les entités nommées, l'extraction PER/ORG, la similarité de mots **et** de phrases et les règles Toulon/EntityRuler, précédemment annoncées ailleurs sans support livré, disposent maintenant de quatre activités dans TD1B. Les règles choisies et les essais de stabilité/ambiguïté ne sont pas rendus facultatifs. La matrice générale S3 et l'inventaire sont corrigés pour ne plus présenter une promesse de prolongement comme une activité couverte.

Le réviseur pédagogique rend **`ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`**, pour 96 cellules et 14 questions, aux trois empreintes ci-dessous. Le réviseur éditorial rend séparément **`ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE`**, après lecture des mêmes cellules, commentaires de code et activités hors question. Il distingue cours, exemples exécutables sur d'autres données, tâches et productions attendues ; les constats bloquants sont levés avant verdict.

Tous les passages pédagogiques visibles ont l'étudiant pour destinataire. Ces trois TD ne bénéficient pas de l'exception réservée aux corrigés de DM. Les justifications de préparation/maintenance sont dans la documentation technique. Le commentaire de tête de restitution « URL injectée lors du déploiement » est conservé parce qu'il appartient au format explicitement fourni par l'enseignant ; il n'est pas utilisé comme texte de cours. Les contextes cachés du tuteur restent des instructions machine, distinctes des explications étudiantes.

## Contrats, tutorat et distribution

Le nouveau circuit de réception TD1B est déclaré **`CHANGEMENT_DE_CONTRAT`** dans `docs/human_review_submission.md` et suit le flux mixte. Il ne fabrique ni note ni évaluateur : le catalogue serveur réserve `assessment: human_review`, `evaluator: null` à ce sujet. Les 33 correcteurs automatiques existants gardent leurs barèmes et contrats. Le dépôt reçu conserve le notebook original, un rapport échappé et un journal sans score ; une erreur d'écriture n'est pas un succès. Aucun code étudiant n'est exécuté, aucun HTML/SVG soumis n'est rendu dans le rapport. Les limites de transaction et de concurrence du stockage sont explicitement documentées.

Vérifications directes de gouvernance : **35 entrées au catalogue, 34 supports actifs, 33 correcteurs automatiques et un dépôt humain ; 45 notebooks au total**, dont les 44 chemins antérieurs et le compagnon. Aucun autre support n'est déclaré révisé par ce pilote. Les métadonnées version 2 et les réponses Q1–Q4, Q1–Q6, Q1–Q4 sont présentes ; les deux anciens correcteurs restent associés aux mêmes identifiants.

Chaque source a sa restitution HTML finale avec `__TAL_PUBLIC_URL__`, et son contexte complet identique entre métadonnées Colab et première cellule Markdown cachée. Les profils bornent le guidage aux notions déjà présentées : NER/filtrage avant Q1/Q2 du compagnon, similarité en Q3, règles en Q4 ; les imports de préparation ne deviennent pas des bibliothèques autorisées dans les réponses. Les contrôles et leur refus d'assistance ne sont pas modifiés par ce lot. La duplication du contexte ne garantit pas son respect effectif par Colab.

Les deux sources de la nouvelle référence figée de tests ont été comparées directement avec `git show` à la base : elles sont identiques octet pour octet. Les nouvelles règles de conservation autorisent la reformulation de la prose, mais gardent cellules originales, ordre, identifiants, métadonnées et AST du code. La seule exception exécutable annoncée est l'ajout exact d'`IPython==8.37.0` dans la préparation TD1 identifiée, justifié par un échec observé du rendu displaCy avec IPython 9.17.1, et documenté dans `docs/s3_spacy_runtime.md`. Cette exception ne réécrit pas la référence pour masquer une modification.

## Preuves techniques et limites

- Verdict final indépendant de `pilot_contract_audit` : **`ACCEPT`**. Le Code-Auditor a exécuté 76 tests ciblés, puis les cinq tests de conservation après le pin de compatibilité. Il a vérifié que l'exception AST se limite à cet ajout exact et que la référence reste inchangée. Il a aussi exécuté indépendamment la seule cellule enseignante fournie `td1-exemple-dependances` dans l'environnement annoncé : HTML produit sans `ImportError`. Cette vérification n'exécute aucune réponse étudiante et n'est pas un essai visuel Colab.
- Le responsable rapporte les 35 profils tuteur vérifiés et les 34 distributions générées puis vérifiées avec une URL neutre ; les sources conservent le placeholder. Les trois notebooks passent lecture JSON, nbformat et analyse syntaxique statique.
- Suite finale : `TMPDIR=/var/tmp /tmp/tal-pilot-validation/bin/python -m unittest discover -s tests -v`, **292 tests réussis en 4,864 s**. Le journal local final a été lu par cet audit. Des essais préalables avaient échoué dans des dépôts temporaires sous `/tmp` ; ils ne sont pas transformés rétrospectivement en succès. La réussite citée est celle de la relance finale avec le répertoire temporaire adapté.
- Quinze exemples enseignants fournis — 4 R2, 7 TD1, 4 TD1B — ont été exécutés par l'intégration dans un environnement isolé avec spaCy 3.8.7, modèles français sm/md 3.8.0 et IPython 8.37.0. Le relevé d'exécution a été consulté. Ce sont les exemples du cours, pas des réponses étudiantes ni une résolution des exercices.
- Non vérifiés par ces résultats : session Colab complète, comportement du LLM intégré, temps réellement nécessaire à un novice, distribution sur le serveur de production et apprentissage effectif. La CI du commit publié reste une preuve à joindre à la PR ; le présent rapport ne prédit pas son résultat.

| Support relu | SHA-256 |
|---|---|
| R2 | `a74becd52bbfbc09a7643d4fd3cd5060daa69f9983308641c7d391e9f84b7e34` |
| TD1 | `d8b38f08f425ef46fa1ae420fc15a32e96ac71dd07d2d9a2486dba5ef973e2bb` |
| TD1B | `023abc0989f0a3fb35de7a16780681d63d2b0804f5ca7aea07bbc2d42497bf2b` |

## Clôture

**Verdict : `CONFORME`.** Les trois revues spécialisées indépendantes sont positives, la matrice préalable est présente, les activités historiques déplacées ont une cible effectivement livrée et la lecture Étudiant-Modèle a été clôturée sur les mêmes empreintes, y compris la préparation TD1 ajustée. Aucun blocage de gouvernance n'est constaté dans ce périmètre.

L'intégration ayant participé à la production, son état doit rester **`MAINTAINER_REVIEW`**, et non `READY_TO_MERGE`. Le mainteneur décide de la fusion et de la production. La CI du commit publié reste à joindre à la PR. Les limites Colab, durée réelle et stockage restent explicites ; toute nouvelle modification des passages relus exige une reprise ciblée par les réviseurs concernés. Ce verdict sur trois supports ne valide pas les 42 autres notebooks du périmètre global.
