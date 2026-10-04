# Revue éditoriale indépendante — intégralité des sept TD S1

## Périmètre et diagnostic initial

Réviseur : TAL-Editorial-Reviewer, indépendant des rédacteurs, lecture seule des supports. Base technique : `670e6c1`. Mission : sept TD S1, 45 questions, toutes les cellules visibles, commentaires fournis, contexte du tuteur et profil par exercice. Aucun contrôle ni DM n'est inclus dans ce verdict. Le diagnostic initial ne vaut pas validation de la réécriture. Les fichiers de référence sont ceux du dossier `Notebooks TD/S1/` à la base ; les sources historiques externes n'ont pas été consultées directement par ce réviseur. Toute affirmation de restauration intégrale de ces sources est exclue.

Lecture initiale exhaustive : TD1 cellules 0–35 ; TD2 0–20 ; TD3 0–37 ; TD4 0–41 ; TD5 0–38 ; TD6 0–39 ; TD7 0–44 (indices depuis zéro, 261 cellules). Le contexte complet du tuteur est dupliqué et la règle S1 aucun code y est explicite ; le comportement réel dans Colab n'est pas observé.

## Constats transmis aux rédacteurs

| Identifiant | Gravité | Passage concerné | Difficulté et reprise demandée |
|---|---|---|---|
| TAL-EDIT-S1-001 | Bloquant | Introduction de tous les supports : contrat v2, preuves du correcteur, éditions refusées | Destinataire mainteneur/concepteur. Remplacer par actions d'étudiant : identification, exécution, enregistrement, dépôt. Ne garder que les contraintes nécessaires à l'utilisation. La cellule canonique de restitution est toutefois conservée exactement conformément à la demande enseignante antérieure ; seul un séparateur visible est ajouté. |
| TAL-EDIT-S1-002 | Bloquant | TD1–TD4 « vos explications restent à relire avec l'enseignant » ; TD5–TD7 « restent à relire » | Promesse ou attente implicite de relecture. Donner des critères d'autoévaluation, distinguer calcul et interprétation, permettre de signaler une difficulté sans promettre une correction individuelle. |
| TAL-EDIT-S1-003 | Bloquant | Appuis mêlant cours, contraintes de Q et essais « après Q » avant la Q | La chronologie et la fonction des passages sont confondues. Séparer rappel, exemple exécutable, entraînement, énoncé autonome et vérification après exercice, sans perte d'activité. |
| TAL-EDIT-S1-004 | Majeur | TD2 Q1–Q6 démonstrations en Markdown | Débutant contraint de créer/copier le code avant de comprendre. Livrer les exemples dans des cellules exécutables distinctes et préserver toutes les questions d'observation. |
| TAL-EDIT-S1-005 | Majeur | TD1 Q4 ; TD4 Q2/Q3 et Q7 | Noms ou données implicites : `phrase_presentation`, `mots`, seuil des mots longs. Nommer les données et résultats dans l'énoncé, ainsi que le seuil strictement supérieur à cinq en Q7. |
| TAL-EDIT-S1-006 | Bloquant | TD5 exemple de Q1 et profil tuteur | `None` apparaît sans explication ni permission. Enseigner le retour implicite et synchroniser la permission limitée à l'exercice. |
| TAL-EDIT-S1-007 | Majeur | TD5 appui composition | « Cela prépare les fonctions … du contrôle ; signatures » expose la fabrication. Expliquer la valeur par défaut et laisser les contraintes dans les seuls énoncés concernés. |
| TAL-EDIT-S1-008 | Majeur | TD6 Q3, Q6 | « Couples » sans type explicite ; deux affichages Q6 concurrents, justification du correcteur. Définir liste de paires, conserver un seul affichage fourni actif à compléter/décommenter selon convention du support. |
| TAL-EDIT-S1-009 | Majeur | TD7 Q3, Q5 et appuis | Correction « une apostrophe » ; convention d'extraction à nommer dans l'énoncé ; remplacer « contrat » par ordre des transformations. |

