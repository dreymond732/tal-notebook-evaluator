# Devoir maison intermédiaire S1 — Spécification pédagogique

Note de suivi (1er octobre 2026) : les chemins S1 cités ci-dessous documentent les sources historiques. Les dénominations actuelles et leur correspondance sont données dans la [revue des TD S1](s1_td_review_distribution.md) ; les activités correspondantes restent conservées.

Statut : cadrage du TAL-Prof, soumis aux revues indépendantes. Nouvelle création demandée après le TD5 ; le document d'inspiration n'est ni remplacé ni modifié.

## Périmètre et sources effectivement examinées

- Pièce fournie : `CorrectionDM-S1.ipynb`, 61 cellules. Elle comprend 16 questions numérotées réparties en quatre ensembles (4 + 2 + 3 + 7), un jeu final, ainsi qu'une activité informelle de renversement de chaîne. Elle sert à calibrer la variété et la charge, pas de corrigé à reproduire.
- Lecture complète du Markdown **et** du code de `Notebooks TD/S1/TD1_S1_python_texte.ipynb` à `TD5_S1_python_texte.ipynb`.
- TD1 : variables, types, expressions numériques, conversion en entier, comparaisons, conjonction, f-string, longueur, appartenance.
- TD2 : strip/lower/replace, index et tranches, split/join, listes, maintien de la source, limites du découpage.
- TD3 : listes, tuples, dictionnaires et items(), ensembles, intersection et différence.
- TD4 : for, conditions, range, while, compteurs, dictionnaire de fréquences, compréhension de liste.
- TD5 : paramètres, return, normalisation, composition, traduction par dictionnaire, résultat structuré.

La référence contient `input`, `eval`, un import aléatoire implicite, la notation scientifique et des opérations non explicitement enseignées par ces cinq TD. Ces éléments ne deviennent pas des prérequis du nouveau devoir. La saisie est remplacée par des données fournies, et le jeu par une suite prédéfinie de propositions. Le contexte personnel/date de naissance est remplacé par des données entièrement synthétiques.

## Format et politique d'assistance

18 questions réparties en cinq parties, avec plusieurs demandes par question. Charge indicative : 3 à 4 heures, à ajuster après observation des premières copies ; ce n'est pas une mesure expérimentale. Travail autonome, consultation des TD autorisée, aucune assistance du tuteur (mode `controle`, y compris quiz, explication, correction et code). Aucun import, fichier externe, réseau, `input`, `eval`, bibliothèque, regex, pandas ou notion du S2 n'est nécessaire.

Sujet : `Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb` ; identifiant tuteur `DM_INTERMEDIAIRE_S1` ; évaluateur `dm-intermediaire-s1`. Identité fictive uniquement dans les modèles ; sujet vierge avec nom/prénom/classe et numéro étudiant suivant le contrat technique existant.

Chaque Q possède une cellule réponse dédiée et un affichage `Résultat Qn :` suivi d'un unique objet Python (liste, dictionnaire, ensemble contenu dans une liste). Les lignes d'affichage peuvent être fournies commentées : elles décrivent l'interface de restitution sans donner l'algorithme. Elles ne doivent pas être remplacées par des sorties attendues. Les valeurs ci-dessous sont réservées au contrat enseignant et au correcteur ; elles ne figurent pas dans les réponses étudiantes.

Le contexte commun est une petite bibliothèque qui organise des ateliers multilingues. Les parties A–D disposent de leurs propres données pour éviter qu'une erreur initiale bloque tout le devoir. La partie E compose volontairement des fonctions ; les appels de chacune restent vérifiables séparément.

## Contrat des questions

### Partie A — Préparer un atelier (Q1–Q3, environ 25 minutes)

**Q1 — Calculer un budget.** Données `inscrits_saisis = "12"`, `tarif = 7.5`, `frais_fixes = 18`. Créer `nb_inscrits` entier, `recette`, `budget_total` correspondant à la recette augmentée des frais fixes. Convention de cet exercice : les frais fixes sont une contribution supplémentaire de la bibliothèque au budget disponible, et non une dépense à soustraire de la recette. Calculer aussi le coût moyen `cout_moyen` en divisant le budget total par le nombre d'inscrits. Afficher `[nb_inscrits, recette, budget_total, cout_moyen, type(nb_inscrits) == int]`. Attendu `[12, 90.0, 108.0, 9.0, True]`. Les calculs partent des données ; pas de constantes-réponses.

