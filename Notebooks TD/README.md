# TD exemples (en cours de tests avec étudiants master littéraire)

Pour évaluation formative. Les TD suivent une progression en difficulté : Bases, Structures, Logique, initiation algorithmique, fichiers.

### Organisation des notebooks et modèle "ia-ready"

Le projet est structuré pour permettre une génération automatisée de nouveaux contenus pédagogiques. Les notebooks "exemples" servent de base pour être déclinés par l'IA, qui peut également générer l'application d'évaluation associée.

**Organisation des fichiers :**
* `app/Notebooks TD/` : Contient les exercices dirigés (ex: `TD2 - S2.ipynb`) et leurs versions corrigées.
* `app/Notebooks contrôles finaux/` : Contient les examens de fin de cycle.

**Capacité de l'IA :** L'architecture modulaire permet à une IA de :
1. **Générer un notebook** : En suivant les conventions de nommage des variables (`reponse_Qx`, `valeur_Qx`) et les marqueurs d'identification (`# Complétez les informations...`).
2. **Générer le module de correction** : En créant un fichier `app_correction_XXX.py` qui définit les dictionnaires `points_breakdown` et `correct_answers`.
3. **Déploiement immédiat** : Il suffit d'ajouter le nouveau module dans le dictionnaire `EVALUATORS` du fichier `routes.py`.



---

### Exemple de prompt pour l'IA

Voici un prompt structuré pour générer un nouveau module complet :

**Objet : Génération d'un nouveau module d'évaluation Python pour le cours de TAL.**
> **Contexte :** je possède une application Flask de correction automatique qui analyse des fichiers `.ipynb`.

**Tâche 1 : Générer un notebook étudiant (`TD_Regex_TAL.ipynb`)**
> * Inclure une cellule d'identification avec les variables `nom`, `prenom`, `classe`.
> * Créer 10 exercices sur les Expressions Régulières.
> * Pour chaque exercice, l'étudiant doit stocker son résultat dans une variable nommée `reponse_Q1`, `reponse_Q2`, etc.
> * Chaque cellule de code doit se terminer par un print : `print(f"Résultat Q1 : {reponse_Q1}")`.

**Tâche 2 : Générer le module de correction (`app_correction_regex.py`)**
> * Utiliser la fonction `run_evaluation` importée de `engine`.
> * Définir le dictionnaire `points_breakdown` (ex: Q1: 5pts, Q2: 5pts, Q3: 10pts).
> * Définir le dictionnaire `correct_answers` avec les solutions attendues.
> * Implémenter la fonction `check_notebook(notebook_content_str, filename)` qui appelle `engine.run_evaluation`.

**Contraintes techniques :**
> * Respecter strictement le format des fichiers existants (voir `app_correction_TD2_S2.py` pour la structure).
> * Utiliser `ast.literal_eval` via le moteur `engine` pour la comparaison des types complexes.

