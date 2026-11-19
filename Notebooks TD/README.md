# Notebooks de TD

Les supports étudiants sont organisés par semestre. Les versions corrigées, lorsqu'elles sont nécessaires, restent séparées des versions distribuées.

## S3 — Fondations Python et TAL

Le dossier `S3/` contient le premier lot du parcours :

- `TD0_S3_diagnostic_texte.ipynb` : diagnostic formatif, du texte brut aux limites de `split()` ;
- `TD1.a_S3_fondations_spacy.ipynb` : document spaCy, tokens, phrases, lemmes et POS ;
- `TD2_S3_analyse_corpus.ipynb` : fréquences de lemmes, filtrage et fonctions paramétrées ;
- `R0_S3_python_texte.ipynb` et `R2_S3_frequences_reutilisables.ipynb` : remédiations formatives distinctes ;
- `TD1.b_S3_doc_spacy.ipynb` : bonus facultatif de lecture du document spaCy après TD1.a.

Consultez [le parcours S3](S3/README.md) pour l’ordre courant et le statut des activités. La spécification de progression et le contrat des activités passerelles sont dans `docs/pedagogy/S3_TD0_TD2_SPECIFICATION.md`.

## Évaluation formative

Les correcteurs ne lancent jamais le code remis. Les notebooks doivent donc être exécutés avant dépôt et produire les marqueurs indiqués (`Résultat Qx :`). Les correcteurs analysent le JSON, le code source et les sorties enregistrées ; ils fournissent un diagnostic de compétence, pas une validation par exécution sur données cachées.

Complétez la cellule d’identification prévue par chaque sujet. Les notebooks S3 en version 2 demandent nom, prénom, classe et numéro étudiant ; les TD S1 conservent leur contrat actuel (nom, prénom, classe).

Les TD0 à TD7 et les activités R0–R2 du S3 disposent d’un correcteur formatif. Le diagnostic technique complète la relecture pédagogique des interprétations. Les notebooks spaCy requièrent, dans Colab, une connexion pour installer explicitement les versions indiquées ; relancez cette cellule après un redémarrage du runtime.

## S1 — Python pour le texte

Le dossier `S1/` présente sept thèmes répartis en quinze cahiers courants. Les TD3 à TD6 se parcourent dans l'ordre A → B → C. Voir [le parcours détaillé](S1/README.md).

| Étape | Cahiers courants | Travail principal |
|---|---|---|
| TD1 | `S1_TD1_variables_types.ipynb` | Variables, types et premières expressions |
| TD2 | `S1_TD2_chaines_sequences.ipynb` | Chaînes, séquences et découpage |
| TD3 | `S1_TD3_A_listes.ipynb`, `S1_TD3_B_tuples.ipynb`, `S1_TD3_C_dictionnaires_ensembles.ipynb` | Listes, tuples, dictionnaires et ensembles |
| TD4 | `S1_TD4_A_conditions_filtres.ipynb`, `S1_TD4_B_bornes_repetitions.ipynb`, `S1_TD4_C_comptages_comprehensions.ipynb` | Conditions, répétitions et comptages |
| TD5 | `S1_TD5_A_fonctions.ipynb`, `S1_TD5_B_parametres_portee.ipynb`, `S1_TD5_C_composition_texte.ipynb` | Fonctions, paramètres et composition |
| TD6 | `S1_TD6_A_fichiers_texte.ipynb`, `S1_TD6_B_donnees_delimitees.ipynb`, `S1_TD6_C_csv.ipynb` | Fichiers UTF-8, données structurées et CSV |
| TD7 | `S1_TD7_expressions_regulieres_pipeline.ipynb` | Expressions régulières et pipeline textuel |

Chaque cahier courant a son correcteur formatif. Les quatre anciennes synthèses S1 et les corrigés historiques sont rangés dans les [archives](../historique/README.md), hors parcours et hors distribution. Leurs déplacements ne suppriment pas les correcteurs de compatibilité des copies déjà commencées. La matrice de couverture et la progression sont dans `docs/pedagogy/S1_COVERAGE_MATRIX.md`.

## Distribution des TD S1

Les sources S1 contiennent une dernière cellule de restitution HTML avec le substitut `__TAL_PUBLIC_URL__`. Le déploiement injecte l’adresse définie dans l’environnement ou le fichier `.env` uniquement dans les copies de `dist/`, à distribuer aux étudiants. Ne distribuez pas directement les sources Git : leur lien de restitution reste volontairement non résolu.

Les identifiants des évaluateurs des cahiers courants restent ceux de leurs métadonnées ; le rangement des archives ne les change pas. La [revue et matrice de conservation](../docs/pedagogy/s1_td_review_distribution.md) détaille les objectifs couverts et les points pédagogiques à approfondir.
