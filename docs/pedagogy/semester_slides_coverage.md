# Diaporamas de semestre — cadrage et couverture S1/S2

## Mission, référence et statut

TAL-Prof, 8 octobre 2026. Branche `pedagogy/semester-overview-slides`, référence technique examinée `590b9a6c78fc6b27f8985e060c6ea2325367f652` (`origin/main`). Mission : compléter les présentations d’organisation et de progression S1 et S2 sur le modèle du diaporama S3 validé. Aucun notebook, correcteur, barème, route, politique de tuteur ou ordre d’apprentissage n’est modifié. Les diaporamas sont des cartes du parcours : ils ne remplacent pas les exercices, exemples, essais ni consignes des notebooks. Le statut de chaque ligne ci-dessous est **CONSERVÉ**, avec condensation de la seule présentation générale ; aucune activité n’est supprimée ou rendue optionnelle.

Sources primaires relues : notebooks actifs du catalogue `app/notebook_catalog.json`, modes et évaluateurs de `app/routes.py`, modules `app/app_correction_TD*_S1.py`, `app/app_correction_TD*_S2.py`, `app/app_correction_DM_intermediaire_S1.py`, `app/app_correction_controle_S1.py`, `app/app_correction_devoirMaisonS2.py`, moteurs `app/s1_revision.py` et `app/s2_revision.py`, références `app/s1_reference.py` et `app/s2_reference.py`. L’annexe fournit chaque chemin, cellule et question. Les anciens cadrages `s1_progression_v2_coverage.md`, `s2_complete_review_coverage.md` et `dm_s1_intermediaire_spec.md` documentent la continuité historique ; les constats actuels sont pris dans les fichiers à la révision ci-dessus. Il ne s’agit pas d’une révalidation des notebooks historiques.

Statut : **ACCEPT préalable — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**, rendu le 8 octobre 2026 par TAL-Pedagogy-Reviewer (`semester_ped_review`) après lecture intégrale et confrontation aux sources. Cette validation autorise la conception des synthèses ; elle ne vaut ni validation des diapositives futures ni révalidation des 233 questions. Le Designer ne transforme pas cette déclaration en son propre verdict. Le diaporama S3 et son lien Drive unique sont conservés ; aucun lien Drive S1/S2 n’a été fourni, donc aucun ne doit être inventé.

## Contrat de présentation étudiante

Chaque TD actif dispose d’un passage propre : vrai titre ou titre court fidèle avec numéro historique, objectif concret, acquis mobilisés, production représentative, lien à l’étape suivante et portée réelle du correcteur. Les DM et contrôles apparaissent à leur place pédagogique, avec leur finalité et leurs conditions d’autonomie. Une vue d’ensemble relie ces étapes. La finalité S1 est de construire, vérifier et expliquer de petits traitements de texte ; S2 explicite les algorithmes et construit une ressource vérifiable ; S3 pourra confronter ces conventions aux bibliothèques TAL et auditer les résultats.

Le support visible s’adresse aux étudiants : ni identifiants de correcteur, métadonnées, GitHub/PR, chemins de maintenance, versions de déploiement, ni notices d’identification. Aucun minutage. Les données, productions et cas limites sont évoqués au niveau nécessaire à l’orientation, sans recopier tout le questionnaire ni donner les réponses. Pas de nouvelle bibliothèque promise. Montrer ce qui est à conserver et à réutiliser (fonctions, conventions de nettoyage, lexiques, fichiers relus, traces utiles) et distinguer les reprises ciblées des approfondissements sans imposer de durée. Les points ci-dessous sont un inventaire technique documentaire : leur affichage dans les diapositives n’est pas nécessaire. Ne pas transformer un score technique de TD en note globale de maîtrise.

S1 : TD1 → TD2 → TD3 → TD4 → TD5 → DM intermédiaire → TD6 → TD7 → contrôle de synthèse. La position du DM est explicitement donnée par son sujet ; la synthèse de fin de S1 réinvestit les fondamentaux et les fichiers sans prétendre évaluer toutes les regex.

S2 : TD3 → contrôle historique TD2 → TD5 → contrôle historique TD4 et DM d’approfondissement → TD6. La succession TD4 puis DM est une présentation pratique, pas l’invention d’une dépendance supplémentaire : tous deux prennent place après TD5. TD3 et TD5 ont chacun deux séances accompagnées, TD6 une ; cette répartition peut être mentionnée sans durée. Ne créer ni TD1 ni six TD successifs. Le contrôle final S2 est archivé/inactif et reste hors parcours distribué.

## Matrice source → diaporama S1

Les sources S1 sont les notebooks énumérés intégralement dans l’annexe. Tous les exercices, données, niveaux d’autonomie et essais restent dans leur support d’origine immédiatement disponible ; aucun déplacement d’activité vers les slides.

