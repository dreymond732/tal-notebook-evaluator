# PT-LLMvsPy — projet d'analyse de corpus (Master 2)

Quatre notebooks et une bibliothèque Python pour vérifier les mesures lexicales, les cooccurrences et les citations proposées par Gemini sur *Le Féminisme* d’Émile Faguet. Revenez aux passages du livre pour discuter l’interprétation du modèle.

**Cet ensemble est maintenant hébergé dans le dépôt public `dreymond732/tal-notebook-evaluator`, sous `PT-LLMvsPy/`.** Le dépôt `dreymond732/PT-LLMvsPy` reste conservé comme origine du développement ; aucune connexion à ce dépôt privé n'est nécessaire pour utiliser cette copie.

[Consulter les sources des enquêtes sur Faguet et les JSON qui en sont tirés](docs/rapports_gemini.md)

## Accès au premier notebook

Créez le dossier **S3-PythonVsLLM** dans **Mon Drive**. [Ouvrez le notebook 01](notebooks/01_preparer_le_corpus_et_mesurer_le_nettoyage.ipynb) dans Colab. Pour conserver vos réponses modifiables, choisissez **Fichier → Enregistrer une copie dans Drive**, rangez la copie dans **S3-PythonVsLLM**, puis ouvrez-la et travaillez dedans. Faites de même pour chaque nouveau cahier.

Le notebook installe les fonctions à partir du **même dépôt public** avec la syntaxe Git de pip pour un sous-dossier Python :

```bash
python -m pip install 'git+https://github.com/dreymond732/tal-notebook-evaluator.git@main#subdirectory=PT-LLMvsPy'
```

La cellule de démarrage résout la référence sélectionnée (`main` ou une branche de test) vers un **SHA Git immuable** et utilise ce SHA à la fois pour la bibliothèque et le document Gemini. Le SHA effectivement utilisé est conservé dans le manifeste de résultats.

La révision `main` fonctionne par défaut ; elle est résolue en commit au démarrage. Les changements de fonctions se testent dans une copie du notebook avec une nouvelle révision.

## Première étape : préparer la source

1. Repérez dans le texte source un appel de note, un séparateur ou un autre élément signalé par l’inventaire.
2. Essayez les règles sur six exemples courts. Écrivez ensuite votre propre exemple, prévoyez le texte obtenu et comparez-le au résultat de la fonction.
3. Appliquez le plan commun à tout le livre et téléchargez le texte nettoyé. Examinez-le dans un éditeur. Retrouvez un passage dans les deux textes et comptez les occurrences du motif que vous avez choisi.
4. Comparez les sept indicateurs calculés avant et après nettoyage. Pour l’un d’eux, relevez les deux valeurs et appuyez votre interprétation sur un passage inspecté.

Le 01 produit dans l’espace temporaire de Colab le TXT nettoyé pour l’inspection et un ZIP qui rassemble le texte, les mesures CSV/JSON, les métadonnées de provenance et les deux fichiers de notes facultatives. Le nom des deux exports porte votre numéro étudiant. Le ZIP porte aussi la date et le numéro de session.

Le corpus source provient du fichier du cours à la révision Git `b92e92b6c216014283056c83aa545881a447b3a5`, SHA-256 **`c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa`**. Le profil de référence produit **446 289 caractères**, SHA-256 **`0885496f4abf4ca9112a3c303f8dc69cb887ffaa34033371aa7c49bad9e38fc2`**.

Le traitement de référence n'est pas présenté comme exempt d'erreurs : les modifications proposées doivent être examinées dans une nouvelle version. Les contre-exemples éventuels seront discutés lors de la revue collective du corpus à utiliser ensuite.

## Du texte nettoyé au dossier d’audit

1. **Au début de chaque cahier**, saisissez le même numéro étudiant, avec ses éventuels zéros initiaux. Dans les noms ci-dessous, `<numero>` représente ce numéro.
2. **Pour garder un résultat**, exécutez la cellule d’export et téléchargez le fichier sur votre ordinateur. Si le téléchargement ne démarre pas, ouvrez le volet **Fichiers** de Colab et choisissez **Télécharger** dans le menu du fichier au chemin affiché. Depuis votre dossier **S3-PythonVsLLM** dans Google Drive, importez le fichier téléchargé. Vérifiez son nom avant de fermer la session Colab.
3. **Pour reprendre dans une nouvelle session**, téléchargez de votre Drive sur l’ordinateur les entrées de la séance indiquées dans le tableau. Dans le volet **Fichiers** du nouveau notebook, importez-les à la racine de `/content` avant d’exécuter les cellules. En local avec Jupyter, placez ces entrées dans le répertoire de travail du cahier.