## Lecture question par question : version de référence

Les cellules `tal-s1-tdN-…` sont les appuis, exemples et essais initiaux ; les cellules `tdN-s1-prompt-qK` et `tdN-s1-answer-qK` contiennent énoncé et réponse. Pour Q1 de TD1/3/4 et Q2 de TD1, l'énoncé initial est seulement un commentaire de réponse. Chaque ligne ci-dessous a été relue avec ses appuis et essais.

| TD / question | Action, données et résultat | Acquis et appui initial précis | Guidage et vigilance |
|---|---|---|---|
| TD1 Q1 | Tarif × mots → cout_total | TD1 c5–8 affectation, calcul, print | Données et affichage fournis ; calcul autonome. |
| TD1 Q2 | Type de note | TD1 c10–12 types | Appel à construire ; exemple distinct. |
| TD1 Q3 | Deux booléens sur nb_mots/prix_par_mot | TD1 c14–16 comparaison, and | Réemploi Q1 explicite à ajouter. |
| TD1 Q4 | Phrase langues → phrase_presentation | TD1 c19–21 f-string | Nom de sortie à expliciter. |
| TD1 Q5 | Chaîne volume → entier +20 | TD1 c24–26 int, concaténation/addition | Conversion autonome. |
| TD1 Q6 | Phrase personnelle, longueur et présence TAL | TD1 c29–31 len, in, repr | Phrase libre ; interprétation de casse. |
| TD2 Q1 | strip, longueurs, conservation source | TD2 c5 rappel + exemple | Toutes les observations doivent rester. |
| TD2 Q2 | lower/replace/in sur texte_propre | TD2 c7 ; TD1 Q6 in | Dépendance Q1 ; justification ordre. |
| TD2 Q3 | Indices et tranches de tokenisation | TD2 c9 | Bornes exclues, longueur source conservée. |
| TD2 Q4 | split, indices, types, longueurs | TD2 c11 ; TD1 type/len | Chaîne versus éléments liste. |
| TD2 Q5 | join puis split avec séparateur identique | TD2 c13 | Dépendance tokens Q4. |
| TD2 Q6 | Trois nettoyages sans boucle, source conservée | TD2 c15 ; Q1–Q4 | Indices imposés, nouvelles chaînes et liste. |
| TD2 Q7 | Phrase imposée, fragments, commentaire argumenté | TD2 Q4, c17 | Observation linguistique autonome, pas nouvelle méthode. |
| TD3 Q1 | append/pop et états outils | TD3 c6–8 ; TD2 liste | Affichage intermédiaire à placer avant retrait. |
| TD3 Q2 | Tuple langues et justification | TD3 c10–12 | Type et stabilité, sans fausse garantie de validité. |
| TD3 Q3 | Lexique quatre traductions | TD3 c15–17 | Convention donnée c19 ; accès et ajout. |
| TD3 Q4 | Parcours items → chaînes anglais -> français | TD3 c21–23 ; TD1 f-string | Première boucle expliquée et exécutée ; lexique Q3. |
| TD3 Q5 | Ensemble et deux effectifs | TD3 c26–28 | Distinction occurrences/formes. |
| TD3 Q6 | Intersection et différence corpus | TD3 c31–33 | Deux opérateurs et sens de différence. |
| TD4 Q1 | Liste majuscules de mots | TD4 c6–8 ; TD3 for/append | Boucle explicite requise. |
| TD4 Q2 | Filtre strict longueur >5 | TD4 c10–12 ; TD1 comparaisons | Nom de donnée mots à ajouter. |
| TD4 Q3 | Présence a sans casse, conserver forme | TD4 c15–17 ; TD2 lower | Nom de donnée mots à ajouter. |
| TD4 Q4 | Pairs 0 à 10 inclus avec range | TD4 c20–22 | Pas, bornes, modulo et essais conservés. |
| TD4 Q5 | Multiples de 7 jusqu'à 70, while | TD4 c25–27 | Condition et progrès ; arrêt anticipé sur papier. |
| TD4 Q6 | Dictionnaire de fréquences texte | TD4 c30–32 ; TD3 dictionnaire | get ou if/else explicitement montrés. |
| TD4 Q7 | Compréhension longueurs mots longs | TD4 c35–37 ; Q2 | Seuil à répéter. |
| TD5 Q1 | Fonction longueur et deux tests | TD5 c6–8 ; TD1 len | def/return/paramètre ; None à introduire. |
| TD5 Q2 | Fonction strip/lower | TD5 c11–13 ; TD2 Q1/Q2 | Essais chaîne vide et espaces. |
| TD5 Q3 | nombre_mots appelle normaliser | TD5 c16–18 ; TD2 split | Composition et valeur par défaut dans entraînement. |
| TD5 Q4 | Traduire mot normalisé ou mot inconnu | TD5 c21–23 ; TD3 lexique, TD4 condition | Normalisation avant recherche ; lexique paramètre. |
| TD5 Q5 | Traduction de chaque fragment puis join | TD5 c26–28 ; TD4 boucle, TD2 join | Réutiliser Q4, gérer vide/inconnu. |
| TD5 Q6 | Résumé texte normalisé/caractères/mots | TD5 c31–33 ; Q1–Q3 | Clés exactes dans énoncé ; tranche vide expliquée. |
| TD6 Q1 | with/open lit affiliations_s1.txt | TD6 c7–9 | Path fourni préparation ; UTF-8/chemin à expliquer. |
| TD6 Q2 | splitlines, conserver lignes utiles | TD6 c12–14 ; TD4 if | Vide versus espaces et ordre. |
| TD6 Q3 | Liste de paires nom-affiliation | TD6 c17–19 ; TD3 liste/tuple | Split limité expliqué ; représentation des paires à préciser. |
| TD6 Q4 | Fonction title + espaces normalisés | TD6 c22–24 ; TD5 fonctions | Convention de graphie ne prouve pas identité. |
| TD6 Q5 | Dictionnaire personne → ensemble affiliations | TD6 c27–29 ; TD3 set/dict | Enseigner add, normaliser avant regroupement. |
| TD6 Q6 | CSV trois colonnes, relecture | TD6 c32–34 ; Q5, TD3 items | csv autorisé ici seulement ; affichage double à clarifier. |
| TD7 Q1 | Regex TAL sans casse → booléen | TD7 c6–9 | search, None, bool, IGNORECASE enseignés. |
| TD7 Q2 | Extraire séquences chiffres | TD7 c12–14 | findall et +, chaînes sans conversion. |
| TD7 Q3 | Lettres accentuées, comparer split | TD7 c17–19 ; TD2 split | Convention apostrophes à rendre explicite. |
| TD7 Q4 | Remplacer date par marqueur | TD7 c22–24 | sub, répétition bornée ; forme ≠ validité calendaire. |
| TD7 Q5 | Fonction quatre transformations ordonnées | TD7 c27–29 ; TD5 fonctions | DATE reste majuscule ; ponctuation conservée. |
| TD7 Q6 | Pipeline texte/mots/fréquences | TD7 c32–34 ; TD4 comptage, Q3/Q5 | Même entrée, vide et interprétation. |
| TD7 Q7 | Limite argumentée regex/français | TD7 c37–39 | Interprétation ouverte, exemple fourni ne dicte pas réponse. |

