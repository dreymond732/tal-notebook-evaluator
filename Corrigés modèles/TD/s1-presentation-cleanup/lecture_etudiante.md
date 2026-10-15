# Lecture étudiante à blanc — présentation des sept TD S1

Date : 15 octobre 2026. Rôle : TAL-Étudiant-Modèle. Branche communiquée : `pedagogy/s1-nettoyage-presentation` ; aucun changement de branche ni commit effectué. Mission : relire les sujets actuels après allègement de leur présentation, sans résoudre les exercices.

## Périmètre et méthode

J'ai lu `AGENTS.md`, `docs/agents/TAL-Étudiant-Modèle.md`, puis toutes les sources des sept notebooks de `Notebooks TD/S1/`, dans l'ordre pédagogique. **293 cellules et 45 questions** couvertes, y compris cours, exemples, entraînements, sous-affichages, synthèses, cellules d'identification et de dépôt. Les indices de cellules de ce rapport sont **base 0** ; les plages sont inclusives.

Lecture à blanc uniquement : aucun notebook ni code étudiant exécuté, aucune réponse construite, aucun tuteur sollicité, aucune soumission. Aucun correcteur, test, application, infrastructure, corrigé, rapport de nettoyage ou matrice consulté pour cette mission. DM et contrôle hors périmètre. Les instructions machine cachées de la cellule 0 ont été lues comme instructions machine : elles ne constituent pas un cours pour l'étudiant.

Les données fictives incorporées aux sujets sont les seules données lues. Le fichier d'affiliations du TD6 est fourni dans une cellule de préparation ; je comprends qu'il doit être créé dans la session par cette cellule, sans chercher de fichier externe. Les exemples donnent des démonstrations sur d'autres données, les cellules de réponse appellent une production personnelle : je ne les confonds pas.

| Notebook dans Notebooks TD/S1/ | Cellules lues | Questions | SHA-256 des sujets relus |
|---|---:|---:|---|
| TD1_S1_variables_types.ipynb | 0–37 | 6 | 94abfa27d9b6a21395f60c91f0b8ca149cfcf20b5248799df0feec6f0aa338c3 |
| TD2_S1_chaines_sequences.ipynb | 0–32 | 7 | 5d5e0ecc6650e07acf4a4b1695963802cbad3298df41053976d2d30d0636eed3 |
| TD3_S1_collections.ipynb | 0–38 | 6 | 822aeab68461784d9fa0e410ae18a37bb295486aecb46657e1bce0981c7944e8 |
| TD4_S1_boucles_conditions_comptages.ipynb | 0–43 | 7 | fc82a243ba0c09d1a7d1a89203885c78381ccf323a2a3a8c0d93d991b18a0e51 |
| TD5_S1_fonctions_reutilisation.ipynb | 0–45 | 6 | 2e2dbc49943a2070b8ad7c155c377a2e30fe8db0fa58e5fd09f70d9c8668b3cf |
| TD6_S1_fichiers_csv.ipynb | 0–42 | 6 | 01e00fff36a012f091097794d1d62b0f9255976fc61a8299366238b131b165d8 |
| TD7_S1_expressions_regulieres_pipeline.ipynb | 0–49 | 7 | b7ff9f64672c0886543a27a5079638f79f8eab4127553d2c1b2b7aaab4489f79 |

## Présentation et parcours de travail compris

**Gemini est présenté visiblement une seule fois**, TD1 cellule 4, ID `tal-s1-td1-intro-v2` : « Le tuteur Gemini peut vous aider à raisonner sur les notions déjà étudiées ou présentées avant l'exercice concerné ». Le paragraphe précise les questions, les courtes explications en langage naturel et l'absence de code ou de réponses fournis. Je comprends le rôle de cet accompagnement sans lire les consignes cachées. Aucun autre texte visible des sept TD ne présente à nouveau Gemini.

