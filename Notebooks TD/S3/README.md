# S3 — Construire un outil d’audit textométrique

Le parcours conduit de la mesure élémentaire à un rapport vérifiable sur une analyse produite par un LLM. Il comprend des exemples commentés, des exercices progressifs et des mises en pratique sur de petits textes ou sur le corpus de Faguet.

## Ordre du parcours

| Ordre | Cahier exécutable | Objectif et production |
|---|---|---|
| TD0 | [Du texte à une mesure vérifiable](TD0_S3_diagnostic_texte.ipynb) | Réviser Python ; produire des fréquences brutes et expliquer les unités comptées. Lire les repères communs pour travailler, utiliser le tuteur et déposer sa copie. |
| R0 | [Python pour le texte](R0_S3_python_texte.ipynb) | Reprendre les manipulations Python avant TD1.a. |
| TD1.a | [Découvrir spaCy et vérifier ses annotations](TD1.a_S3_fondations_spacy.ipynb) | Lire et contrôler tokens, lemmes, catégories, phrases et positions. |
| TD1.b — facultatif | [Reprendre le parcours et la sélection des tokens](TD1.b_S3_doc_spacy.ipynb) | Reprendre la création d’un `Doc`, le parcours de ses tokens et la sélection par catégorie si ces opérations restent difficiles après TD1.a. Sinon, passer directement à TD1.c. |
| TD1.c | [Entités nommées, similarité et règles](TD1.c_S3_entites_similarite_regles.ipynb) | Extraire des mentions, comparer mots et phrases, éprouver des règles et interpréter leurs résultats. |
| R2 | [Fréquences réutilisables](R2_S3_frequences_reutilisables.ipynb) | Consolider les fonctions de comptage et de filtrage avant TD2 ; TD1.b n’est pas un prérequis. |
| TD2 | [Fréquences et filtres](TD2_S3_analyse_corpus.ipynb) | Construire des fonctions réutilisables ; comparer filtres et représentations. |
| TD3 | [Concordances et citations](TD3_S3_concordances_citations.ipynb) | Retrouver les preuves dans le texte original et qualifier les écarts de citation. |
| TD4 | [Cooccurrences](TD4_S3_cooccurrences.ipynb) | Définir les contextes et valider des comptages sur de petits cas contrôlés. |
| TD5 | [Associations](TD5_S3_associations.ipynb) | Distinguer effectif, proportion et force d’association. |
| TD6 | [Visualisations](TD6_S3_visualisations.ipynb) | Observer distributions et sensibilité des résultats aux paramètres. |
| TD7 | [Audit final d’une analyse de LLM](TD7_S3_audit_llm.ipynb) | Assembler un outil reproductible et un rapport d’audit justifié. |

## Démarrer dans Colab

Ouvrez votre copie dans [Google Colab](https://colab.research.google.com/), puis suivez les repères communs présentés au début du TD0. Une connexion est nécessaire pour installer les outils et télécharger les textes. Si Colab demande un redémarrage, suivez les indications du notebook.

Conservez vos sorties et téléchargez votre notebook ainsi que l’export JSON lorsque le TD en prévoit un. Les fichiers laissés seulement dans Colab peuvent disparaître avec la session. Chaque TD fournit les données nécessaires même si un export précédent manque ; vos fonctions restent à reprendre depuis le notebook où vous les avez écrites.

Les critères propres à chaque exercice vous permettent de vérifier les résultats et les interprétations. TD1.c comporte quatre vérifications automatiques ; les interprétations linguistiques restent à examiner à partir des textes et des critères proposés. Les contrôles associés à TD1.a et TD2 conservent leur périmètre : les activités de TD1.c n’y ajoutent pas de questions.

## Données

Le dossier [ressources](ressources/README.md) décrit le corpus original fourni, la transcription de la conversation Gemini, les affirmations à auditer et les petits exemples pédagogiques. Les trois prompts forment une conversation progressive. Les estimations du LLM sont des affirmations à vérifier, pas des valeurs de référence.
