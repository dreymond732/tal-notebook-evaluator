# Lecture préalable des 71 questions du parcours S3

Date : 7 octobre 2026. Rôle : TAL-Étudiant-Modèle. Branche annoncée : `pedagogy/notebook-presentation-order`.

## Mission et périmètre

Vérification rédactionnelle, sans résolution nouvelle, exécution de notebook ni soumission. Aucune identité réelle utilisée ; aucune copie étudiante produite. Seul fichier écrit : cette note. Aucun sujet modifié. Les scripts utilisés ont uniquement lu le JSON des notebooks ; ils n'ont exécuté aucune cellule.

Contrats lus : `AGENTS.md` et `docs/agents/TAL-Étudiant-Modèle.md`. Sources pédagogiques lues : les douze notebooks de `Notebooks TD/S3`, son `README.md` et `ressources/README.md`. Aucun correcteur, test de dépôt, corrigé existant, infrastructure ou source externe consulté. Aucun ancien sujet nécessaire à cette lecture. Les liens externes, les fichiers de corpus/affirmations/citations et leurs sorties réelles ne sont pas vérifiés : leur chargement est décrit dans les sujets, leur contenu n'a pas été inféré.

Indices de cellules ci-dessous à partir de zéro. Lecture du contenu visible intégrale (Markdown et code fourni), y compris préparation, exemples, consignes, réponses à compléter, exports et restitution : TD0 c0–28 ; R0 c0–16 ; TD1.a c0–39 ; TD1.b c0–25 ; TD1.c c0–35 ; R2 c0–25 ; TD2 c0–38 ; TD3 c0–39 ; TD4 c0–46 ; TD5 c0–45 ; TD6 c0–52 ; TD7 c0–49. Les longs contextes cachés ne sont pas relus comme une source étudiante : seule leur présence après le titre dans la même première cellule a été constatée pour les douze cahiers. L'identité métadonnées/commentaire caché ne relève pas de cette lecture.

Ordre compris : TD0, R0 si Q1–Q5 bloquent, TD1.a, TD1.b facultatif, TD1.c, R2, TD2–TD7. Le statut facultatif de TD1.b est explicite et ne conditionne pas R2. Le caractère conditionnel est confirmé par la relecture finale de R0 ; le README reste plus succinct.

## Constats transmis aux revues

- **L1 — retiré après contre-lecture éditoriale :** `Été : lire.` comporte bien 11 caractères (3 + 1 + 1 + 1 + 4 + 1). Mon premier signalement était une erreur de lecture ; aucun défaut du sujet n'est retenu.
- **L2 — résolu et relu, TD0 c10 :** `mots.` absent des données est remplacé par `rôle.`, présent dans `texte_source`. La demande d'observation rejoint désormais les données.
- **L3 — réserve pédagogique antérieure, TD0 c24 :** distinguer tokenisation, lemmatisation et famille lexicale est demandé avant l'explication visible du lemme dans TD1.a c9. Le diagnostic peut viser des acquis antérieurs ; ceux-ci n'ont pas été consultés. Je signale cette limite sans en faire un défaut créé par la révision de présentation.
- **L4 — résolu et relu, R0 c1 :** l'ouverture indique désormais « Après TD0, reprenez ce cahier si nécessaire avant TD1.a ». Le README donne l'ordre sans répéter cette condition ; l'ouverture lève l'ambiguïté.
- **L5 — résolu et relu, TD0 c6 :** la référence au « temps déjà prévu » a été retirée.
- **L6 — résolu et relu, TD2 c35 et TD3 c36 :** les notices sur les informations d'identification et « mauvaise version du notebook » ont été retirées.
- **L7 — réserve pédagogique antérieure, TD4 c10 :** `is_alpha` intervient sans définition visible préalable repérée. Une définition locale lèverait l'hésitation sur les tokens alphabétiques. Ce point dépasse la seule révision de présentation ; les acquis plus anciens ne sont pas vérifiés.
- **L8 — observation de présentation résiduelle :** le commentaire de restitution « URL injectée lors du déploiement » décrit la fabrication et les blocs de lien répètent trois étapes générales. Transmis à la revue éditoriale pour distinguer commentaire technique existant, fonctionnement du bloc de dépôt et texte pédagogique. Aucun blocage de compréhension d'une question n'en est déduit.

