# Projet Faguet — utiliser le notebook 01 dans Colab

## Ouverture et versions

Le notebook est disponible dans [PT-LLMvsPy/notebooks](../notebooks/01_corpus_protocole.ipynb), au sein du dépôt GitHub public `dreymond732/tal-notebook-evaluator`.

Dans Google Drive, créez le dossier **Mon Drive → S3-PythonVsLLM**. Ouvrez le notebook dans Colab et choisissez **Fichier → Enregistrer une copie dans Drive**. Rangez la copie dans votre dossier **S3-PythonVsLLM**, puis ouvrez-la pour y saisir vos réponses. Vous pourrez les modifier et relancer les cellules au prochain cours. La bibliothèque est installée depuis GitHub à la révision `REVISION_GIT`, résolue en SHA de commit au début de la session. `VERSION_NOTEBOOK` reste modifiable pour comparer les versions.

## Le répertoire de travail

Le notebook 01 affiche son répertoire de travail temporaire sous `/content`. Saisissez votre numéro étudiant tel qu’il apparaît sur vos documents, en conservant ses lettres et ses éventuels zéros initiaux. Gardez le même numéro pour les quatre cahiers.

| Fichier à télécharger au 01 | Usage |
|---|---|
| `faguet_nettoye_<numero>.txt` | Lire le texte nettoyé dans un éditeur et le reprendre pour les calculs suivants. |
| `FAGUET_01_<numero>_<date>_<session>.zip` | Conserver ensemble le texte, les observations, les mesures CSV/JSON, les commentaires et les métadonnées. Le numéro de session identifie une exécution. |

Dans ces noms, `<numero>` correspond à votre numéro étudiant. À l’intérieur du ZIP, le texte du corpus porte le nom `faguet_nettoye.txt`. Les cahiers suivants peuvent le lire directement dans l’archive.

## Travail scientifique

1. Charger Faguet et les fonctions communes, puis observer les six exemples.
2. Exécuter le nettoyage complet et télécharger la version épurée pour l'ouvrir dans un éditeur.
3. Rechercher éventuellement des anomalies : ancre dans le corpus initial, fenêtre autour d'elle, fonction impliquée, motif à compter. Les observations peuvent être consignées librement dans `NOTES_INSPECTION`, mais ne bloquent pas le calcul.
4. Calculer automatiquement les sept indicateurs sur le texte original et le texte nettoyé : tokens, types, hapax, TTR, part d'hapax, nombre de phrases et longueur moyenne. Les valeurs, les paramètres, la version de la bibliothèque et le SHA des textes sont enregistrés.
5. Ajouter si nécessaire un commentaire libre et préparer l'archive ZIP.

Une anomalie peut justifier une nouvelle révision des fonctions ; **elle n'empêche pas l'enregistrement des mesures de la version courante**.

## Garder ses résultats et reprendre dans Colab

1. Exécutez la cellule de téléchargement du TXT, puis celle du ZIP en fin de séance. Si le navigateur ne récupère pas le fichier, ouvrez **Fichiers** dans Colab, suivez le chemin affiché et choisissez **Télécharger** dans le menu du fichier.
2. Ouvrez **Mon Drive → S3-PythonVsLLM** dans Google Drive et importez depuis votre ordinateur les deux fichiers téléchargés. Avant de fermer la session Colab, vérifiez que les fichiers portant votre numéro figurent bien dans ce dossier.
3. À chaque nouvelle séance, téléchargez les entrées nécessaires depuis **S3-PythonVsLLM** sur votre ordinateur. Ouvrez le nouveau cahier dans Colab et utilisez le bouton d’import du volet **Fichiers** pour les placer directement dans `/content`. Saisissez votre numéro étudiant, puis exécutez le cahier.
4. À la fin des cahiers 02 à 04, téléchargez à son tour le JSON produit par la dernière cellule et importez-le dans **S3-PythonVsLLM**. Après une correction, ouvrez le dernier téléchargement et vérifiez votre numéro et la réponse modifiée. Si le navigateur a ajouté `(1)`, rendez au fichier le nom prévu dans le tableau. Remplacez uniquement votre propre ancienne version dans Drive et, si vous l’aviez déjà remise, dans le dossier partagé.

| Séance | À importer dans Colab | À récupérer et à ranger |
|---|---|---|
| [02 · Mesures lexicales](../notebooks/02_mesures_lexicales.ipynb) | Le TXT nettoyé **ou** le ZIP du 01 | `resultats_02_<numero>.json` |
| [03 · Relations lexicales](../notebooks/03_relations_lexicales.ipynb) | Le même TXT ou ZIP **et** le JSON du 02 | `resultats_03_<numero>.json` |
| [04 · Audit](../notebooks/04_audit_llm.ipynb) | Le même TXT ou ZIP **et** les JSON des 02 et 03 | `resultats_04_<numero>.json` |

### Reprendre vos propres exports d’une ancienne séance

Conservez les fichiers d’origine. Dupliquez vos propres exports dans **S3-PythonVsLLM** et donnez aux copies les noms utilisés par les cahiers actuels.

| Ancien export | Nom de la copie |
|---|---|
| `faguet_nettoye.txt` | `faguet_nettoye_<numero>.txt` |
| `FAGUET_v…_<date>_<session>.zip` | `FAGUET_01_<numero>_<date>_<session>.zip` en conservant la date et le numéro de session d’origine |
| `resultats_02.json`, `resultats_03.json` | `resultats_02_<numero>.json`, `resultats_03_<numero>.json` |

Le numéro ajouté au nom permet d’attribuer votre remise. Les métadonnées historiques restent celles enregistrées à l’époque. Importez dans Colab les copies correspondant à la séance. Vous pouvez ainsi réutiliser les calculs compatibles. Si votre ancien JSON du 03 ne contient pas l’analyse des associations annoncées dans le rapport Studio, reprenez le cahier 03 et exportez son résultat complet avant l’audit du 04.

## Copier les pièces dans le dossier partagé

- **Revue du 01.** Dans l’interface de Drive, copiez votre ZIP depuis **S3-PythonVsLLM** dans le dossier partagé du projet. Gardez l’original dans votre dossier personnel.
- **Revue finale du 04.** Depuis ce même dossier personnel, copiez les trois JSON des 02, 03 et 04 vers le dossier partagé. L’équipe PT y retrouvera votre protocole, vos résultats, vos passages et votre conclusion individuelle. Indiquez le ZIP du 01 déjà partagé pour identifier le corpus correspondant.

Vérifiez que les fichiers portant votre numéro figurent dans le dossier partagé. [Ouvrir le dossier partagé du projet](https://drive.google.com/drive/folders/18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO)

## Contrôles et reproductibilité

Le corpus initial est téléchargé depuis le commit public `b92e92b6c216014283056c83aa545881a447b3a5`. SHA-256 attendu : `c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa`.

Les mesures Gemini proviennent du dossier `PT-LLMvsPy/data/` à la même révision Git que le code. Les règles de nettoyage et de calcul sont enregistrées dans `metadonnees_analyse.json`. L'empreinte du texte épuré permet de voir si deux exécutions ont produit la même sortie.

Les activités de préparation, de mesure et de vérification sont détaillées dans [la progression des quatre cahiers](../README.md#du-texte-nettoyé-au-dossier-daudit).

Tests sur une copie du dépôt public :

```bash
cd PT-LLMvsPy
python -m pip install -e ".[test,nlp]"
python -m pytest -q
python scripts/verifier_corpus_td01.py
```
