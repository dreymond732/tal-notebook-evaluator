# Lecture étudiante et copie de référence — Contrôle S1 v2

Identité fictive : **Camille Modele**, classe **M1-TILT-2027**. Aucun numéro étudiant ajouté. Mandat : validation enseignante hors épreuve, sans aide à un étudiant en contrôle. Les consignes cachées du tuteur restent celles du contrôle dans les deux emplacements d’origine ; aucune assistance tutorielle n’est activée.

Source : `Notebooks contrôles finaux/DevoirS1.ipynb`, métadonnée TAL version 2 ; empreinte SHA-256 du sujet synchronisé après retouches cosmétiques : `033339bc1e14ced85638919998df45aed92c6c74e14426d66e90902f7aa9d13d`. Branche de mission communiquée : `pedagogy/controle-s1-td1-5`.

**État : non exécuté.** Les valeurs ci-dessous sont des prévisions de lecture et de calcul manuel, jamais des sorties observées. Toutes les cellules de code de la copie ont `outputs: []` et `execution_count: null`. Aucun dépôt serveur, aucune exécution de cellule, aucune consultation de correcteur, test, corrigé existant ou historique n’a été effectuée. Une analyse syntaxique statique des cellules résolues ne vaut pas exécution ni validation des résultats.

## Ressources et limites de lecture

Le sujet a été lu dans ses 70 cellules (indices 0 à 69). La lecture préalable de chaque question est consignée ci-dessous avant l’application de sa réponse. Les références aux cellules sont des indices commençant à zéro, dans les ressources autorisées :

| Abréviation | Ressource autorisée | Cellules pédagogiques mobilisées et relues |
|---|---|---|
| TD1 | `Notebooks TD/S1/S1_TD1_variables_types.ipynb` | 1–36, notamment 6–10, 16–20, 26–32 |
| TD2 | `Notebooks TD/S1/S1_TD2_chaines_sequences.ipynb` | 1–31, notamment 5–28 |
| TD3-A | `Notebooks TD/S1/S1_TD3_A_listes.ipynb` | 1–34, notamment 3–17, 18–34 |
| TD3-B | `Notebooks TD/S1/S1_TD3_B_tuples.ipynb` | 1–34, notamment 3–18 et 23–32 |
| TD3-C | `Notebooks TD/S1/S1_TD3_C_dictionnaires_ensembles.ipynb` | 1–34, notamment 3–17 |
| TD4-A | `Notebooks TD/S1/S1_TD4_A_conditions_filtres.ipynb` | 1–40, notamment 4–15 et 28–32 |
| TD4-B | `Notebooks TD/S1/S1_TD4_B_bornes_repetitions.ipynb` | 4–12, 16–40 ; bornes, arrêt et compteur de tours |
| TD4-C | `Notebooks TD/S1/S1_TD4_C_comptages_comprehensions.ipynb` | 1–40, notamment 10–29 |
| TD5-A | `Notebooks TD/S1/S1_TD5_A_fonctions.ipynb` | 1–42, notamment 4–9 et 16–39 |
| TD5-B | `Notebooks TD/S1/S1_TD5_B_parametres_portee.ipynb` | 1–42, notamment 4–33 |
| TD5-C | `Notebooks TD/S1/S1_TD5_C_composition_texte.ipynb` | 1–44, notamment 4–29 et 36–41 |
| DM | `Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb` | 1–44, notamment Q3, Q8, Q12, Q15 et Q17 |

Les méthodes sont construites à partir de ces cours, exemples et exercices ; aucune copie des TD n’a été produite dans ce mandat limité aux deux livrables. Les annexes de licence et cellules de dépôt ne servent pas de preuve d’apprentissage. Les sorties enregistrées des ressources n’ont pas servi à construire les réponses. Aucun passage du sujet ne reste incompris au point de bloquer une réponse, sous les réserves explicites de Q28. Aucune notion supplémentaire n’est indispensable à la copie : les écritures non introduites sont signalées et, lorsqu’elles font partie de l’ossature imposée, distinguées des réponses construites.

