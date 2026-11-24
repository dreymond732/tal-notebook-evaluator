# Projet Faguet — utiliser le notebook 01 dans Colab

## Ouverture et versions

Le notebook est disponible dans [PT-LLMvsPy/notebooks](../notebooks/01_preparer_le_corpus_et_mesurer_le_nettoyage.ipynb), au sein du dépôt GitHub public `dreymond732/tal-notebook-evaluator`.

Dans Google Drive, créez le dossier **Mon Drive → S3-PythonVsLLM**. Ouvrez le notebook dans Colab et choisissez **Fichier → Enregistrer une copie dans Drive**. Rangez la copie dans votre dossier **S3-PythonVsLLM**, puis ouvrez-la pour y saisir vos réponses. Vous pourrez les modifier et relancer les cellules au prochain cours. La bibliothèque est installée depuis GitHub à la révision `REVISION_GIT`, résolue en SHA de commit au début de la session. `VERSION_NOTEBOOK` reste modifiable pour comparer les versions.

## Le répertoire de travail

Le notebook 01 affiche son répertoire de travail temporaire sous `/content`. Saisissez votre numéro étudiant tel qu’il apparaît sur vos documents, en conservant ses lettres et ses éventuels zéros initiaux. Gardez le même numéro pour les quatre cahiers.

| Fichier à télécharger au 01 | Usage |
|---|---|
| `faguet_nettoye_<numero>.txt` | Lire le texte nettoyé dans un éditeur et le reprendre pour les calculs suivants. |
| `FAGUET_01_<numero>_<date>_<session>.zip` | Conserver ensemble le texte, les observations, les mesures CSV/JSON, les commentaires et les métadonnées. Le numéro de session identifie une exécution. |

Dans ces noms, `<numero>` correspond à votre numéro étudiant. À l’intérieur du ZIP, le texte du corpus porte le nom `faguet_nettoye.txt`. Les cahiers suivants peuvent le lire directement dans l’archive.

## Travail scientifique

1. Chargez le texte de Faguet. Choisissez un élément de l’inventaire et retrouvez-le à la position indiquée dans la source.
2. Exécutez les six exemples fournis. Sur une phrase de votre choix, prédisez l’effet d’une règle, puis comparez votre prédiction au texte obtenu.
3. Appliquez le plan commun au livre, téléchargez le TXT et ouvrez-le dans un éditeur. Lisez des passages au début, au milieu et à la fin. Pour examiner un changement, recherchez une courte chaîne de caractères dans l’original, relisez le passage nettoyé et comptez les occurrences d’un motif dans les deux textes. Vous pouvez garder une trace de vos observations dans `NOTES_INSPECTION`, y compris si aucun défaut n’apparaît dans les passages lus.
4. Lisez le tableau des sept indicateurs calculés dans les mêmes conditions avant et après nettoyage. Choisissez une ligne, relevez les deux valeurs et leur écart, puis appuyez votre explication sur un passage. Vous pouvez consigner votre interprétation dans `COMMENTAIRES_ANALYSE`. Exécutez la cellule de création du ZIP même si vous laissez ces commentaires vides.

## Garder ses résultats et reprendre dans Colab

1. Exécutez la cellule de téléchargement du TXT, puis celle du ZIP en fin de séance. Si le navigateur ne récupère pas le fichier, ouvrez **Fichiers** dans Colab, suivez le chemin affiché et choisissez **Télécharger** dans le menu du fichier.
2. Ouvrez **Mon Drive → S3-PythonVsLLM** dans Google Drive et importez depuis votre ordinateur les deux fichiers téléchargés. Avant de fermer la session Colab, vérifiez que les fichiers portant votre numéro figurent bien dans ce dossier.
3. À chaque nouvelle séance, téléchargez les entrées nécessaires depuis **S3-PythonVsLLM** sur votre ordinateur. Ouvrez le nouveau cahier dans Colab et utilisez le bouton d’import du volet **Fichiers** pour les placer directement dans `/content`. Saisissez votre numéro étudiant, puis exécutez le cahier.
4. À la fin des cahiers 02 à 04, téléchargez à son tour le JSON produit par la dernière cellule et importez-le dans **S3-PythonVsLLM**. Après une correction, ouvrez le dernier téléchargement et vérifiez votre numéro et la réponse modifiée. Si le navigateur a ajouté `(1)`, rendez au fichier le nom prévu dans le tableau. Remplacez uniquement votre propre ancienne version dans Drive et, si vous l’aviez déjà remise, dans le dossier partagé.

| Séance | À importer dans Colab | À récupérer et à ranger |
|---|---|---|
| [02 · Comparer les fréquences des formes et des lemmes](../notebooks/02_comparer_les_frequences_des_formes_et_des_lemmes.ipynb) | Le TXT nettoyé **ou** le ZIP du 01 | `resultats_02_<numero>.json` |
| [03 · Mesurer les cooccurrences par phrase et par fenêtre](../notebooks/03_mesurer_les_cooccurrences_par_phrase_et_par_fenetre.ipynb) | Le même TXT ou ZIP **et** le JSON du 02 | `resultats_03_<numero>.json` |
| [04 · Vérifier une affirmation par le calcul et la lecture](../notebooks/04_verifier_une_affirmation_par_le_calcul_et_la_lecture.ipynb) | Le même TXT ou ZIP **et** les JSON des 02 et 03 | `resultats_04_<numero>.json` |

**Après le 02.** Ouvrez le JSON téléchargé et retrouvez `numero_etudiant` ainsi qu’une réponse que vous venez d’écrire dans `observations`. Le 03 reprend ce JSON avec le TXT ou le ZIP du 01. Conservez l’original du JSON dans **S3-PythonVsLLM** jusqu’à la remise des trois JSON à la revue du 04.

**Après le 03.** Dans le JSON téléchargé, vérifiez votre `numero_etudiant`, votre `conclusion` et les passages conservés dans `studio → principal → passages`. Rangez `resultats_03_<numero>.json` dans **S3-PythonVsLLM**. Au 04, importez le TXT ou le ZIP du 01 **et** les JSON des 02 et 03. À la revue finale, copiez les trois JSON depuis votre dossier personnel vers le dossier partagé.

### Reprendre vos propres exports d’une ancienne séance

Conservez les fichiers d’origine. Dupliquez vos propres exports dans **S3-PythonVsLLM** et donnez aux copies les noms utilisés par les cahiers actuels.

| Ancien export | Nom de la copie |
|---|---|
| `faguet_nettoye.txt` | `faguet_nettoye_<numero>.txt` |
| `FAGUET_v…_<date>_<session>.zip` | `FAGUET_01_<numero>_<date>_<session>.zip` en conservant la date et le numéro de session d’origine |
| `resultats_02.json`, `resultats_03.json` | `resultats_02_<numero>.json`, `resultats_03_<numero>.json` |

Le numéro ajouté au nom permet d’attribuer votre remise. Les métadonnées historiques restent celles enregistrées à l’époque. Importez dans Colab les copies correspondant à la séance. Vous pouvez ainsi réutiliser les calculs compatibles. Si votre ancien JSON du 03 ne contient pas l’analyse des associations annoncées dans le rapport Studio, reprenez le cahier 03 et exportez son résultat complet avant l’audit du 04.

**À la fin du 04.** Ouvrez le fichier téléchargé `resultats_04_<numero>.json` et retrouvez `numero_etudiant`, `lecture_du_binome` et `conclusion`. Rangez la version vérifiée dans **S3-PythonVsLLM**. Après correction, rouvrez le nouveau téléchargement pour y lire votre dernière réponse avant d’actualiser votre copie de remise.

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
