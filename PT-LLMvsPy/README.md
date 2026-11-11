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

En cas d'essai sur la branche de migration, renseigner temporairement `REVISION_GIT = "feat/pt-llmvspy-colab-integrated"`. Après sa fusion, la référence `main` fonctionne par défaut.

## Première étape : préparer la source

1. Découvrir les fonctions sur des exemples courts.
2. Nettoyer le **texte Faguet intégral** et télécharger une première version lisible.
3. Examiner le fichier dans Bloc-notes ou un autre éditeur, puis relever les éventuelles anomalies dans le texte original et estimer leur fréquence avec un motif défini.
4. Choisir de **conserver ou réviser**, puis calculer les sept métriques lexicales de base sur l'original et le texte préparé.

Les sorties sont conservées avec la version du notebook, la révision Git des fonctions, les paramètres spaCy, les empreintes du texte et le journal d'inspection.

Le corpus source provient du fichier du cours à la révision Git `b92e92b6c216014283056c83aa545881a447b3a5`, SHA-256 **`c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa`**. Le profil de référence produit **446 289 caractères**, SHA-256 **`0885496f4abf4ca9112a3c303f8dc69cb887ffaa34033371aa7c49bad9e38fc2`**.

Le traitement de référence n'est pas présenté comme exempt d'erreurs : les modifications proposées doivent être examinées dans une nouvelle version. L'examen des contre-exemples précède la décision collective sur le corpus à utiliser ensuite.

## Dépôt des résultats

Le notebook envoie une archive de travail individuelle vers le [dossier Google Drive partagé](https://drive.google.com/drive/folders/18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO) après une autorisation Google explicite. Les fichiers sont contrôlés et l'archive locale reste disponible si le dépôt échoue.

L'accès au dossier exige un droit de contribution Google Drive ; il ne découle pas de l'accès au dépôt GitHub.

## Les autres notebooks

Les notebooks [02 — mesures lexicales](notebooks/02_mesures_lexicales.ipynb), [03 — relations lexicales](notebooks/03_relations_lexicales.ipynb) et [04 — audit LLM](notebooks/04_audit_llm.ipynb) sont importés avec l'historique du projet, **mais leur définition et leur chargement des données restent à reprendre**. Ils devront tous travailler sur le **corpus épuré validé** à l'issue du notebook 01.

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