## État du verdict

`REQUEST_CHANGES` — `NON_DÉMONTRÉE` sur la base initiale. Relecture finale et empreintes en attente. Ni cette lecture ni l'exécution automatisée ne prouvent le comportement Colab, la durée réelle ou l'apprentissage en classe.

## Relecture finale — version gelée du 4 octobre 2026

TAL-Prof a produit la matrice préalable `docs/pedagogy/s1_editorial_complete_coverage.md`. Les originaux ont été retrouvés et lus avant le démarrage de la conception. Le cadrage a ensuite reçu le verdict indépendant `ACCEPT_SUR_PÉRIMÈTRE_COURANT` de `s1_ped_reviewer`, avant le feu vert donné aux Designers. La matrice distingue les lacunes héritées de 2025 et la conservation du parcours actuellement distribué. Ce rapport ne prétend pas restaurer l'intégralité des enseignements de 2025.

Toutes les cellules visibles finales et leurs commentaires ont été relus, en deux lots puis par relecture des modifications tardives. Les 45 questions de la table précédente restent identifiables par `tdN-s1-answer-qK`. Les appuis et exemples portent toujours les identifiants cités ; les indices initiaux de la table décrivent la référence, pas la version finale. Les nouveaux énoncés TD1 Q1/Q2, TD3 Q1, TD4 Q1, les six exemples exécutables TD2 et toutes les nouvelles cellules de vérification ont également été lus. Aucun contrôle, DM ou archive n'est inclus dans ce verdict.