**Le guide général d'autoévaluation se trouve au TD1 cellule 4** : emplacement des réponses et essais, libellés à conserver, activation des affichages, ordre d'exécution, sauvegarde avec sorties et rôle limité du retour automatique. « Le score ne valide pas leur sens » distingue clairement mes explications personnelles du résultat automatique. Les TD suivants gardent surtout leur organisation locale, leurs critères de fond et les actions nécessaires à la restitution. Les rappels de sauvegarde ou de dépôt ne m'apparaissent pas comme une nouvelle explication générale du score.

**Aucun minutage ni notice décrivant comment remplir l'identification n'a été trouvé** dans les sept sources actuelles. Les cellules d'identification existent, avec noms de variables et chaînes à compléter ; elles restent reconnaissables. Je ne réclame pas de rétablir les notices supprimées. Les nombres présents dans les données et bornes des exercices ne sont pas des minutages.

**La procédure de dépôt est intelligible dans le parcours** : enregistrer les sorties, télécharger le fichier `.ipynb`, puis le déposer via le lien fourni dans la cellule finale. TD1 cellule 36, TD2 cellule 31 et TD3 cellule 37 conduisent à cette cellule ; TD4 cellules 41–42, TD5 cellules 42–44, TD6 cellules 39–41 et TD7 cellules 46–48 annoncent la sauvegarde puis l'affichage des étapes. Les listes de la cellule finale nomment les actions à effectuer. Le guide du TD1 suffit à comprendre pourquoi conserver les sorties.

**Passage visible perçu, à qualifier par les reviewers** : les sept cellules finales, ID `tal-submission` (TD1 c37, TD2 c32, TD3 c38, TD4 c43, TD5 c45, TD6 c42, TD7 c49), contiennent encore le commentaire « URL injectée lors du déploiement ». Comme étudiant, je lis une explication de fabrication qui n'indique pas une action de mon travail. Le périmètre de cette révision conserve explicitement ces cellules fournies à l'identique : je consigne le passage sans demander sa modification ici, sans le qualifier de régression et sans bloquer la lecture. Je n'ai pas consulté l'infrastructure pour en déduire le fonctionnement du lien.

**Aucun blocage nouveau précis repéré dans les productions demandées** au cours de cette relecture. Cette conclusion décrit les sujets actuels ; sans lecture de matrice ni comparaison historique, elle ne certifie pas à elle seule une conservation intégrale source → cible. Les preuves ci-dessous indiquent ce qui demeure compréhensible dans chaque activité.

## Preuves par question

« Clair » signifie que je peux identifier le but, les données et la production attendue depuis les seuls sujets. Ce terme ne prouve ni une résolution correcte ni la maîtrise d'étudiants réels. Les colonnes indiquent aussi où les notions sont présentées et quels essais ou critères je comprends devoir utiliser, sans donner les réponses.

### TD1 — Variables et types

| Question et cellules | But, données et production compris | Notions, prédiction, essai et vérification |
|---|---|---|
| Q1, 6–10 | Depuis prix et nombre de mots fournis, produire le coût dans la variable nommée puis l'afficher. | Affectation/calcul/print expliqués 5–7 ; prédiction d'un calcul mémorisé et essai 8 ; comparaison manuelle demandée 9. Clair. |
| Q2, 11–15 | Identifier le type de la note fournie, avec prédiction commentée et affichage. | Types/type expliqués 11–12 ; essai sur trois représentations 13. Je distingue prédiction personnelle et ligne d'affichage fournie. Clair. |
| Q3, 16–20 | Réutiliser les deux données de Q1 pour produire deux booléens calculés. | Comparaisons et and introduits 16–17 ; essais de limite 18 ; vérification contre saisie directe d'un booléen 19. Clair. |
| Q4, 21–25 | Créer les langues imposées puis une phrase au format exact par interpolation. | f-string/accolades expliquées 21–22 ; annonce différente en essai 23 ; espaces/apostrophe/point à vérifier 24. Clair. |
| Q5, 26–30 | Convertir la chaîne fournie avant l'ajout ; afficher valeur et type du résultat. | Conversion/concaténation distinguées 26–27 ; autres données en essai 28 ; type entier demandé 29. Clair. |
| Q6, 31–35 | Choisir une phrase et en afficher longueur, présence exacte du fragment et représentation de la source. | len/in/casse/repr expliqués 31–32 ; essai distinct 33 ; compte des espaces/ponctuation et commentaire justificatif 34. Le choix personnel n'est pas jugé automatiquement. Clair. |