| Source | Acquis, notions et activité obligatoire à représenter | Production et finalité | Cible, statut |
|---|---|---|---|
| TD1 — Variables, types et premières expressions ; Q1–Q6 | Débuter dans le notebook ; affectation/calcul, type, comparaison et conjonction, f-string, conversion, longueur/appartenance ; prédire puis exécuter | Coût de traduction, annonce, description d’une phrase personnelle ; relier valeur, type et expression | Passage TD1 et méthode de travail, CONSERVÉ |
| TD2 — Chaînes et séquences ; Q1–Q7 et traces Qnb | Réutiliser TD1 ; nettoyer en gardant la source, transformer, indexer/trancher, split/join, vérifier plusieurs chaînes sans boucle | Texte transformé, fragments et reconstruction ; expliquer pourquoi un découpage par espaces ne suffit pas à définir les mots | Passage TD2, CONSERVÉ |
| TD3 — Collections : listes, tuples, dictionnaires et ensembles ; Q1–Q6 | Réutiliser chaînes/listes ; mutation de liste, référence tuple, lexique, premier parcours for/items, occurrences versus formes, intersection/différence | Lexique bilingue et comparaison de vocabulaires ; choisir une structure adaptée | Passage TD3, CONSERVÉ |
| TD4 — Boucles, conditions et comptages ; Q1–Q7 | Réutiliser collections et premier for ; transformer/filtrer, bornes range, arrêt while, compter par dictionnaire, compréhension | Liste filtrée et fréquences ; rendre explicites répétition, décision et arrêt | Passage TD4, CONSERVÉ |
| TD5 — Fonctions et réutilisation du code ; Q1–Q6 | Réutiliser TD1–4 ; paramètres/return, normalisation, cas vides/inconnus, composition, paramètre par défaut dans l’essai | Fonctions de traduction mot à mot et résumé textuel ; distinguer afficher et retourner, réutiliser les paramètres | Passage TD5, CONSERVÉ |
| DM intermédiaire — Une bibliothèque prépare ses ateliers ; Q1–Q18 | Après TD5 ; travail individuel autonome sur TD1–5, cours/TD/notes autorisés, aucune assistance IA/tuteur ; cinq parties budget/annonces/ressources/automatisation/fonctions | Résoudre une situation nouvelle, expliquer bornes/choix et composer un outil ; ni import ni fichier requis | Jalon DM après TD5 et avant TD6, CONSERVÉ |
| TD6 — Lire, transformer et écrire des fichiers ; Q1–Q6 | Réutiliser fonctions/collections ; UTF-8, fermeture avec with, lignes, split limité, normalisation et dédoublonnage, CSV avec relecture | Transformer des affiliations en données structurées et vérifier le fichier produit ; csv introduit ici, pathlib fourni | Passage TD6, CONSERVÉ |
| TD7 — Motifs, expressions régulières et pipeline ; Q1–Q7 | Réutiliser fonctions et comptage ; re/search/findall/sub, classes/accents, dates formelles, ordre des transformations | Nettoyage puis extraction et fréquences ; identifier une limite linguistique et l’information manquante | Passage TD7 et transition S2, CONSERVÉ |
| Contrôle S1 — fondamentaux Python et TAL ; Q1–Q30 | Réinvestir variables/chaînes, listes/itérations, dictionnaires/conditions, fonctions/modularité et synthèse/fichiers ; corriger du code erroné/incomplet en autonomie | Vérifier rigueur syntaxique et algorithmique ; ne pas présenter une validation complète de toutes les compétences du semestre | Jalon de synthèse S1, CONSERVÉ |

## Matrice source → diaporama S2

| Source et vrai titre | Acquis, notions et activités obligatoires à représenter | Production et finalité | Cible, statut |
|---|---|---|---|
| TD3 - S2 ; sous-titre source « Parcours S2 — algorithmique et structures » ; Q1–Q30 | Acquis S1 ; conversions/indices/bornes, collections/compréhensions, fonctions/tri/ensembles/exceptions, factorielle/recherche/récursion/Euclide, bigrammes/statistiques/complexité ; ateliers anagrammes, aplatissement, Fibonacci et ensembles | Corriger, tester et expliquer un algorithme ; passer de l’instruction isolée à un traitement réutilisable | Passage TD3 couvrant ses deux parties, CONSERVÉ |
| Contrôle S2 : renforcement et algorithmique (historique TD2) ; Q1–Q13 | Après TD3 et ateliers ; chaînes/listes, logique/dictionnaires, boucles imbriquées, Fibonacci, anagrammes, compréhension conditionnelle | Transférer en autonomie les acquis consolidés ; le numéro TD2 ne fixe pas l’ordre | Jalon après TD3, CONSERVÉ |
| TD5 : Approfondissement et algorithmique avancée ; Q1–Q25 | Après TD3 ; compréhensions, chaînes/logique, structures imbriquées/tri/fréquences, tokenisation et stopwords, n-grammes/Jaccard/TF, produit scalaire/préfixe commun/comptage/pipeline ; atelier transposition | Assembler et comparer des algorithmes de texte avec conventions explicites ; pas de promesse de « compréhension » du langage | Passage TD5 couvrant les cinq parties, CONSERVÉ |
| Contrôle S2 : manipulation des ensembles (historique TD4) ; Q1–Q14 | Après TD5 ; unicité/appartenance, intersection/union/différences/inclusion, recherche/nettoyage/absents, Jaccard et pangramme | Choisir et expliquer l’intérêt des ensembles dans des algorithmes textuels | Jalon après TD5, CONSERVÉ |
| Devoir maison intermédiaire d’approfondissement ; Q1–Q30 | Après TD5 et atelier transposition ; bases puis compréhensions, boucles imbriquées, fréquences, zip/inversion/transposition/intersection/factorielle ; toutes les questions obligatoires, tuteur sans aide | Réinvestir S1/S2 en autonomie et traiter de nouveaux cas ; pas de notion de fichier exigée avant TD6 | Jalon après TD5, CONSERVÉ |
| TD6 : Manipulation de Fichiers et Ressources Linguistiques ; Q1–Q10 | Après TD3/TD5 ; fichiers S1, chaîne brut→normalisation→tokens→filtrage→fréquences→CSV relu ; boucles/conditions/méthodes de chaînes, sans regex ni Counter | Construire un lexique de fréquences traçable sur corpus fourni ; conserver le brut, relire l’export et interpréter les choix | Passage TD6 et transition S3, CONSERVÉ |
| Contrôle Final S2 : Algorithmique et Fichiers ; Q1–Q18 | Archive recensée ; aucun correcteur actif, hors distribution | Aucune épreuve supplémentaire annoncée ni dépôt activé | Archive maintenue dans cette documentation, hors parcours actif ; CONSERVÉ |

