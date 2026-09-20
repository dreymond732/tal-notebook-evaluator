# S3 — Contrôles cumulatifs et transfert des acquis

## Décision, périmètre et hypothèses

L'enseignant demande une série de contrôles centrés sur le TD précédent et mobilisant les acquis antérieurs, avec des activités consistantes permettant d'appliquer les compétences dans d'autres contextes. Le premier porte sur TD1 et inclut les bases du TD0. La réalisation comprend **sept nouveaux notebooks**, de `Controle_TD1_S3.ipynb` à `Controle_TD7_S3.ipynb`, dans `Notebooks contrôles finaux/S3/`.

La [matrice préalable](S3_CONTROLES_COVERAGE_MATRIX.md), relue indépendamment avant conception, fixe les objectifs et le transfert. Les TD existants restent inchangés. La durée de 120 minutes par contrôle est une hypothèse de planification reprise des créneaux de TD, et non une durée mesurée. Le barème technique proposé est de 20 points (2 pour Q1 et 3 pour chacune des six suivantes) ; il reste sous décision finale de l'enseignant.

Les notebooks sont des contrôles sommatifs, même si leur fonction pédagogique est de consolider. La résolution se fait sans assistant ; la consolidation passe par le réinvestissement puis par une reprise avec l'enseignant après la passation. Cette série ne fournit ni corrigés étudiants modèles ni correction détaillée accessible pendant le contrôle.

## Organisation commune

Chaque notebook comprend, dans cet ordre :

1. La cellule Markdown gérée par la politique du tuteur, en première position, synchronisée avec les métadonnées.
2. Titre, objectifs, durée prévisionnelle, prérequis, modalités autorisées et limites de la note technique.
3. Identification et préparation fournie : imports déjà rencontrés, installation du modèle si nécessaire, au moins deux jeux de textes pédagogiques originaux et les seules données d'entrée.
4. Sept exercices avec plusieurs demandes liées, cellules de réponse vierges et sortie technique JSON par exercice. La production d'un calcul ne remplace pas la rédaction ou l'examen du texte demandés.
5. Grille humaine annoncée, sauvegarde et dépôt du notebook avec les sorties enregistrées.

Un contrôle n'est pas une copie du TD dont on aurait changé quelques mots : les corpus, situations et demandes de comparaison changent ; les traitements doivent fonctionner sur plusieurs données. Le second contexte nécessite une application effective du code, pas seulement un paragraphe imaginant un usage possible.

Les notes personnelles des TD et les fonctions antérieurement écrites par l'étudiant sont autorisées, à condition d'être adaptées, exécutées et expliquées. Les corrigés et les assistants sont interdits. Les fonctions ne sont pas fournies sous forme de solution dans la préparation. Il n'est pas nécessaire de retrouver un fichier personnel ou une variable d'une précédente session Colab : les données sont embarquées et les fonctions peuvent être reconstruites avec les acquis.

## Définir le problème sans guider sa résolution

Les énoncés fournissent les conventions indispensables à une mesure non ambiguë : unité, corpus, casse, expression contiguë, fenêtre et borne, contexte, agrégation, dénominateur, traitement des valeurs indéfinies, champs de livraison. Ces définitions sont des contraintes du problème.

Ils ne donnent pas l'algorithme, de pseudo-code, de formule nouvelle, d'exemple résolu sur un autre texte, de résultats attendus ou de correction partielle. Une cellule de réponse peut réserver le nom de la variable de livraison ; elle ne doit pas fournir la fonction évaluée. Les imports et l'instruction de sérialisation JSON appartiennent au dispositif de dépôt, pas à une aide à la résolution.

La distinction est vérifiée par la revue pédagogique : demander une comparaison entre deux mesures est une tâche ; expliquer quelle boucle écrire ou quel filtre appliquer est un guidage à supprimer.

## Cumul des prérequis

| Contrôle | Socle utilisable et limites |
|---|---|
| C1 | Python TD0 et spaCy TD1, `displacy`, JSON. Listes, ensembles, dictionnaires, boucles, fonctions ; pas de `Counter`, de WordCloud ou de cooccurrence exigés. |
| C2 | C1 + `Counter`, exclusions et fonctions par POS, contrôle manuel des lemmes, expressions et WordCloud/Matplotlib du TD2. Le pour-mille est illustré dans TD2 mais n'y fait pas l'objet d'un exercice autonome : son calcul obligatoire est réservé au C5. |
| C3 | C2 + concordances, recherche exacte/normalisée, expressions, positions et vérification des citations. La recherche approchée ne constitue pas un acquis obligatoire. |
| C4 | C3 + présence par contexte, marges, union/somme, paires de positions et frontières. Aucun indice d'association ni table 2×2 n'est requis avant le TD5. |
| C5 | C4 + normalisation quantitative, proportions conditionnelles, table 2×2, zéros et indéfinis, sensibilité. La comparaison du taux global avec une moyenne non pondérée de taux attend le C6. Pas de PMI obligatoire. |
| C6 | C5 + représentations de positions, segments mécaniques, cartes de chaleur, matrices, sensibilité, export et retour aux passages. |
| C7 | C6 + moteur d'audit paramétrable, formalisation des affirmations, comparaison sous protocole, transfert sur un jeu indépendant, rapport intégré. |