Les consignes générales, le barème et les sections sont adressés à l’étudiant. Je n’ai pas repéré de note de conception explicitement adressée à un auteur dans le sujet visible. Les commentaires correctifs de Q6 donnent cependant une part importante du diagnostic ; ils sont une aide déjà fournie, non une découverte de cette copie.

## Points à transmettre aux revues indépendantes

- Q28 : préciser la forme testée dans le lexique ; le parcours antérieur normalise avant la recherche, le contrôle reste compatible avec une recherche littérale.
- Q26 : `isupper()` est présent mais non expliqué dans les ressources pédagogiques lues. Une solution par comparaison à la version minuscule reste possible avec les acquis.
- Q7, Q10, Q13 et Q17 : écritures `+=` et `**` présentes dans le sujet sans introduction retrouvée ; `!=`, `values()`, `elif` apparaissent aussi dans du code fourni. Elles n’obligent pas à adopter de nouvelle méthode pour résoudre les questions.
- Q1, Q17, Q21 : harmoniser la formulation locale avec le format imposé d’affichage et les exceptions de réponse numérique. Le commentaire de Q23 a depuis été corrigé ; voir la note de postlecture.
- Q27 : la compréhension de dictionnaire n’est pas introduite dans les appuis visibles ; la boucle explicitement autorisée permet de répondre.
- Q24 figure dans la partie fonctions/modularité, tout en évaluant une boucle autonome. Ce classement n’empêche pas sa résolution.

## Q1 — Lecture préalable

- **Compréhension :** Convertir la quantité textuelle avant de multiplier, sans changer les données.
- **Données :** nb_mots = "3000" ; taux_unitaire = 0.05.
- **Production attendue :** cout_total numérique, transmis à valeur_Q1 et à l’affichage fourni.
- **Origine des notions :** TD1 cellules 6–10 (calcul), 26–30 (int et conversion).
- **Ambiguïtés ou manque repéré avant résolution :** Le texte annonce « Coût total : 150.0 € », mais la ligne imposée ajoute « Résultat Q1 : ». Je conserve cette ligne, conformément aux instructions générales.

**Réponse construite par raisonnement, sans exécution :** cout_total = int(nb_mots) * taux_unitaire ; valeur prévue 150.0. Le résultat numérique est déjà fourni par l’énoncé ; le traitement est construit.

## Q2 — Lecture préalable

- **Compréhension :** Choisir les deux bornes d’une tranche, sans changer la source ni l’extraction.
- **Données :** La chaîne corpus_brut et le fragment cible extraction.
- **Production attendue :** Deux entiers et mot_extrait égal à la cible.
- **Origine des notions :** TD2 cellules 13–16 (indices et fin exclue).
- **Ambiguïtés ou manque repéré avant résolution :** Plusieurs couples de bornes, notamment négatives, peuvent convenir. L’énoncé n’impose pas de bornes positives.

**Réponse construite par raisonnement, sans exécution :** Je numérote à partir de zéro : e commence à 19, n est à 28 ; bornes construites 19 et 29. Le fragment cible est fourni.

## Q3 — Lecture préalable

- **Compréhension :** Réparer uniquement la syntaxe de la condition.
- **Données :** note = 12 ; seuil = 10.
- **Production attendue :** Une condition valide donnant valeur_Q3 = True.
- **Origine des notions :** TD1 cellules 16–20 (>=) ; TD4-A cellule 10 (if, deux-points et indentation).
- **Ambiguïtés ou manque repéré avant résolution :** Aucune ambiguïté bloquante. Le titre de la partie « variables, types et chaînes » comprend ici une condition apprise plus tard.

**Réponse construite par raisonnement, sans exécution :** Ajout de : à la ligne du if. True est une valeur cible déjà fournie.

## Q4 — Lecture préalable