Attention scientifique dans le résumé TD5 : Q24 est intitulée historiquement « Matrice de co-occurrence (simplifiée) » mais demande le comptage des mots d’un vocabulaire dans un contexte, sans paire ni fenêtre ; les diapositives doivent dire « comptage dans un contexte » ou expliciter cette limite, sans prétendre qu’une vraie matrice de cooccurrences a été construite. Le TD6 S2 construit une ressource de fréquences et non une analyse linguistique exhaustive. Dans TD3, seul Q22 nécessite `math` ; la présence d’un import Counter n’autorise pas son emploi partout.

## Portée du correcteur, à décliner par TD

Fond commun à dire simplement : le serveur lit le code et les résultats enregistrés ; il n’exécute pas les programmes. Un résultat reconnu donne un retour technique sur les cas fournis, pas une preuve de généralité, d’auteur, de fraîcheur des sorties ou de compréhension. Les explications demandent une lecture humaine. Les copies peuvent contenir une solution valable non reconnue ; l’enseignant peut la réexaminer. En TD le retour est formatif ; en contrôle/DM le retour étudiant est un accusé de dépôt, sans rapport détaillé public.

| TD | Ce qui est réellement vérifié | Limite propre à faire comprendre |
|---|---|---|
| S1 TD1 | Valeurs/types et constructions requises ; Q6 longueur et présence de TAL reliées à la phrase enregistrée | Une phrase et des cas enregistrés ne prouvent ni tous les calculs possibles ni l’interprétation correcte des types |
| S1 TD2 | Deux traces par question, résultat/type/ordre et manipulation ; Q1–6 deux demi-points ; Q7 découpage et présence du commentaire | Le sens de l’interprétation sur mots/fragments n’est pas noté automatiquement |
| S1 TD3 | États liste, tuple et justification présente, lexique et parcours, ensembles et opérations | Une justification présente ne prouve pas le bon choix de structure ; ordre des ensembles sans importance |
| S1 TD4 | Sorties des transformations/filtres/boucles/comptages et constructions locales attendues | Le score ne garantit pas arrêt ou bonnes bornes sur d’autres entrées ; conserver prédiction et tests |
| S1 TD5 | Appels/retours et traces des fonctions, normalisation, traduction et composition | Aucun test exécuté par le serveur ; généralité des fonctions et traduction linguistique non certifiées |
| S1 TD6 | Traces de lecture, lignes, normalisation, affiliations et contenu CSV enregistré ; indices de lecture/écriture | Le serveur n’ouvre pas les fichiers étudiants : l’export et sa relecture doivent réellement être faits dans le notebook |
| S1 TD7 | Traces de recherche/extraction/remplacement/pipeline ; Q3 commentaire présent ; Q7 présence seulement | Qualité de la limite linguistique et pertinence de l’interprétation à relire ; date formelle ≠ validité calendaire |
| S2 TD3 | 30 traces typées, certaines constructions explicites (while, fonction, récursion, recherche sans in, boucles imbriquées) et valeurs | Le score ne démontre ni complexité réelle ni correction de tous les cas limites, ni qualité des explications |
| S2 TD5 | 25 valeurs de référence ; compréhensions explicitement repérées Q1–2, calcul relié à l’affichage pour beaucoup d’autres questions | Ne pas prétendre que chaque stratégie algorithmique est intégralement contrôlée ; comparer choix de tokenisation, n-grammes et mesures soi-même |
| S2 TD6 | 10 questions, lecture/écriture repérées, fréquences, aperçu CSV et toutes lignes Q9b, tri et en-tête Q10b | Le serveur n’ouvre aucun fichier ; traces et structure de code ne garantissent pas un fichier réellement actuel ni tout autre corpus |

Sources exactes de cette section : `app/s1_reference.py:CHECKS`, `app/app_correction_TD2_S1.py:check_notebook`, `app/s2_reference.py:SYNTAX`, `SPECIAL_VALUES`, `CHECKS`, et les moteurs `check_s1`/`check_s2`. Le DM S1 réclame une relecture du raisonnement, des cinq explications Q2/Q6/Q12/Q14/Q17, des tests et de la généralité des fonctions ; son /20 technique n’est pas une note globale.

## Notes de barème et anomalies préexistantes — documentation seulement