**Q2 — Lire une expression.** Données `stock = 60`, `reserve = 12`, `ateliers = 4`. Calculer `quantite_a = stock - reserve / ateliers` et `quantite_b = (stock - reserve) / ateliers`. Afficher `[quantite_a, quantite_b]`, attendu `[57.0, 12.0]`. Ajouter `# Explication Q2 :` en deux ou trois phrases : différence d'ordre des opérations et formule correspondant à un partage égal du stock restant. Le sujet fournit les deux expressions à interpréter ; il ne fournit pas leur résultat.

**Q3 — Tester une inscription.** Données `langue = "italien"`, `langues_ouvertes = ("français", "italien", "espagnol")`, `places = 0`, `tarif = 7.5`. Construire `langue_proposee`, `inscription_possible` (langue proposée ET strictement plus de zéro place), `tarif_valide` (tarif strictement positif). Construire par f-string `message` : `Atelier italien : 0 place(s).` Afficher `[langue_proposee, inscription_possible, tarif_valide, message]` : `[True, False, True, "Atelier italien : 0 place(s)."]`.

### Partie B — Préparer les annonces (Q4–Q7, environ 35 minutes)

**Q4 — Transformer sans effacer.** Donnée `annonce_brute = "  ATELIER de LIVRES  "`. Construire `annonce_propre` (bords retirés), `annonce_normalisee` (minuscules), `annonce_adaptee` (remplacer `livres` par `récits`). Afficher `[annonce_propre, annonce_normalisee, annonce_adaptee, annonce_brute]`. Attendu `["ATELIER de LIVRES", "atelier de livres", "atelier de récits", "  ATELIER de LIVRES  "]`. La source doit rester intacte.

**Q5 — Extraire une référence.** Donnée `reference = "BIB-FR-2026"`. Produire `premier_caractere`, `dernier_caractere`, `service` (3 premiers caractères), `code_langue` (indices 4 inclus à 6 exclu), `annee` (quatre derniers caractères). Afficher ces cinq valeurs dans une liste. Attendu `["B", "6", "BIB", "FR", "2026"]`. Utiliser indices/tranches, sans recopier les fragments.

**Q6 — Interpréter un découpage.** Donnée `phrase = "Lire, c’est partager des récits !"`. Créer `fragments` par découpage aux espaces, `nb_fragments`, `troisieme_fragment`, `dernier_fragment`. Afficher `[fragments, nb_fragments, troisieme_fragment, dernier_fragment]`. Attendu `[["Lire,", "c’est", "partager", "des", "récits", "!"], 6, "partager", "!"]`. Commentaire `# Explication Q6 :` : les six fragments ne prouvent pas l'existence de six mots linguistiques ; discuter virgule, apostrophe et point d'exclamation sur ces données (2–3 phrases).

**Q7 — Reconstruire une annonce.** Donnée indépendante `rubriques = ["lecture", "traduction", "échange"]`. Construire `ligne` séparée par `" | "`, puis `rubriques_retrouvees` par le séparateur exact et `aller_retour` par comparaison de listes. Afficher `[ligne, rubriques_retrouvees, aller_retour]` : `["lecture | traduction | échange", ["lecture", "traduction", "échange"], True]`. Aucun découpage codé manuellement élément par élément.

### Partie C — Organiser des ressources (Q8–Q10, environ 30 minutes)

**Q8 — Manipuler une liste et un tuple.** Donnée `programme = ["accueil", "lecture", "pause"]`. Retirer le dernier élément puis ajouter `"échange"`. Créer `langues_reference`, tuple français/italien/espagnol dans cet ordre. Afficher `[programme, langues_reference, type(langues_reference) == tuple]` : `[["accueil", "lecture", "échange"], ("français", "italien", "espagnol"), True]`. Les méthodes de manipulation doivent être visibles, pas seulement une nouvelle liste finale. Commentaire facultatif sur le choix d'une référence stable.

