# S3 — Construire un outil d’audit textométrique

Huit TD de **deux heures** conduisent de la mesure élémentaire à un rapport vérifiable sur une analyse produite par un LLM. Chaque séance comprend plusieurs exemples commentés, des exercices progressifs et un transfert au corpus de Faguet. Les durées sont des budgets de conception ; elles seront ajustées après la première séance en classe.

| Ordre | Cahier exécutable | Objectif et production |
|---|---|---|
| TD0 | [Du texte à une mesure vérifiable](TD0_S3_diagnostic_texte.ipynb) | Réviser Python ; produire des fréquences brutes et expliquer les unités comptées. |
| TD1 | [Annotations spaCy](TD1_S3_fondations_spacy.ipynb) | Lire et contrôler tokens, lemmes, catégories, phrases et positions. |
| TD2 | [Fréquences et filtres](TD2_S3_analyse_corpus.ipynb) | Construire des fonctions réutilisables ; comparer filtres et représentations. |
| TD3 | [Concordances et citations](TD3_S3_concordances_citations.ipynb) | Retrouver les preuves dans le texte original et qualifier les écarts de citation. |
| TD4 | [Cooccurrences](TD4_S3_cooccurrences.ipynb) | Définir les contextes et valider des comptages sur de petits cas contrôlés. |
| TD5 | [Associations](TD5_S3_associations.ipynb) | Distinguer effectif, proportion et force d’association. |
| TD6 | [Visualisations](TD6_S3_visualisations.ipynb) | Observer distributions et sensibilité des résultats aux paramètres. |
| TD7 | [Audit final d’une analyse de LLM](TD7_S3_audit_llm.ipynb) | Assembler un outil reproductible et un rapport d’audit justifié. |

## Démarrer dans Colab

1. Ouvrir dans [Google Colab](https://colab.research.google.com/) la copie distribuée par l’enseignant, issue de `dist/Notebooks TD/S3/` après déploiement. Les sources restent consultables via **Ouvrir un notebook → GitHub** et `dreymond732/tal-notebook-evaluator` ; leur adresse de restitution est un substitut, à remplacer uniquement par le déploiement.
2. Enregistrer sa propre copie, compléter nom, prénom, classe et numéro étudiant, puis suivre les cellules dans l’ordre. La première cellule Markdown et les métadonnées contiennent les mêmes règles du tuteur : il accompagne le raisonnement sans réaliser le travail.
3. Exécuter la préparation fournie : elle installe les versions prévues si nécessaire et récupère les données à un commit fixé. Une connexion est nécessaire au premier téléchargement ; les données locales sont ensuite vérifiées par empreinte. Après une nouvelle session Colab, relancer la préparation.
4. Conserver les sorties et télécharger le notebook ainsi que l’export JSON de fin de séance. Les fichiers laissés seulement dans le runtime Colab sont temporaires. Les séances fournissent leurs données de départ, même si un export précédent manque.

Les résultats automatiques contrôlent des traces enregistrées ; l’enseignant relit les interprétations et les choix méthodologiques.

La dernière cellule affiche le lien de restitution. Elle contient seulement `__TAL_PUBLIC_URL__` dans les sources Git ; `bash deploy.sh` injecte la configuration locale dans les copies distribuées. Les onze supports S3 gardent le contrat de correction v2 : cette revue ajoute des appuis et complète les métadonnées sans changer les questions ni les traces attendues. Les anciennes copies v2 complètes restent compatibles ; les versions antérieures sont refusées avec « mauvaise version du notebook ».

## Données et remédiations

Le dossier [ressources](ressources/README.md) décrit le corpus original fourni, la transcription de la conversation Gemini, les affirmations à auditer et les petits exemples pédagogiques. Les trois prompts forment une conversation progressive. Les estimations du LLM sont des affirmations à vérifier, pas des valeurs de référence.

Les remédiations [R0 — Python et texte](R0_S3_python_texte.ipynb), [R1 — Doc spaCy](R1_S3_doc_spacy.ipynb) et [R2 — Fréquences réutilisables](R2_S3_frequences_reutilisables.ipynb) sont conservées et utilisables selon les difficultés repérées. Elles complètent les huit séances principales.