- TD S1 : maxima 6, 7, 6, 7, 6, 6 et 7 points ; 45 questions principales. Les traces complémentaires et essais ne créent pas de questions ou points supplémentaires.
- DM S1 : 18 questions, Q1–14 à 1 point, Q15–18 à 1,5 point, total technique 20 ; points partiels selon résultats vérifiés.
- TD S2 : TD3 30 questions/30 points ; TD5 25/25 ; TD6 10/20. Contrôles TD2 13/20, TD4 14/40 ; DM 30/40. Les poids précis sont inventoriés ci-dessous.
- **Anomalie préexistante contrôle S1** : le sujet annonce Q30 à 1 point, `POINTS_BREAKDOWN` lui attribue 2 points. Le correcteur déclare un maximum de 35, mais ses Q1–25 à 1 et Q26–30 à 2 totalisent 35, auxquels s’ajoute 1 point d’identification (36). Le sujet totalise 34 pour les questions et 1 pour l’identification (35). Ne publier aucun barème global du contrôle dans le diaporama ; ne corriger ni sujet ni module dans cette mission.
- Contrôle final S2 inactif : 18 questions ; sections annoncées 5 + 5 + 6 + 4 = 20 points, sans pondération fiable par question ni correcteur actif. Aucun score inventé.
- Pas de « note exacte » calculée ici pour un étudiant : seules les pondérations réelles sont recensées. Pas d’exécution de copie étudiante.

## Acceptation et relais

Chaque TD actif doit rester identifiable et posséder un objectif et une limite propre ; tous les jalons d’évaluation, l’ordre pédagogique et la distinction TD/contrôle/DM doivent être fidèles. La couverture de contenu n’exige pas une slide par question : l’annexe permet de vérifier qu’aucun chapitre substantiel n’a été oublié dans la synthèse. Les exercices restent intégralement dans leurs supports ; aucune réduction de charge/autonomie n’est autorisée. Pas de futur support annoncé comme déjà disponible.

Fichier produit : celui-ci uniquement. Contrat affecté : présentation générale, aucun changement de contrat d’évaluation. Vérifications : inventaire du catalogue confronté aux cellules des notebooks, lecture des poids et critères dans les modules réels ; lecture des positions explicites des DM/contrôles S2. Risques : numérotation S2 trompeuse, réactivation involontaire du final archivé, confusion entre score et maîtrise, anomalie du contrôle S1, surpromesse « cooccurrences » TD5 Q24, liens inexistants. Revue demandée avant conception : validation de cette couverture par TAL-Pedagogy-Reviewer ; revues des fichiers HTML par les reviewers indépendants après réalisation. Cette note n’est pas son propre verdict.

## Annexe — inventaire intégral des questions et poids

Les cellules sont numérotées à partir de zéro dans le JSON source. Chaque rubrique donne le titre visible exact et le chemin courant. Les libellés de la table sont extraits du titre de question ou du premier commentaire de sa cellule réponse ; la consigne complète, les données, le code à compléter et les appuis restent dans les cellules référencées et celles qui les précèdent. Les « points correcteur » proviennent des modules réels ; la différence du contrôle S1 reste explicite ci-dessus. 93 questions S1 actives ; 122 questions S2 actives et 18 dans le final inactif : **233 questions recensées**.

### TD1 S1 — Variables, types et premières expressions

Source : `Notebooks TD/S1/TD1_S1_variables_types.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 10 | Q1 — calculez le coût total dans cout_total, puis affichez-le | 1 |
| Q2 | 15 | Q2 — affichez le type de note | 1 |
| Q3 | 20 | Exercice 3 — Affectation ou comparaison | 1 |
| Q4 | 25 | Exercice 4 — Insérer des valeurs dans une phrase | 1 |
| Q5 | 30 | Exercice 5 — Convertir avant de calculer | 1 |
| Q6 | 35 | Exercice 6 — Décrire une phrase personnelle | 1 |

Total recensé dans ce support : 6 questions.


### TD2 S1 — Chaînes et séquences

Source : `Notebooks TD/S1/TD2_S1_chaines_sequences.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 8 | Q1 — construisez texte_propre à partir de texte_brut. | 1 |
| Q2 | 12 | Q2 — construisez votre étape intermédiaire, puis texte_transforme. | 1 |
| Q3 | 16 | Q3 — construisez premier, dernier, debut, puis milieu. | 1 |
| Q4 | 20 | Q4 — construisez tokens et réalisez les observations demandées. | 1 |
| Q5 | 24 | Q5 — construisez phrase_avec_barres, puis tokens_reconstruits. | 1 |
| Q6 | 28 | Q6 — nettoyez les trois chaînes séparément, puis construisez la nouvelle liste. | 1 |
| Q7 | 30 | Q7 — construisez phrase_limite, tokens_limite, puis votre commentaire. | 1 |

Total recensé dans ce support : 7 questions.


### TD3 S1 — Collections : listes, tuples, dictionnaires et ensembles

Source : `Notebooks TD/S1/TD3_S1_collections.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 10 | Q1 — ajoutez "tokeniseur", retirez le dernier élément, puis affichez la liste restante | 1 |
| Q2 | 15 | Exercice 2 — Choisir une référence stable | 1 |
| Q3 | 21 | Exercice 3 — Construire un lexique bilingue | 1 |
| Q4 | 26 | Exercice 4 — Parcourir le lexique | 1 |
| Q5 | 31 | Exercice 5 — Distinguer occurrences et formes | 1 |
| Q6 | 36 | Exercice 6 — Comparer deux vocabulaires | 1 |

Total recensé dans ce support : 6 questions.


### TD4 S1 — Boucles, conditions et comptages

Source : `Notebooks TD/S1/TD4_S1_boucles_conditions_comptages.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 10 | Q1 — avec une boucle for, construisez majuscules avec les mots convertis en majuscules | 1 |
| Q2 | 15 | Exercice 2 — Filtrer selon la longueur | 1 |
| Q3 | 20 | Exercice 3 — Filtrer selon une lettre | 1 |
| Q4 | 25 | Exercice 4 — `range` et positions | 1 |
| Q5 | 30 | Exercice 5 — `while` avec condition d’arrêt | 1 |
| Q6 | 35 | Exercice 6 — Compter des formes | 1 |
| Q7 | 40 | Exercice 7 — Compréhension de liste | 1 |

