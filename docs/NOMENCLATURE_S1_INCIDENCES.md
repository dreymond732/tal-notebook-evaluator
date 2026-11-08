# Analyse d'incidence — nomenclature des TD du S1

## Décision appliquée à la première étape

La nomenclature **visible et distribuée** suit `S1_TD{n}`. Les déclinaisons
des **TD4, TD5 et TD6** sont `S1_TD{n}_A`, `_B`, `_C`,
avec la correspondance `one → A`, `bis → B`, `ter → C`.

Pour le TD3, déjà diffusé comme synthèse unique, les approfondissements
restent provisoirement `S1_TD3_one`, `S1_TD3_bis`, `S1_TD3_ter`.
Cette décision respecte la borne explicite « TD4 à TD6 » ; toute
généralisation de A/B/C au TD3 demandera un arbitrage séparé.

Le reste du nom descriptif des fichiers est conservé.

## Correspondance des fichiers

| Source précédente | Source renommée |
|---|---|
| TD1_S1_variables_types | S1_TD1_variables_types |
| TD2_S1_chaines_sequences | S1_TD2_chaines_sequences |
| TD3_S1_collections | S1_TD3_collections |
| TD3-one_S1_listes | S1_TD3_one_listes |
| TD3-bis_S1_tuples | S1_TD3_bis_tuples |
| TD3-ter_S1_dictionnaires_ensembles | S1_TD3_ter_dictionnaires_ensembles |
| TD4_S1_boucles_conditions_comptages | S1_TD4_boucles_conditions_comptages |
| TD4-one_S1_conditions_filtres | S1_TD4_A_conditions_filtres |
| TD4-bis_S1_bornes_repetitions | S1_TD4_B_bornes_repetitions |
| TD4-ter_S1_comptages_comprehensions | S1_TD4_C_comptages_comprehensions |
| TD5_S1_fonctions_reutilisation | S1_TD5_fonctions_reutilisation |
| TD5-one_S1_fonctions | S1_TD5_A_fonctions |
| TD5-bis_S1_parametres_portee | S1_TD5_B_parametres_portee |
| TD5-ter_S1_composition_texte | S1_TD5_C_composition_texte |
| TD6_S1_fichiers_csv | S1_TD6_fichiers_csv |
| TD6-one_S1_fichiers_texte | S1_TD6_A_fichiers_texte |
| TD6-bis_S1_donnees_delimitees | S1_TD6_B_donnees_delimitees |
| TD6-ter_S1_csv | S1_TD6_C_csv |
| TD7_S1_expressions_regulieres_pipeline | S1_TD7_expressions_regulieres_pipeline |

Tous les noms sont des fichiers `.ipynb` dans `Notebooks TD/S1/`.
Les 19 titres H1 visibles et les chemins de session tutorielle sont
alignés ; le contexte complet du tuteur et les identifiants des cellules
ne doivent pas être réécrits.

## Conséquences vérifiées

1. **Correcteurs** : chaque identifiant public `td1-s1` à
   `td7-s1` et `tdN-one/bis/ter-s1` reste inchangé.
   Les modules `app/app_correction_*.py`, les contrats
   `metadata.tal.id/evaluator/version`, les barèmes et les URL
   `/eval/<identifiant>` restent inchangés. Les copies précédemment
   distribuées restent recevables par leur correcteur d'origine.
2. **Distribution** : `app/notebook_catalog.json`, le manifeste
   `docs/pedagogy/tutor_sessions.json`, les README et les tests
   doivent pointer vers les nouveaux chemins. Après déploiement,
   `app/prepare_student_notebooks.py render` remplace les fichiers
   gérés sous `dist/`. Il faudra rediffuser les liens ou fichiers
   si les étudiants accèdent directement aux noms de fichiers.
3. **Historique des évaluations** : le répertoire physique actuel
   est dérivé du module correcteur via `storage_layout.storage_id()`.
   **Cette PR ne le change pas**. Par exemple, un TD4 renommé
   `S1_TD4` reste stocké dans `soumissions/TD4_S1/`.
   Les  CSV et le suivi `progression.py` continuent donc de fonctionner.
4. **Preuves historiques** : les instantanés figés ne sont ni supprimés,
   ni remplacés. Les tests comparent les copies renommées aux
   originaux en reconstituant uniquement les titres et chemins
   modifiés. Les contenus des exercices, sorties et métadonnées
   de correction restent vérifiés.

## Faut-il refaire la migration ?

**Pas pour renommer les cahiers, titres, liens et URL visibles.**
Le renommage des fichiers pédagogiques n'impose aucune migration
des journaux d'évaluation, puisque les clés techniques ne changent pas.

**Oui, si le répertoire de production doit aussi devenir** :
`soumissions/S1_TD4/notes_S1_TD4.csv`, `nb/`, `rapport/`,
et `soumissions/S1_TD4_A/` pour les variantes.

Ce changement de stockage devrait faire l'objet d'une PR distincte,
avec une migration **v2** spécialement conçue pour les répertoires
déjà consolidés par la migration #35. L'ancien
`app/migrate_storage.py --apply` sert à regrouper les répertoires
de classe et les anciens `-v2` : il ne doit pas être considéré comme
un outil de migration `TD4_S1 → S1_TD4`.

Plan de migration physique ultérieure :

1. Geler les dépôts, sauvegarder l'intégralité de `soumissions/`
   (y compris `suivi/`, CSV et base SQLite éventuelle du portail).
2. Inventorier le stockage existant, les chemins cible et les collisions.
   Préparer un rapport `--dry-run` ne faisant **aucune écriture**.
3. Sous le verrou partagé avec la consolidation, copier chaque notebook
   et rapport vers le nouveau dossier en conservant tous les essais.
   Fusionner les éventuels CSV cible et source selon la provenance
   et l'identifiant de réception ; refuser tout conflit non résolu.
4. Mettre à jour `storage_layout.storage_id()`, `progression.py`,
   le migrateur et les tests ; conserver les anciennes routes HTTP
   et les modules de correction.
5. Comparer avant/après le nombre de lignes, d'étudiants, les min/max,
   le nombre d'essais, les empreintes de fichiers et les anomalies.
   Une seconde exécution doit être idempotente.
6. Ne supprimer les anciennes archives qu'après validation explicite
   sur une sauvegarde et une période d'observation en production.

Un changement des identifiants de correcteurs ou des métadonnées
`tal` serait beaucoup plus risqué et **n'est pas nécessaire**
pour répondre à la demande de nomenclature.

## Ce qui reste hors de cette PR

Les supports S2/S3, les devoirs maison, les correcteurs de contrôle,
les dossiers de stockage physiques et le code des correcteurs
ne sont pas renommés ici. Une extension de la règle « semestre
en tête » à S2/S3 doit faire l'objet d'un inventaire distinct,
notamment pour les TD1.a/b/c du S3 et les révisions R0/R1/R2.

Aucune migration ni aucun déploiement de données nominatives
ne sont exécutés depuis GitHub.

## Mise en œuvre de la deuxième étape

La migration physique prévue est maintenant implémentée sur la branche de la PR de stockage S1 v2, dans `app/migrate_storage_s1.py`. Voir [MIGRATION_PHYSIQUE_S1_V2.md](MIGRATION_PHYSIQUE_S1_V2.md). L'inventaire ci-dessus conserve sa valeur d'historique de la décision prise lors du premier renommage pédagogique.
