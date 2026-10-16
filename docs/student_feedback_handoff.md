# Restitution étudiante S1/S3 — livraison et vérifications

Mission : `code/rapports-pedagogiques-s1-s3`, base `c81c38641ecddb66c5ea65c78eafbd2d8d3cbbc5`.

## Problème et résultat

Les anciens rapports pouvaient remplacer la réponse étudiante par un verdict (« validé ») ou par un diagnostic d'absence de sortie, et appeler « solution » une description du validateur. Le rapport des TD actifs S1/S3 montre désormais séparément le code retrouvé, ses sorties sauvegardées (erreurs comprises), leur position dans le notebook, le diagnostic, une action et un exemple de résolution à afficher à la demande. Les explications et essais non notés sont conservés dans un complément repliable. Le total est un score formatif provisoire.

Le périmètre actuel est de 19 correcteurs, 116 questions : 7 TD et 45 questions S1 ; 12 TD/révisions et 71 questions S3. Les sujets, marqueurs, versions, règles de validation, tolérances, barèmes et instructions des tuteurs sont inchangés. Les contrôles continuent à retourner seulement un reçu public ; aucun exemple n'y est dévoilé.

## Fichiers et schéma de restitution

- `app/report_evidence.py` extrait les cellules `answer` liées explicitement à chaque question, sans exécution du code soumis. Les sources et sorties textuelles sont reproduites ; les sorties HTML/SVG ne sont pas rendues. Les affichages riches restent signalés dans le complément.
- `app/s1_feedback.py` et `app/s3_feedback.py` contiennent les exemples applicatifs de confiance et leurs explications ; ils n'utilisent jamais un contenu soumis comme programme à exécuter.
- `s1_revision.py`, `app_correction_TD2_S1.py`, `s3_audit.py` et `revision_s3.py` enrichissent les résultats des TD. L'enrichissement S3 reste hors de `grade_traces`, partagé avec les contrôles.
- Le template formatif consomme `student_code`, `student_output`, `answer_cells`, `diagnostic`, `action`, `solution_code` et `solution_explanation`. Les consommateurs des champs historiques restent compatibles. Le S2 conserve sa présentation de repli ; ses exemples complets constituent le lot suivant du plan.

Les contenus soumis restent échappés par Jinja. Les numéros de cellules commencent à 1 dans la copie, indépendamment de leur position dans le sujet. Les sorties manquantes, mal formées ou répétées restent visibles sans devenir des preuves valides. Une source préremplie peut être présente sans avoir été écrite par l'étudiant. Le correcteur ne certifie ni l'auteur ni l'actualité des sorties sauvegardées.

## Plan et exemples consultables

Le [plan complet](pedagogy/plan_restitution_etudiante_s1_s3.md) donne les priorités, l'inventaire par question, la matrice de couverture, les critères d'acceptation et le déploiement. Les anciens HTML transmis ne permettent pas de reconstruire les notebooks absents.

Deux [exemples synthétiques](examples/README.md) permettent de consulter la nouvelle présentation : succès TD1 S1 et sortie inexploitable TD1.a S3. Ils se régénèrent sans exécuter de code étudiant :

```bash
python tests/render_feedback_examples.py --output-dir /tmp/tal-feedback
```

## Compatibilité des PR S1 en attente

Les PR #31 et #32 restent ouvertes et ne sont pas fusionnées par cette mission. Leurs douze nouveaux TD one/bis/ter ajoutent 72 questions hors du catalogue de `main` utilisé ici. Une simulation dans des copies temporaires a vérifié les 12 identifiants : preuves structurées présentes, notes vierges inchangées 0/6, aucun exemple historique appliqué à tort. Les 7 tests de l'expansion S1 et les 6 tests supplémentaires TD4 passent après résolution du conflit.

Un conflit textuel est attendu dans `app/s1_revision.py` à l'intégration : conserver les deux lignes suivantes, ainsi que les imports correspondants :

```python
enrich_s1_details(notebook, evaluator, details)
optional_review = evaluator in STRICT_S1
```

