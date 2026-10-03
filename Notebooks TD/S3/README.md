# S3 — Construire un outil d’audit textométrique

Neuf TD de **deux heures** conduisent de la mesure élémentaire à un rapport vérifiable sur une analyse produite par un LLM. Les séances comprennent des exemples commentés, des exercices progressifs et des mises en pratique sur de petits textes ou sur le corpus de Faguet. Le TD1B poursuit la découverte de spaCy après TD1 ; les numéros TD2 à TD7 restent inchangés. Les durées sont indicatives : signalez à l’enseignant les étapes qui demandent davantage de temps.

| Ordre | Cahier exécutable | Objectif et production |
|---|---|---|
| TD0 | [Du texte à une mesure vérifiable](TD0_S3_diagnostic_texte.ipynb) | Réviser Python ; produire des fréquences brutes et expliquer les unités comptées. |
| TD1 | [Annotations spaCy](TD1_S3_fondations_spacy.ipynb) | Lire et contrôler tokens, lemmes, catégories, phrases et positions. |
| TD1B | [Entités nommées, similarité et règles](TD1B_S3_entites_similarite_regles.ipynb) | Extraire des mentions, comparer mots et phrases, éprouver des règles ; travail remis pour relecture enseignante, sans note automatique. |
| TD2 | [Fréquences et filtres](TD2_S3_analyse_corpus.ipynb) | Construire des fonctions réutilisables ; comparer filtres et représentations. |
| TD3 | [Concordances et citations](TD3_S3_concordances_citations.ipynb) | Retrouver les preuves dans le texte original et qualifier les écarts de citation. |
| TD4 | [Cooccurrences](TD4_S3_cooccurrences.ipynb) | Définir les contextes et valider des comptages sur de petits cas contrôlés. |
| TD5 | [Associations](TD5_S3_associations.ipynb) | Distinguer effectif, proportion et force d’association. |
| TD6 | [Visualisations](TD6_S3_visualisations.ipynb) | Observer distributions et sensibilité des résultats aux paramètres. |
| TD7 | [Audit final d’une analyse de LLM](TD7_S3_audit_llm.ipynb) | Assembler un outil reproductible et un rapport d’audit justifié. |

## Démarrer dans Colab

1. Ouvrez dans [Google Colab](https://colab.research.google.com/) la copie distribuée par l’enseignant.
2. Enregistrez votre propre copie, complétez votre nom, votre prénom, votre classe et votre numéro étudiant, puis suivez les cellules dans l’ordre. Si vous sollicitez le tuteur, précisez votre hésitation : il accompagne le raisonnement sans réaliser les exercices à votre place.
3. Exécutez la préparation fournie. Une connexion est nécessaire pour installer les outils et télécharger les textes. Si Colab demande un redémarrage, suivez les indications du notebook.
4. Conservez vos sorties et téléchargez votre notebook ainsi que l’export JSON lorsque la séance en prévoit un. Les fichiers laissés seulement dans Colab peuvent disparaître avec la session. Chaque TD fournit les données nécessaires même si un export précédent manque.
5. La dernière cellule affiche le lien de restitution. Utilisez-le pour déposer votre travail avec ses observations.

Les retours automatiques vérifient certains résultats enregistrés ; l’enseignant examine vos interprétations et vos choix de méthode. **TD1B est reçu pour relecture enseignante, sans note automatique.** Les contrôles associés aux TD1 et TD2 conservent leur périmètre actuel : les nouvelles activités du compagnon ne constituent pas des questions supplémentaires dans ces contrôles.

Si le dépôt signale « mauvaise version du notebook », reprenez la copie à jour distribuée par l’enseignant, sans changer vous-même son numéro de version.

## Données et remédiations

Le dossier [ressources](ressources/README.md) décrit le corpus original fourni, la transcription de la conversation Gemini, les affirmations à auditer et les petits exemples pédagogiques. Les trois prompts forment une conversation progressive. Les estimations du LLM sont des affirmations à vérifier, pas des valeurs de référence.

Les remédiations [R0 — Python et texte](R0_S3_python_texte.ipynb), [R1 — Doc spaCy](R1_S3_doc_spacy.ipynb) et [R2 — Fréquences réutilisables](R2_S3_frequences_reutilisables.ipynb) sont conservées et utilisables selon les difficultés repérées. Elles complètent les neuf séances principales. R2 consolide les fonctions et les fréquences après TD1/R1, avant TD2.