- **Compréhension :** Retirer espaces de bord et point sans mettre le mot en minuscules.
- **Données :** mot_sale = "  Terminologie. ".
- **Production attendue :** valeur_Q4 chaîne conservant la majuscule initiale.
- **Origine des notions :** TD2 cellules 5–12 (strip, replace) ; TD5-A cellule 28 (composition des méthodes).
- **Ambiguïtés ou manque repéré avant résolution :** strip avec argument serait une variante non introduite dans les appuis ; elle n’est pas nécessaire. La source n’a qu’un point final.

**Réponse construite par raisonnement, sans exécution :** mot_sale.strip().replace(".", "") ; Terminologie est la cible fournie.

## Q5 — Lecture préalable

- **Compréhension :** Combiner appartenance aux langues et disponibilité strictement positive.
- **Données :** italien ; tuple français/italien ; places = 0.
- **Production attendue :** inscription_possible booléen calculé sur les données intactes.
- **Origine des notions :** TD1 cellules 16–20 (and, >) ; TD3-B cellules 3–4 (tuple) ; DM Q3 cellules 8–9 (même situation).
- **Ambiguïtés ou manque repéré avant résolution :** Aucune ambiguïté repérée.

**Réponse construite par raisonnement, sans exécution :** (langue in langues_proposees) and (places > 0) ; False prévu car aucune place.

## Q6 — Lecture préalable

- **Compréhension :** Retirer morphosyntaxe et ajouter segmentation par modification de liste.
- **Données :** Liste de trois outils, morphosyntaxe en dernière position.
- **Production attendue :** La liste modifiée et valeur_Q6 associée.
- **Origine des notions :** TD3-A cellules 8–12 (pop sans argument et append) ; DM Q8 cellules 20–21.
- **Ambiguïtés ou manque repéré avant résolution :** Les commentaires donnent déjà la distinction remove/pop et l’absence de add. remove et pop avec indice ne sont pas nécessaires : pop() a été enseigné.

**Réponse construite par raisonnement, sans exécution :** outils_tal.pop() puis outils_tal.append("segmentation"). La liste finale est fournie dans l’énoncé.

## Q7 — Lecture préalable

- **Compréhension :** Compter les mots dont la longueur dépasse strictement six.
- **Données :** alignement, corpus, traduction, python, lexique ; compteur fourni.
- **Production attendue :** Condition correcte dans la boucle et compte final.
- **Origine des notions :** TD4-A cellules 10–15 (longueur et borne stricte) ; TD4-C cellules 4–8 (compteur).
- **Ambiguïtés ou manque repéré avant résolution :** Le code fourni utilise += et !=, écritures non retrouvées dans les cours visibles autorisés. Seul le if doit être corrigé ; += reste fourni.

**Réponse construite par raisonnement, sans exécution :** Condition len(mot) > 6 ; compte prévu 3 (alignement, traduction, lexique).

## Q8 — Lecture préalable

- **Compréhension :** Transformer chaque variable mot en majuscules au moment de son ajout.
- **Données :** Liste machine, learning, nlp ; liste résultat vide.
- **Production attendue :** Liste de chaînes en majuscules, même ordre.
- **Origine des notions :** TD3-A cellules 13–17 (parcours et append) ; TD4-A cellules 4–9 (.upper).
- **Ambiguïtés ou manque repéré avant résolution :** Le commentaire annonce des lignes à corriger alors qu’une seule suffit.

**Réponse construite par raisonnement, sans exécution :** resultat.append(mot.upper()). La liste finale est donnée par le sujet.

## Q9 — Lecture préalable

- **Compréhension :** Parcourir les indices de la liste du dernier au premier.
- **Données :** notes = [9, 12, 15].
- **Production attendue :** Paramètres de range produisant les trois positions inversées.
- **Origine des notions :** TD3-A cellules 3–7 (indices) ; TD4-B cellules 4–12 (range et pas négatif).
- **Ambiguïtés ou manque repéré avant résolution :** L’énoncé dit afficher les éléments ; le code accumule la liste puis l’affiche, ce qui précise le format.

**Réponse construite par raisonnement, sans exécution :** range(len(notes) - 1, -1, -1) donne les indices 2, 1, 0 ; liste cible [15, 12, 9] fournie.

## Q10 — Lecture préalable