Relecture ciblée finale : TD0 c5/c6/c10/c24/c28 ; R0 c1 ; TD2 c35 ; TD3 c36 ; tableau de parcours du README. Les constats clos ci-dessus reposent sur les textes relus, pas sur une annonce de tests.
Ces constats sont des obstacles de lecture ou des réserves de présentation, pas des diagnostics du serveur. Les commentaires expliquant la vérification des ressources locales sont utiles pour comprendre le chargement ; ils ne constituent pas à eux seuls un blocage étudiant.

## Lecture question par question

Chaque ligne note ce que je comprends devoir réaliser avant tout essai. « Clair » signifie que données, production et moyens sont identifiables à la lecture ; cela ne valide ni l'exécution ni le correcteur. Les exemples fournis sont des ressources d'apprentissage ; les fonctions, essais personnels, analyses et traces demandées restent à construire par l'étudiant.

### TD0 — 7 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c7 | Lire `corpus_td0.txt`, préserver Faguet et comparer à `texte_source` | `resultat_q1.caracteres`, égalité, longueur Faguet et commentaire | UTF-8, `with`, longueur : c5–6 | Clair ; signalement L1 retiré ; chemin Faguet visible en c3 |
| Q2 c10 | Découper `texte`, observer les unités et créer un essai | Liste complète `mots_bruts` sous `mots`, observation | `split` et ponctuation : c9 | Clair après résolution L2 (`rôle.`) |
| Q3 c12 | Compter `mots_bruts` par longueur et boucle ; transférer à Faguet | `occurrences`, comparaison et unité nommée | Boucle et compteur réactivés dans l'objectif ; Q1–2 | Clair ; acquis Python supposés, R0 indiqué au bilan |
| Q4 c15 | Construire les formes distinctes, comparer au total | `formes`, deux phrases et comparaison de casse/pluriel | `set`, occurrence/forme : c14 | Clair |
| Q5 c20 | Fonction de fréquences sur liste, vide puis passage Faguet | Dictionnaire complet `frequences`, cinq paires et deux invariants | Fonction, `.get`, `return` : c17 ; contrôles c18 | Clair |
| Q6 c22 | Minuscule puis découpage et appel de Q5 | Fréquences complètes, trois comparaisons, conservation du total | `lower` annoncé dans la consigne ; fonction Q5 | Clair ; introduction de `lower` concise |
| Q7 c24 | Comparer découpage et regroupements ; lire G1 et proposer protocole | `split` sur exemple fixé, `limites`, Markdown argumenté | Découpage Q2 ; normalisation Q6 | L3 ; contenu de G1 non vérifié dans cette mission |

### R0 — 4 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c6 | Compter les fragments du texte fourni, du vide et d'« Un essai » | Fonction `compter_mots`, `tests_comptage` à trois clés | `return` c5 ; `split`, `len` TD0 | Clair |
| Q2 c8 | Mettre en minuscules et découper le texte c4 | `mots_normalises` avec répétitions et ponctuation | TD0 Q2/Q6, méthodes nommées ici | Clair |
| Q3 c12 | Fonction normalisant et comptant deux textes | `tests_frequences`, deux dictionnaires calculés | `.get` c10, fonction TD0 Q5 | Clair |
| Q4 c14 | Réutiliser Q3 sur « Python Python. » et interpréter | `bilan_limite.comptes` et phrase `limite` | Q3 et séparation ponctuation TD0 | Clair |