| Cahier | Entrées à reprendre de votre dossier personnel | Exports à y ranger |
|---|---|---|
| 01 | Le cahier charge les sources du projet. | `faguet_nettoye_<numero>.txt` puis `FAGUET_01_<numero>_<date>_<session>.zip` |
| 02 | Le TXT **ou** le ZIP du 01 | `resultats_02_<numero>.json` |
| 03 | Le TXT ou le ZIP du 01 **et** le JSON du 02 | `resultats_03_<numero>.json` |
| 04 | Le TXT ou le ZIP du 01 **et les deux JSON** des 02 et 03 | `resultats_04_<numero>.json` |

**Deux moments de partage.** À la première revue, copiez le ZIP du 01 depuis **S3-PythonVsLLM** dans le dossier partagé. À la revue du 04, copiez-y les trois JSON des 02, 03 et 04 pour que l’équipe PT puisse reprendre votre contribution avec sa conclusion et ses preuves. Vous pouvez renvoyer au ZIP déjà partagé. [Dossier partagé du projet](https://drive.google.com/drive/folders/18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO)

Lors de la séance précédente, vous avez fait le point sur les [TD1 à TD7](../Notebooks%20TD/S3/README.md#du-bilan-des-td-à-la-première-enquête-sur-faguet), puis ouvert le cahier 01. Pour la revue du 25 novembre, montrez un passage avant et après nettoyage et justifiez votre décision à l’oral, en donnant l’écart mesuré. Les résultats et leur provenance figurent dans votre ZIP. Vous ouvrirez ensuite le 02 avec le texte retenu. Les quatre cahiers fournissent les fonctions Python. Sur un exemple personnel, prévoyez leur résultat, exécutez-les, puis expliquez ce qu’elles mesurent sur le livre.

| Cahier | Essai sur un exemple personnel | Question à résoudre sur Faguet |
|---|---|---|
| [01 · Préparer un corpus et mesurer l’effet du nettoyage](notebooks/01_preparer_le_corpus_et_mesurer_le_nettoyage.ipynb) | Ajoutez à quelques lignes une note ou un appel de note. Prévoyez ce que la règle de nettoyage retirera. | Quels mots comptons-nous encore après nettoyage ? Retrouvez un passage avant et après transformation et comparez les deux versions avec les mêmes indicateurs. Le TXT retenu sert aux trois cahiers suivants. |
| [02 · Comparer les fréquences des formes et des lemmes](notebooks/02_comparer_les_frequences_des_formes_et_des_lemmes.ipynb) | Testez un pluriel, un nombre et une virgule. Comparez les formes en minuscules et les lemmes selon les tokens retenus. | Le volume, les hapax (types attestés une seule fois) et le TTR (types/tokens) dépendent-ils du filtre ? Le STTR compare des blocs complets de même taille. Pour expliquer le gain d’un champ lexical, contrôlez en contexte une forme regroupée par le lemmatiseur. |
| [03 · Mesurer les cooccurrences par phrase et par fenêtre](notebooks/03_mesurer_les_cooccurrences_par_phrase_et_par_fenetre.ipynb) | Dans « droit femme droit », prenez *femme* comme pivot et *droit* comme associé. Comptez les pivots couverts et les paires dans une fenêtre d’un token de chaque côté. Insérez une virgule et recommencez. | Le rapport chiffré transmis le 10 novembre 2026 annonce 208 phrases rapprochant *femme(s)* et *homme(s)*. M4 propose de compter les phrases avec les lemmes *femme* et *droit* et laisse l’effectif à calculer. Comparez l’union des phrases, les fenêtres ±5 et ±10 et les suites contiguës de deux ou trois tokens. Le PMI rapporte la présence commune à celle attendue sous indépendance. Relisez deux passages pour interpréter l’association. |
| [04 · Vérifier une affirmation par le calcul et la lecture](notebooks/04_verifier_une_affirmation_par_le_calcul_et_la_lecture.ipynb) | Testez un intervalle décimal, puis cherchez un mot entier et une citation dans des phrases dont vous connaissez le locuteur. | Les ratios du rapport concordent-ils avec ses propres effectifs et ses unités sont-elles comparables aux vôtres ? Vérifiez ensuite une citation de la transcription et son attribution. Choisissez une enquête sur le sens des mots (polysémie), l’attitude du locuteur (modalisation) ou les voix dans l’énoncé (polyphonie). Confrontez votre lecture à celle d’un binôme. |

Si vous modifiez une réponse, relancez les cellules concernées et la cellule d’export, puis téléchargez et rangez la nouvelle version du JSON. Si le navigateur ajoute `(1)` au nom, ouvrez le dernier téléchargement et vérifiez votre numéro et la présence de votre correction. Remettez ce fichier sous le nom prévu dans le tableau et remplacez uniquement votre propre version antérieure, dans votre Drive puis, si elle a déjà été partagée, dans le dossier partagé.

### Les quatre séances du S3

| Séance de 2026 | Activité | Ce que chacun montre en revue |
|---|---|---|
| 25 novembre · Revue du 01 et lancement du 02 | Présentez le 01 préparé. Comparez les mesures avant et après nettoyage, puis ouvrez le 02 avec le texte retenu. | Retrouvez le même passage dans les deux versions et montrez la copie du ZIP du 01 dans le dossier partagé. |
| 27 novembre · Poursuite et revue du 02 | Prévoir le résultat d’une fonction sur une phrase personnelle, puis regarder ce que changent les filtres et la lemmatisation dans le livre. | Expliquer les entrées de l’appel et l’écart d’effectif à partir d’une occurrence localisée. |
| 16 décembre · 03 | Classer des phrases à la main. Tous comptent sur Faguet les phrases associant *femme(s)* à *homme(s)*. Répartir entre binômes les annonces sur le mariage et le féminisme. Pour M4, déplacer un mot ou ajouter une virgule sur un exemple, puis comparer les fenêtres ±5 et ±10 pour *femme / droit*. Examiner aussi une suite contiguë comme *union libre*. | Distinguer une phrase commune, un pivot couvert, une paire de positions et une suite contiguë. Nommer la convention retenue et présenter deux passages. |
| 18 décembre · 04 | Rouvrir les résultats des 02 et 03, examiner la portée de « toujours », vérifier les mots et l’attribution d’une citation, puis faire relire un passage à un autre binôme. | Confronter les constats aux affirmations de Gemini et justifier sa conclusion individuelle. |

Après la revue du 04, l’équipe du projet tuteuré reprend les contributions de la promotion en janvier et février. Elle regroupe les résultats comparables, rédige la conclusion collective et éprouve un prompt en vérifiant les chiffres et les citations de la nouvelle réponse. [Présentation du projet](../app/static/PT_LLMvsPy_cadrage_projet_tutore.html)

**Observation individuelle.** Annoncer une courte manipulation sans assistance de l’IA, avec les cellules et les fonctions fournies. Demander à chacun d’expliquer une ligne, de prévoir puis d’essayer un autre paramètre, et d’appuyer une conclusion limitée sur un passage retrouvé. Pour le suivi, relever séparément **compte expliqué**, **passage retrouvé**, **variation interprétée** et **conclusion justifiée**. Employer « observé », « à reprendre » ou « non observé » selon ce que l’étudiant a effectivement montré.

## Développement et vérification

Pour préparer le débriefing du 02, la [comparaison des deux versions](docs/reprise_notebook_02.md) situe les tâches déplacées, les références mobilisées et les mesures obtenues sur Faguet.

Pour le 03, la [fiche sur les relations lexicales](docs/reprise_notebook_03.md) met en regard les anciennes et les nouvelles tâches. Elle donne un exemple à compter au tableau, les résultats sur Faguet et les références sur la cooccurrence et le PMI.

Dans une copie locale du dépôt public :

```bash
cd PT-LLMvsPy
python -m pip install -e ".[test,nlp]"
python -m pytest -q
python scripts/verifier_corpus_td01.py
python scripts/verifier_notebook02.py
```

GitHub Actions vérifie aussi l'**installation Git du sous-dossier** depuis le dépôt public, pour reproduire le parcours d'import de Colab.

La documentation détaillée est dans [le guide de lancement](docs/deploiement_colab_drive_td01.md). La provenance de l'import du dépôt d'origine est décrite dans [MIGRATION.md](MIGRATION.md).

La [fiche de préparation du 04](docs/reprise_notebook_04.md) compare les tâches avant et après la reprise, détaille les ratios et donne des repères pour discuter une attribution en TD.

## Références méthodologiques

- Manning, C. D., Raghavan, P. et Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press, chapitre 2. https://doi.org/10.1017/CBO9780511809071
- Bird, S., Klein, E. et Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media, chapitre 3. https://www.nltk.org/book/ch03.html
- Sandve, G. K. et al. (2013). *Ten simple rules for reproducible computational research*. PLOS Computational Biology, 9(10), e1003285. https://doi.org/10.1371/journal.pcbi.1003285