- **Compréhension :** Faire commencer le compte à cinq puis le diminuer en gardant compteur > 0.
- **Données :** Initialisation incorrecte à zéro, boucle et liste fournies.
- **Production attendue :** Liste de cinq entiers décroissants, puis arrêt.
- **Origine des notions :** TD4-B cellules 16–21 (état initial, mise à jour, arrêt).
- **Ambiguïtés ou manque repéré avant résolution :** À la première lecture, faute dans « CORRECTION REQUISES (LIGNES SUIVANTESS) », corrigée depuis en « CORRECTIONS REQUISES (LIGNES SUIVANTES) ». L’incrémentation += fournie n’a pas d’appui visible ; une affectation ordinaire suffit.

**Réponse construite par raisonnement, sans exécution :** Initialisation à 5 puis compteur = compteur - 1 ; cible [5, 4, 3, 2, 1] fournie ; première valeur exclue 0.

## Q11 — Lecture préalable

- **Compréhension :** Lire une clé absente en donnant une valeur de repli.
- **Données :** terminologie contient source et domaine, sans cible.
- **Production attendue :** valeur_Q11 chaîne inconnu, sans accès direct à une clé absente.
- **Origine des notions :** TD3-C cellule 8 (clés) ; TD4-C cellules 22–23 (.get) ; TD5-B cellules 28–29 (repli textuel).
- **Ambiguïtés ou manque repéré avant résolution :** Le nom d’exception KeyError n’est pas défini dans les appuis cités ; l’erreur sur clé absente est expliquée. Aucune gestion try/except nécessaire.

**Réponse construite par raisonnement, sans exécution :** terminologie.get("cible", "inconnu"). Le repli est fourni par le sujet.

## Q12 — Lecture préalable

- **Compréhension :** Déballer les paires du dictionnaire plutôt que ses seules clés.
- **Données :** frequences = {le: 2, chat: 1} et dictionnaire à reconstruire.
- **Production attendue :** Boucle utilisant les paires, puis dictionnaire à afficher.
- **Origine des notions :** TD3-C cellules 3–7 (items et déballage).
- **Ambiguïtés ou manque repéré avant résolution :** « Afficher le dictionnaire correctement » est assez général, mais la cellule précise qu’il faut reconstruire un dictionnaire, pas afficher chaque paire séparément.

**Réponse construite par raisonnement, sans exécution :** for cle, valeur in frequences.items(): ; dictionnaire prévu identique à la donnée.

## Q13 — Lecture préalable

- **Compréhension :** Créer le compteur d’une nouvelle clé à un, augmenter les occurrences suivantes.
- **Données :** Liste talk, is, cheap, talk.
- **Production attendue :** Dictionnaire freq de nombres d’occurrences.
- **Origine des notions :** TD3-C cellule 8 (in sur clés) ; TD4-C cellules 16–20 (fréquences avec if/else).
- **Ambiguïtés ou manque repéré avant résolution :** values() et += apparaissent dans le code fourni sans introduction retrouvée dans les appuis ; values est retiré par la correction, += demeure fourni.

**Réponse construite par raisonnement, sans exécution :** if mot in freq et initialisation à 1 ; cible fournie {talk: 2, is: 1, cheap: 1}.

## Q14 — Lecture préalable

- **Compréhension :** Choisir des valeurs qui rendent vraie la première condition.
- **Données :** Branches avec a > 5 ou b == 10 ; deuxième branche indépendante de la réponse ciblée.
- **Production attendue :** Modification de la seule première ligne, résultat chaîne Vrai.
- **Origine des notions :** TD1 cellules 16–20 (comparaisons) ; TD4-B cellule 34 (or) ; TD3-B cellule 18 (affectation multiple par déballage).
- **Ambiguïtés ou manque repéré avant résolution :** Une infinité de triplets convient. Aucun triplet unique ne doit être déduit de la consigne. elif est fourni, sans être nécessaire pour atteindre la première branche.

**Réponse construite par raisonnement, sans exécution :** Choix a, b, c = 6, 0, 0 ; première comparaison vraie, Vrai cible fournie.

