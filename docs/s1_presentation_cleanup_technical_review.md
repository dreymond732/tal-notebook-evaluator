# Nettoyage de présentation S1 — revue technique indépendante

## Handoff et verdict

Mission : contrôle technique indépendant du nettoyage des sept TD S1 demandé le 15 octobre 2026. Rôle : TAL-Code-Auditor. Branche `pedagogy/s1-nettoyage-presentation`, source de comparaison `590b9a6c78fc6b27f8985e060c6ea2325367f652`. Le Designer a modifié les supports ; l'intégration a adapté le périmètre d'un test historique. L'auditeur n'a modifié aucun notebook, test, module, document suivi ou règle : seule cette sortie `/tmp/s1-cleanup-code-review.md` est produite par lui.

**Verdict : ACCEPT sur le nettoyage de présentation et l'adaptation du test, au périmètre et aux empreintes ci-dessous.** Aucun TAL-AUD nouveau dans ce diff. Ce verdict ne clôt aucun constat de l'audit S1 précédent et ne remplace pas les verdicts pédagogique, éditorial, gouvernance ou mainteneur.

Sources normatives et cadrage lus : AGENTS.md, fiche TAL-Code-Auditor, matrice de permissions et workflow déjà lus pour l'audit S1, matrice préalable `docs/pedagogy/s1_presentation_cleanup_coverage.md` acceptée par un reviewer distinct avant conception. Inspection directe de `tests/test_presentation_order.py`, `tests/test_s1_progression_preservation.py`, helper historique et liste explicite S1_RENAMED_SUBJECTS.

## Fichiers et invariants confrontés indépendamment

Les sept fichiers sont `Notebooks TD/S1/TD1_S1_variables_types.ipynb`, `TD2_S1_chaines_sequences.ipynb`, `TD3_S1_collections.ipynb`, `TD4_S1_boucles_conditions_comptages.ipynb`, `TD5_S1_fonctions_reutilisation.ipynb`, `TD6_S1_fichiers_csv.ipynb`, `TD7_S1_expressions_regulieres_pipeline.ipynb`. Le seul test modifié est `tests/test_presentation_order.py`.

Comparaison JSON exhaustive avec chaque blob du commit `590b9a6`, sans exécution d'aucune cellule :

- 293 cellules conservées, mêmes identifiants, ordre, types et tous champs hors source strictement identiques ; objets racines hors cellules identiques, métadonnées et profils inclus.
- 157 cellules de code : AST identiques. Les sources de 156 cellules sont exactement conservées ; la seule différence de code concerne le retrait exact du commentaire `# Complétez les informations entre les guillemets.` au TD2, cellule 4 en base 1. Les quatre affectations et le commentaire du rappel TD1 restent identiques.
- Les 45 cellules réponses sont exactement conservées, sources comprises : 6+7+6+7+6+6+7. Marqueurs principaux et complémentaires, affichages commentés, variables et données inchangés.
- 44 exemples, 52 cellules d'essai/vérification/synthèse, deux préparations et sept restitutions conservent leurs sources exactes. Tous les outputs et execution_count sont identiques, sans génération de sorties.
- La première cellule et les deux contextes du tuteur restent identiques dans chaque notebook. La nouvelle présentation visible de Gemini est ajoutée seulement dans l'introduction TD1 ; aucun élargissement caché de profil, concept ou bibliothèque.
- Les seules sources modifiées sont dans les cellules autorisées par la matrice : 44 Markdown et le commentaire de code TD2. Toute cellule non autorisée a été comparée intégralement et reste identique.

Cellules sources modifiées, indices en base 1 :

| TD | Cellules |
|---|---|
| TD1 | 3, 5, 7, 12, 17, 22, 27, 32, 37 |
| TD2 | 2, 3, 4, 5, 6, 10, 14, 18, 22, 26, 30, 32 |
| TD3 | 3, 5, 7, 12, 17, 23, 28, 33, 38 |
| TD4 | 5, 7, 12, 17, 22, 27, 32, 37, 42 |
| TD5 | 5, 43 |
| TD6 | 5, 40 |
| TD7 | 5, 47 |

Lecture de l'intégralité des différences source par cellule : retraits limités aux budgets/minutages, notices d'identification et procédure générale répétée ; regroupement de cette procédure et présentation Gemini au TD1. Les contenus locaux et les synthèses gardent leurs données, questions et critères. La conformité pédagogique/éditoriale de ces textes exige les deux avis spécialisés distincts.

Aucun diff dans `app/`, `tests/fixtures/`, `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md` ou `docs/agents/`. Aucun correcteur, barème, référence, route, template ou schéma de persistance changé. Aucun contrat modifié par le seul retrait du commentaire d'identité : le chemin strict d'identification v2 est couvert par les tests sur le sujet réel.

## Adaptation du test historique

L'ancien test `test_outside_s3_td_only_title_moves_no_field_or_prose_changes` rétablissait le déplacement du titre puis exigeait une égalité de toute la prose S1 au snapshot du commit `1ee4581`. Cette condition était adaptée au précédent lot de présentation S3, et incompatible avec le nettoyage S1 désormais explicitement autorisé.