### TD1.a — 6 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c16 | Lire `doc` sans ponctuation et comparer cinq annotations manuelles sur leur texte propre | Six champs par token sous `annotations`, prédictions et commentaires | `Doc`, `Token` c3 ; attributs c9–10 ; positions c11–13 ; JSON c14–15 | Clair : trace et comparaison portent explicitement sur deux textes distincts |
| Q2 c20 | Parcourir phrases de `doc`, tester abréviation et citation séparément | Liste `phrases` texte/nombre de tokens, essais et observation Faguet | `Span`, `sents`, bornes : c18–19 | Clair |
| Q3 c24 | Comparer trois sélections de lemmes sur `doc` | `noms`, `verbes`, `mots_pleins` ordonnés, répétitions et justification | Filtre, `is_stop`, exemple adjectifs : c22–23 | Clair |
| Q4 c28 | Visualiser première phrase, lire une dépendance et risque de citation | Figure, formes, positions, relation et interprétation | `head`, `dep_`, displaCy : c26–27 | Clair ; lecture humaine et modèle distincts |
| Q5 c32 | Comparer trois découpages du même `texte_td0` | `split`, `tokens`, `non_ponctuation`, deux écarts explicités | `is_space`, `is_punct` : c30–31 ; TD0 | Clair ; conventions différentes explicites |
| Q6 c34 | Réinvestir sur extrait choisi de 2–4 phrases | Extrait, cinq premiers tokens, phrases, listes NOUN/VERB, question et limite | Ensemble du TD ; autonomie annoncée | Clair ; ponctuation et bornes de l'extrait précisées |

### TD1.b facultatif — 4 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c9 | Analyser la phrase c6 et compter tous les tokens | `doc`, affichage `len(doc)`, explication de l'unité | Rappel c7–8, TD1.a | Clair |
| Q2 c15 | Décrire tous les tokens de ce `doc` | `annotations`, triples forme/lemme/POS, ordre et ponctuation | Attributs et tuples c11–14 | Clair |
| Q3 c19 | Sélectionner les lemmes des noms prédits | Liste `noms`, rapprochement aux triples | Condition et exemple adjectifs c17–18 | Clair |
| Q4 c21 | Adapter le filtre aux verbes | Liste `verbes`, commentaire si désaccord | Q3 | Clair ; vide explicitement valide |

### TD1.c — 4 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c11 | Comparer repérage humain et entités de `texte_q1` | `entites_q1`, couples ordonnés et observations avant/après | Entités, labels, `doc.ents` : c9–10 | Clair ; absence de DATE/MONEY cadrée |
| Q2 c16 | Filtrer PER/ORG sur `texte_q2` puis texte personnel | Quatre listes et texte personnel ; observations | Filtrage et faux positif c14–15 | Clair |
| Q3 c21 | Comparer deux couples de mots, deux phrases et une variante | Booléens vecteurs, trois scores, variante et score, interprétation | Vecteurs, moyenne, limites et `similarity` : c19–20 | Clair ; pas d'ordre de score imposé |
| Q4 c29 | Règle Toulon puis trois règles ; éprouver cinq textes | Avant/après, règles, pipeline, essais complets et tableau commenté | `EntityRuler`, règles exactes, comparaison : c24–28 | Clair ; relance et exact/variante/ambiguïté explicités |

### R2 — 4 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c9 | Compter les lemmes NOUN du texte c6 dans une fonction | `frequences_lemmas`, retour `Counter` sans aucune exclusion | `Counter`, paramètres, `None`, `return` : c7–8 ; TD1.a | Clair ; TD1.b non requis |
| Q2 c13 | Montrer tous les tokens pour expliquer le compte | Triples `annotations`, vérification et commentaire | Tuples c11–12 ; TD1.a | Clair |
| Q3 c19 | Réécrire Q1 avec `is_stop` et exclusions par lemme | `tests_filtrage` avec/sans `['texte']`, prédictions | Mots vides, `None`, appartenance : c15–18 | Clair ; aucune différence artificielle exigée |
| Q4 c23 | Comparer classements complets de la fonction révisée | `classements.avant/apres`, commentaire | `.most_common`, ex æquo : c21–22 | Clair ; même filtre spaCy des deux côtés |

