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

Les identifiants personnels ne sont pas demandés dans les notebooks de TD.

TD0 et les activités R0–R2 disposent d'un correcteur. TD1 et TD2 sont corrigés en séance dans ce lot. Les notebooks spaCy requièrent, dans Colab, une connexion pour installer explicitement les versions indiquées ; relancez cette cellule après un redémarrage du runtime.

## S1 — Python pour le texte

Le dossier `S1/` contient les sept TD préparant le contrôle final S1 :

- `TD1_S1_python_texte.ipynb` : notebook, variables, types et premières expressions ;
- `TD2_S1_python_texte.ipynb` : chaînes, séquences et découpage naïf ;
- `TD3_S1_python_texte.ipynb` : listes, tuples, dictionnaires et ensembles ;
- `TD4_S1_python_texte.ipynb` : boucles, tests, comptages et compréhension ;
- `TD5_S1_python_texte.ipynb` : fonctions, retours et composition ;
- `TD6_S1_python_texte.ipynb` : fichiers UTF-8, données structurées et CSV ;
- `TD7_S1_python_texte.ipynb` : expressions régulières et pipeline textuel.

Chaque TD a un correcteur formatif associé. La matrice de couverture et la progression sont dans `docs/pedagogy/S1_COVERAGE_MATRIX.md`.