**Q9 — Construire un lexique.** Créer `lexique` avec `book → livre`, `story → récit`, `reader → lecteur`, dans cet ordre. Ajouter ensuite `library → bibliothèque`. Avec `items()` et une boucle, produire `entrees_lexique`, liste de chaînes `anglais -> français` dans l'ordre d'insertion. Afficher `[lexique, lexique["story"], entrees_lexique]`. Attendu `[{"book":"livre", "story":"récit", "reader":"lecteur", "library":"bibliothèque"}, "récit", ["book -> livre", "story -> récit", "reader -> lecteur", "library -> bibliothèque"]]`.

**Q10 — Comparer les thèmes de deux ateliers.** Données `themes_a = ["récit", "langue", "récit", "mémoire", "lecture"]`, `themes_b = ["lecture", "image", "langue", "image"]`. Construire deux ensembles, `themes_communs`, `themes_seulement_a`. Afficher `[len(themes_a), len(vocabulaire_a), themes_communs, themes_seulement_a]`. Attendu `[5, 4, {"langue", "lecture"}, {"récit", "mémoire"}]`. Ordre des ensembles sans importance. Ne pas imposer tri ou conversion non nécessaires.

### Partie D — Automatiser et contrôler (Q11–Q14, environ 50 minutes)

**Q11 — Filtrer puis mesurer.** Donnée `etiquettes = [" LIVRE ", "Art", " LANGUE", "récit", " IMAGE "]`. Par boucle `for`, construire `etiquettes_normalisees`, puis `etiquettes_retenues` contenant celles d'au moins 5 caractères. Par compréhension de liste produire `longueurs_retenues`. Afficher `[etiquettes_normalisees, etiquettes_retenues, longueurs_retenues]`. Attendu `[["livre", "art", "langue", "récit", "image"], ["livre", "langue", "récit", "image"], [5,6,5,5]]`.

**Q12 — Produire deux séries bornées.** Produire avec `range` et une boucle `for` les numéros pairs de 2 à 12 inclus dans `numeros_pairs`. Une diffusion d'annonce touche 3 personnes au premier tour et le double à chacun des tours suivants. Avec `while`, construire `diffusion` des six premiers effectifs et `total_contacts` de leur somme, sans utiliser la fonction `sum`. Afficher `[numeros_pairs, diffusion, total_contacts]` : `[[2,4,6,8,10,12], [3,6,12,24,48,96], 189]`. Commentaire `# Explication Q12 :` : variable qui fait avancer la boucle, condition d'arrêt et sixième effectif avant l'itération suivante (2–3 phrases).

**Q13 — Compter des demandes.** Donnée `demandes = ["lecture", "traduction", "lecture", "échange", "traduction", "lecture"]`. Par parcours construire `frequences`, puis `demandes_repetees`, liste des thèmes demandés au moins deux fois, dans l'ordre de première apparition. À partir du dictionnaire, calculer `total_verifie` par accumulation. Afficher `[frequences, demandes_repetees, total_verifie, total_verifie == len(demandes)]`. Attendu `[{"lecture":3, "traduction":2, "échange":1}, ["lecture", "traduction"], 6, True]`. Utiliser `items()` pour la synthèse ; `.get` ou branche conditionnelle acceptés.

**Q14 — Suivre une recherche bornée.** Données `cible = 42`, `propositions = [15, 60, 42, 99]`, `limite = 5`. Par `while`, traiter les propositions dans l'ordre jusqu'à réussite, épuisement de la liste ou limite atteinte. Construire `diagnostics` (`"trop petit"`, `"trop grand"`, `"trouvé"`), `tentatives_utilisees`, `trouve`, `tentatives_restantes` (limite moins nombre effectivement traité). Afficher `[diagnostics, tentatives_utilisees, trouve, tentatives_restantes]` : `[["trop petit", "trop grand", "trouvé"], 3, True, 2]`. Le 99 n'est pas traité. En affichages supplémentaires distincts du marqueur Q14, vérifier la même logique avec `[15,60]` (épuisement), `[15,60,20,30]` et limite 2 (limite), ainsi qu'une liste vide. Ne pas réécrire les sorties attendues. Une fonction auxiliaire est autorisée mais pas obligatoire. Commentaire `# Explication Q14 :` : expliquer pourquoi ces trois motifs d'arrêt sont distincts. Le correcteur principal ne dépend que du cas canonique ; les essais complémentaires sont présentés à l'enseignant.