Les cellules 2 et 4 rendent compréhensibles l'ordre d'exécution, le rôle de `#` et l'activation des lignes fournies. La synthèse 36 demande des explications appuyées sur les essais, pas seulement des sorties.

### TD2 — Chaînes et séquences

| Question et cellules | But, données et production compris | Notions, prédiction, essai et vérification |
|---|---|---|
| Q1, 5–8 | Nettoyer les bords de texte_brut, conserver la source, afficher texte propre et deux longueurs. | Méthode/immuabilité/strip introduits 5–6 ; len déjà TD1 ; prédiction puis explication source/espaces en 7–8. Clair. |
| Q2, 9–12 | Transformer le résultat précédent en deux étapes, afficher résultat et présences, montrer source conservée. | lower/replace en 9–10, in TD1 ; justification de l'ordre selon ces données demandée 11. L'exemple différent aide à interpréter sans fournir la réponse. Clair. |
| Q3, 13–16 | Extraire caractères et tranches du mot fourni et expliquer leurs bornes. | Indices positifs/négatifs et fin exclue en 13–14 ; dessin préalable des indices ; contrôle de longueur/source en 15. Clair. |
| Q4, 17–20 | Découper la phrase, afficher liste et éléments, comparer comptes et types. | split/liste/convention tokens en 17–18 ; distinction caractère/élément explicitement demandée 19. Prédiction des comptes possible avec TD1. Clair. |
| Q5, 21–24 | Assembler les tokens précédents avec le séparateur imposé, reconstruire et comparer la liste. | join/split exact en 21–22 ; prédiction des séparateurs ; égalité des listes précisée 23. Critère d'aller-retour clair. |
| Q6, 25–28 | Nettoyer séparément les trois chaînes fournies et construire une nouvelle liste ordonnée. | Liste littérale en 25–26 ; nettoyage déjà Q1–Q2 ; traitement par indices explicitement imposé, sans boucle. Observation source/espaces/accents définie 27. Clair. |
| Q7, 29–30 | Prédire puis observer le découpage de la phrase exacte et rédiger une limite fondée sur un fragment. | split déjà Q4 ; apostrophes/ponctuation à observer précisées 29. Les critères demandent lien observation/limite et distinguent présence d'un commentaire de son fond. Clair. |

Le rappel du TD1 (2–3), les exemples distincts (4), les commentaires personnels et le bilan 31 permettent de situer cours, démonstration, exercice et interprétation sans guide de score répété.

### TD3 — Collections