Total recensé dans ce support : 7 questions.


### TD5 S1 — Fonctions et réutilisation du code

Source : `Notebooks TD/S1/TD5_S1_fonctions_reutilisation.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 10 | Exercice 1 — Première fonction | 1 |
| Q2 | 16 | Exercice 2 — Normaliser | 1 |
| Q3 | 22 | Exercice 3 — Compter les mots | 1 |
| Q4 | 28 | Exercice 4 — Traduire un mot | 1 |
| Q5 | 34 | Exercice 5 — Traduire une phrase | 1 |
| Q6 | 40 | Exercice 6 — Composer un résumé | 1 |

Total recensé dans ce support : 6 questions.


### Devoir maison intermédiaire S1 — Une bibliothèque prépare ses ateliers

Source : `Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 5 | Question 1 — Calculer un budget | 1 |
| Q2 | 7 | Question 2 — Lire deux expressions | 1 |
| Q3 | 9 | Question 3 — Tester une inscription | 1 |
| Q4 | 12 | Question 4 — Transformer sans effacer | 1 |
| Q5 | 14 | Question 5 — Extraire une référence | 1 |
| Q6 | 16 | Question 6 — Interpréter un découpage | 1 |
| Q7 | 18 | Question 7 — Reconstruire une annonce | 1 |
| Q8 | 21 | Question 8 — Modifier un programme et fixer une référence | 1 |
| Q9 | 23 | Question 9 — Construire un lexique | 1 |
| Q10 | 25 | Question 10 — Comparer deux ateliers | 1 |
| Q11 | 28 | Question 11 — Filtrer puis mesurer | 1 |
| Q12 | 30 | Question 12 — Produire deux séries bornées | 1 |
| Q13 | 32 | Question 13 — Compter des demandes | 1 |
| Q14 | 34 | Question 14 — Suivre une recherche bornée | 1 |
| Q15 | 37 | Question 15 — Normaliser une notice | 1,5 |
| Q16 | 39 | Question 16 — Compter une collection | 1,5 |
| Q17 | 41 | Question 17 — Traduire avec une ressource fournie | 1,5 |
| Q18 | 43 | Question 18 — Composer une synthèse | 1,5 |

Total recensé dans ce support : 18 questions.


### TD6 S1 — Lire, transformer et écrire des fichiers

Source : `Notebooks TD/S1/TD6_S1_fichiers_csv.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 11 | Exercice 1 — Lire sans oublier de fermer | 1 |
| Q2 | 16 | Exercice 2 — Lignes utiles | 1 |
| Q3 | 21 | Exercice 3 — Lire une ligne structurée | 1 |
| Q4 | 26 | Exercice 4 — Normaliser une personne | 1 |
| Q5 | 32 | Exercice 5 — Affiliation(s) unique(s) | 1 |
| Q6 | 38 | Exercice 6 — Écrire un CSV | 1 |

Total recensé dans ce support : 6 questions.


### TD7 S1 — Motifs, expressions régulières et pipeline

Source : `Notebooks TD/S1/TD7_S1_expressions_regulieres_pipeline.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 12 | Exercice 1 — Rechercher | 1 |
| Q2 | 17 | Exercice 2 — Extraire plusieurs nombres | 1 |
| Q3 | 22 | Exercice 3 — Extraire des suites de lettres | 1 |
| Q4 | 27 | Exercice 4 — Remplacer des dates | 1 |
| Q5 | 33 | Exercice 5 — Fonction de nettoyage | 1 |
| Q6 | 39 | Exercice 6 — Pipeline de synthèse | 1 |
| Q7 | 45 | Exercice 7 — Limite méthodologique | 1 |

Total recensé dans ce support : 7 questions.


### 📘 Contrôle S1 : fondamentaux Python et TAL