### TD2 — 7 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c9 | Lire microcorpus, annoter, compter et montrer dix tokens hors ponctuation | Trois comptes, dix annotations et observation | Lecture/Doc c7–8 ; TD1.a | Clair ; ressource chargée mais non ouverte dans la mission |
| Q2 c14 | Deux fonctions comptant NOUN/VERB filtrés, essais répétés | Comptes complets `noms/verbes`, cinq premiers et vérifications | Counter et dénominateur c11–12 ; exclusions c13 ; R2 | Clair |
| Q3 c20 | Choisir une exclusion réellement présente et justifier | `exclusions`, comptes avant/après, `justification` | Filtre et invariants c16–19 | Clair ; conserver un nom pour Q6 annoncé |
| Q4 c23 | Compter POS hors ponctuation/espaces | Compte `pos`, `top3`, `limite` | Distribution et ex æquo c22 ; TD1.a | Clair |
| Q5 c27 | Filtrer lemmes de contenu et juger cinq occurrences | `lemmes`, cinq annotations/jugements, `limite_modele` | Forme/lemme/expression, PhraseMatcher c25–26 | Clair ; annotations conservées sans correction |
| Q6 c31 | Dessiner nuage et barres des mêmes noms filtrés de Q3 | Deux figures, fréquences, hypothèse et concordance à rechercher | WordCloud/Matplotlib c29–30 | Clair ; cas vide et recalcul explicités |
| Q7 c33 | Généraliser les fonctions et transférer aux 5 000 premiers caractères Faguet | Cinq comptes de comparaison sur microcorpus, essais vides, transfert séparé | Q2 et paramètres ; autonomie annoncée | Clair |

### TD3 — 7 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c10 | Lire notice, conversation, affirmations et empreinte | Fiche `sha256`, six ids, prompts, manquants, limite | Provenance et sources c9 | Clair ; ressources elles-mêmes hors lecture, disponibilité non certifiée |
| Q2 c17 | Fonction de concordance, tests limites puis source_test et Faguet | Trois concordances `droit`, absence `justice`, tests et trois contextes | `find`, tranches c7–8 ; contexte c12–13 ; while/erreur c14–16 | Clair |
| Q3 c23 | Comparer fragment/forme/lemme sur petit texte, expression en transfert | Trois listes de formes/bornes, explication et transfert séparé | Rappels c19–22 ; TD2 PhraseMatcher | Clair |
| Q4 c25 | Vérifier trois citations exactes sans normalisation | Trois ids/citations/débuts/booléens, `limite` | Recherche Q2, source intacte | Clair ; absence textuelle distincte d'absence d'idée |
| Q5 c30 | Normaliser absentes, localiser passage C1 par fragment | Passage source exact, début, différence, verdict argumenté | Fonction fournie c27–28, positions et qualifications c29 | Clair ; existence du candidat non vérifiée ici |
| Q6 c32 | Deux passages « professions », puis deux cas personnels | Deux tests exact/altéré avec attentes préalables, règle humaine | Q4–5 ; autonomie annoncée | Clair ; sélection effective de passages non vérifiée |
| Q7 c34 | Dossier G1/G2 avec trois occurrences distinctes | `preuves` bornées, convention proposée et limite | Concordances et notion fenêtre/agrégation définie ici | Clair ; contexte choisi librement, source préservée |

