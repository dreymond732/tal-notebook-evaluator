# PT-LLMvsPy — projet d'analyse de corpus (Master 2)

Quatre notebooks et une bibliothèque Python pour vérifier les mesures lexicales, les cooccurrences et les citations proposées par Gemini sur *Le Féminisme* d’Émile Faguet. Revenez aux passages du livre pour discuter l’interprétation du modèle.

**Cet ensemble est maintenant hébergé dans le dépôt public `dreymond732/tal-notebook-evaluator`, sous `PT-LLMvsPy/`.** Le dépôt `dreymond732/PT-LLMvsPy` reste conservé comme origine du développement ; aucune connexion à ce dépôt privé n'est nécessaire pour utiliser cette copie.

[Consulter les sources des enquêtes sur Faguet et les JSON qui en sont tirés](docs/rapports_gemini.md)

## Ouvrir le cahier de préparation du corpus

Créez le dossier **S3-PythonVsLLM** dans **Mon Drive**. Ouvrez [Préparer un corpus et mesurer l’effet du nettoyage](notebooks/01_preparer_le_corpus_et_mesurer_le_nettoyage.ipynb) dans Colab.

Dans Colab, exécutez la cellule d’initialisation au début de chaque séance. Elle charge la bibliothèque depuis la branche `main` du dépôt public. Pour bénéficier aussi de nouvelles consignes, ouvrez le cahier de la séance depuis le dépôt et conservez vos copies déjà renseignées.

Avec Jupyter, vous pouvez installer la même bibliothèque dans l’environnement de votre noyau avant d’ouvrir le cahier :

```bash
python -m pip install --force-reinstall --no-deps 'tal-toolkit[nlp] @ git+https://github.com/dreymond732/tal-notebook-evaluator.git@main#subdirectory=PT-LLMvsPy'
python -m pip install 'tal-toolkit[nlp]'
```

Ce cahier permet aussi d’utiliser les sources d’un clone local. Son archive conserve le texte nettoyé, le plan appliqué, la branche `main` et les versions du cahier et de la bibliothèque.

## Première étape : préparer la source

1. Repérez dans le texte source un appel de note, un séparateur ou un autre élément signalé par l’inventaire.
2. Essayez les opérations sur six exemples courts. Lisez le code d’une opération avec `print(getsource(retirer_appels_notes))`. Dans `nettoyer`, déplacez une instruction ou insérez un traitement, par exemple `texte = texte.replace("_", "")`. Prévoyez le résultat sur votre exemple, puis vérifiez-le.
3. Appliquez la même fonction `nettoyer` à tout le livre et téléchargez le texte nettoyé. Examinez-le dans un éditeur. Choisissez deux expressions qui encadrent le passage et figurent une seule fois dans chacune des trois versions. Lisez ce qui se trouve entre elles dans l’original, le nettoyage de référence et votre TXT. Comptez votre motif avant et après nettoyage. Le journal détaillé du nettoyage de référence est facultatif.
4. Comparez les sept indicateurs calculés avant et après nettoyage. Pour l’un d’eux, relevez les deux valeurs et appuyez votre interprétation sur un passage inspecté.

Le cahier de préparation du corpus produit dans l’espace temporaire de Colab le TXT nettoyé pour l’inspection et un ZIP qui rassemble le texte, les mesures CSV/JSON, les métadonnées de provenance et les deux fichiers de notes facultatives. Chaque nom de fichier contient votre numéro étudiant. Le ZIP porte aussi la date et le numéro de session.

Le corpus source provient du [fichier du cours](../Notebooks%20TD/S3/ressources/faguet_source.txt) sur `main`. Son empreinte SHA-256 est **`c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa`**. Le profil de référence produit **446 289 caractères**, SHA-256 **`0885496f4abf4ca9112a3c303f8dc69cb887ffaa34033371aa7c49bad9e38fc2`**.

Le traitement de référence n'est pas présenté comme exempt d'erreurs : les modifications proposées doivent être examinées dans une nouvelle version. Les contre-exemples éventuels seront discutés lors de la revue collective du corpus à utiliser ensuite.

## Du texte nettoyé au dossier d’audit

1. **Au début de chaque cahier**, saisissez le même numéro étudiant, avec ses éventuels zéros initiaux. Dans les noms ci-dessous, `<numero>` représente ce numéro.
2. **Pour garder un résultat**, exécutez la cellule d’export et téléchargez le fichier sur votre ordinateur. Si le téléchargement ne démarre pas, ouvrez le volet **Fichiers** de Colab et choisissez **Télécharger** dans le menu du fichier au chemin affiché. Depuis votre dossier **S3-PythonVsLLM** dans Google Drive, importez le fichier téléchargé. Vérifiez son nom avant de fermer la session Colab.
3. **Pour reprendre dans une nouvelle session**, téléchargez de votre Drive sur l’ordinateur les entrées de la séance indiquées dans le tableau. Dans le volet **Fichiers** du nouveau notebook, importez-les à la racine de `/content` avant d’exécuter les cellules. En local avec Jupyter, placez ces entrées dans le répertoire de travail du cahier.

