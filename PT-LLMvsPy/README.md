# PT-LLMvsPy — bibliothèque et notebooks de textométrie

Projet tuteuré S3 : confronter des analyses lexicométriques formulées par Gemini aux calculs textuels reproductibles réalisés en Python. Les résultats de LLM sont des **annonces à vérifier**, non un oracle numérique.

## Notebook 01 — architecture de l'analyse

- **GitHub** : bibliothèque commune, code Python testé, notebooks et documents de référence. La maintenance relève de l'enseignant.
- **Colab** : chaque participant conserve sa copie du notebook et définit deux versions : `REVISION_GIT` pour le code et `VERSION_NOTEBOOK` pour l'expérience. Le fichier nettoyé est examiné dans un éditeur avant d'être retenu.
- **Google Drive** : une archive `FAGUET_<identifiant>_v<version>_...zip` conserve les résultats, le journal d'inspection, la révision Git et les métriques original/épuré.

**Important : ce dépôt est encore privé.** Pour que l'installation GitHub anonyme fonctionne dans Colab et qu'aucun jeton GitHub ne soit demandé aux étudiantes, le propriétaire doit **rendre PT-LLMvsPy public** ou publier une copie publique appropriée. Examiner au préalable le contenu du dépôt et ses éventuelles informations internes. Le passage en public n'est pas automatique.

**Dossier de dépôt configuré dans le notebook :** https://drive.google.com/drive/folders/18KPGO5jGPt5f8t_Gq1km79hno4rqy1xO

**Notebook :** [01_corpus_protocole.ipynb](notebooks/01_corpus_protocole.ipynb)

**Guide de mise en service :** [déploiement Colab → Drive](docs/deploiement_colab_drive_td01.md).

## Notebook 01 — inspection et choix de révision

1. **Comprendre** les fonctions, notamment les notes et renvois, les séparateurs et les retours typographiques, à partir de six micro-exemples.
2. **Nettoyer le corpus complet et sauvegarder** un fichier texte à ouvrir dans Bloc-notes ou un autre éditeur.
3. **Inspecter les anomalies** : ancre du texte original, fenêtre, fonction suspectée, comptage d'occurrences du motif, puis décision motivée `conserver` ou `reviser`. Zéro anomalie est possible si l'inspection a été documentée.
4. **Mesurer** avec un même pipeline spaCy et comparer tokens, types, hapax, TTR, proportion d'hapax, phrases et longueur moyenne.

Une révision des fonctions se teste dans une **nouvelle copie** du notebook, avec `VERSION_NOTEBOOK` incrémentée, `REVISION_GIT` mise à jour et `MODE_REVISION='exploration'`. Une sortie expérimentale est identifiée comme telle, sans reprendre l'étiquette de standardisation du résultat de référence.

Le **profil commun** est identifié par faguet-td01-standard-v1 et fourni par [protocole_td01.py](src/tal_toolkit/protocole_td01.py). Il impose le corpus d'origine, l'ordre et les effectifs des transformations, le SHA-256 du texte épuré et les paramètres de mesure.

Corpus Faguet original attendu : SHA-256 **c9832aecd99b11f3c769d11173fd6039a4948a8ee86484658dd8c7a25848a8fa**.

Texte épuré standard : **446 289 caractères**, SHA-256 **0885496f4abf4ca9112a3c303f8dc69cb887ffaa34033371aa7c49bad9e38fc2**. Ces valeurs proviennent du test d'intégration sur le véritable fichier figé, et non des comptes de Gemini.

**Standardisé n'implique pas infaillible** : les paramètres, la version, la provenance et le résultat sont contrôlés, mais l'enseignant demeure responsable de la validation scientifique et de toute correction de la bibliothèque.

## Principaux modules

- [io_corpus.py](src/tal_toolkit/io_corpus.py) — octets d'origine, empreintes et provenance.
- [pretraitements.py](src/tal_toolkit/pretraitements.py) — opérations ordonnées, notes imbriquées, masquages réversibles et journal.
- [epuration.py](src/tal_toolkit/epuration.py) — texte lisible, approbation, table d'alignement source.
- [protocole_td01.py](src/tal_toolkit/protocole_td01.py) — protocole Faguet imposé et contrôles globaux.
- [metriques_globales.py](src/tal_toolkit/metriques_globales.py) et [comparaison_td01.py](src/tal_toolkit/comparaison_td01.py) — métriques et comparaison homogène.
- [inspection_td01.py](src/tal_toolkit/inspection_td01.py) — fenêtres originales, attribution des fonctions par rejeu, comptages des motifs et journal de décision.
- [soumission_td01.py](src/tal_toolkit/soumission_td01.py) — ZIP versionné, journal d'inspection, dépôt Drive par ID et relecture SHA-256.
- [linguistic.py](src/tal_toolkit/linguistic.py), [textometry.py](src/tal_toolkit/textometry.py), [audit_llm.py](src/tal_toolkit/audit_llm.py) — outils réutilisables du semestre.
- [collecter_td01.py](scripts/collecter_td01.py) — synthèse enseignante des archives recueillies.
- [verifier_corpus_td01.py](scripts/verifier_corpus_td01.py) — contrôle de bout en bout sur le vrai texte Faguet.

Les notices Gemini et les prompts expérimentaux restent conservés sous [data](data/) et [docs](docs/), sans mélange entre les comptes globaux de P0 et les intervalles de cooccurrences G1–G6.

## Développement et vérification

Dans un clone autorisé du dépôt :

    python -m pip install -e ".[test,nlp]"
    python -m pytest -q
    python scripts/verifier_corpus_td01.py

La CI GitHub vérifie les tests unitaires, le notebook, les simulations d'upload Drive et le prétraitement de Faguet entier. Elle **ne construit plus de wheel**.

L'authentification et l'upload réels sur Drive doivent être testés depuis un compte Google étudiant doté de droits d'écriture sur le dossier cible ; aucune opération réelle sur ce dossier n'est prétendue validée à ce stade.

## Contribution

Les étudiantes déposent les résultats via Colab. Les corrections du code commun sont examinées séparément par l'enseignant dans des PR GitHub. Voir [CONTRIBUTING.md](CONTRIBUTING.md).

Le notebook 02 antérieur reste temporairement disponible pour l'audit détaillé des annonces Gemini ; le notebook 01 regroupe désormais les prétraitements et la comparaison original/épuré.

**État :** PR #2 fusionnée. Révision pédagogique et cycle d'inspection en [PR #4](https://github.com/dreymond732/PT-LLMvsPy/pull/4). Le dépôt est privé : l'accès GitHub depuis Colab et le dépôt Drive réel restent à tester avant diffusion.