### TD4 — 7 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c10 | Marges sur quatre listes puis formes minuscules par phrase Faguet | `chat`, `livre`, `N`, fonction `marge`, observations Faguet | Présence/marge c8–9 ; phrases TD1.a | L7 : `is_alpha` non défini localement |
| Q2 c16 | Cooccurrence booléenne, trois paires microcorpus et deux Faguet | Trois comptes, assertions, cas absent et phrases preuves | Assertion c13–15 ; convention par phrase c14 | Clair |
| Q3 c21 | Distinguer somme des paires et union sur trois listes | `somme_paires`, `union`, fonction, lecture ligne Gemini | Repère c19 et exemple c20 | Clair |
| Q4 c27 | Compter paires de positions en fenêtre sur flux fixé | `k1/k3`, paires manuelles, Faguet k5/k10 avec indices | `token.i/idx` c24 ; distance, enumerate/abs c25–26 ; refus TD3 | Clair ; fonction et conservation des preuves demandées |
| Q5 c31 | Comparer flux concaténé/phrases puis trois frontières Faguet | `sans_frontiere/dans_phrase`, tableau aux unités explicites | Frontières c30 ; fonctions précédentes | Clair ; paragraphe non assimilé au chapitre |
| Q6 c36 | Formes/lemmes sur annotations manuelles puis Faguet | Deux comptes, cinq observations et recherche d'expression | Distinction c34–35 ; TD3 expression | Clair ; nouvelle convention d'espaces explicitée |
| Q7 c41 | Assembler mesures par phrase et export des deux paires Faguet | N/cooc/marges microcas, bornes/vide, `td4_mesures.json`, bilan | Q1–6 ; JSON c6–7 ; réemploi c39–40 | Clair ; format export libre mais contenu demandé |

### TD5 — 7 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c11 | Représenter huit phrases compatibles puis proportions | `conditionnelle/base`, fonction et paire TD4 avec dénominateurs | Tableau c8 ; proportions c9–10 | Clair |
| Q2 c15 | Comparer associés A/B et deux associés Faguet | Quatre proportions, comparaison et passages | Fréquence/concentration c14 et Q1 | Clair ; pas de significativité requise |
| Q3 c20 | Taux petits extraits puis moitiés alphabétiques de Faguet | `court/long`, fonction, effectifs/tailles/taux/indices | Pour mille c18–19 ; cas indéfini c8 | Clair ; taille zéro à traiter explicitement |
| Q4 c24 | Inverser condition sur mêmes marges | Deux proportions, fonction/test, 2 × 2 et commentaires | Population c23 ; tableau c8 | Clair |
| Q5 c30 | Distinguer absence pivot/associé et faibles effectifs | `sans_pivot/sans_associe`, tests, terme rare et limite | `None`/arrondi c27–29 | Clair ; PMI explicitement facultative après prérequis |
| Q6 c36 | Couverture des positions du pivot, trois fenêtres Faguet | `k1/k3`, nombres couverts/totaux, sensibilité | Position couverte c33–35 ; fenêtres TD4 | Clair pour couples distincts étudiés |
| Q7 c40 | Synthèse microcas et export de deux paires/trois fenêtres | effectif/dénominateur/proportion, `td5_associations.json`, paragraphe | Q1–6 ; rapport c39 | Clair ; recomptage de seconde paire annoncé si nécessaire |

### TD6 — 7 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c13 | Positions petit flux puis dispersion trois pivots Faguet | Positions/relatives, fonction, dispersion, deux passages | Matplotlib c9 ; position relative/eventplot c11–12 | Clair |
| Q2 c18 | Segmenter petit flux puis dix segments Faguet | Effectifs/tailles, test 11 tokens, bornes et contrôles | Intervalles/segments vides c16–17 | Clair ; flux entier et tailles alphabétiques distincts |
| Q3 c24 | Calculer taux puis carte trois pivots × dix segments | Taux microcas, matrice/effectifs, figure et case choisie | Axes, matrice, imshow c21–23 ; TD5 | Clair ; même échelle et indéfini signalés |
| Q4 c29 | Paires par fenêtre et couverture à part | k/cooc microcas, tables/courbes deux paires et commentaires | Courbe c27–28 ; TD4/TD5 | Clair ; changement d'unité explicite |
| Q5 c35 | Contexte par tranche, puis passages de la case retenue | Début/fin/contexte microcas ; passages exacts et lecture | Original/tranche c32–34 ; TD3 | Clair ; changement de case autorisé si nécessaire |
| Q6 c40 | Reprendre taux en barres puis matrice cooccurrences trois pivots | Étiquettes/valeurs, figures/table/légende, relecture par voisin | Barres c38–39, Q3 et TD4 | Clair en séance ; dépend d'une relecture humaine non réalisable ici |
| Q7 c47 | Agréger effectifs/tailles, exporter et interpréter | Trois valeurs microcas, JSON, figures, deux paragraphes, table pour audit | Agrégation c43–44 ; savefig c45–46 | Clair |

