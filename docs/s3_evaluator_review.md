# Revue technique des onze TD et révisions S3

Branche : `pedagogy/s3-progression-review`, base `933b0df6565fbd7d64f02db941eda5e8358eb16e`.

Cette revue conserve les onze contrats v2, les 67 questions, leurs traces et leurs barèmes : R0–R2 sur 4 points chacun, TD1 sur 6 et les sept autres TD sur 7. Aucun code soumis n’est exécuté. La qualité des analyses, figures et interprétations reste soumise à relecture humaine.

## Vérifications par groupe

| Évaluateurs | Ce qui est vérifié | Limite maintenue |
|---|---|---|
| R0 | Calcul lié à la sortie, valeurs et types enregistrés, cas vide et essais | Analyse statique partielle, sans authentification des sorties |
| R1–R2 | Annotations et comptes de référence, catégories filtrées, exclusions, variantes de boucles | Référence du pipeline fixé, pas vérité linguistique |
| TD0 | Texte fixe, comptages, découpage et fréquences exacts | Interprétation des limites relue |
| TD1–TD2 | spaCy 3.8.7 / fr_core_news_sm 3.8.0, positions et annotations, fréquences, cohérence des figures | Extraits libres, pertinence des figures et jugements relus |
| TD3 | SHA-256 du corpus original, positions préservant les CRLF, citations exactes et provenance | Lemme proposé et interprétation des citations relus |
| TD4–TD7 | Microcas quantitatifs déterministes : unité, marges, union, dénominateurs, segments, protocoles | Transferts au corpus et rapport d’audit relus, sans score automatique de qualité |

Pour les onze supports : version antérieure refusée, identité complète requise, cellules `answer` seules habilitées à fournir une trace de correction. Les cellules `practice`, `provided` et `example` ne peuvent fournir le crédit d’une autre cellule. Les consignes et la restitution HTML ne contribuent pas au score.

## Corrections et preuves

1. **R0, code mort après retour.** Une fonction `return 15` suivie d’un `return len(texte.split())` pouvait donner un point avec les sorties attendues. L’analyse retient désormais le premier retour inconditionnel. Le cas inverse conserve son point : un retour mort ultérieur n’invalide pas le calcul réellement retourné.
2. **R1–R2, dépendances inutiles.** R2 Q2 qui analyse elle-même `texte` ne dépend plus d’une fonction réussie en Q1. R1 Q2–Q4 peuvent également reconstruire localement `doc = nlp(texte)`. La dépendance reste nécessaire lorsque le document n’est défini ni dans la réponse ni dans Q1.
3. **R2, filtres équivalents.** Les comparaisons à `False`, les inégalités à `True` et les gardes `continue` sont acceptées. Un garde sur un autre objet ou sur `token.text` ne remplace pas l’exclusion du lemme. Cette tolérance n’autorise pas le tuteur à introduire des notions absentes de son périmètre.
4. **R1–R2, sens du filtre POS.** La présence de `pos_` et du mot `NOUN` ou `VERB` ne suffit plus : une sélection `!=` qui inverse la consigne est refusée, même accompagnée d’anciennes traces correctes. L’égalité miroir, la négation de l’inégalité et le garde d’exclusion restent admis. Il s’agit d’une vérification de formes syntaxiques définies, pas d’une preuve de correction de tout programme Python.
5. **R0–R2, rapport enseignant.** La collecte bornée `review_evidence` inclut désormais toutes les réponses et les essais explicitement rattachés par `tal_review`, dont les observations de Q2. Le texte est échappé ; les sorties HTML/SVG ne sont pas exécutées. Une sortie mal formée reste une anomalie locale de réponse et ne fait pas échouer le collecteur du rapport.
6. **TD1–TD3, présence des rédactions.** Les champs argumentatifs vides sont signalés séparément, sans attribuer ni retirer le point technique au titre de leur qualité.
7. **TD2 Q6, filtre vide.** Après avis du Prof, le besoin de données non vides est conservé : le sujet demande de réadapter le filtre pour construire deux figures. Le retour indique explicitement de reprendre Q3 puis Q6. Le dictionnaire vide en Q3 reste un essai techniquement valide ; Q6 est non vérifiable tant que sa dépendance reste vide.

`tests/test_s3_review_regressions.py` comporte treize tests nouveaux, reposant sur des sources et traces inertes. Les huit suites S3 ciblées totalisent **102 tests réussis** lors du handoff Architecte, y compris les contrôles qui utilisent le collecteur partagé. La validation globale, les revues indépendantes et la CI sont consignées dans les rapports d’intégration et de gouvernance de la PR.

## Handoff à la revue indépendante

Fichiers produits : `app/revision_s3.py`, `app/s3_review.py`, `app/app_correction_TD1_S3.py`, `app/app_correction_TD2_S3.py`, `app/app_correction_TD3_S3.py`, `tests/test_s3_review_regressions.py` et ce document. Les sujets, tuteurs, règles de distribution et fichiers normatifs ne sont pas modifiés par l’Architecte.

Critères d’acceptation : faux positifs/faux négatifs reproduits puis corrigés ; maintien des contrats v2 et barèmes ; absence d’exécution de code soumis ; reprise des révisions dans le rapport enseignant ; absence de régression des contrôles ; validation indépendante des constats TAL-AUD-S3-001 à 004.