Source : `Notebooks contrôles finaux/DevoirS1.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 6 | Question 1 : correction de type (1.0 pt) | 1 |
| Q2 | 8 | Question 2 : indexation et slicing (1.0 pt) | 1 |
| Q3 | 10 | Question 3 : rigueur syntaxique (1.0 pt) | 1 |
| Q4 | 12 | Question 4 : nettoyage de chaîne (1.0 pt) | 1 |
| Q5 | 14 | Question 5 : évaluation booléenne (choix multiple) (1.0 pt) | 1 |
| Q6 | 17 | Question 6 : modification de liste (1.0 pt) | 1 |
| Q7 | 19 | Question 7 : parcours avec condition (1.0 pt) | 1 |
| Q8 | 21 | Question 8 : itération d'index erronée (1.0 pt) | 1 |
| Q9 | 23 | Question 9 : parcours inversé (1.0 pt) | 1 |
| Q10 | 25 | Question 10 : `IndexError` (1.0 pt) | 1 |
| Q11 | 28 | Question 11 : accès sécurisé (1.0 pt) | 1 |
| Q12 | 30 | Question 12 : Itération de Dictionnaire (1.0 pt) | 1 |
| Q13 | 32 | Question 13 : décompte de fréquence (Correction logique) (1.0 pt) | 1 |
| Q14 | 34 | Question 14 : logique conditionnelle (1.0 pt) | 1 |
| Q15 | 36 | Question 15 : filtrage de dictionnaire (1.0 pt) | 1 |
| Q16 | 39 | Question 16 : fonction simple (1.0 pt) | 1 |
| Q17 | 41 | Question 17 : distinguer `print` et `return` (1.0 pt) | 1 |
| Q18 | 43 | Question 18 : portée du `return` (1.0 pt) | 1 |
| Q19 | 45 | Question 19 : modularité (1.0 pt) | 1 |
| Q20 | 47 | Question 20 : retour de dictionnaire (1.0 pt) | 1 |
| Q21 | 49 | Question 21 : arguments par défaut (Choix multiple) (1.0 pt) | 1 |
| Q22 | 51 | Question 22 : argument manquant (Correction) (1.0 pt) | 1 |
| Q23 | 53 | Question 23 : portée des variables (1.0 pt) | 1 |
| Q24 | 55 | Question 24 : Boucle `while` (Correction logique) (1.0 pt) | 1 |
| Q25 | 57 | Question 25 : modularité (Correction + Renseignement) (1.0 pt) | 1 |
| Q26 | 60 | Question 26 : séparer par Casse (Correction Logique) (2.0 pts) | 2 |
| Q27 | 62 | Question 27 : Création de Dictionnaire (2.0 pts) | 2 |
| Q28 | 64 | Question 28 : traducteur Mot à Mot (2.0 pts) | 2 |
| Q29 | 66 | Question 29 : synthèse de traitement (Correction logique) (2.0 pts) | 2 |
| Q30 | 68 | Question 30 : (1.0 pt) | 2 |

Total recensé dans ce support : 30 questions.


### TD3 - S2

Source : `Notebooks TD/S2/TD3_S2_algorithmique_structures.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 12 | Exercice 1 : calculer un coût total avec conversion de types | 1 |
| Q2 | 17 | Exercice 2 : extraire une sous-chaîne par indices | 1 |
| Q3 | 22 | Exercice 3 : écrire une condition composée | 1 |
| Q4 | 30 | Exercice 4 : nettoyer une chaîne de caractères | 1 |
| Q5 | 35 | Exercice 5 : choisir la structure adaptée | 1 |
| Q6 | 40 | Exercice 6 : modifier une liste avec insert et pop | 1 |
| Q7 | 45 | Exercice 7 : compter avec une boucle et enumerate | 1 |
| Q8 | 50 | Exercice 8 : utiliser une compréhension de liste | 1 |
| Q9 | 55 | Exercice 9 : compter des occurrences avec un dictionnaire | 1 |
| Q10 | 60 | Exercice 10 : écrire une boucle while correcte | 1 |
| Q11 | 65 | Exercice 11 : définir une fonction simple | 1 |
| Q12 | 70 | Exercice 12 : utiliser un paramètre par défaut | 1 |
| Q13 | 75 | Exercice 13 : trier une liste avec key | 1 |
| Q14 | 80 | Exercice 14 : manipuler des ensembles | 1 |
| Q15 | 88 | Exercice 15 : gérer une erreur avec try et except | 1 |
| Q16 | 93 | Exercice 16 : implémenter un factoriel itératif | 1 |
| Q17 | 98 | Exercice 17 : trouver un maximum et sa position | 1 |
| Q18 | 103 | Exercice 18 : produire des bigrammes | 1 |
| Q19 | 108 | Exercice 19 : construire un dictionnaire avec zip | 1 |
| Q20 | 113 | Exercice 20 : filtrer avec une compréhension | 1 |
| Q21 | 118 | Exercice 21 : choisir la bonne complexité | 1 |
| Q22 | 123 | Exercice 22 : calculer une moyenne et un écart-type | 1 |
| Q23 | 128 | Exercice 23 : renseigner une valeur calculée | 1 |
| Q24 | 133 | Exercice 24 : écrire une fonction de recherche linéaire | 1 |
| Q25 | 138 | Exercice 25 : écrire une fonction récursive simple | 1 |
| Q26 | 143 | Exercice 26 : produire un dictionnaire par compréhension | 1 |
| Q27 | 148 | Exercice 27 : sélectionner les deux plus grandes valeurs | 1 |
| Q28 | 156 | Exercice 28 : filtrer des stopwords | 1 |
| Q29 | 161 | Exercice 29 : produire toutes les paires entre deux listes | 1 |
| Q30 | 169 | Exercice 30 : implémenter l'algorithme d'euclide | 1 |

Total recensé dans ce support : 30 questions.


### 📘 Contrôle S2 : renforcement et algorithmique