### TD7 — 7 questions

| Question / cellule | Attente et données | Production comprise | Notions et lieu d'apprentissage | Lecture |
|---|---|---|---|---|
| Q1 c13 | Identifier quatre champs absents/None et lire six annonces | `mesurable/manquants`, tableau et `protocoles_audit` séparés | Champs c10–11 ; annonce/protocole c12 | Clair ; portée limitée de la présence des champs explicitée |
| Q2 c19 | Assembler moteur union et recherche d'expression | N/cooc/marges, indices de preuves, tests expression et Faguet | Contiguïté c16–17, moteur c18 ; TD4 | Clair ; espaces seuls filtrés dans représentation dédiée |
| Q3 c24 | Vérifier citation/variante puis trois citations réelles | Exacte/bornes/altérée, statuts et différences | Exactitude c22–23 ; TD3 | Clair ; difflib optionnel, non nécessaire |
| Q4 c30 | Comparer intervalle seulement si protocole défini | Deux libellés exacts, fonction/tests bornes, garde préalable | Statut/recomptage c27 ; comparaison c28–29 | Clair |
| Q5 c34 | Étendre moteur somme des paires aux six annonces | Somme/union microcas, six protocoles/recomptages, preuves et figure | Agrégation c33 ; TD4 ; Matplotlib repris explicitement | Clair ; charge conséquente mais composantes annoncées |
| Q6 c39 | Nouveau corpus manuel, cas voisin et limites | N/cooc/marges, lot attendu/observé, cinq observations linguistiques | Lot manuel c37 ; généralité c38 | Clair en séance ; cas voisin hors mission de lecture |
| Q7 c44 | Assembler fonction audit, deux annonces test et dossier complet | Deux verdicts, JSON six lignes/citations/tests, tableau, synthèse 200–300 mots et figure | Assemblage c42–43 et Q1–6 | Clair ; `protocole_original` est distingué des choix exploratoires |

## Verdict de lecture et limites

Les 71 consignes disposent d'une production identifiable. Le parcours rend généralement explicites données fixes, petits essais, transferts à Faguet, interprétations humaines et limites du retour automatique. Les exemples et les espaces de réponse sont distingués ; la plupart des nouvelles opérations sont présentées avant emploi. Les quatre questions du complément TD1.b sont lisibles sans leur conférer le statut de prérequis de R2.

Verdict : lecture des 71 questions achevée, sans blocage de présentation restant sur les questions après les corrections relues. L1 est retiré ; L2, L4, L5 et L6 sont clos. L3 et L7 restent des limites de vérification des acquis, non des régressions établies ; L8 est une observation de présentation transmise à la revue. Ces distinctions ont été transmises aux rôles Editorial-Reviewer et Pedagogy-Reviewer. Cette note ne remplace ni leurs verdicts indépendants, ni une vérification technique, ni une lecture humaine des productions effectivement réalisées.

Restent non vérifiés : contenu effectif et disponibilité réseau des ressources, résultats spaCy, exécution et redémarrage Colab, sorties JSON, figures rendues, export réel, compatibilité de correction, comportement du tuteur, comparaison historique des couvertures, métadonnées internes. Aucune réussite étudiante, absence de bug ou conformité du serveur n'est déduite de cette lecture.