| Question et cellules | But, données et production compris | Notions, prédiction, essai et vérification |
|---|---|---|
| Q1, 6–10 | Ajouter puis retirer un outil et montrer l'état intermédiaire avant l'état final. | append/pop et valeur renvoyée expliqués 6–7 ; essai sur villes 8 ; placement des deux affichages explicite 9–10. Clair. |
| Q2, 11–15 | Représenter les trois langues données dans un tuple et justifier cette référence stable. | Tuple/ordre/mutabilité en 11–12 ; essai distinct 13 ; explication reliée aux possibilités de modification 14. Le fond n'est pas présenté comme autocorrigé. Clair. |
| Q3, 16–21 | Construire le lexique, ajouter une entrée, afficher traduction ciblée et dictionnaire complet. | Clés/valeurs/ajout en 16–17 ; essai sur animaux 18 ; correspondances autorisées entièrement fournies 20. Clair. |
| Q4, 22–26 | Réutiliser le lexique de Q3 pour produire une liste de fiches au séparateur exact. | for/indentation/items/déballage/accumulation introduits 22–23 ; essai 24 ; nombre de fiches et couverture de toutes les entrées à vérifier 25. Clair. |
| Q5, 27–31 | Transformer la liste fournie en ensemble et comparer occurrences et formes distinctes. | set/len/ordre non signifiant en 27–28 ; essai d'occurrence supplémentaire 29 ; contrôle manuel des valeurs distinctes 30. Clair. |
| Q6, 32–36 | À partir des deux corpus donnés, produire communs et éléments uniquement du premier. | Intersection/différence et asymétrie expliquées 32–33 ; essai sur langues 34 ; vérification dans listes sources 35. Clair. |

Les dépendances Q3 → Q4 sont annoncées cellule 2. La synthèse 37 demande de justifier le choix de collection avec une manipulation : elle conserve une activité d'interprétation.

### TD4 — Boucles et comptages

| Question et cellules | But, données et production compris | Notions, prédiction, essai et vérification |
|---|---|---|
| Q1, 6–10 | Transformer les mots fournis en majuscules via for, conserver ordre et source. | Parcours de liste/upper en 6–7, for TD3 ; états intermédiaires et essai de villes 8. Clair. |
| Q2, 11–15 | Filtrer la liste précédente avec un seuil strict de longueur. | if imbriqué et distinction > / >= en 11–12 ; essai 13 ; exclusion du cas exactement à la borne à contrôler 14. Clair. |
| Q3, 16–20 | Chercher la lettre indiquée sans casse puis conserver l'écriture originale des mots retenus. | Test distinct de valeur conservée en 16–17 ; lower/in déjà vus ; essai d'une autre lettre et discussion accent 18. Clair. |
| Q4, 21–25 | Produire une liste croissante d'entiers pairs sur l'intervalle donné avec range. | Début inclus/fin exclue/pas et modulo expliqués 21–22 ; essais de parcours inverse et parité 23. But et bornes clairs. |
| Q5, 26–30 | Construire les multiples demandés avec while qui progresse et s'arrête. | Condition/mise à jour en 26–27 ; essai borné et réflexion sans exécution d'une boucle infinie 28 ; prédiction dernière retenue/première rejetée 29. Clair. |
| Q6, 31–35 | Compter les occurrences des formes de la liste préparée dans un dictionnaire. | get ou if/else en 31–32 ; états à chaque occurrence en essai 33 ; cohérence total/liste à vérifier 34. Clair, aucune fonction sum imposée. |
| Q7, 36–40 | Construire par compréhension les longueurs des mots retenus au seuil strict. | Compréhension décomposée 36–37 ; boucle/compréhension à comparer en essai 38 ; confrontation aux mots de Q2 en 39. Clair. |

La cellule 4 évoque aussi les essais après définition d'une fonction, alors qu'aucune fonction n'est à écrire dans ce TD. C'est une information générique sans application ici ; elle ne crée pas de dépendance ni de blocage dans les exercices. Je n'en déduis pas une régression du nettoyage.

### TD5 — Fonctions et réutilisation