Source : `Notebooks contrôles finaux/S2/Controle_TD2_S2_algorithmique.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 6 | Question 1 : inversion de chaîne (1.0 pt) | 1 |
| Q2 | 8 | Question 2 : assemblage de liste (1.0 pt) | 1 |
| Q3 | 10 | Question 3 : formatage numérique (1.0 pt) | 1 |
| Q4 | 12 | Question 4 : compréhension de liste simple (1.0 pt) | 1 |
| Q5 | 14 | Question 5 : unicité avec set (1.0 pt) | 1 |
| Q6 | 17 | Question 6 : construction de dictionnaire (1.0 pt) | 1 |
| Q7 | 19 | Question 7 : somme de valeurs (1.0 pt) | 1 |
| Q8 | 21 | Question 8 : filtrage conditionnel (2.0 pts) | 2 |
| Q9 | 23 | Question 9 : comptage de fréquence (2.0 pts) | 2 |
| Q10 | 26 | Question 10 : boucles imbriquées (2.0 pts) | 2 |
| Q11 | 28 | Question 11 : suite de Fibonacci (2.0 pts) | 2 |
| Q12 | 30 | Question 12 : détection d'anagrammes (2.0 pts) | 2 |
| Q13 | 32 | Question 13 : compréhension conditionnelle (3.0 pts) | 3 |

Total recensé dans ce support : 13 questions.


### TD5 : Approfondissement et algorithmique avancée

Source : `Notebooks TD/S2/TD5_S2_algorithmes_texte.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 9 | Exercice 1 : Carrés des pairs | 1 |
| Q2 | 13 | Exercice 2 : Filtrage de mots | 1 |
| Q3 | 17 | Exercice 3 : Dictionnaire de longueurs | 1 |
| Q4 | 21 | Exercice 4 : Inversion de phrase | 1 |
| Q5 | 25 | Exercice 5 : Association (Zip) | 1 |
| Q6 | 30 | Exercice 6 : Palindrome | 1 |
| Q7 | 34 | Exercice 7 : Anagrammes | 1 |
| Q8 | 38 | Exercice 8 : Distance de Hamming | 1 |
| Q9 | 42 | Exercice 9 : Générateur d'acronyme | 1 |
| Q10 | 46 | Exercice 10 : Chiffrement de César | 1 |
| Q11 | 51 | Exercice 11 : Aplatissement de liste | 1 |
| Q12 | 58 | Exercice 12 : Fusion de dictionnaires | 1 |
| Q13 | 62 | Exercice 13 : Inversion de dictionnaire | 1 |
| Q14 | 66 | Exercice 14 : Tri complexe | 1 |
| Q15 | 70 | Exercice 15 : Élément le plus fréquent | 1 |
| Q16 | 75 | Exercice 16 : Tokenisation simple | 1 |
| Q17 | 79 | Exercice 17 : Suppression des mots vides (Stopwords) | 1 |
| Q18 | 83 | Exercice 18 : Bigrammes | 1 |
| Q19 | 87 | Exercice 19 : Trigrammes | 1 |
| Q20 | 91 | Exercice 20 : Indice de Jaccard | 1 |
| Q21 | 96 | Exercice 21 : Calcul de TF (Term Frequency) | 1 |
| Q22 | 100 | Exercice 22 : Produit scalaire (Dot product) | 1 |
| Q23 | 104 | Exercice 23 : Plus long préfixe commun | 1 |
| Q24 | 108 | Exercice 24 : Matrice de co-occurrence (simplifiée) | 1 |
| Q25 | 112 | Exercice 25 : Pipeline complet | 1 |

Total recensé dans ce support : 25 questions.


### 📘 Contrôle S2 : manipulation des ensembles