## Q15 — Lecture préalable

- **Compréhension :** Filtrer les paires sur la longueur strictement supérieure à trois de leur clé.
- **Données :** Lexique avec le, TAL, mot, code.
- **Production attendue :** Dictionnaire longs_mots conservant seulement les clés admissibles.
- **Origine des notions :** TD3-C cellules 3–7 (items et construction) ; TD4-A cellules 10–15 (strict >).
- **Ambiguïtés ou manque repéré avant résolution :** Aucune ambiguïté repérée ; la phrase sur les clés de trois caractères lève la confusion de borne.

**Réponse construite par raisonnement, sans exécution :** if len(mot) > 3 ; résultat prévu {code: nom}.

## Q16 — Lecture préalable

- **Compréhension :** Retourner la salutation pour qu’elle soit reçue par la variable de l’appelant.
- **Données :** Fonction saluer_personne et appel David.
- **Production attendue :** Une chaîne retournée dépendant du paramètre.
- **Origine des notions :** TD1 cellule 26 (concaténation) ; TD5-A cellules 4–9 (print/return) ; TD5-B Q4 cellules 25–26.
- **Ambiguïtés ou manque repéré avant résolution :** Aucune ambiguïté repérée.

**Réponse construite par raisonnement, sans exécution :** return "Bonjour, " + nom_personne ; Bonjour, David cible fournie.

## Q17 — Lecture préalable

- **Compréhension :** Faire retourner le carré plutôt que le double.
- **Données :** Paramètre nombre, appel avec 4 et print intermédiaire fourni.
- **Production attendue :** valeur_Q17 égale au carré du nombre reçu.
- **Origine des notions :** TD1 cellule 6 (multiplication) ; TD5-A cellules 4–9 et 16–18 (retour d’un calcul).
- **Ambiguïtés ou manque repéré avant résolution :** Le print intermédiaire n’est pas explicitement interdit ni demandé. Je le conserve, donc le futur affichage contiendra aussi une ligne 16. ** n’est pas introduit dans les appuis lus ; il reste dans le code fourni et n’est pas nécessaire pour écrire le retour.

**Réponse construite par raisonnement, sans exécution :** return nombre * nombre ; valeur prévue 16. Le print existant ne remplace pas ce retour.

## Q18 — Lecture préalable

- **Compréhension :** Choisir le retour selon une longueur au moins égale à six.
- **Données :** Paramètre mot ; appel corpus, six caractères.
- **Production attendue :** analyse si len >= 6, court sinon.
- **Origine des notions :** TD4-A cellules 28–32 (borne incluse) ; TD5-A cellules 22–26 (retours conditionnels).
- **Ambiguïtés ou manque repéré avant résolution :** Aucune ambiguïté repérée ; la longueur de corpus est explicitée. pass est seulement un emplacement à remplacer, non une notion nécessaire.

**Réponse construite par raisonnement, sans exécution :** if len(mot) >= 6: return "analyse", sinon return "court". Cible analyse déjà déductible explicitement du texte.

## Q19 — Lecture préalable

- **Compréhension :** Définir les deux transformations et conserver leur composition.
- **Données :** Appel enlever_ponctuation(minuscules("NLTK.")).
- **Production attendue :** Deux chaînes retournées ; résultat final nltk.
- **Origine des notions :** TD2 cellules 9–12 (lower, replace) ; TD5-C cellules 12–13 (composition).
- **Ambiguïtés ou manque repéré avant résolution :** Le nom enlever_ponctuation est plus large que la consigne, qui demande seulement d’enlever les points. Je retire uniquement les points, conformément au texte.

**Réponse construite par raisonnement, sans exécution :** return texte.lower() et return texte_sale.replace(".", "") ; nltk cible fournie.

## Q20 — Lecture préalable