| Question et cellules | But, données et production compris | Notions, prédiction, essai et vérification |
|---|---|---|
| Q1, 6–11 | Définir une fonction recevant une chaîne et retournant sa longueur, puis tester les entrées données. | def/paramètre/localité/return/None en 6–7, len TD1 ; essai fonction distincte 8 ; cas vide après réponse 11. Clair. |
| Q2, 12–17 | Définir normaliser avec bords retirés et minuscules, en conservant espaces internes. | Méthodes TD2, rappel et exemple 12–13 ; essai distinct 14 ; cas vide/espaces après réponse 17. Clair. |
| Q3, 18–23 | Compter les fragments en réutilisant normaliser ; retourner un nombre. | Composition et comportement vide de split expliqués 18–19 ; essai de valeur par défaut 20 ; cas vide/espaces multiples 23. Clair. |
| Q4, 24–29 | Normaliser le mot puis chercher dans le lexique reçu, sinon retourner la forme normalisée. | Paramètre dictionnaire et sensibilité des clés en 24–25 ; essais de présence 26 ; entrées connues/inconnues/vides en 29. Clair. |
| Q5, 30–35 | Traduire chaque fragment par appel à Q4 puis retourner une chaîne recomposée. | for TD3–4, join TD2 ; recomposition/liste vide en 30–31, essai 32 ; vérifications d'inconnu/espaces/vide après réponse 35. Clair. |
| Q6, 36–41 | Retourner un résumé à trois clés précises décrivant le texte normalisé reçu. | Retour dictionnaire en 36–37 et fonctions précédentes ; essai de tranche vide 38 ; nouvelle entrée et vide en 41, cohérence comptes/texte demandée. Clair. |

Le positionnement des vérifications après les fonctions est explicite cellule 4 et matériellement respecté dans le parcours. Les cellules 42–43 conservent une synthèse personnelle sur un test utile et une difficulté.

### TD6 — Fichiers et CSV

| Question et cellules | But, données et production compris | Notions, prédiction, essai et vérification |
|---|---|---|
| Q1, 5–11 | Lire le fichier fourni par préparation, conserver le contenu et afficher sa longueur. | Préparation à exécuter sans modification 5–6 ; with/open/read/UTF-8 expliqués 7–8 ; essai sur fichier distinct 9. Clair. |
| Q2, 12–16 | Découper le contenu et conserver les lignes utiles dans l'ordre. | splitlines/chaîne vide/espaces en 12–13 ; entraînement filtre 14, if/for TD4. Nombre de lignes à afficher identifié. Clair. |
| Q3, 17–21 | Séparer chaque ligne au premier point-virgule en deux champs et conserver graphies/ordre. | maxsplit expliqué 17–18, essai 19 ; tuples/listes TD3 ; premier couple et liste complète demandés 20–21. Clair, deux représentations autorisées. |
| Q4, 22–27 | Définir la normalisation des personnes selon la convention donnée et afficher les variantes. | split/join/strip déjà TD2, title introduit 22–23 ; essai 24, cas imposés 25–27. Graphie et preuve d'identité clairement distinguées. |
| Q5, 28–33 | Regrouper les affiliations distinctes par personne normalisée depuis Q3 et Q4. | set vide/add et dictionnaire de valeurs ensembles expliqués 28–29 ; essai de doublon 30 ; vérification de chaque personne 31–33. Clair. |
| Q6, 34–38 | Écrire un CSV avec en-tête/colonnes précis puis afficher sa relecture fournie. | Import/csv.writer/writerow/mode/newline en 34–35 ; essai distinct 36 ; séparateur intérieur/extérieur et contrôle nombre/cohérence définis 37. Clair. |

La préparation fournie avec Path est distinguée du travail personnel. Les dépendances du traitement et le statut du CSV sont expliqués avant les questions concernées ; aucun fichier extérieur à retrouver.

### TD7 — Motifs et pipeline