Source : `Notebooks contrôles finaux/S2/Controle_TD4_S2_ensembles.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 6 | Question 1 : dédoublonnage (2.0 pts) | 2 |
| Q2 | 8 | Question 2 : modification d'ensemble (2.0 pts) | 2 |
| Q3 | 10 | Question 3 : test d'appartenance rapide (2.0 pts) | 2 |
| Q4 | 13 | Question 4 : intersection (3.0 pts) | 3 |
| Q5 | 15 | Question 5 : union (3.0 pts) | 3 |
| Q6 | 17 | Question 6 : différence (3.0 pts) | 3 |
| Q7 | 19 | Question 7 : différence symétrique (3.0 pts) | 3 |
| Q8 | 21 | Question 8 : sous-ensemble (2.0 pts) | 2 |
| Q9 | 24 | Question 9 : optimisation de recherche (3.0 pts) | 3 |
| Q10 | 26 | Question 10 : algorithme de nettoyage (3.0 pts) | 3 |
| Q11 | 28 | Question 11 : mots communs sans boucles (3.0 pts) | 3 |
| Q12 | 30 | Question 12 : gestion des absents (Différence) (3.0 pts) | 3 |
| Q13 | 32 | Question 13 : Index de Jaccard (NLP) (4.0 pts) | 4 |
| Q14 | 34 | Question 14 : Pangramme (Superset) (4.0 pts) | 4 |

Total recensé dans ce support : 14 questions.


### Devoir maison intermédiaire d'approfondissement

Source : `Notebooks contrôles finaux/S2/Devoir_maison_S2_approfondissement.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 5 | Q1: Slicing: extrayez 'bon' de 'bonjour'. | 1 |
| Q2 | 6 | Q2: Ajoutez 4 à la liste [1, 2, 3]. | 1 |
| Q3 | 7 | Q3: Récupérez le dernier élément de [1, 2, 3]. | 1 |
| Q4 | 8 | Q4: Récupérez la valeur de 'age'. | 1 |
| Q5 | 9 | Q5: Ajoutez 'ville': 'Paris' au dictionnaire. | 1 |
| Q6 | 10 | Q6: Calculez la somme de [1, 2, 3]. | 1 |
| Q7 | 11 | Q7: Mettez 'test' en majuscules. | 1 |
| Q8 | 12 | Q8: Remplacez 'chat' par 'chien' dans 'mon chat'. | 1 |
| Q9 | 13 | Q9: Trouvez la longueur de la liste. | 1 |
| Q10 | 14 | Q10: Créez un set des éléments uniques. | 1 |
| Q11 | 15 | Q11: Vérifiez si 10 est strictement supérieur à 5. | 1 |
| Q12 | 16 | Q12: Séparez 'a-b-c' en liste avec le délimiteur '-'. | 1 |
| Q13 | 17 | Q13: Concaténez [1] et [2]. | 1 |
| Q14 | 18 | Q14: Valeur absolue de -5. | 1 |
| Q15 | 19 | Q15: Maximum de [1, 9, 3]. | 1 |
| Q16 | 20 | Q16: Convertissez la chaîne '42' en entier. | 1 |
| Q17 | 21 | Q17: Arrondissez 3.14159 à 2 décimales. | 1 |
| Q18 | 22 | Q18: Vérifiez (booléen) si 2 est dans [1, 2, 3]. | 1 |
| Q19 | 23 | Q19: Récupérez la liste (list) des clés du dictionnaire. | 1 |
| Q20 | 24 | Q20: Récupérez la liste (list) des valeurs du dictionnaire. | 1 |
| Q21 | 26 | Q21: Compréhension: liste des carrés de 1 à 5 inclus. | 2 |
| Q22 | 27 | Q22: Compréhension: dictionnaire associant x à x**2 pour x dans [1, 2, 3]. | 2 |
| Q23 | 28 | Q23: Filtrez les nombres pairs de la liste avec une compréhension. | 2 |
| Q24 | 29 | Q24: Aplatissez [[1, 2], [3, 4]] avec des boucles imbriquées. | 2 |
| Q25 | 30 | Q25: Comptez les fréquences des lettres dans 'abac'. | 2 |
| Q26 | 31 | Q26: Zippez ['a', 'b'] et [1, 2] pour former un dictionnaire. | 2 |
| Q27 | 32 | Q27: Inversez clés/valeurs du dictionnaire. | 2 |
| Q28 | 33 | Q28: Transposez la matrice (les lignes deviennent des colonnes). | 2 |
| Q29 | 34 | Q29: Trouvez les éléments communs aux deux listes. | 2 |
| Q30 | 35 | Q30: Calculez la factorielle 5*4*3*2*1 de 5 avec une boucle. | 2 |

Total recensé dans ce support : 30 questions.


### TD6 : Manipulation de Fichiers et Ressources Linguistiques

Source : `Notebooks TD/S2/TD6_S2_fichiers_ressources.ipynb`. Statut : actif.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 13 | Exercice 1 : Lecture simple | 1 |
| Q2 | 17 | Exercice 2 : Lecture ligne à ligne (Liste) | 1 |
| Q3 | 21 | Exercice 3 : Nettoyage d'une ligne | 2 |
| Q4 | 27 | Exercice 4 : Tokenisation | 2 |
| Q5 | 31 | Exercice 5 : Filtrage numérique | 2 |
| Q6 | 35 | Exercice 6 : Stopwords (Mots vides) | 2 |
| Q7 | 41 | Exercice 7 : Pipeline complet | 3 |
| Q8 | 45 | Exercice 8 : Comptage (Fréquences) | 3 |
| Q9 | 51 | Exercice 9 : Écriture CSV simple | 2 |
| Q10 | 55 | Exercice 10 : Formatage avancé | 2 |

Total recensé dans ce support : 10 questions.


### Contrôle Final S2 : Algorithmique et Fichiers

Source : `Notebooks contrôles finaux/S2/Controle_final_S2_algorithmique_fichiers.ipynb`. Statut : archive inactive.

| Question | Cellule réponse | Libellé source | Points correcteur |
|---|---:|---|---:|
| Q1 | 7 | Q1 : Liste des nombres de 0 à 50 divisibles par 3 mais PAS par 9. | non défini |
| Q2 | 8 | Q2 : Filtrage de mots longs | non défini |
| Q3 | 9 | Q3 : Fusion de dictionnaires (Somme des valeurs) | non défini |
| Q4 | 10 | Q4 : Extraction de clés | non défini |
| Q5 | 11 | Q5 : Similarité de Jaccard (Intersection / Union) | non défini |
| Q6 | 13 | Q6 : Nombre total de lignes du fichier 'corpus_litterature.txt' | non défini |
| Q7 | 14 | Q7 : Nombre de lignes NON vides (contenant du texte) | non défini |
| Q8 | 15 | Q8 : Extraction | non défini |
| Q9 | 16 | Q9 : Lecture partielle | non défini |
| Q10 | 18 | Q10 : Fonction de nettoyage | non défini |
| Q11 | 19 | Q11 : Tokenisation complète | non défini |
| Q12 | 20 | Q12 : Suppression des Stopwords | non défini |
| Q13 | 21 | Q13 : Fréquences | non défini |
| Q14 | 22 | Q14 : Le mot le plus fréquent | non défini |
| Q15 | 24 | Q15 : Export CSV trié | non défini |
| Q16 | 25 | Q16 : Sous-corpus filtré | non défini |
| Q17 | 26 | Q17 : Statistiques de longueur | non défini |
| Q18 | 27 | Q18 : Copie de sauvegarde | non défini |

Total recensé dans ce support : 18 questions.
