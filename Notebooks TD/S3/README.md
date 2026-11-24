# S3 — Construire un outil d’audit textométrique

Le parcours conduit de la mesure élémentaire à un rapport vérifiable sur une analyse produite par un LLM. Il comprend des exemples commentés, des exercices progressifs et des mises en pratique sur de petits textes ou sur le corpus de Faguet.

## Ordre du parcours

| Cahier | Notion travaillée | Pourquoi l’essayer sur un texte ? |
|---|---|---|
| [TD0 · Du texte à une mesure vérifiable](TD0_S3_diagnostic_texte.ipynb) | Chaîne d’origine, occurrences, vocabulaire et fréquence brute | Retrouvez à la main un mot répété. Vous pouvez alors expliquer la différence entre le nombre de mots lus et le nombre de formes distinctes. |
| [R0 · Python pour le texte](R0_S3_python_texte.ipynb), si nécessaire | Découpage, minuscules et dictionnaire de fréquences | Reprenez un exemple court pour voir pourquoi deux graphies se retrouvent ou non sous la même entrée. |
| [TD1.a · Fondations spaCy](TD1.a_S3_fondations_spacy.ipynb) | Tokens, lemmes, catégories grammaticales, dépendances et frontières de phrases | Revenez aux caractères d’origine pour vérifier où commence l’unité et si l’annotation convient dans la phrase. |
| [TD1.b · Parcourir un document spaCy](TD1.b_S3_doc_spacy.ipynb), facultatif | Parcours d’un `Doc` et sélection par catégorie | Si le parcours des tokens reste difficile, refaites-le pour les noms, puis pour les verbes. Sinon, passez directement au TD1.c. |
| [TD1.c · Entités, similarité et règles](TD1.c_S3_entites_similarite_regles.ipynb) | Mentions de personnes ou d’organisations, proximité vectorielle et règles de reconnaissance | Vérifiez les mentions reconnues. Comparez deux phrases proches dont la négation change le sens, puis éprouvez une règle sur un autre exemple. |
| [R2 · Fréquences réutilisables](R2_S3_frequences_reutilisables.ipynb), à terminer avant TD2 | Fonction de comptage, noms, lemmes et filtres | Sur le même texte, comparez le classement avant et après l’ajout d’un mot à votre liste d’exclusions. TD1.b reste facultatif. |
| [TD2 · Fréquences et filtres](TD2_S3_analyse_corpus.ipynb) | Formes, lemmes, catégories, exclusions et classement | Modifiez un seul filtre et expliquez pourquoi un mot change de rang. Vous pourrez alors comparer deux listes de fréquences sur une base commune. |
| [TD3 · Concordances et citations](TD3_S3_concordances_citations.ipynb) | Mot ou expression en contexte, recherche exacte ou normalisée, bornes du passage | Retrouvez les mots cités dans le texte d’origine. Si seule une formulation voisine apparaît, relevez la différence avant de juger sa fidélité. |
| [TD4 · Cooccurrences](TD4_S3_cooccurrences.ipynb) | Présence par phrase, union des groupes, répétitions et fenêtre autour d’un pivot | Un mot entouré de deux associés fournit deux paires de positions dans une seule phrase. Précisez l’unité avant d’annoncer un total. |
| [TD5 · Associations](TD5_S3_associations.ipynb) | Dénominateur, marges de présence, proportion conditionnelle et score d’association | Deux mots fréquents peuvent se rencontrer souvent. Comparez leur présence commune à celle attendue sous indépendance et examinez les petits effectifs. |
| [TD6 · Visualisations](TD6_S3_visualisations.ipynb) | Dispersion, segments et carte de chaleur | Relisez un passage dans un segment où le mot est fréquent. Puis faites varier la fenêtre pour mesurer son effet sur les cooccurrences. |
| [TD7 · Audit d’une analyse de LLM](TD7_S3_audit_llm.ipynb) | Affirmation, protocole, recomptage, preuve et verdict | Testez votre moteur sur un corpus nouveau. Dans votre rapport, indiquez ce que vous avez pu vérifier et quelle précision manque à une annonce. |

## Des TD aux quatre cahiers communs

Après le TD7, toute la promotion applique ces méthodes au *Féminisme* de Faguet. Le **01** fixe le texte commun. Le **02** reprend les filtres et les lemmes pour expliquer un écart de décompte. Le **03** reprend les phrases, les fenêtres et les scores pour préciser ce que vous comptez quand deux mots apparaissent ensemble. Le **04** réunit mesures et passages afin de juger un nombre, les mots d’une citation et la voix qui les énonce. Vous retrouverez les dates, les fichiers à reprendre et la remise finale dans le [parcours des quatre cahiers](../../PT-LLMvsPy/README.md#du-texte-nettoyé-au-dossier-daudit).

En janvier et février, l’équipe du projet tuteuré rapproche les conclusions individuelles obtenues selon des conventions comparables, rédige une réponse collective et la confronte à une nouvelle réponse du LLM. [Cadrage du projet tuteuré](../../app/static/PT_LLMvsPy_cadrage_projet_tutore.html)

## Démarrer dans Colab

Ouvrez votre copie dans [Google Colab](https://colab.research.google.com/), puis suivez les repères communs présentés au début du TD0. Une connexion est nécessaire pour installer les outils et télécharger les textes. Si Colab demande un redémarrage, suivez les indications du notebook.

Conservez vos sorties et téléchargez votre notebook ainsi que l’export JSON lorsque le TD en prévoit un. Les fichiers laissés seulement dans Colab peuvent disparaître avec la session. Chaque TD fournit les données nécessaires même si un export précédent manque ; vos fonctions restent à reprendre depuis le notebook où vous les avez écrites.

Les critères propres à chaque exercice vous permettent de vérifier les résultats et les interprétations. TD1.c comporte quatre vérifications automatiques ; les interprétations linguistiques restent à examiner à partir des textes et des critères proposés. Les contrôles associés à TD1.a et TD2 conservent leur périmètre : les activités de TD1.c n’y ajoutent pas de questions.

## Données

Le dossier [ressources](ressources/README.md) décrit le corpus original fourni, la transcription de la conversation Gemini, les affirmations à auditer et les petits exemples pédagogiques. Les trois prompts forment une conversation progressive. Les estimations du LLM sont des affirmations à vérifier, pas des valeurs de référence.
