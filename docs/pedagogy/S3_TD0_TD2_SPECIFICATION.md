# S3 — lot fondations TD0 à TD2

## Décision enseignante validée

La matrice des huit TD source est validée dans `docs/pedagogy/S3_COVERAGE_MATRIX.md`. Les versions complètes de TD0–TD2 remplacent les prototypes légers ; R0–R2 restent des passerelles de consolidation.

Ce lot installe le début du parcours S3 : diagnostic Python/texte (TD0), premières annotations spaCy (TD1), puis analyse de corpus réutilisable (TD2). Les notebooks R0, R1 et R2 sont des activités formatives brèves, à réaliser avant la séance suivante.

## Progression

| Support | Compétence construite | Seuil pour la suite |
|---|---|---|
| TD0 | Lire un fichier, manipuler une chaîne et une liste, interpréter les limites de `split()` | L'étudiant distingue découpage brut et tokenisation linguistique. |
| R0 | Écrire une fonction de comptage et produire un dictionnaire de fréquences | Boucle, dictionnaire, fonction et sortie explicite. |
| TD1 | Construire un `Doc` spaCy ; parcourir tokens, lemmes, POS et phrases | L'étudiant sait interroger une annotation. |
| R1 | Filtrer les noms et verbes d'un `Doc` | Itération et condition sur `token.pos_`. |
| R2 | Construire une fréquence de lemmes filtrée avec `Counter` | Fonction paramétrée, stopwords et interprétation. |
| TD2 | Réutiliser et discuter une fonction de fréquences sur un corpus | Comparer les résultats bruts et filtrés. |

## Statut du TD0

Le TD0 est diagnostique et formatif : le résultat n'est pas une note certificative. Il signale trois états : `PRÊT`, `À CONSOLIDER` ou `ACCOMPAGNEMENT RECOMMANDÉ`. Le passage au TD1 ne repose pas sur un seuil bloquant ; R0 est l'activité de consolidation prescrite lorsque les éléments Python ne sont pas acquis.

## Contrat des autocorrecteurs formatifs

Le serveur ne doit jamais exécuter du code étudiant. Chaque notebook complémentaire demande donc :

1. une fonction explicitement nommée ;
2. une cellule d'essai sur un jeu de données fourni ;
3. des sorties exécutées, précédées de marqueurs stables tels que `Résultat Q1 :`.

Le correcteur analyse uniquement le JSON du notebook, son code source et ses sorties enregistrées. Il fournit un diagnostic par compétence. Il ne prétend pas tester la fonction sur des entrées cachées : cette limite est explicitement affichée dans les supports.

## Données et reproductibilité

Les exemples sont embarqués dans les notebooks ; aucun chemin Google Drive ni donnée personnelle n'est requis. Dans Colab, TD1, R1, R2 et TD2 exigent une connexion pour installer explicitement `spacy==3.8.7` et `fr_core_news_sm==3.8.0`. En cas de redémarrage du runtime, il faut relancer cette cellule avant de charger le modèle.

## Périmètre des correcteurs

TD0 et les trois activités passerelles disposent d'un correcteur formatif. TD1 et TD2 sont des TD en présence : leur correction est guidée par l'enseignant ; ils ne sont pas présentés comme autocorrigés dans ce lot.

## Hors périmètre du lot

Les groupes nominaux, les dépendances syntaxiques, les plongements, les corpus parallèles et le projet bilingue sont traités dans les lots ultérieurs.