### Partie E — Construire un outil réutilisable (Q15–Q18, environ 55 minutes)

**Q15 — Normaliser par une fonction.** Définir `normaliser_notice(texte)` : bords retirés, minuscules, espaces internes et ponctuation conservés ; retourner la chaîne, ne pas se limiter à l'afficher. Afficher `[normaliser_notice("  LIVRE  "), normaliser_notice(""), normaliser_notice("  Deux  MOTS !  ")]`. Attendu `["livre", "", "deux  mots !"]`. Aucun recours à une variable globale.

**Q16 — Compter une collection quelconque.** Définir `compter_elements(elements)` qui retourne un dictionnaire des occurrences en parcourant la liste. Elle n'applique aucune normalisation implicite et ne modifie pas l'entrée. Afficher `[compter_elements(["livre","récit","livre"]), compter_elements([]), compter_elements(["Livre","livre"])]`. Attendu `[{"livre":2, "récit":1}, {}, {"Livre":1, "livre":1}]`. Paramètre, accumulation, retour effectif exigés ; le dictionnaire des résultats ne doit pas être codé en dur.

**Q17 — Traduire avec une ressource fournie.** Définir `traduire_etiquette(mot, lexique)` : appeler `normaliser_notice`, retourner la traduction si la forme normalisée est une clé ; sinon retourner la forme normalisée. Définir `traduire_annonce(texte, lexique)` : découper, appeler `traduire_etiquette` pour chaque fragment et reconstruire avec un espace. Données `lexique_test = {"book":"livre", "story":"récit"}`. Afficher `[traduire_etiquette(" BOOK ", lexique_test), traduire_etiquette(" MAP ", lexique_test), traduire_annonce("BOOK story MAP", lexique_test), traduire_annonce("", lexique_test), traduire_etiquette("BOOK", {"book":"ouvrage"})]`. Attendu `["livre", "map", "livre récit map", "", "ouvrage"]`. Le dernier cas vérifie le recours au paramètre dictionnaire. Commentaire `# Explication Q17 :` : pourquoi cela ne constitue pas une traduction linguistique de phrases au sens général, à partir de deux limites concrètes (2–3 phrases).

**Q18 — Composer une synthèse.** Définir `bilan_notice(texte)` qui appelle `normaliser_notice` et `compter_elements`. Retourner un dictionnaire avec exactement `texte_normalise`, `nb_caracteres`, `nb_fragments`, `nb_formes`, `frequences`. Décompte de caractères après normalisation ; fragments obtenus par `split()` ; formes distinctes sensibles aux accents et à la ponctuation, après minuscules. Afficher `[bilan_notice("  LIVRE récit livre  "), bilan_notice(""), bilan_notice("Livre livre, LIVRE")]`. Attendu `[{"texte_normalise":"livre récit livre", "nb_caracteres":17, "nb_fragments":3, "nb_formes":2, "frequences":{"livre":2,"récit":1}}, {"texte_normalise":"", "nb_caracteres":0, "nb_fragments":0, "nb_formes":0, "frequences":{}}, {"texte_normalise":"livre livre, livre", "nb_caracteres":18, "nb_fragments":3, "nb_formes":2, "frequences":{"livre":2,"livre,":1}}]`. Les deux longueurs ont été vérifiées indépendamment (17 et 18) ; l'unité est le caractère Python, espaces inclus. Pas de division donc aucun comportement spécial à inventer sur la chaîne vide.

## Couverture source et progression cible

