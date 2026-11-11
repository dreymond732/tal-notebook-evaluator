# Projet Faguet — lancer le premier notebook dans Google Colab

## 1. Où se trouve la bibliothèque ?

Les fichiers de travail sont réunis dans le sous-dossier
[`PT-LLMvsPy/`](https://github.com/dreymond732/tal-notebook-evaluator/tree/main/PT-LLMvsPy)
du dépôt GitHub **public** `dreymond732/tal-notebook-evaluator`.

La branche de préparation est
[`feat/pt-llmvspy-colab-integrated`](https://github.com/dreymond732/tal-notebook-evaluator/tree/feat/pt-llmvspy-colab-integrated/PT-LLMvsPy).
Aucun jeton GitHub ni copie de wheel n'est nécessaire.

Le dépôt privé `dreymond732/PT-LLMvsPy` reste conservé comme origine historique ;
les fichiers distribués aux étudiants proviennent désormais du dépôt public.

## 2. Ouvrir le notebook

1. Ouvrir [`notebooks/01_corpus_protocole.ipynb`](../notebooks/01_corpus_protocole.ipynb).
2. Télécharger le fichier ou l'ouvrir dans Colab depuis GitHub.
3. Dans Colab, **Fichier → Enregistrer une copie dans Drive**.
4. Exécuter les cellules dans l'ordre.

À la première exécution, le notebook appelle `pip` depuis le même dépôt public,
en indiquant le sous-dossier Python :

```bash
python -m pip install 'git+https://github.com/dreymond732/tal-notebook-evaluator.git@main#subdirectory=PT-LLMvsPy'
```

**Version des fonctions.** `REVISION_GIT` peut désigner une branche, un tag ou
un commit. Le notebook résout automatiquement cette référence en un SHA Git
précis avant l'installation ; il charge les documents de référence à cette
même révision et consigne le SHA dans le dossier de résultats. Cette résolution
évite de mélanger les fichiers si une branche évolue pendant la séance.

Avant la fusion de la branche de migration, utiliser temporairement
`REVISION_GIT = "feat/pt-llmvspy-colab-integrated"`. Après fusion, conserver
`REVISION_GIT = "main"`.

## 3. Première étape scientifique : nettoyer, examiner, décider

Le travail comporte quatre moments :

1. Découverte des fonctions et de leurs effets sur des exemples courts.
2. Traitement complet du texte Faguet. Le fichier nettoyé est produit dans
   l'espace Colab et proposé au téléchargement pour examen dans un éditeur.
3. Recherche d'erreurs éventuelles : ancre retrouvée dans le corpus original,
   fenêtre autour de cette ancre, fonctions ayant modifié la zone, estimation
   des occurrences d'un motif représentatif. La liste d'anomalies peut être
   vide si la méthode d'inspection est décrite.
4. Décision motivée de conserver ou de réviser le nettoyage, puis comparaison
   des sept mesures lexicales sur l'original et le texte préparé.

En cas de révision, conserver les fichiers et le journal, créer une nouvelle
copie du notebook, incrémenter `VERSION_NOTEBOOK`, renseigner la nouvelle
`REVISION_GIT` et choisir `MODE_REVISION="exploration"`.

Le **mode référence** vérifie l'empreinte attendue du texte nettoyé. Une sortie
d'**exploration** garde son statut propre tant qu'elle n'a pas été revue.

## 4. Corpus et documents de référence

- Le corpus Faguet initial est téléchargé depuis le dépôt public de cours au
  commit `b92e92b6c216014283056c83aa545881a447b3a5` et vérifié par
  SHA-256 : `c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa`.
- Les mesures rapportées par Gemini sont dans
  `PT-LLMvsPy/data/annonces_globales_gemini.json`, récupéré à la **même
  révision Git** que le code.
- La version épurée du protocole de référence fait 446 289 caractères,
  empreinte `0885496f4abf4ca9112a3c303f8dc69cb887ffaa34033371aa7c49bad9e38fc2`.
  Cette valeur vérifie une version précise du résultat ; elle ne prouve pas
  que toute transformation textuelle serait sans défaut.

## 5. Dépôt individuel sur Drive

À la fin de l'analyse, une archive `FAGUET_<identifiant>_v<version>_...zip`
réunit : le journal `inspection.json`, les paramètres et versions, les sept
mesures comparatives, le texte épuré, ses empreintes et le rapport critique.

Le bouton du notebook dépose cette archive dans le
[dossier partagé](https://drive.google.com/drive/folders/18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO)
après connexion Google et confirmation. Il vérifie ensuite l'intégrité du
fichier distant. Un téléchargement local est prévu si le dépôt échoue.

Il faut avoir le droit **d'ajouter des fichiers** au dossier Drive. Les droits
Drive sont indépendants des droits GitHub.

## 6. Les autres notebooks

Les notebooks 02 à 04 sont importés, mais leur définition et leur usage sont
encore en cours de révision. Tous devront repartir du **corpus nettoyé retenu
et documenté par le notebook 01**, et non retélécharger silencieusement le
texte brut.

## 7. Contrôles de développement

Depuis la racine du clone public :

```bash
cd PT-LLMvsPy
python -m pip install -e '.[test,nlp]'
python -m pytest -q
python scripts/verifier_corpus_td01.py
```

La CI dédiée du dépôt public effectue les mêmes tests et vérifie en plus
l'installation de `tal-toolkit` depuis GitHub avec le fragment
`#subdirectory=PT-LLMvsPy`.

La chaîne Git a été vérifiée automatiquement. Le dépôt **réel** dans le
Drive partagé nécessite toujours un essai avec un compte Google autorisé.

Pour la provenance de l'import : [MIGRATION.md](../MIGRATION.md).