- **Compréhension :** Décrire le paramètre dans les deux valeurs du dictionnaire.
- **Données :** Mot Termino et structure longueur/minuscules déjà fournie.
- **Production attendue :** Dictionnaire retourné calculé à partir du mot reçu.
- **Origine des notions :** TD1 cellule 31 (len) ; TD2 cellule 9 (lower) ; TD5-C cellules 24–28 (retour de dictionnaire).
- **Ambiguïtés ou manque repéré avant résolution :** L’énoncé fournit un exemple unique ; la règle générale impose néanmoins de calculer avec le paramètre, pas de remplacer une constante par une autre.

**Réponse construite par raisonnement, sans exécution :** longueur: len(mot), minuscules: mot.lower() ; {longueur: 7, minuscules: termino} cible fournie.

## Q21 — Lecture préalable

- **Compréhension :** Déduire le résultat quand le second argument utilise son défaut.
- **Données :** f(x, y=10), appel f(5), quatre choix.
- **Production attendue :** Numéro du choix dans reponse_Q21.
- **Origine des notions :** TD5-B cellules 16–21 (paramètres par défaut).
- **Ambiguïtés ou manque repéré avant résolution :** La règle générale interdit de recopier une valeur finale, mais cette question demande explicitement le numéro d’un choix : je suis la consigne locale.

**Réponse construite par raisonnement, sans exécution :** 5 + 10 = 15 ; choix construit 3.

## Q22 — Lecture préalable

- **Compréhension :** Rendre le deuxième argument facultatif avec le défaut approprié.
- **Données :** addition(a, b), appel addition(5), résultat ciblé 15.
- **Production attendue :** Signature modifiée, addition utilisant les deux paramètres.
- **Origine des notions :** TD5-B cellules 16–21 (défaut numérique).
- **Ambiguïtés ou manque repéré avant résolution :** « Appel sans le paramètre b » devrait préciser « sans argument pour b » ; le paramètre reste dans la définition.

**Réponse construite par raisonnement, sans exécution :** def addition(a, b=10): return a + b. Le résultat cible 15 est fourni.

## Q23 — Lecture préalable

- **Compréhension :** Suivre la valeur transmise de y vers x puis le retour.
- **Données :** Code en Markdown : y = 5 ; calculer(x) retourne x * 2.
- **Production attendue :** Valeur numérique dans reponse_Q23.
- **Origine des notions :** TD5-A cellules 4–9 (appel et retour) ; TD5-B cellules 4–6 (paramètre et argument).
- **Ambiguïtés ou manque repéré avant résolution :** À la première lecture, le commentaire parlait de « valeur de resultat qui serait retournée » : calculer retourne 10, puis resultat stocke cette valeur. Ce commentaire a été corrigé en « valeur numérique stockée dans resultat » ; cette ambiguïté est levée dans le sujet synchronisé. La réponse numérique reste une exception locale explicite à l’interdiction générale de recopier une valeur finale.

**Réponse construite par raisonnement, sans exécution :** 5 * 2 = 10 ; reponse_Q23 = 10.

## Q24 — Lecture préalable

- **Compréhension :** Produire quatre termes, en séparant le rang du terme courant.
- **Données :** Premier effectif 4 ; doublement à chaque tour ; liste vide fournie.
- **Production attendue :** Boucle while finie construisant effectifs, sans break ni liste littérale finale.
- **Origine des notions :** TD4-B cellules 22–26 (compteur distinct du terme) ; DM Q12 cellules 29–30 (diffusion doublée).
- **Ambiguïtés ou manque repéré avant résolution :** La première valeur appartient au premier tour : le texte le précise. Aucune ambiguïté bloquante.

**Réponse construite par raisonnement, sans exécution :** Initialiser effectif = 4 et tour = 0 ; ajouter, doubler, augmenter le tour tant que tour < 4. Liste prévue [4, 8, 16, 32].

## Q25 — Lecture préalable

- **Compréhension :** Retourner le paramètre sans espaces de bord et en minuscules, en gardant tout le reste.
- **Données :** Trois appels fournis : texte avec apostrophe/virgule, vide, texte avec deux espaces intérieurs.
- **Production attendue :** Fonction autonome et liste des trois retours dans l’ordre fourni.
- **Origine des notions :** TD2 cellules 5–12 ; TD5-A cellules 28–33 (normalisation conservant espaces intérieurs) ; DM Q15 cellules 36–37.
- **Ambiguïtés ou manque repéré avant résolution :** Aucune ambiguïté repérée ; ponctuation et espaces intérieurs sont explicitement conservés.

