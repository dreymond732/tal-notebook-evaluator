# Notebooks de TD

Les supports étudiants sont organisés par semestre. Les versions corrigées, lorsqu'elles sont nécessaires, restent séparées des versions distribuées.

## S3 — Fondations Python et TAL

Le dossier `S3/` contient le premier lot du parcours :

- `TD0_S3_diagnostic_texte.ipynb` : diagnostic formatif, du texte brut aux limites de `split()` ;
- `TD1_S3_fondations_spacy.ipynb` : document spaCy, tokens, phrases, lemmes et POS ;
- `TD2_S3_analyse_corpus.ipynb` : fréquences de lemmes, filtrage et fonctions paramétrées ;
- `R0_S3_python_texte.ipynb`, `R1_S3_doc_spacy.ipynb` et `R2_S3_frequences_reutilisables.ipynb` : activités passerelles formatives, respectivement avant TD1, avant TD2 et avant TD2.

La spécification de progression et le contrat des activités passerelles sont dans `docs/pedagogy/S3_TD0_TD2_SPECIFICATION.md`.

## Évaluation formative

Les correcteurs ne lancent jamais le code remis. Les notebooks doivent donc être exécutés avant dépôt et produire les marqueurs indiqués (`Résultat Qx :`). Les correcteurs analysent le JSON, le code source et les sorties enregistrées ; ils fournissent un diagnostic de compétence, pas une validation par exécution sur données cachées.

Complétez la cellule d’identification prévue par chaque sujet. Les notebooks S3 en version 2 demandent nom, prénom, classe et numéro étudiant ; les TD S1 conservent leur contrat actuel (nom, prénom, classe).

Les TD0 à TD7 et les activités R0–R2 du S3 disposent d’un correcteur formatif. Le diagnostic technique complète la relecture pédagogique des interprétations. Les notebooks spaCy requièrent, dans Colab, une connexion pour installer explicitement les versions indiquées ; relancez cette cellule après un redémarrage du runtime.

## S1 — Python pour le texte

Le dossier `S1/` contient les sept TD préparant le contrôle final S1 :

- `TD1_S1_variables_types.ipynb` : notebook, variables, types et premières expressions ;
- `TD2_S1_chaines_sequences.ipynb` : chaînes, séquences et découpage naïf ;
- `TD3_S1_collections.ipynb` : listes, tuples, dictionnaires et ensembles ;
- `TD4_S1_boucles_conditions_comptages.ipynb` : boucles, tests, comptages et compréhension ;
- `TD5_S1_fonctions_reutilisation.ipynb` : fonctions, retours et composition ;
- `TD6_S1_fichiers_csv.ipynb` : fichiers UTF-8, données structurées et CSV ;
- `TD7_S1_expressions_regulieres_pipeline.ipynb` : expressions régulières et pipeline textuel.

Chaque TD a un correcteur formatif associé. La matrice de couverture et la progression sont dans `docs/pedagogy/S1_COVERAGE_MATRIX.md`.

## Distribution des TD S1

Les sept sources S1 contiennent une dernière cellule de restitution HTML avec le substitut `__TAL_PUBLIC_URL__`. Le déploiement injecte l’adresse définie dans l’environnement ou le fichier `.env` uniquement dans les copies de `dist/`, à distribuer aux étudiants. Ne distribuez pas directement les sources Git : leur lien de restitution reste volontairement non résolu.

Les identifiants des évaluateurs restent `td1-s1` à `td7-s1`, indépendamment des nouveaux noms de fichiers. La [revue et matrice de conservation](../docs/pedagogy/s1_td_review_distribution.md) détaille les objectifs couverts et les points pédagogiques à approfondir.