| Support dans `Notebooks TD/S1/` | Toutes cellules relues (indices inclusifs) | SHA-256 final |
|---|---|---|
| TD1_S1_variables_types.ipynb | 0–37 (38) | d842f8962bfbc754296345ccc4ba191db97b27253d033f725e754a53259f7acf |
| TD2_S1_chaines_sequences.ipynb | 0–32 (33) | 17e0ba28fc732b26270d62018b4e48d4a04e005d042329819534549ac09c78bd |
| TD3_S1_collections.ipynb | 0–38 (39) | e01e6ed9ae0c7db5158e3397ef9c4091964b4ad1c0072e7f91c9e700d83ce1a7 |
| TD4_S1_boucles_conditions_comptages.ipynb | 0–43 (44) | 71298b908b755cd2db81c2585fca4f9ecdcd1b7366161a80c845b3abc20a1f6d |
| TD5_S1_fonctions_reutilisation.ipynb | 0–45 (46) | 38aa2dfd789abe9e7aef7280d71f9bba716430105e3b5043742122fcdd14cf89 |
| TD6_S1_fichiers_csv.ipynb | 0–42 (43) | 85fbce645000e443ff378b94fdd9e3653bc7f98feaacca1b8c06bcb30773c50d |
| TD7_S1_expressions_regulieres_pipeline.ipynb | 0–49 (50) | 04fe8873b656a41e1b87468ea252d576309314443bc260fa869cd98cdef4024f |

### Résolution des constats

- **001–002 résolus** : les introductions expliquent les actions de l'étudiant, les affichages et les limites du retour automatique. Aucune promesse de relecture systématique ; autoévaluation et signalement d'une difficulté précise. La cellule canonique de restitution demeure inchangée sur instruction enseignante, avec séparateur visible.
- **003 résolu** : cours et exemples identifiés, énoncés séparés. Les onze vérifications de TD5 Q1–Q6, TD6 Q4–Q5 et TD7 Q4–Q6 sont désormais réellement après leur réponse (`tdN-s1-verification-qK`), avec renvois explicites. Leurs tests sur vide, inconnu, espaces, graphies, nettoyage et comptage sont conservés. Les autres essais accompagnent des exemples distincts avant l'exercice et ne requièrent pas un résultat futur.
- **004 résolu** : TD2 Q1–Q6 possèdent six cellules exécutables d'exemple `s1-editorial-td2-exemple-qK`, précédées du cours et des observations, suivies d'un énoncé distinct. Q7 demeure autonome et interprétatif, sans solution ajoutée. Les observations détaillées de chaque question sont conservées.
- **005 résolu** : TD1 Q4 nomme `phrase_presentation` ; TD4 Q2/Q3 renvoient à `mots`, Q7 répète la borne strictement supérieure à cinq et la production de longueurs.
- **006 résolu** : `tal-s1-td5-fonction-notions` explique le résultat `None` avant l'exemple. Après synchronisation, `None` est autorisé dans les notions de Q1 et dans les deux copies du contexte. Aucun élargissement de bibliothèques.
- **007 résolu** : valeur par défaut et composition expliquées pour leur utilité dans le travail ; notes de préparation au contrôle retirées. Les essais de fonction avec paramètre par défaut restent présents.
- **008 résolu** : TD6 Q3 définit chaque paire et accepte liste ou tuple ; Q6 ne conserve qu'un affichage fourni non ambigu. Les commandes `set()` et `add()` sont expliquées avant Q5 ; `join()` sur ensemble est expliqué avant Q6 ; le cours CSV précède l'import et l'exemple.
- **009 résolu** : TD7 corrige apostrophe et explique la convention de suites de lettres dans Q3, l'ordre des transformations dans Q5. Le module `re` et l'appel de ses fonctions sont présentés avant emploi. Q7 reçoit un exemple conceptuel nom/verbe sur « porte » et demande un autre cas personnel, avec critères d'autoévaluation plutôt qu'une promesse de correction.

