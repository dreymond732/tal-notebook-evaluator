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