Ordre possible : #31, #32, puis cette PR ; même résolution si celle-ci entre avant #31. Les exemples spécifiques des 72 nouvelles questions restent à produire et à relire sur leurs sujets stabilisés. Cette vérification de compatibilité ne vaut pas une validation pédagogique de ces nouvelles restitutions.

## Validation et limites

Les résultats finaux, revues et verdicts sont consignés ci-dessous pour le lot stabilisé. **334 tests de régression réussis**, compilation et vérification des espaces du diff réussies ; instructions des tuteurs vérifiées et distribution de 34 sujets générée puis vérifiée avec une adresse neutre. Les vérifications sont distinguées de la mise en production, qui reste une décision du mainteneur.

- Le test `test_feedback_routes.py` réalise 38 dépôts réels : chacun des 19 correcteurs via `/submit` et sa route dédiée, sous `/universite/tal`. Il contrôle le code, la sortie et l'erreur affichés, leur échappement HTML et leur présence dans le rapport sauvegardé ; copie et CSV sont conservés.
- Les 45 exemples S1 sont compilés et exécutés comme code applicatif de confiance dans des répertoires temporaires ; leurs sorties alimentent des copies synthétiques, acceptées aux scores maximaux par les correcteurs existants.
- La revue pédagogique indépendante a compilé les 71 exemples S3 et exécuté 44 exemples ne nécessitant pas les modèles spaCy : TD0, R0, cinq questions TD3 et TD4–TD7. Les 27 autres ont été relus statiquement ; les pipelines spaCy fixés ne sont pas exécutés ici. Les références linguistiques des validateurs existants restent inchangées.
- Les tests de protection des contrôles, de navigation, de proxy, de persistance et de compatibilité des sources sont conservés. Les instructions des tuteurs et la distribution sont vérifiées avec une adresse neutre.
- La QA dans un navigateur interactif n'est pas effectuée : le téléchargement Chromium a retourné une archive vide. La structure des HTML rendus, l'échappement et les mécanismes d'affichage sont vérifiés par tests et lecture. Docker n'est pas disponible localement ; son test existant reste prévu dans la CI.
- Aucun ancien rapport archivé n'est régénéré ; il faut une nouvelle soumission ou le notebook original. Aucun sujet n'est redistribué pour ce seul changement de présentation.

L'intégration est auto-produite : le verdict d'intégration sera `MAINTAINER_REVIEW`, jamais une autorisation de fusion ou de déploiement.

## Revues indépendantes reçues

- **TAL-Code-Auditor : ACCEPT.** Extraction et rendu, compatibilité du tuple et des champs historiques, collecte des erreurs, contrôle des 19 évaluateurs/116 exemples, préservation des barèmes et confidentialité des contrôles. Le cas de traceback mal formé `[None]`, initialement identifié comme TAL-AUD-001, est corrigé et retesté via les routes réelles : HTTP 200, valeur signalée et rapport sauvegardé.
- **TAL-Pedagogy-Reviewer : ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE.** Les 116 questions et leurs exemples sont confrontés aux 19 sujets actifs et à la matrice du plan. Les remarques TAL-PED-001 à 006 sont corrigées : filtrage des lignes vides et noms de variables S1 ; boucles/fonctions TD0 S3 ; signatures, Counter et filtres TD2 ; affichage des figures ; essais contrastés TD1.c. Les réponses personnelles restent des exemples à adapter et les transferts non notés restent explicités. Vérification indépendante : 116 exemples compilés et 89 exécutés, avec la limite des 27 exemples spaCy non exécutés.
- **TAL-Editorial-Reviewer : ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE.** La [revue éditoriale](../reports/editorial/rapports-s1-s3.md) donne les passages et repères relus par question. Son auteur a rédigé le plan sous rôle Prof puis relu exclusivement les textes produits par les autres agents ; il exclut son propre plan de son verdict.
- **TAL-Governance-Auditor : CONFORME.** Le [rapport de gouvernance](../reports/governance/rapports-s1-s3.md) consigne la conformité et ses preuves. Les rôles de revue n'ont modifié aucun produit audité ; aucune règle normative n'a été modifiée pour lever une objection.

Le producteur ne prononce pas sa propre validation. Les comptes rendus ci-dessus enregistrent les verdicts reçus des reviewers ; ils ne les remplacent pas.
