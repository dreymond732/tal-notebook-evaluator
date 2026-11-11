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

## Les autres notebooks

Le [notebook 02 — audit du nettoyage et mesures lexicales](notebooks/02_mesures_lexicales.ipynb) reprend directement **`/content/analyse_faguet_v2_0_0/faguet_nettoye.txt`** et ses métadonnées. Il teste la réapplication des opérations OP01–OP12 puis calcule les métriques globales, le STTR, cinq champs lexicaux, des marqueurs énonciatifs, des locutions et des mentions orthographiques. Les lemmes exigent un modèle annotant. Les résultats et preuves sont enregistrés dans **`/content/analyse_faguet_n2_v1_0_0/`**.

Les notebooks [03 — relations lexicales](notebooks/03_relations_lexicales.ipynb) et [04 — audit LLM](notebooks/04_audit_llm.ipynb) restent à reprendre ; ils devront utiliser le **même texte nettoyé** et la même provenance. Les cooccurrences détaillées par phrase ou fenêtres ±5/±10 relèvent du notebook 03.

## Développement et vérification

Dans une copie locale du dépôt public :

```bash
cd PT-LLMvsPy
python -m pip install -e ".[test,nlp]"
python -m pytest -q
python scripts/verifier_corpus_td01.py
```

GitHub Actions vérifie aussi l'**installation Git du sous-dossier** depuis le dépôt public, pour reproduire le parcours d'import de Colab.

La documentation détaillée est dans [le guide de lancement](docs/deploiement_colab_drive_td01.md). La provenance de l'import du dépôt d'origine est décrite dans [MIGRATION.md](MIGRATION.md).

## Références méthodologiques

- Manning, C. D., Raghavan, P. et Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press, chapitre 2. https://doi.org/10.1017/CBO9780511809071
- Bird, S., Klein, E. et Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media, chapitre 3. https://www.nltk.org/book/ch03.html
- Sandve, G. K. et al. (2013). *Ten simple rules for reproducible computational research*. PLOS Computational Biology, 9(10), e1003285. https://doi.org/10.1371/journal.pcbi.1003285