Aucune bibliothèque supplémentaire, API de LLM ou clé n'est nécessaire. Les données et rapports sont des créations pédagogiques. Le rapport du C7 **simule une réponse de LLM** ; il ne doit pas être attribué à Gemini, à un autre modèle ou à une expérience qui n'a pas eu lieu.

## Contrat scientifique et preuves

Les règles de la [progression S3](S3_AUDIT_SPECIFICATION.md#contrat-scientifique-de-mesure) restent applicables : formes, lemmes et familles sont distingués ; expressions contiguës ; paires et contextes ne sont pas interchangeables ; union et somme restent séparées ; marges et dénominateurs appartiennent au même univers ; division par zéro produit une valeur indéfinie ; indices et tranches permettent le retour au texte source.

Les annotations spaCy sont discutables, même avec un modèle figé. Les contrôles automatiques peuvent vérifier des positions, des comptes sur des données déterministes et des invariants ; ils ne certifient pas l'analyse linguistique. Les justifications doivent faire référence aux passages effectivement fournis.

Au C7, chaque affirmation est appréciée séparément. Un protocole incomplet reste incomplet ; sa reconstruction doit être présentée comme un choix de l'auditeur. Une affirmation complètement définie peut être corroborée ou contredite selon ce protocole. Les données doivent permettre des statuts différents : l'objectif n'est pas d'obtenir systématiquement une réfutation.

## Deux évaluations distinctes

**Score technique automatique /20.** Les sorties enregistrées ont un contrat de types et de contenu. Les traces sont `S3_Cn_Qm:` suivies d'un objet JSON. L'instruction de dépôt et sa sortie doivent appartenir à la même cellule. Le serveur n'exécute pas le code étudiant. Un fichier avec des sorties cohérentes ne garantit ni que ces sorties viennent des fonctions présentes, ni que les fonctions se généralisent. Des contrôles de structure ne doivent jamais être présentés comme une validation scientifique complète.

**Relecture humaine.** La grille suivante utilise les appréciations « maîtrisé », « partiel », « à reprendre » et demande une preuve localisée. Elle n'est pas additionnée automatiquement au score technique et ne produit pas de fausse note globale.

| Critère | Preuve à relire |
|---|---|
| Choix et respect des unités | Définition effectivement appliquée, distinctions forme/lemme/expression, contexte et dénominateur selon le contrôle |
| Mise en œuvre et transfert | Fonctions réutilisées sur les deux contextes, absence de nombres fixés à la main pour simuler un calcul, essais pertinents |
| Contrôle linguistique et documentaire | Annotations discutées, passages et positions vérifiés, citations qualifiées avec prudence |
| Justification des résultats | Explication fondée sur effectifs, paramètres et preuves ; limites reconnues ; pas d'inférence d'opinion à partir d'une fréquence |
| Représentation et restitution | Lisibilité des tableaux et figures requis, axes et unités, cohérence avec leurs données, rapport traçable |

L'absence d'une sortie technique n'empêche pas l'enseignant de lire une démarche pertinente ; inversement, un score technique complet ne suffit pas à valider les critères humains. Les graphiques, raisonnements et contre-exemples ne sont pas évalués par la longueur d'un commentaire ou la présence de mots-clés.

Le rapport détaillé de correction et la grille de relecture restent du côté enseignant ; le dépôt étudiant ne doit pas révéler des valeurs de référence, comparaisons détaillées ou critères permettant de reconstruire une solution pendant la passation. Les limites du dépôt et la réussite de la réception peuvent être indiquées sans divulguer la correction.

## Tuteur et passation

Les sept profils portent `activity: "controle"` dans `tutor_sessions.json`. La politique `CONTROL_RULES` s'applique à chacun. Les instructions sont injectées dans les métadonnées et dans la cellule Markdown dédiée en tout début du notebook : aucune aide, aucun quiz, aucun indice, aucune explication ou génération/modification de code pendant le contrôle. Cette règle s'applique également à une question formulée sans mentionner le contrôle.

Ces instructions expriment le comportement attendu ; elles ne constituent pas un verrou technique sur un service tiers. Les modalités de passation doivent donc être explicites et l'enseignant conserve la responsabilité de l'organisation de l'évaluation. Aucun notebook ne promet qu'une instruction Markdown empêchera toute assistance extérieure.

## Critères de livraison et risques résiduels

Sont attendus : sept notebooks valides et sans sorties préremplies ; sept profils de tuteur cohérents ; sept correcteurs reliés aux routes, templates et persistance ; contrôle de compatibilité marqueurs/types/barèmes ; absence d'exécution serveur ; revue indépendante pédagogique et technique ; gouvernance.

Le contrôle statique et les essais des correcteurs ne constituent pas une passation dans Colab, une observation du temps réel en classe ni une validation d'une copie étudiante modèle. Ces points ne doivent pas être déclarés réussis s'ils n'ont pas été réalisés. La lisibilité des modèles linguistiques, le temps d'installation et l'intégration des réponses complexes demandent une vigilance particulière lors de la première utilisation.