**Réponse construite par raisonnement, sans exécution :** return texte.strip().lower() ; valeurs prévues ["l'analyse,", "", "deux  mots !"]. Les deux espaces internes sont conservés.

## Q26 — Lecture préalable

- **Compréhension :** Répartir selon la présence d’au moins une majuscule, pas selon un mot entièrement en majuscules.
- **Données :** Python, code, TAL, texte, Nlp ; deux listes vides.
- **Production attendue :** Dictionnaire avec catégories et ordre conservés.
- **Origine des notions :** TD2 cellule 9 (lower) ; TD1 cellules 16–17 (== et booléens) ; TD4-A cellules 28–32 (partition).
- **Ambiguïtés ou manque repéré avant résolution :** isupper est fourni sans introduction retrouvée dans les cours visibles. any et islower ne sont pas introduits non plus. La comparaison d’un mot à sa version minuscule se construit avec les acquis, mais l’inférence est plus autonome que les exemples antérieurs. Pour ces données, ne pas se limiter au premier caractère.

**Réponse construite par raisonnement, sans exécution :** Condition (mot == mot.lower()) == False : elle utilise seulement lower, égalité et booléen, notions déjà vues. Le dictionnaire cible est fourni par l’énoncé.

## Q27 — Lecture préalable

- **Compréhension :** Associer chaque mot à sa longueur par un traitement.
- **Données :** phrase, texte, mot.
- **Production attendue :** Dictionnaire valeur_Q27 calculé par boucle ou compréhension.
- **Origine des notions :** TD3-C cellules 3–7 (ajouter une association) ; TD3-A cellules 13–17 (mot et longueur).
- **Ambiguïtés ou manque repéré avant résolution :** La compréhension de dictionnaire est proposée mais n’est pas introduite dans les cours visibles ; les compréhensions de liste le sont. La boucle autorisée suffit.

**Réponse construite par raisonnement, sans exécution :** Boucle for mot in mots, puis valeur_Q27[mot] = len(mot). Le dictionnaire final est déjà fourni en commentaire.

## Q28 — Lecture préalable

- **Compréhension :** Consulter le lexique reçu et retourner un repli en minuscules si la clé manque.
- **Données :** Lexique book/livre, dog/chien ; appels dog et CAT.
- **Production attendue :** Fonction avec if/else et return ; liste de deux résultats.
- **Origine des notions :** TD3-C cellule 8 (test de clé) ; TD5-B cellules 28–33 (traduction et paramètre dictionnaire) ; DM Q17 cellules 40–41.
- **Ambiguïtés ou manque repéré avant résolution :** Le contrôle ne dit pas de normaliser avant la recherche, contrairement au TD5-B Q5 et au DM Q17. DOG pourrait donc donner dog ou chien selon la lecture. Je retiens la lecture littérale : recherche sur mot tel que reçu, minuscules seulement pour un inconnu ; pas de strip implicite. Les appels fournis ne distinguent pas les deux règles.

**Réponse construite par raisonnement, sans exécution :** if mot in lexique: return lexique[mot], else return mot.lower(). Cible fournie [chien, cat].

## Q29 — Lecture préalable

- **Compréhension :** Conserver le nettoyage fourni et compter les caractères de la phrase originale reçue.
- **Données :** Phrase Le TAL est cool. ; fonction de nettoyage ; split et compréhension déjà fournis.
- **Production attendue :** Dictionnaire avec liste nettoyée et nombre de caractères original.
- **Origine des notions :** TD1 cellule 31 (caractères, espaces et ponctuation) ; TD2 cellule 17 (split) ; TD4-C cellule 28 (compréhension) ; TD5-C cellules 24–29 (plusieurs informations).
- **Ambiguïtés ou manque repéré avant résolution :** Attention : le TD5-C et le DM mesurent le texte normalisé, ici c’est explicitement la phrase originale. Le nom mots_nettoyés décrit des fragments de split, pas une segmentation linguistique générale ; aucun changement de convention n’est demandé.