| Question et cellules | But, données et production compris | Notions, prédiction, essai et vérification |
|---|---|---|
| Q1, 5–12 | Chercher le motif indiqué sans casse dans le texte donné et conserver un booléen. | Import re expliqué 5–6 ; search/bool/None/IGNORECASE en 8–9 ; essais présence/absence 10. Clair. |
| Q2, 13–17 | Extraire toutes les suites de chiffres dans l'ordre en gardant des chaînes. | Classes/+ et findall en 13–14 ; prédictions et essai sans nombre 15. Type de sortie explicitement demandé 16. Clair. |
| Q3, 18–22 | Extraire les suites de lettres accentuées selon convention puis commenter une différence avec split. | Classes étendues et limites 18–19 ; essais accent/apostrophe 20 ; critère fragment observé/caractère responsable 21. Clair. |
| Q4, 23–28 | Remplacer la forme de date donnée, préserver les autres caractères et nombres. | sub/répétition bornée en 23–24 ; essai de forme incomplète 25 ; test après réponse 28. Reconnaissance formelle distincte de validité calendaire. Clair. |
| Q5, 29–34 | Définir une chaîne de transformations dans l'ordre imposé, retourner le texte puis tester. | Effet de l'ordre sur marqueur en 29–30 ; prédiction/explication 31 ; cas vide/espaces/date 34. Casse du marqueur et ponctuation conservée explicites. Clair. |
| Q6, 35–40 | Réutiliser nettoyage puis extraction et comptage, retourner trois informations nommées. | Pipeline expliqué 35, comptage repris du TD4 en 36 ; prédiction 37 ; cohérence liste/effectifs et effet possible du marqueur à interpréter 38–40. Clair. |
| Q7, 41–45 | Expliquer une limite linguistique par un cas personnel différent de l'exemple. | Forme/sens et correspondances vides expliqués 41–42 ; essai 43 ; critères cas concret/décision/information utile, avec limite du score, en 44. Clair. |

## Limites et handoff

Fichier créé uniquement : `Corrigés modèles/TD/s1-presentation-cleanup/lecture_etudiante.md`. Aucun nouveau notebook modèle, aucune solution, aucune modification des sept sujets ni des autres ressources. Aucune identité réelle consultée.

Contrat examiné : compréhension étudiante des sujets et présentation demandée dans AGENTS, en tenant compte du périmètre communiqué qui conserve les cellules finales fournies à l'identique. Références autorisées comparées : notions des TD précédents du même parcours courant ; aucune matrice historique ni aucun autre rapport utilisé.

Vérification effectuée : lecture exhaustive des 293 sources de cellules et preuve documentaire sur les 45 questions ; comptage des cellules, recherche ciblée dans leurs sources des présentations Gemini et des minutages, empreintes des sujets. Ces scripts lisent le JSON ; ils n'exécutent pas le code des notebooks. Aucun test de correcteur ou de code étudiant, conformément à la mission.

Résultat de lecture : données, productions, notions introduites avant usage, prédictions, entraînements et critères d'interprétation identifiables pour les 45 questions. Présentation de Gemini et guide général visibles au TD1 ; notices d'identification et minutages absents. Dépôt compréhensible sur le plan des actions décrites. Aucun passage précis resté incompris empêchant d'engager une question ; le commentaire de fabrication des cellules finales est consigné séparément.

Non vérifié : rendu Colab, fonctionnement du lien et du dépôt, exécution, résultats calculés, duplication du tuteur dans les métadonnées, qualité réelle de l'accompagnement, comportement des correcteurs, durée et maîtrise d'étudiants réels. Le titre suivi du commentaire caché dans la première cellule est observable dans les sources, sans valider le rendu ni l'équivalence des métadonnées.

Risques : confondre compréhension d'une consigne et aptitude à résoudre ; compter le contexte machine comme enseignement ; affirmer une conservation historique exhaustive sans la revue source → cible. Aucun de ces raccourcis n'est adopté ici.

Critères d'acceptation proposés aux reviewers : maintenir les données/formats et critères locaux identifiés ; vérifier indépendamment le niveau de couverture et l'écriture française ; qualifier le commentaire des cellules finales au regard du périmètre autorisé. Verdict demandé : revue pédagogique et revue éditoriale **distinctes**, puis gouvernance. Ce rapport est un contrôle complémentaire de lecture, sans validation de cours réel ni verdict READY_TO_MERGE.