| Compétence pratiquée dans le devoir de référence | Nouvelle activité | Relation aux TD |
|---|---|---|
| Affectations, expressions et priorités | Q1–Q3, Q12 | TD1, TD4 |
| Conversion et concaténation de valeurs | Q1, Q3, Q7 | TD1–TD2 |
| Lecture et interprétation de code | Q2, interprétations Q6/Q12/Q14 | TD1–TD4 |
| Répétition bornée, séries et croissance | Q12 | TD4 |
| Comptage des tentatives et arrêt | Q14 | TD4–TD5 |
| Conditions, seuils et cas distincts | Q3, Q11, Q13, Q14, Q17 | TD1, TD4, TD5 |
| Distinction répétitions/éléments uniques | Q10, Q13, Q16, Q18 | TD3–TD5 |
| Fonctions de transformation de chaînes | Q15, Q17, Q18 | TD2, TD5 |
| Jeu final de devinette | Q14, transformé en simulation reproductible | TD4–TD5 |

La nouvelle création élargit aux collections, aux limites des unités textuelles et à la composition, réellement travaillées dans les TD1–5. Elle ne prétend pas reproduire les six opérations arithmétiques de la référence : puissance et modulo n'y sont pas démontrés dans ces cinq TD. Le renversement de chaîne informel n'est pas reconduit comme exigence ; ses compétences sous-jacentes (parcours, indices, construction de chaîne, fonctions) sont réinvesties.

| TD | Couverture vérifiable |
|---|---|
| TD1 | Q1–Q3 : variables/types/conversion/calculs/logique/f-string ; Q5–Q6 : longueur |
| TD2 | Q4–Q7 : transformation, source, indices/tranches, split/join, ponctuation ; Q15/Q17/Q18 : réemploi |
| TD3 | Q8 : liste/tuple ; Q9 : dictionnaire/items ; Q10 : ensembles ; Q13/Q16 : occurrences |
| TD4 | Q11 : for/filtre/compréhension ; Q12 : range/while ; Q13 : comptage ; Q14 : arrêt multiple |
| TD5 | Q15–Q18 : paramètres/return/cas limites/composition/lexique/synthèse ; absence de dépendances globales |

## Évaluation et limites du correcteur

Q1–Q14 : 1 point chacune ; Q15–Q18 : 1,5 point chacune, total 20. Points partiels par objectif vérifié. La vérification technique concerne les structures, les traces enregistrées et les sorties canoniques. Le serveur n'exécute jamais la copie ; il ne peut donc pas démontrer la validité générale d'une fonction ni l'authenticité d'une sortie. Les cas limites supplémentaires réduisent les omissions, sans constituer une preuve complète.

Le résultat /20 est **provisoire et technique**. Les cinq explications Q2/Q6/Q12/Q14/Q17 sont regroupées dans le rapport privé pour lecture ciblée ; leur présence seule ne vaut pas validation de leur pertinence. L'enseignant confirme ou ajuste les points des questions concernées après lecture, sans ajout automatique de points au-delà de 20. Les essais supplémentaires Q14 sont également remontés comme éléments à examiner. Aucun score ou indice de correction n'est renvoyé à l'étudiant en mode contrôle.

## Critères d'acceptation et risques

- 18 questions substantielles ; 5 parties ; aucune réponse ou amorce d'algorithme dans les cellules étudiantes.
- Respect du périmètre TD1–TD5 ; toutes les données nécessaires sont locales, synthétiques et fournies.
- Notebooks historiques et pièce d'inspiration inchangés.
- Tuteur de contrôle dans métadonnées et première cellule Markdown, contrat TAL technique et intégration au registre.
- Solution modèle indépendante non exécutée, respectant exclusivement les acquis ; vérification statique et fixtures de correction séparées couvrant sorties canoniques, frontières de boucle et chaîne vide ; exécution finale par l'enseignant.
- Source vierge sans sorties de solution ; cellule de dépôt injectée uniquement dans les copies distribuables.
- Revues pédagogique, code, gouvernance, intégration conformément au workflow.
- Risques : charge variable à domicile, transmission de solutions entre étudiants, faux positifs d'une analyse AST et faux sentiment de preuve lié aux sorties sauvegardées. Ne pas présenter les règles textuelles du tuteur comme un dispositif de verrouillage.
