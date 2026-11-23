# PT-LLMvsPy — projet d'analyse de corpus (Master 2)

Bibliothèque Python et quatre notebooks pour examiner les mesures lexicales annoncées par des LLM sur *Le Féminisme* d'Émile Faguet, puis les comparer à des calculs documentés.

**Cet ensemble est maintenant hébergé dans le dépôt public `dreymond732/tal-notebook-evaluator`, sous `PT-LLMvsPy/`.** Le dépôt `dreymond732/PT-LLMvsPy` reste conservé comme origine du développement ; aucune connexion à ce dépôt privé n'est nécessaire pour utiliser cette copie.

## Accès au premier notebook

[Ouvrir / télécharger le notebook 01](notebooks/01_corpus_protocole.ipynb). Dans Colab, utiliser *Fichier → Importer un notebook*, puis conserver une copie personnelle dans votre Drive.

Le notebook installe les fonctions à partir du **même dépôt public** avec la syntaxe Git de pip pour un sous-dossier Python :

```bash
python -m pip install 'git+https://github.com/dreymond732/tal-notebook-evaluator.git@main#subdirectory=PT-LLMvsPy'
```

La cellule de démarrage résout la référence sélectionnée (`main` ou une branche de test) vers un **SHA Git immuable** et utilise ce SHA à la fois pour la bibliothèque et le document Gemini. Le SHA effectivement utilisé est conservé dans le manifeste de résultats.

La révision `main` fonctionne par défaut ; elle est résolue en commit au démarrage. Les changements de fonctions se testent dans une copie du notebook avec une nouvelle révision.

## Première étape : préparer la source

1. Découvrir les fonctions sur des exemples courts.
2. Nettoyer le **texte Faguet intégral** et télécharger une première version lisible.
3. Examiner le fichier dans Bloc-notes ou un autre éditeur, puis relever les éventuelles anomalies dans le texte original et estimer leur fréquence avec un motif défini.
4. Calculer les sept métriques lexicales de base sur l'original et le texte préparé. Les observations et les éventuelles corrections n'interrompent pas les calculs.

**Les résultats sont enregistrés dans `/content/analyse_faguet_v2_0_0/`** pour la version 2.0.0. Le dossier contient le texte nettoyé, les mesures CSV/JSON, les notes éventuelles et les métadonnées de provenance. L'archive ZIP est identifiée par une date et un nombre aléatoire, sans identifiant étudiant.

Le corpus source provient du fichier du cours à la révision Git `b92e92b6c216014283056c83aa545881a447b3a5`, SHA-256 **`c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa`**. Le profil de référence produit **446 289 caractères**, SHA-256 **`0885496f4abf4ca9112a3c303f8dc69cb887ffaa34033371aa7c49bad9e38fc2`**.

Le traitement de référence n'est pas présenté comme exempt d'erreurs : les modifications proposées doivent être examinées dans une nouvelle version. Les contre-exemples éventuels seront discutés lors de la revue collective du corpus à utiliser ensuite.

## Dépôt des résultats

