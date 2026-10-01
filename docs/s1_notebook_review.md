# TD S1 — Relais du Designer

## Mission et périmètre

Branche `pedagogy/s1-review-distribution`, référence source `b12b40f`. La matrice du Prof, [TD S1 — Revue pédagogique et distribution](pedagogy/s1_td_review_distribution.md), a été lue et validée par l’Orchestrateur avant modification. La demande porte sur les dénominations, les métadonnées et la restitution HTML ; les constats pédagogiques de fond restent documentés dans la matrice sans modifier implicitement la progression.

## Fichiers et bilan de couverture

| Source dans `Notebooks TD/S1/` | Cible dans le même dossier | Cellules initiales conservées | Cellules finales | Réponses principales |
|---|---|---:|---:|---:|
| `TD1_S1_python_texte.ipynb` | `TD1_S1_variables_types.ipynb` | 15 | 16 | 6 |
| `TD2_S1_python_texte.ipynb` | `TD2_S1_chaines_sequences.ipynb` | 19 | 20 | 7 |
| `TD3_S1_python_texte.ipynb` | `TD3_S1_collections.ipynb` | 16 | 17 | 6 |
| `TD4_S1_python_texte.ipynb` | `TD4_S1_boucles_conditions_comptages.ipynb` | 18 | 19 | 7 |
| `TD5_S1_python_texte.ipynb` | `TD5_S1_fonctions_reutilisation.ipynb` | 17 | 18 | 6 |
| `TD6_S1_python_texte.ipynb` | `TD6_S1_fichiers_csv.ipynb` | 18 | 19 | 6 |
| `TD7_S1_python_texte.ipynb` | `TD7_S1_expressions_regulieres_pipeline.ipynb` | 20 | 21 | 7 |

Les 123 cellules initiales gardent intégralement leurs sources, types, ordre, sorties, compteurs d’exécution et identifiants préexistants. Les 45 réponses principales et les sept traces complémentaires du TD2 restent identiques. Aucune activité, donnée, exemple, interprétation ou exigence d’autonomie n’est supprimée ou déplacée.

Les 71 cellules initialement dépourvues de `metadata.tal` sont désormais décrites : énoncés et rappels en `prompt`, préparation du fichier et import fourni en `provided`, premier Markdown du tuteur en `infrastructure`. Les identifiants Q1–Qn des réponses et `identity` restent inchangés. Les cellules qui n’avaient pas de `id` en reçoivent un stable, construit à partir du TD, du rôle et de l’identifiant de question ou section ; les IDs existants sont conservés.

Chaque notebook reçoit une seule dernière cellule canonique `submission`, produite par `submission_cell()` sans argument. Elle contient seulement `__TAL_PUBLIC_URL__`, aucune sortie et aucune exécution enregistrée. Les sept cellules de restitution constituent un mécanisme fourni hors évaluation ; `IPython.display` et `html.escape` ne deviennent pas des outils autorisés pour résoudre les exercices.

`Notebooks TD/README.md` référence les nouveaux noms et indique de distribuer les copies de `dist/`. Deux affirmations devenues inexactes sur l’identification et les correcteurs S3 y sont rectifiées. Le présent relais constitue le second document pédagogique modifié par le Designer.

## Contrat et tuteur

Les racines `metadata.tal` restent strictement identiques : IDs et évaluateurs `td1-s1` à `td7-s1`, version 1. Le renommage ne change aucun barème, marqueur ni réponse attendue. Dans les métadonnées du tuteur, seul `tal_tutor.session.notebook` suit le nouveau chemin. Les instructions Colab et le premier Markdown restent strictement identiques, avec les règles S1 de guidage sans code.

Le catalogue, le générateur et les tests relèvent des autres producteurs. Leurs vérifications indépendantes doivent confirmer que l’ajout de métadonnées et d’une cellule fournie ne modifie pas le diagnostic formatif.

## Vérifications réalisées par le producteur

Une comparaison JSON contre les sept sources du commit `b12b40f` démontre l’égalité de chaque cellule initiale après retrait des seuls ajouts autorisés (`metadata.tal` lorsque absent et `id` lorsque absent). Une comparaison séparée vérifie l’égalité des métadonnées racine après la seule substitution du chemin de session.

`validate_cell_metadata()` accepte les 130 cellules finales, toutes munies d’un couple question/rôle unique. Tous les IDs de cellule sont uniques dans leur notebook. `check_source()` accepte les sept sources et chacune se termine par une cellule exactement égale à `submission_cell()`. Aucun notebook étudiant n’a été exécuté pour ces vérifications.

## Risques et critères d’acceptation

Les sources Git ont volontairement un lien non résolu : distribuer exclusivement les copies générées dans `dist/`. Les anciennes copies renommées doivent être retirées du répertoire de distribution par le mécanisme de manifeste, sans effacer les fichiers non gérés. Les sept contrats S1 restent en version 1 : les anciennes copies compatibles ne sont pas rendues invalides par un simple changement de nom.

Les limites pédagogiques de la matrice — étayage inégal, parcours du dictionnaire avant la séance sur les boucles, charge réelle non mesurée — restent à traiter dans un chantier explicite. L’identité S1 n’acquiert pas de numéro étudiant obligatoire par cette opération.

Verdicts demandés : revue pédagogique indépendante de conservation de couverture, revue technique du routage et de la génération, puis gouvernance et intégration. Le Designer rapporte ses vérifications sans valider lui-même sa production.
