# S1 : correction et distribution v2

Les sept TD S1 utilisent un contrat explicite v2 : métadonnées racine, une cellule d’identification et les cellules de réponse Q1…Qn. Les barèmes restent 6, 7, 6, 7, 6, 6 et 7 points. Les contrôles S1, le devoir maison et le S2 gardent leurs contrats existants.

## Identification et anciennes copies

`strict_contract_identity` réutilise le contrôle S3 : quatre affectations littérales uniques pour `nom`, `prenom`, `classe` et `numero_etudiant`. Le numéro accepte de 1 à 64 lettres ASCII, chiffres, tirets ou soulignements. Les commentaires et les sous-chaînes de noms de variables ne constituent pas une identité.

Une version antérieure ou des cellules obligatoires absentes provoquent « mauvaise version du notebook », avant correction et persistance. Une cellule réponse présente mais vide donne une preuve absente. Les dépôts automatiques et les anciennes URL directes appliquent la même vérification. Les fichiers historiques restent intacts : les nouvelles soumissions vont dans `soumissions/tdN-s1-v2/` et portent le numéro étudiant, distinguant les homonymes.

## Preuves inertes

`s1_revision.py` relie un `print` explicite à une sortie `stdout` unique dans la cellule de réponse correspondante. Les marqueurs historiques sont conservés. Les nouvelles traces complémentaires restent dans cette cellule. Le code est analysé par AST ; seuls les littéraux des sorties sont lus avec `ast.literal_eval`, après bornage. Aucun programme étudiant ni fichier qu’il désigne n’est exécuté ou ouvert.

Les résultats sont comparés aux références de `s1_reference.py` avec des types stricts : booléens distincts des entiers, listes ordonnées, ensembles et dictionnaires sans ordre imposé. Le CSV est une chaîne `repr` enregistrée, décodée puis analysée en mémoire. Les chaînes libres sont relevées pour leur présence, jamais notées pour leur pertinence par un mot-clé ou leur longueur.

La vérification de syntaxe suit les affectations précédentes, les mutations, les appels aux fonctions et leurs expressions de retour. Les commentaires, les exemples, les exercices `practice`, les fonctions non appelées, les calculs sans lien avec l’affichage et le code après un retour direct ne donnent pas de crédit. Les imports fournis peuvent définir des alias de bibliothèque, sans fournir de solution. Les constructions dans les branches dépendant d’une valeur inconnue restent une analyse statique conservatrice : elles ne certifient pas le chemin réellement exécuté, ni la généralité du programme.

Le TD2 conserve son évaluateur détaillé antérieur et ses sous-traces à demi-point ; seules l’identification v2, l’isolation des cellules et la présentation du score changent.

## Retour et limites

Le résultat s’affiche comme **score technique provisoire**. Le diagnostic distingue résultat incorrect, preuve absente, construction demandée non repérée et dépendance manquante empêchant sa vérification. Les productions à relire sont rassemblées et échappées dans le rapport HTML. Une référence fixe permet de vérifier une question même si la sortie d’une étape antérieure manque, dès lors que ses dépendances syntaxiques restent présentes.

Les sorties peuvent être périmées ou modifiées manuellement. Aucune analyse statique ne certifie leur authenticité, la compréhension de l’étudiant ou l’exécution sur des cas non enregistrés. Ces limites sont affichées dans les retours.

## Déploiement

Après fusion, exécuter `git pull`, puis `bash deploy.sh` avec `TAL_PUBLIC_URL` configurée. Le déploiement régénère les copies de `dist/Notebooks TD/S1/`, injecte l’adresse dans leur cellule HTML finale et vérifie le résultat. Redistribuer les sept nouvelles copies : modifier seulement le numéro de version d’une ancienne copie n’est pas une migration valide. L’adresse réelle n’est pas ajoutée aux sources Git.