| Cahier | Entrées à reprendre de votre dossier personnel | Exports à y ranger |
|---|---|---|
| Préparer un corpus et mesurer l’effet du nettoyage | Le cahier charge les sources du projet. | `faguet_nettoye_<numero>.txt` puis `FAGUET_01_<numero>_<date>_<session>.zip` |
| Comparer les fréquences des formes et des lemmes | Le TXT nettoyé **ou** son archive ZIP | `resultats_02_<numero>.json` |
| Mesurer les cooccurrences par phrase et par fenêtre | Le TXT nettoyé ou son ZIP **et** `resultats_02_<numero>.json` | `resultats_03_<numero>.json` |
| Vérifier une affirmation par le calcul et la lecture | Le TXT nettoyé ou son ZIP **et** les deux fichiers `resultats_02_<numero>.json` et `resultats_03_<numero>.json` | `resultats_04_<numero>.json` |

**Deux moments de partage.** À la première revue, copiez le ZIP du corpus nettoyé depuis **S3-PythonVsLLM** dans le dossier partagé. À la revue finale, copiez-y les trois JSON des fréquences, des cooccurrences et de l’audit pour que l’équipe PT puisse reprendre votre contribution avec sa conclusion et ses preuves. Vous pouvez renvoyer au ZIP déjà partagé. [Dossier partagé du projet](https://drive.google.com/drive/folders/18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO)

Lors de la séance précédente, vous avez fait le point sur les [TD1 à TD7](../Notebooks%20TD/S3/README.md#du-bilan-des-td-à-la-première-enquête-sur-faguet), puis ouvert *Préparer un corpus et mesurer l’effet du nettoyage*. Pour la revue du 25 novembre, montrez un passage avant et après nettoyage et justifiez votre décision à l’oral, en donnant l’écart mesuré. Les résultats et leur provenance figurent dans votre ZIP. Vous ouvrirez ensuite *Comparer les fréquences des formes et des lemmes* avec le texte retenu. Les quatre cahiers fournissent les fonctions Python. Lisez le code d’une fonction. Prévoyez puis vérifiez son résultat sur un exemple personnel. Modifiez une instruction, comparez les deux résultats et appliquez votre choix au livre.

| Cahier | Essai sur un exemple personnel | Question à résoudre sur Faguet |
|---|---|---|
| [01 · Préparer un corpus et mesurer l’effet du nettoyage](notebooks/01_preparer_le_corpus_et_mesurer_le_nettoyage.ipynb) | Sur le titre `_Féminisme français_`, essayez deux ordres pour la mise entre guillemets et le retrait des `_`. Dans quel ordre le motif entouré de `_` est-il encore présent au moment du remplacement ? | Entre deux expressions repères, comparez le titre et son appel de note dans l’original, la référence et votre TXT. Reliez un écart de comptage à ce que vous avez lu. Le TXT retenu sert aux trois cahiers suivants. |
| [02 · Comparer les fréquences des formes et des lemmes](notebooks/02_comparer_les_frequences_des_formes_et_des_lemmes.ipynb) | Testez les trois filtres communs sur une phrase contenant un pluriel, un nombre et une virgule. Changez ensuite la condition du filtre personnel. Quels tokens garde-t-il ? | Le volume, les hapax (formes ou lemmes attestés une seule fois) et le TTR (nombre d’unités distinctes divisé par le nombre d’occurrences retenues) dépendent-ils du filtre ? Le STTR compare des blocs complets de même taille. Pour expliquer un écart entre formes et lemmes, revenez à une occurrence. Dans la phrase où vous trouvez *droits*, quels mots éclairent son rattachement au champ du droit ? |
| [03 · Mesurer les cooccurrences par phrase et par fenêtre](notebooks/03_mesurer_les_cooccurrences_par_phrase_et_par_fenetre.ipynb) | Dans « droit femme droit », prenez *femme* comme pivot et *droit* comme associé. Comptez les pivots couverts et les paires dans une fenêtre d’un token de chaque côté. Insérez une virgule et recommencez. | Le rapport chiffré transmis le 10 novembre 2026 annonce 208 phrases rapprochant *femme(s)* et *homme(s)*. Recomptez ces phrases dans votre TXT et choisissez-en deux dans votre relevé. Donnez leurs numéros et citez les mots qui permettent de discuter le « toujours » du rapport. La conversation soulève une autre question. Combien de phrases contiennent les lemmes *femme* et *droit* ? Pour ce couple, comparez aussi les paires en fenêtre à deux rayons. Examinez les suites contiguës de deux ou trois tokens. Le PMI rapporte la présence commune à celle attendue sous indépendance. |
| [04 · Vérifier une affirmation par le calcul et la lecture](notebooks/04_verifier_une_affirmation_par_le_calcul_et_la_lecture.ipynb) | Testez un intervalle décimal, puis cherchez un mot entier et une citation dans des phrases dont vous connaissez le locuteur. | Les ratios du rapport concordent-ils avec ses propres effectifs et ses unités sont-elles comparables aux vôtres ? Si vos JSON les contiennent, reprenez votre calcul personnel du 02 et le couple choisi au 03. Cherchez la formulation entière d’une citation de la transcription. Si elle manque, essayez quelques mots repères. Lisez le contexte et citez ce qui permet d’identifier qui parle ou expliquez votre doute. Choisissez une enquête sur le sens des mots (polysémie), l’attitude du locuteur (modalisation) ou les voix dans l’énoncé (polyphonie). Confrontez votre lecture à celle d’un binôme. |

Si vous modifiez une réponse, relancez les cellules concernées, puis celles de la section d’export (les deux dernières cellules de code dans le 02). Ensuite, téléchargez et rangez la nouvelle version du JSON. Si le navigateur ajoute `(1)` au nom, ouvrez le dernier téléchargement et vérifiez votre numéro et la présence de votre correction. Remettez ce fichier sous le nom prévu dans le tableau et remplacez uniquement votre propre version antérieure, dans votre Drive puis, si elle a déjà été partagée, dans le dossier partagé.

### Les quatre séances du S3

| Séance de 2026 | Activité | Ce que chacun montre en revue |
|---|---|---|
| 25 novembre · Du corpus nettoyé aux fréquences | Présentez votre corpus, comparez les mesures avant et après nettoyage, puis ouvrez le cahier sur les fréquences avec le texte retenu. | Montrez le même passage entre vos deux repères dans l’original, la référence et votre TXT. Expliquez votre choix à l’oral et montrez la copie du ZIP dans le dossier partagé. |
| 27 novembre · Comparer les fréquences des formes et des lemmes | Essayez un filtre personnel sur une phrase avant de l’appliquer au livre. | À filtre constant, expliquez un écart entre formes et lemmes. Citez quelques mots de la phrase pour justifier le sens retenu. |
| 16 décembre · Mesurer les cooccurrences par phrase et par fenêtre | Classer des phrases à la main. Tous comptent sur Faguet les phrases associant *femme(s)* à *homme(s)*. Répartir entre binômes les annonces sur le mariage et le féminisme. Pour les lemmes *femme* et *droit*, compter les phrases communes puis comparer les paires de positions aux rayons ±5 et ±10. Examiner aussi une suite contiguë comme *union libre*. | Distinguer une phrase commune, un pivot couvert, une paire de positions et une suite contiguë. Pour discuter le « toujours » du rapport, présenter deux phrases numérotées du relevé *femme(s)/homme(s)* et citer les mots qui étayent la lecture. |
| 18 décembre · Vérifier une affirmation par le calcul et la lecture | Rouvrir les JSON des fréquences et des cooccurrences, examiner la portée de « toujours », vérifier les mots et l’attribution d’une citation, puis faire relire un passage à un autre binôme. | Donner le résultat de la recherche de la citation et, si un passage est retrouvé, citer un indice d’attribution. Justifier sa conclusion individuelle après la lecture du binôme. |

Après la revue finale, l’équipe du projet tuteuré reprend les contributions de la promotion en janvier et février. Elle regroupe les résultats comparables, rédige la conclusion collective et éprouve un prompt en vérifiant les chiffres et les citations de la nouvelle réponse. [Présentation du projet](../app/static/PT_LLMvsPy_cadrage_projet_tutore.html)

**Observation individuelle.** Annoncer une courte manipulation sans assistance de l’IA, avec les cellules et les fonctions fournies. Demander à chacun d’expliquer une ligne, de prévoir puis d’essayer un autre paramètre, et d’appuyer une conclusion limitée sur un passage retrouvé. Pour le suivi, relever séparément **compte expliqué**, **passage retrouvé**, **variation interprétée** et **conclusion justifiée**. Employer « observé », « à reprendre » ou « non observé » selon ce que l’étudiant a effectivement montré.

## Développement et vérification

Pour préparer le débriefing sur les fréquences, la [comparaison des deux versions](docs/reprise_notebook_02.md) situe les tâches déplacées, les références mobilisées et les mesures obtenues sur Faguet.

Pour les cooccurrences, la [fiche sur les relations lexicales](docs/reprise_notebook_03.md) met en regard les anciennes et les nouvelles tâches. Elle donne un exemple à compter au tableau, les résultats sur Faguet et les références sur la cooccurrence et le PMI.

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

La [fiche de préparation de l’audit](docs/reprise_notebook_04.md) compare les tâches avant et après la reprise, détaille les ratios et donne des repères pour discuter une attribution en TD.

## Références méthodologiques

- Manning, C. D., Raghavan, P. et Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press, chapitre 2. https://doi.org/10.1017/CBO9780511809071
- Bird, S., Klein, E. et Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media, chapitre 3. https://www.nltk.org/book/ch03.html
- Sandve, G. K. et al. (2013). *Ten simple rules for reproducible computational research*. PLOS Computational Biology, 9(10), e1003285. https://doi.org/10.1371/journal.pcbi.1003285