L'intégration le renomme `test_unrevised_subjects_only_move_title_without_other_changes`. Elle conserve l'exclusion S3 précédente et ajoute uniquement l'appartenance à `set(S1_RENAMED_SUBJECTS.values())` : les sept chemins exacts des TD S1, liste déjà vérifiée par les tests existants. Aucune exclusion générique S1, aucun remplacement de fixture, aucune suppression des assertions restantes.

Périmètre vérifié depuis le snapshot : 35 supports moins 12 TD S3 déjà hors comparaison stricte moins sept TD S1 revus, soit **16 supports restant soumis à l'égalité stricte historique**. L'autre test global continue à contrôler les 35 titres/contextes, métadonnées de cellules, IDs et ordre, AST du code, sorties et périmètres cachés du tuteur. `test_s1_progression_preservation` protège toujours les 45 questions et les affichages commentés. La preuve JSON directe contre `590b9a6` limite le nettoyage courant plus fortement que l'AST seul.

Le journal initial de l'intégration `/tmp/s1-cleanup-presentation-initial.log` montre sept échecs, tous dans l'ancien sous-test strict et correspondant aux sept TD S1. Après adaptation, les assertions restantes réussissent. Ce changement de périmètre du test accompagne une modification de prose autorisée ; il ne déclare pas l'équivalence pédagogique par test et ne contourne pas un échec du contrat d'évaluation.

## Tests et preuves

L'auditeur a exécuté indépendamment les modules existants suivants via unittest :

```python
modules = [
    'test_presentation_order',
    'test_s1_progression_preservation',
    'test_td2_s1',
    'test_s1_v2_results',
]
```

**38 tests exécutés, 38 PASS**, en Python `.venv` ; aucun nouveau test ajouté. Ces contrôles vérifient le périmètre du test adapté, les invariants historiques, les 45 questions, les résultats des wrappers S1 sur les sujets réels et les variantes statiques autorisées. Pour TD2, ils couvrent notamment l'identification extraite de la cellule réelle, le tuple à cinq éléments, le plafond 7, les erreurs, la non-exécution et GET/POST avec persistance. Les six autres modules S1 passent leurs cas positifs end-to-end dans les sujets réels et conservent leurs plafonds 6/6/7/6/6/7.

L'auditeur a également lu `/tmp/s1-cleanup-full-tests.log` : l'intégration y rapporte **302 tests PASS**, sans erreur ni échec. Les 38 tests sont une réexécution ciblée d'une partie de cette suite, et non 38 tests supplémentaires distincts. Le tuteur 35 profils, distribution check/render/verify 34 supports et compile ont été rapportés PASS par l'intégration ; ils n'ont pas été relancés par cet auditeur. Aucune exécution de notebook corrigé ou étudiant.

## Empreintes des fichiers relus

SHA-256 :

| Fichier | Empreinte |
|---|---|
| TD1_S1_variables_types.ipynb | 94abfa27d9b6a21395f60c91f0b8ca149cfcf20b5248799df0feec6f0aa338c3 |
| TD2_S1_chaines_sequences.ipynb | 5d5e0ecc6650e07acf4a4b1695963802cbad3298df41053976d2d30d0636eed3 |
| TD3_S1_collections.ipynb | 822aeab68461784d9fa0e410ae18a37bb295486aecb46657e1bce0981c7944e8 |
| TD4_S1_boucles_conditions_comptages.ipynb | fc82a243ba0c09d1a7d1a89203885c78381ccf323a2a3a8c0d93d991b18a0e51 |
| TD5_S1_fonctions_reutilisation.ipynb | 2e2dbc49943a2070b8ad7c155c377a2e30fe8db0fa58e5fd09f70d9c8668b3cf |
| TD6_S1_fichiers_csv.ipynb | 01e00fff36a012f091097794d1d62b0f9255976fc61a8299366238b131b165d8 |
| TD7_S1_expressions_regulieres_pipeline.ipynb | b7ff9f64672c0886543a27a5079638f79f8eab4127553d2c1b2b7aaab4489f79 |
| tests/test_presentation_order.py | 4ccdb25263712e689d9bf7fab8dfdec5205f1718bb919ed99a6be118d2bd1f50 |

## Limites et relais

Les anomalies de contrôle final, le faux positif DM, les corrigés absents et le modèle TD2 historique incompatibles restent hors scope et non résolus. Le verdict NON_CONFORME antérieur sur l'ensemble S1 n'est pas levé. Aucune nouvelle recherche de défaut sans rapport ni nouvelle suite élargie n'a été effectuée après les preuves ciblées nécessaires.

La fraîcheur/authenticité de sorties futures, la compréhension des étudiants, le comportement effectif Colab/Gemini, l'exécution humaine des corrigés et Docker/production restent non certifiés. Aucun merge, switch de branche ou commit réalisé par cet auditeur.

Conditions techniques remplies pour ce lot : liste exacte des sept TD, aucune perte d'activité technique, absence de changement de contrat, invariants JSON/code/tuteur conservés, test historique adapté uniquement à la prose autorisée, contrôles pertinents PASS. Relais demandé à la gouvernance avec les avis pédagogique et éditorial indépendants ; l'intégration ayant produit le test et la synthèse, la décision finale relève du mainteneur sous MAINTAINER_REVIEW.
