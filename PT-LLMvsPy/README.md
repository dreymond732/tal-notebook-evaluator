# PT-LLMvsPy — projet d'analyse de corpus (Master 2)

Bibliothèque Python et quatre notebooks pour examiner les mesures lexicales annoncées par des LLM sur *Le Féminisme* d'Émile Faguet, puis les comparer à des calculs documentés.

**Cet ensemble est maintenant hébergé dans le dépôt public `dreymond732/tal-notebook-evaluator`, sous `PT-LLMvsPy/`.** Le dépôt `dreymond732/PT-LLMvsPy` reste conservé comme origine du développement ; aucune connexion à ce dépôt privé n'est nécessaire pour utiliser cette copie.

## Accès au premier notebook

Créez le dossier **S3-PythonVsLLM** dans **Mon Drive**. [Ouvrez le notebook 01](notebooks/01_corpus_protocole.ipynb) dans Colab. Pour conserver vos réponses modifiables, choisissez **Fichier → Enregistrer une copie dans Drive**, rangez la copie dans **S3-PythonVsLLM**, puis ouvrez-la et travaillez dedans. Faites de même pour chaque nouveau cahier.

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

Le 01 produit dans l’espace temporaire de Colab le TXT nettoyé pour l’inspection et un ZIP qui rassemble le texte, les mesures CSV/JSON, les observations et les métadonnées de provenance. Le nom des deux exports porte votre numéro étudiant. Le ZIP porte aussi la date et le numéro de session.

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

| Cahier | Essai sur un exemple personnel | Application au texte de Faguet |
|---|---|---|
| [02 — Compter les mots](notebooks/02_mesures_lexicales.ipynb) | Écrire une phrase au singulier et au pluriel, prévoir les unités retenues et comparer les sorties du tokeniseur et du lemmatiseur. | Expliquer un écart de fréquence, vérifier l’annotation d’une occurrence et préparer les deux tâches communes du 03. Les mesures et observations figurent dans `resultats_02_<numero>.json`. |
| [03 — Vérifier les cooccurrences](notebooks/03_relations_lexicales.ipynb) | Inventer des phrases qui distinguent présence, répétition et proximité. Prévoir ce que changera une virgule ou le rayon d’une fenêtre. | Compter les phrases associant *femme(s)* et *homme(s)*. Studio en annonce 208. Examiner les autres associations et séquences du rapport, puis appliquer le protocole *femme / droit* de la conversation M4. Les deux analyses ont des entrées distinctes dans `resultats_03_<numero>.json`. |
| [04 — Auditer les affirmations de Gemini](notebooks/04_audit_llm.ipynb) | Compter à la main, tester un intervalle décimal et prévoir quelles occurrences un mot entier retrouvera dans son propre texte. | Reprendre les ratios du 02 et les passages du 03, examiner la portée de « toujours », vérifier une citation et son attribution, puis confronter deux lectures du cotexte. Le dossier et la conclusion sont sauvegardés dans `resultats_04_<numero>.json`. |

Si vous modifiez une réponse, relancez les cellules concernées et la cellule d’export, puis téléchargez et rangez la nouvelle version du JSON. Si le navigateur ajoute `(1)` au nom, ouvrez le dernier téléchargement et vérifiez votre numéro et la présence de votre correction. Remettez ce fichier sous le nom prévu dans le tableau et remplacez uniquement votre propre version antérieure, dans votre Drive puis, si elle a déjà été partagée, dans le dossier partagé.

### Les quatre séances du S3

| Séance de 2026 | Activité | Ce que chacun montre en revue |
|---|---|---|
| 25 novembre · 01 | Nettoyer le livre, inspecter un passage et comparer les mesures de base avant et après préparation. | Retrouver le passage dans les deux textes et identifier le corpus retenu pour la suite. |
| 27 novembre · 02 | Prévoir le résultat d’une fonction sur une phrase personnelle, puis regarder ce que changent les filtres et la lemmatisation dans le livre. | Expliquer les entrées de l’appel et l’écart d’effectif à partir d’une occurrence localisée. |
| 16 décembre · 03 | Classer des phrases à la main. Tous comptent sur Faguet les phrases associant *femme(s)* à *homme(s)*. Répartir entre binômes les annonces sur le mariage et le féminisme. Pour M4, déplacer un mot ou ajouter une virgule sur un exemple, puis comparer les fenêtres ±5 et ±10 pour *femme / droit*. Examiner aussi une suite contiguë comme *union libre*. | Distinguer une phrase commune, un pivot couvert, une paire de positions et une suite contiguë. Nommer la convention retenue et présenter deux passages. |
| 18 décembre · 04 | Rouvrir les résultats des 02 et 03, examiner la portée de « toujours », vérifier les mots et l’attribution d’une citation, puis faire relire un passage à un autre binôme. | Confronter les constats aux affirmations de Gemini et justifier sa conclusion individuelle. |

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
