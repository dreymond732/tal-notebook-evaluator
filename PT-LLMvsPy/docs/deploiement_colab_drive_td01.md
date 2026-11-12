# Projet Faguet — utiliser le notebook 01 dans Colab

## Ouverture et versions

Le notebook est disponible dans [PT-LLMvsPy/notebooks](../notebooks/01_corpus_protocole.ipynb), au sein du dépôt GitHub public `dreymond732/tal-notebook-evaluator`.

Ouvrir le notebook dans Colab, puis enregistrer une copie dans votre Drive. La bibliothèque est installée depuis GitHub à la révision `REVISION_GIT`, résolue en SHA de commit au début de la session. `VERSION_NOTEBOOK` reste modifiable pour comparer les versions.

## Le répertoire de travail

La version `2.0.0` produit directement tous ses fichiers dans :

```text
/content/analyse_faguet_v2_0_0/
    faguet_source.txt
    faguet_nettoye.txt
    observations_nettoyage.txt
    comparaison_metriques.csv
    comparaison_metriques.json
    commentaires_analyse.txt
    metadonnees_analyse.json
    FAGUET_v2_0_0_<dateUTC>_<numeroAleatoire>.zip
```

Le nom de l'archive intègre automatiquement la date UTC et un **nombre aléatoire de neuf chiffres** généré à l'exécution. Il n'y a pas de champ « identifiant étudiant » et aucune décision de validation imposée.

Un nouveau numéro `VERSION_NOTEBOOK` produit un autre dossier `analyse_faguet_v...`.

## Travail scientifique

1. Charger Faguet et les fonctions communes, puis observer les six exemples.
2. Exécuter le nettoyage complet et télécharger la version épurée pour l'ouvrir dans un éditeur.
3. Rechercher éventuellement des anomalies : ancre dans le corpus initial, fenêtre autour d'elle, fonction impliquée, motif à compter. Les observations peuvent être consignées librement dans `NOTES_INSPECTION`, mais ne bloquent pas le calcul.
4. Calculer automatiquement les sept indicateurs sur le texte original et le texte nettoyé : tokens, types, hapax, TTR, part d'hapax, nombre de phrases et longueur moyenne. Les valeurs, les paramètres, la version de la bibliothèque et le SHA des textes sont enregistrés.
5. Ajouter si nécessaire un commentaire libre et préparer l'archive ZIP.

Une anomalie peut justifier une nouvelle révision des fonctions ; **elle n'empêche pas l'enregistrement des mesures de la version courante**.

## Retrouver le Drive partagé

Ouvrir [le dossier partagé du projet](https://drive.google.com/drive/folders/18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO) avec son compte Google. Si le dossier figure uniquement dans « Partagés avec moi », ajouter un **raccourci dans Mon Drive**.

La cellule de fin de notebook monte le Drive :

```python
from google.colab import drive
drive.mount("/content/drive")
```

Après avoir identifié le chemin du dossier partagé sous `/content/drive/MyDrive/`, le renseigner dans `DOSSIER_DEPOT_DRIVE`. La cellule de dépôt copie l'archive et vérifie son SHA-256. Elle ne crée pas de dossier de destination et refuse d'écraser un fichier de même nom.

La copie locale reste disponible dans `/content/analyse_faguet_v2_0_0/` si le partage n'est pas accessible.

**Attention :** Colab conserve ses fichiers locaux seulement pendant la durée de vie de son environnement. Il faut récupérer le texte et les résultats avant fermeture de la session. Une copie sur Drive suppose un dossier accessible en écriture.

## Contrôles et reproductibilité

Le corpus initial est téléchargé depuis le commit public `b92e92b6c216014283056c83aa545881a447b3a5`. SHA-256 attendu : `c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa`.

Les mesures Gemini proviennent du dossier `PT-LLMvsPy/data/` à la même révision Git que le code. Les règles de nettoyage et de calcul sont enregistrées dans `metadonnees_analyse.json`. L'empreinte du texte épuré permet de voir si deux exécutions ont produit la même sortie.

Le [notebook 02](../notebooks/02_mesures_lexicales.ipynb) lit directement `faguet_nettoye.txt` et `metadonnees_analyse.json` produits ici, dans le même dossier de travail. En cas de nouvelle session Colab, recopier ce dossier depuis Drive ou adapter `DOSSIER_N1`. Les notebooks 03 et 04 restent à redéfinir.

Tests sur une copie du dépôt public :

```bash
cd PT-LLMvsPy
python -m pip install -e ".[test,nlp]"
python -m pytest -q
python scripts/verifier_corpus_td01.py
```
