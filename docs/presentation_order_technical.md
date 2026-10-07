# Présentation du parcours — rapport technique

## Mission et référence

Rôle producteur : TAL-Code-Architect. Branche `pedagogy/notebook-presentation-order` ; référence exacte `1ee45813283cec79463a8acc4b6204f50cbafe74`. Réalisation après ACCEPT préalable de la matrice `docs/pedagogy/presentation_order_2026.md`. Ce rapport demande une revue indépendante ; il ne rend pas de verdict sur son propre code.

## Génération des deux contextes

`app/tutor_metadata.py` conserve la cellule gérée et toutes ses métadonnées. La première cellule contient désormais un titre H1 visible, puis le contexte complet dans le commentaire HTML. Les instructions Colab et HTML restent identiques. Si le titre figure déjà avant le commentaire, il est conservé, sans réécriture d’après le manifeste. Sinon, le générateur déplace uniquement la ligne du premier H1 introductif ; sa cellule d’origine, ses espaces, ses objectifs et toute sa prose restent présents. Les titres suivants, dont « Sauvegarde » du contrôle S1, ne sont pas déplacés.

Un titre absent provoque une erreur explicite. Les cellules gérées ambiguës, les blocs partiels, doublons de tuteur et contextes Colab étrangers restent refusés. La migration ne lance aucun code du notebook et reste idempotente. Le générateur conserve les formats anciens : pas d’ajout d’ID de cellule de niveau supérieur dans les notebooks antérieurs à nbformat 4.5.

Le producteur technique n’a pas écrit directement les notebooks ; l’Integration-Master a exécuté la génération après gel des douze supports S3 par le Designer.

## Noms et accès

| Chemin antérieur sous `Notebooks TD/S3/` | Nouveau chemin | Identifiant de correction inchangé | Version inchangée |
|---|---|---|---:|
| `TD1_S3_fondations_spacy.ipynb` | `TD1.a_S3_fondations_spacy.ipynb` | `td1-s3` | 2 |
| `R1_S3_doc_spacy.ipynb` | `TD1.b_S3_doc_spacy.ipynb` | `td-r1-s3` | 2 |
| `TD1B_S3_entites_similarite_regles.ipynb` | `TD1.c_S3_entites_similarite_regles.ipynb` | `td1b-s3` | 3 |

Le catalogue et les intitulés de `app/routes.py` suivent ces chemins. L’ordre affiché est TD0, R0, TD1.a, TD1.b (bonus facultatif), TD1.c, R2, TD2 à TD7, puis les contrôles. Les URL, modules, versions, marqueurs, barèmes et règles de validation restent inchangés. La génération distribuable utilise les nouveaux noms et n’émet pas les anciens chemins dans un répertoire neuf.

## Conservation et adaptation précise des tests

La nouvelle fixture `tests/fixtures/presentation_order_source_baseline.json` fige les **35 textes JSON bruts exacts** extraits de la référence par `git show`, avant rédaction. Aucune fixture ni empreinte historique existante n’a été recalculée.

Le nouveau test global vérifie :

- H1 visible et commentaire HTML complet dans la même cellule pour les 35 sujets ; un seul bloc tuteur ;
- identité et métadonnées de toutes les cellules, ordre et nombre des cellules, identifiants et versions des notebooks conservés ;
- AST de chaque cellule de code conservé ; pour les erreurs syntaxiques volontairement proposées dans DevoirS1, source complète inchangée ; sorties et compteurs inchangés ;
- permissions de bibliothèques et notions par exercice conservées ;
- hors des douze TD S3, **égalité complète** au parent après inversion du seul déplacement de titre, avec une exception explicitement nommée : le prérequis du contrôle TD1 est renommé « TD1.a » dans la configuration du tuteur ;
- titre personnalisé déjà placé avant le commentaire conservé, métadonnées personnalisées préservées et deuxième génération identique ;
- ordre réel du menu Flask, titres TD1.a/b/c, routes stables et distribution aux nouveaux chemins.

Le helper indépendant `presentation_order_evidence.py` ne fait pas appel au générateur testé : il inverse seulement le déplacement H1 avec contrôle de titre et d’identité d’introduction. Les anciennes vérifications historiques de hashes passent par les textes bruts de ce parent pour les fichiers structurellement modifiés ; leur contenu courant reste protégé par le nouveau test exhaustif. Les comparaisons S2 normalisent uniquement ce déplacement de titre avant leurs assertions historiques.

La comparaison S3 conserve AST et métadonnées ; les modifications de prose des douze TD sont explicitement autorisées par la matrice et nécessitent les revues pédagogique et éditoriale indépendantes. Le test de route qui repérait la cellule d’identité par une phrase exacte utilise maintenant son rôle technique `identification` ; il continue à vérifier POST, persistance et échappement HTML.

## Vérifications et limites

Exécution ciblée avec `/tmp/tal-presentation-venv/bin/python` : 7 nouveaux tests de présentation, 22 tests du tuteur, 8 tests d’intégrité historique, 14 tests de conservation et 21 tests d’audit/routage S3. La suite globale finale est exécutée séparément par l’Integration-Master, après stabilisation du lot.

Aucun test ne prétend démontrer la prise en compte effective des instructions par Gemini/Colab. La modification ne revalide pas les contenus S1/S2, ne crée aucune nouvelle correction et ne change pas le niveau d’assistance autorisé en contrôle. La distribution doit être régénérée lors du déploiement pour obtenir les nouveaux noms ; les anciennes copies restent identifiables par leurs métadonnées inchangées.

## Résultats d’intégration finale

L’intégration a exécuté la suite complète : **302 tests, tous réussis**. La synchronisation des 35 profils est conforme. La préparation des 34 notebooks distribuables réussit en modes `check`, `render` et `verify`, avec une URL neutre et sans modification des sources. `git diff --check` ne signale aucune erreur. Verdict indépendant TAL-Code-Auditor : **ACCEPT** (43 tests ciblés et vérification des snapshots bruts). Les contenus spaCy n’ont pas été réexécutés pour cette modification de présentation ; leur AST est conservé.
