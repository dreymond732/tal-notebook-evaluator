# S3 — lot fondations TD0 à TD2

## Décision enseignante validée

Ce lot installe le début du parcours S3 : diagnostic Python/texte (TD0), premières annotations spaCy (TD1), puis analyse de corpus réutilisable (TD2). Les notebooks R0, R1 et R2 sont des activités formatives brèves, à réaliser avant la séance suivante.

## Progression

| Support | Compétence construite | Seuil pour la suite |
|---|---|---|
| TD0 | Lire un fichier, manipuler une chaîne et une liste, interpréter les limites de `split()` | L'étudiant distingue découpage brut et tokenisation linguistique. |
| R0 | Écrire une fonction de comptage et produire un dictionnaire de fréquences | Boucle, dictionnaire, fonction et sortie explicite. |
| TD1 | Construire un `Doc` spaCy ; parcourir tokens, lemmes, POS et phrases | L'étudiant sait interroger une annotation. |
| R1 | Filtrer les noms et verbes d'un `Doc` | Itération et condition sur `token.pos_`. |
| TD2 | Concevoir une fonction de fréquences de lemmes filtrée et paramétrée | `Counter`, argument de fonction, stopwords et interprétation. |
| R2 | Comparer une fréquence brute et une fréquence filtrée | Réutilisation d'une fonction et lecture critique du résultat. |

## Statut du TD0

Le TD0 est diagnostique et formatif : le résultat n'est pas une note certificative. Il signale trois états : `PRÊT`, `À CONSOLIDER` ou `ACCOMPAGNEMENT RECOMMANDÉ`. Le passage au TD1 ne repose pas sur un seuil bloquant ; R0 est l'activité de consolidation prescrite lorsque les éléments Python ne sont pas acquis.

## Contrat des autocorrecteurs formatifs

Le serveur ne doit jamais exécuter du code étudiant. Chaque notebook complémentaire demande donc :

1. une fonction explicitement nommée ;
2. une cellule d'essai sur un jeu de données fourni ;
3. des sorties exécutées, précédées de marqueurs stables tels que `Résultat Q1 :`.

Le correcteur analyse uniquement le JSON du notebook, son code source et ses sorties enregistrées. Il fournit un diagnostic par compétence. Il ne prétend pas tester la fonction sur des entrées cachées : cette limite est explicitement affichée dans les supports.

## Données et reproductibilité

Les exemples sont embarqués dans les notebooks. Aucun chemin Google Drive, donnée personnelle, téléchargement automatique ou installation silencieuse n'est requis. TD1 et TD2 indiquent le modèle `fr_core_news_sm` et la commande d'installation à exécuter dans Colab.

## Hors périmètre du lot

Les groupes nominaux, les dépendances syntaxiques, les plongements, les corpus parallèles et le projet bilingue sont traités dans les lots ultérieurs.