**Réponse construite par raisonnement, sans exécution :** Remplacer len(mots) par len(phrase). Compte manuel : 2 + 1 + 3 + 1 + 3 + 1 + 5 = 16 ; liste cible [le, tal, est, cool] fournie.

## Q30 — Lecture préalable

- **Compréhension :** Mémoriser le meilleur mot, sans remplacer à égalité ; prévoir la liste vide.
- **Données :** Trois appels : liste ordinaire, égalité livre/récit, liste vide.
- **Production attendue :** Fonction de recherche sans max, source inchangée, retour recalculé à chaque appel.
- **Origine des notions :** TD4-C cellules 10–15 (meilleur candidat, vide) ; TD5-A cellules 22–26 (return conditionnel) ; TD5-C cellules 6–8 et 36–41 (état local et parcours).
- **Ambiguïtés ou manque repéré avant résolution :** Le cas de plusieurs chaînes vides n’est pas isolé dans les appels ; la convention "" le couvre. Les exemples précédents cherchent un maximum numérique non vide : le transfert aux longueurs et la gestion du vide sont une synthèse.

**Réponse construite par raisonnement, sans exécution :** Si len(mots) == 0, retourner "" ; sinon candidat = mots[0], parcourir et remplacer seulement si la longueur est strictement supérieure. Retours prévus [bibliothèque, livre, ""].

## Postlecture — Synchronisation des retouches cosmétiques

Après la résolution, trois passages du sujet ont été comparés et synchronisés : commentaire de Q10 corrigé en « CORRECTIONS REQUISES (LIGNES SUIVANTES) » ; consigne Markdown de Q17 simplifiée ; commentaire de Q23 précisant « valeur numérique stockée dans resultat ». Ce dernier commentaire était déjà à jour dans la copie au moment de cette synchronisation : aucune nouvelle modification n’y a été nécessaire. L’ambiguïté de vocabulaire signalée pour Q23 est donc corrigée ; la question continue de demander une réponse numérique explicite. La réserve sur le print intermédiaire de Q17 reste pertinente.

Empreinte de la première lecture : `f2d21774e2ce340d77c4a29d807e5165403ac479064fdba85a436cafbf68421f`. Empreinte du sujet synchronisé : `033339bc1e14ced85638919998df45aed92c6c74e14426d66e90902f7aa9d13d`. Comparaison stricte : tous les Markdown correspondent maintenant au sujet courant ; les solutions sont inchangées, vérifiées par comparaison de leurs arbres syntaxiques avant et après la synchronisation. Métadonnées inchangées, sorties toujours vides, compteurs d’exécution toujours nuls. Aucune nouvelle exécution.

## Handoff et critères de vérification

Fichiers produits : `Controle_S1_v2_corrige_non_execute.ipynb` et `lecture_etudiante.md`, exclusivement dans le dossier de cette mission. Le notebook conserve les 70 cellules du sujet, les métadonnées TAL et l’intégralité des contextes du tuteur ; seules l’identité fictive et les réponses de code sont modifiées. Les affichages Q1 à Q30 sont conservés.

Hypothèses : recherche littérale de clé en Q28 ; conservation du print intermédiaire en Q17 ; choix positif de bornes en Q2 et triplet valide parmi plusieurs en Q14.

Vérification faite : lecture JSON et analyse syntaxique statique des cellules, sans exécution. Vérification restante : exécution humaine en session vierge et comparaison des sorties réelles aux prévisions ; adéquation au correcteur non vérifiée. Les valeurs attendues restent indépendantes de tout correcteur.

Le producteur ne valide pas sa propre copie. Verdict demandé : revue indépendante des solutions, puis verdicts pédagogique et éditorial distincts sur les ambiguïtés. Cette copie ne constitue ni un score, ni une validation de lisibilité, ni une autorisation de diffusion ou de fusion.