Deux détails supplémentaires TD2 ont été corrigés et relus : espace avant le point en Q6 ; mention de cellules d'essai inexistantes remplacée par emplacement effectif des observations et manipulations.

### Preuve finale par question et activités non notées

Pour chacune des 45 lignes du tableau initial, la relecture finale confirme : données nommées, production indiquée dans l'énoncé ou affichage fourni sans ambiguïté, acquis enseignés dans les cellules d'appui identifiées et/ou TD antérieurs cités, distinction démonstration/entraînement/réponse. Les dépendances Q1→Q2/Q3 et Q4→Q5 au TD2, lexique Q3→Q4 au TD3, mots Q1→Q2/Q3/Q7 au TD4, fonctions Q1–Q5→Q6 au TD5, lecture→regroupement→CSV au TD6 et nettoyage→pipeline au TD7 sont compréhensibles. L'étudiant reste chargé de construire son code : les affichages fournis ne constituent pas une solution de traitement.

Les activités non notées ont été relues sans échantillonnage : six groupes exemple/essai TD1, six exemples commentés TD2 et observations de Q1–Q7, six groupes TD3, sept groupes TD4, six groupes TD5 et six vérifications finales, six groupes TD6 et deux vérifications finales, sept groupes TD7 et trois vérifications finales. Les synthèses ne promettent pas de relecture ; elles demandent de confronter prédictions, résultats et explications. Les bibliothèques réellement enseignées demeurent aucune pour TD1–TD5, `csv` au TD6 Q6, `re` au TD7 ; `Path` et les imports d'affichage restent fournis, sans permission générale au tuteur.

### Vérifications et limites distinctes

Le réviseur a contrôlé par lecture et script JSON l'égalité du contexte complet entre métadonnées Colab et première cellule cachée pour les sept supports, la règle textuelle « Au S1 : langage naturel seulement, aucun code » et l'ajout `None` dans les notions TD5 Q1. Le calcul SHA-256 ci-dessus ancre la revue aux versions finales. Le réviseur n'a modifié ni notebook, ni code, ni profil du tuteur. Les validations techniques d'exécution et de distribution relèvent du rapport d'intégration ; elles ne sont pas transformées ici en preuve d'apprentissage.

Le retour du lecteur Étudiant-Modèle reste distinct dans `Corrigés modèles/TD/s1-editorial-complete/`. Le verdict pédagogique et la correspondance historique sont ceux de TAL-Prof/Pedagogy-Reviewer dans la matrice et le handoff. Aucune exécution humaine en classe, durée mesurée ni observation du comportement effectif de Colab n'a été réalisée par le réviseur.

## Verdict éditorial final

**ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE**, sur les sept versions finales ci-dessus (293 cellules, 45 questions et activités d'entraînement). Aucun blocage éditorial ouvert. Ce verdict valide la rédaction du lot courant, pas une restauration exhaustive des sources 2025, ni les contrôles S1, ni la fusion. Prochaine étape : revue technique, gouvernance et décision du mainteneur.