Le notebook monte votre Drive avec `drive.mount()`. Il reste à repérer le [dossier Google Drive partagé](https://drive.google.com/drive/folders/18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO), puis à renseigner son chemin dans `DOSSIER_DEPOT_DRIVE`. L'archive est copiée avec vérification SHA-256 et reste disponible dans `/content` si le dépôt échoue.

L'accès au dossier exige un droit de contribution Google Drive ; il ne découle pas de l'accès au dépôt GitHub.

## Du texte nettoyé au dossier d’audit

Dans Colab, créez **Mon Drive → PT-Faguet** et placez-y le fichier `faguet_nettoye.txt` ou l’archive ZIP du 01. Les trois notebooks utilisent ce dossier personnel, y compris d’une séance à l’autre. Si le texte ou l’archive se trouve ailleurs, indiquez son chemin dans **SOURCE_01**. Pour travailler dans un autre dossier de résultats, utilisez le même **DOSSIER_PERSONNEL** dans les trois cahiers. Ouvrez chaque cahier dans sa propre session. Si vous rattachez le 02 à un noyau qui a déjà importé la bibliothèque du 01, redémarrez ce noyau avant la première cellule. En local, le dossier par défaut est `PT-Faguet/` dans le répertoire de travail de Jupyter.

| Cahier | Manipulation | Trace sauvegardée par la dernière cellule |
|---|---|---|
| [02 — Compter les mots de Faguet](notebooks/02_mesures_lexicales.ipynb) | Prévoir un compte sur une phrase, comparer formes et lemmes à filtre constant, puis relire un emploi dans le livre. | `resultats_02.json` contient les mesures, les observations et le couple de mots proposé pour le 03. |
| [03 — Relations lexicales](notebooks/03_relations_lexicales.ipynb) | Classer des phrases à la main, retrouver deux mots dans Faguet, changer une convention de comptage et interpréter les passages. | `resultats_03.json` contient la question, les unités, les effectifs, les positions des passages et la conclusion. |
| [04 — Audit de Gemini](notebooks/04_audit_llm.ipynb) | Examiner un chiffre, vérifier une citation, puis enquêter sur un problème de sens en confrontant deux lectures. | `resultats_04.json` rassemble les pièces examinées, les contextes et le jugement argumenté. |

La dernière cellule actualise le JSON du cahier. Pour conserver le travail personnel, renseignez les champs de réponse puis relancez les cellules concernées et la sauvegarde. Ces trois JSON sont des fichiers de travail personnels. La procédure de dépôt collectif décrite plus haut concerne l’archive du 01.

### Quatre temps de TD en classe

| Temps | Activité | Ce que l’étudiant peut montrer |
|---|---|---|
| 1 · Du 01 au 02 | Compter les unités d’une phrase sur papier, puis comparer avec l’affichage. Sur Faguet, retrouver une graphie dont le découpage mérite discussion. | Expliquer ce qui entre dans un compte et montrer la graphie dans le texte. |
| 2 · Commencer le 03 | Trier individuellement les phrases du microcorpus dans les quatre cases. Comparer les classements en binôme puis appliquer la même règle au couple choisi au 02. | Expliquer pourquoi une phrase où le pivot apparaît deux fois contribue une seule fois à l’effectif des phrases communes. |
| 3 · Interpréter le 03 | Un étudiant change le rayon, l’autre prédit l’effet. Inverser les rôles pour la ponctuation. Échanger une conclusion et le passage censé l’étayer. | Nommer le paramètre changé, donner les deux effectifs avec leur unité et retrouver un indice qui soutient ou limite la lecture. |
| 4 · Conduire le 04 | Examiner ensemble un chiffre et les conditions du calcul. Chaque binôme vérifie ensuite une citation et choisit une enquête sur le sens. Un second binôme relit un extrait avant la conclusion individuelle. | Distinguer une valeur comparable, une méthode annoncée et une citation retrouvée, puis expliquer ce que le passage permet de conclure. |

**Observation individuelle.** Annoncer une courte manipulation sans assistance de l’IA, avec les cellules et les fonctions fournies. Demander à chacun d’expliquer une ligne, de prévoir puis d’essayer un autre paramètre, et d’appuyer une conclusion limitée sur un passage retrouvé. Pour le suivi, relever séparément **compte expliqué**, **passage retrouvé**, **variation interprétée** et **conclusion justifiée**. Employer « observé », « à reprendre » ou « non observé » selon ce que l’étudiant a effectivement montré.

## Développement et vérification

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

## Références méthodologiques

- Manning, C. D., Raghavan, P. et Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press, chapitre 2. https://doi.org/10.1017/CBO9780511809071
- Bird, S., Klein, E. et Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media, chapitre 3. https://www.nltk.org/book/ch03.html
- Sandve, G. K. et al. (2013). *Ten simple rules for reproducible computational research*. PLOS Computational Biology, 9(10), e1003285. https://doi.org/10.1371/journal.pcbi.1003285
