# Revue éditoriale indépendante — S1, renforcement Swinnen

## Périmètre et méthode

Mission : TAL-Editorial-Reviewer indépendant des producteurs. Branche de mission : `pedagogy/s1-swinnen-renforcement` ; base historique/technique `c81c38641ecddb66c5ea65c78eafbd2d8d3cbbc5`. Le présent rapport est la seule zone modifiée par ce rôle. Référence normative : `AGENTS.md`, `docs/agents/TAL-Editorial-Reviewer.md`, `EDITORIAL_REVIEW_TEMPLATE.md`, matrice de permissions et workflow. Matrice préalable comparée : `docs/pedagogy/s1-swinnen-expansion.md`.

Lecture exhaustive des cellules pédagogiques, du code/commentaires fourni, des essais, des réponses vides, des bilans et de la restitution des neuf nouveaux cahiers ; contrôle séparé du contexte tuteur final. Les neuf annexes légales identiques sont repliables : leur prose documentaire n'est pas évaluée comme cours à acquérir au niveau S1. Aucune version historique antérieure plus riche que la base identifiée n'est disponible ; aucune restauration supplémentaire n'est revendiquée.

Sources comparées intégralement : `Notebooks TD/S1/TD3_S1_collections.ipynb` (39 cellules), `TD5_S1_fonctions_reutilisation.ipynb` (46), `TD6_S1_fichiers_csv.ipynb` (43). Les anciens minutages et notices d'identification n'ont pas été importés dans les nouveaux supports. Les sources historiques ne sont pas elles-mêmes revalidées par cette mission.

Les indices ci-dessous commencent à 0. Chaque ligne Q couvre le cours préalable, son exemple distinct, l'essai préalable, l'énoncé, la réponse et les vérifications postérieures, lorsqu'elles existent. L'essai est nommé dans une colonne propre afin de ne pas le confondre avec la réponse évaluée. Pour toutes les réponses, les données et print commentés sont fournis ; les variables calculées, fonctions, boucles et fichiers demandés restent à construire. Les commentaires sont écrits dans la cellule d'essai/réponse concernée ; les commentaires de bilan ont leur cellule propre.

Prérequis amont vérifiés : TD1 cours cellules 5–6 (affectation/calcul/print), 11 (types), 16 (comparaisons), 21 (f-strings), 26 (concaténation), 31 (len/présence/repr) ; TD2 cours 5 (strip), 9 (lower/replace), 13 (indices/tranches), 17 (split/listes), 21 (join), 25 (listes littérales). TD4 cours 6 (parcours), 11 (if), 21 (range/list), 31 (dictionnaire/if/else/get) et 36 (compréhension). TD3 n'exige pas TD4. Les TD5 et TD6 réutilisent les acquis antérieurs explicités et introduisent leurs nouveautés avant emploi.

## Révisions locales relues

| Fichier sous `Notebooks TD/S1/` | Identifiant | Cellules relues | SHA-256 du fichier final |
|---|---|---|---|
| `TD3-one_S1_listes.ipynb` | `TD3_ONE_S1` | 0–36, annexe légale repliable exclue de l'évaluation du niveau | `288e4f7b8140673dd2a7a0d655d51eb86acd7d23008ac97789a03bb7f6dc387c` |
| `TD3-bis_S1_tuples.ipynb` | `TD3_BIS_S1` | 0–36, annexe légale repliable exclue de l'évaluation du niveau | `460a9ccae7e3d51e3dbd635d71895971c798caa8f34717a59bab8fee0491df17` |
| `TD3-ter_S1_dictionnaires_ensembles.ipynb` | `TD3_TER_S1` | 0–36, annexe légale repliable exclue de l'évaluation du niveau | `6cd0efc98d97df16b74aeaa2b5c4e7380162d703bb135eed7019078e9894a126` |
| `TD5-one_S1_fonctions.ipynb` | `TD5_ONE_S1` | 0–44, annexe légale repliable exclue de l'évaluation du niveau | `438ac959a2f968b928713f8b38eee8af09e1f701406f44fbc39000a3b30607ba` |
| `TD5-bis_S1_parametres_portee.ipynb` | `TD5_BIS_S1` | 0–44, annexe légale repliable exclue de l'évaluation du niveau | `4797771f4e1ccc3cb9f38bc1a8d1e748904433fcbb41bc64d758020250d3eb03` |
| `TD5-ter_S1_composition_texte.ipynb` | `TD5_TER_S1` | 0–46, annexe légale repliable exclue de l'évaluation du niveau | `def84c356b76f087408f50d4d8924433b30b7e35c4cc5f7eb2043ef9be907e92` |
| `TD6-one_S1_fichiers_texte.ipynb` | `TD6_ONE_S1` | 0–43, annexe légale repliable exclue de l'évaluation du niveau | `365291b577cbdfca84122cfca9fb69b7c3d6ad96406ac28a32971427039d18ff` |
| `TD6-bis_S1_donnees_delimitees.ipynb` | `TD6_BIS_S1` | 0–44, annexe légale repliable exclue de l'évaluation du niveau | `69b5f249b785cd8e1298c36fa74d09624c6bfb1eb9dff38abd82c2c06cf32fff` |
| `TD6-ter_S1_csv.ipynb` | `TD6_TER_S1` | 0–45, annexe légale repliable exclue de l'évaluation du niveau | `385df4b0434f4d4480cc26a5483c3b04cfec9c3ed9c8d4d9a8b8859e633a5de8` |

## TD3-one_S1_listes.ipynb

| Question / cellules lues | Action et données | Production à construire / afficher | Cours antérieur et statut de la tâche | Essais et vérifications obligatoires relus |
|---|---|---|---|---|
| Q1, 3–7 ; réponse `td3-one-s1-06` | Lire les cinq mots fournis aux positions demandées. | premier, dernier, milieu ; trois valeurs avec Q1. | Cours `td3-one-s1-02` avant Q1. Guidé ; indices/tranches rappelés, sélections à construire. | Quatre villes puis répétition ; prédire première/dernière/centrales et expliquer ce que len compte. |
| Q2, 8–12 ; réponse `td3-one-s1-11` | Modifier outils par ajout puis retrait de tokeniseur. | Q2a après ajout ; Q2 après retrait avec outil_retire ; chronologie conservée. | Cours `td3-one-s1-07` avant Q2. Guidé ; données et affichages fournis, opérations à écrire. | Deux villes puis troisième ; distinguer état de liste et valeur renvoyée par pop. |
| Q3, 13–17 ; réponse `td3-one-s1-16` | Parcourir les quatre noms sans changer leur ordre. | fiches_noms en chaînes nom : longueur ; explication de la liste vide avant boucle. | Cours `td3-one-s1-12` avant Q3. Transfert guidé ; for, indentation et append enseignés dans le cours antérieur. | Trois prénoms libres ; afficher nom/longueur puis construire fiches ; interpréter initialisation. |
| Q4, 18–22 ; réponse `td3-one-s1-21` | Parcourir Janvier/Février/Mars et recomposer une chaîne. | Affichages pendant boucle, puis ligne_mois avec espaces intérieurs et aucun aux bords. | Cours `td3-one-s1-17` avant Q4. Réinvestissement ; concaténation et strip expliqués avant question. | Trois villes et liste vide ; comparer chaîne obtenue et ordre. |
| Q5, 23–27 ; réponse `td3-one-s1-26` | Entrelacer les mois et jours des deux listes fournies. | calendrier alterné ; deux éléments par mois ; sources inchangées. | Cours `td3-one-s1-22` avant Q5. Guidé ; indice incrémenté introduit avant exercice, sans range ni zip requis. | Villes/codes postaux libres ; suivre indice i et les deux ajouts. |
| Q6, 28–32 ; réponse `td3-one-s1-31` | Copier reference puis remplacer son premier mot et ajouter analyse dans revision. | Q6 montre original et copie ; justification de la distinction alias/copie. | Cours `td3-one-s1-27` avant Q6. Choix de méthode laissé ; tranche ou parcours ; portée superficielle explicitement bornée. | Trois villes par tranche puis parcours ; copie vide seulement, sans remplacement du premier élément inexistant. |

Hors questions : introduction et transitions relues ; destinataire étudiant, données du parcours et finalité expliquées. Bilan : essai repris, explication et difficulté restante ; réexécution dans l’ordre et sorties conservées. Restitution `tal-submission` relue : URL publique substituable et trois étapes de dépôt, pas de solution ni adresse privée enregistrée.

## TD3-bis_S1_tuples.ipynb

| Question / cellules lues | Action et données | Production à construire / afficher | Cours antérieur et statut de la tâche | Essais et vérifications obligatoires relus |
|---|---|---|---|---|
| Q1, 3–7 ; réponse `td3-bis-s1-06` | Créer la référence français/italien/espagnol. | langues_romanes, type et choix_tuple en affichages séparés. | Cours `td3-bis-s1-02` avant Q1. Guidé ; syntaxe tuple et non-modification expliquées, aucune confusion stabilité/exactitude. | Deux autres codes ; type et dernier élément ; argumenter un usage de liste. |
| Q2, 8–12 ; réponse `td3-bis-s1-11` | Isoler premier code comme tuple singleton ; extraire indices 1 et 2. | code_unique, codes_centraux et types. | Cours `td3-bis-s1-07` avant Q2. Guidé ; virgule et bornes introduites avant emploi. | Comparer (7)/(7,) ; trois tranches de villes et tranche vide. |
| Q3, 13–17 ; réponse `td3-bis-s1-16` | Parcourir Jean/Sonia/Maximilien sans changer le tuple. | fiches_noms + tuple source ; expliquer liste résultat versus référence tuple. | Cours `td3-bis-s1-12` avant Q3. Transfert ; for/append acquis TD3-one, rappel local. | Trois villes, puis nom répété ; vérifier conservation ordre/répétitions. |
| Q4, 18–22 ; réponse `td3-bis-s1-21` | Déballer Alice, 22 ans, 1.72 m. | prenom_fiche, age_fiche, taille_fiche ; commentaire sens des positions. | Cours `td3-bis-s1-17` avant Q4. Guidé ; déballage enseigné avant question ; données fictives annoncées. | Fiche fictive personnelle ; types puis inversion interprétative âge/taille. |
| Q5, 23–27 ; réponse `td3-bis-s1-26` | Parcourir les trois paires code/langue et déballer chacune. | fiches_langues en chaînes code -> langue, espaces imposés ; ordre intact. | Cours `td3-bis-s1-22` avant Q5. Réinvestissement ; tuple de tuples et déballage for expliqués. | Deux paires ville/pays libres ; paire entière versus premier élément. |
| Q6, 28–32 ; réponse `td3-bis-s1-31` | Recomposer reference_etendue puis reference_revisee à partir du tuple initial. | Trois tuples affichés ; expliquer pourquoi reconstruire ne modifie pas ancien tuple. | Cours `td3-bis-s1-27` avant Q6. Choix de tranches/concaténation ; try/except explicitement fourni sans reproduction demandée. | Observation TypeError contrôlée, recomposition du dernier code, comparaison liste. |

Hors questions : introduction et transitions relues ; destinataire étudiant, données du parcours et finalité expliquées. Bilan : essai repris, explication et difficulté restante ; réexécution dans l’ordre et sorties conservées. Restitution `tal-submission` relue : URL publique substituable et trois étapes de dépôt, pas de solution ni adresse privée enregistrée.

## TD3-ter_S1_dictionnaires_ensembles.ipynb

| Question / cellules lues | Action et données | Production à construire / afficher | Cours antérieur et statut de la tâche | Essais et vérifications obligatoires relus |
|---|---|---|---|---|
| Q1, 3–7 ; réponse `td3-ter-s1-06` | Construire lexique book/language/data, ajouter corpus puis parcourir les paires. | Q1a traduction, Q1b lexique, Q1 entrees_lexique ; commentaire réaffectation. | Cours `td3-ter-s1-02` avant Q1. Guidé ; cours clé/valeur/items avant emploi ; variante langue/langage explicite. | Deux animaux puis troisième ; réaffecter clé, parcourir paires, prédire tours et initialisation. |
| Q2, 8–12 ; réponse `td3-ter-s1-11` | Créer personnes avec Alice/Malo, ajouter Zoé puis consulter fiche et taille. | Dictionnaire entier, fiche_malo, taille_zoe ; positions âge/taille interprétées. | Cours `td3-ter-s1-07` avant Q2. Guidé ; dictionnaire de tuples introduit, déballage acquis TD3-bis. | Deux fiches fictives ; appartenance clé présente/absente sans accès absent. |
| Q3, 13–17 ; réponse `td3-ter-s1-16` | Inverser codes_langues par parcours ; pas de réécriture manuelle. | codes_inverses et sa longueur ; justification des valeurs distinctes. | Cours `td3-ter-s1-12` avant Q3. Réinvestissement autonome de construction ; méthode générale illustrée sur couleurs distinctes. | Pays/capitales libres puis collision volontaire ; comparer longueurs et expliquer perte. |
| Q4, 18–22 ; réponse `td3-ter-s1-21` | Construire vocabulaire à partir des six formes historiques. | Q4 total/distincts et Q4b ensemble entier ; vérifier valeurs sans ordre. | Cours `td3-ter-s1-17` avant Q4. Guidé ; conversion set introduite avant question. | Ajouter poésie puis tester casse/accent ; expliquer perte de fréquence. |
| Q5, 23–27 ; réponse `td3-ter-s1-26` | Partir de set vide et ajouter les langues de observations par parcours. | Ensemble, taille, appartenance français/allemand ; liste source conservée. | Cours `td3-ter-s1-22` avant Q5. Réinvestissement autonome de boucle et add ; set() versus {} explicités. | Trois villes dont répétition ; longueurs après ajouts et deux tests, comparer liste. |
| Q6, 28–32 ; réponse `td3-ter-s1-31` | Comparer corpus_a et corpus_b historiques. | communs, seulement_a, seulement_b ; expliquer orientation et fréquence/position perdues. | Cours `td3-ter-s1-27` avant Q6. Choix syntaxe opérateur/méthode ; opérations définies dans cours et exemple distinct. | Deux ensembles de langues ; intersection/deux différences puis répétitions dans sources. |

Hors questions : introduction et transitions relues ; destinataire étudiant, données du parcours et finalité expliquées. Bilan : essai repris, explication et difficulté restante ; réexécution dans l’ordre et sorties conservées. Restitution `tal-submission` relue : URL publique substituable et trois étapes de dépôt, pas de solution ni adresse privée enregistrée.

## TD5-one_S1_fonctions.ipynb

| Question / cellules lues | Action et données | Production à construire / afficher | Cours antérieur et statut de la tâche | Essais et vérifications obligatoires relus |
|---|---|---|---|---|
| Q1, 4–9 ; réponse `td5-e0997ae9fcab` | Définir longueur_texte sur paramètre chaîne. | Retours pour TAL/corpus ; entier réutilisable. | Cours `td5-504eaa47e846` avant Q1. Fonction à construire ; cours def/appel/local/return/None et exemple encadrer/montrer distincts. | Avant : annoncer sur deux thèmes et stockage ; après : vide, autre texte +1 et différence print/return. |
| Q2, 10–15 ; réponse `td5-b310b597c4b6` | Définir ligne_caracteres(nombre, caractere) pour entier positif/nul et caractère unique. | Appels fournis puis résultat entouré de crochets. | Cours `td5-26eacf737e5a` avant Q2. Guidé ; répétition de chaîne expliquée, résultat générique à construire. | Avant : xo multiplié et point zéro ; après : zéro/un/autre caractère et rôles des arguments. |
| Q3, 16–21 ; réponse `td5-e5fc197a89bd` | Définir volume_boite avec trois dimensions positives/nulles. | Appels fournis, retour entier ou décimal. | Cours `td5-9f470cd5efb1` avant Q3. Transfert ; exemple en deux dimensions, calcul tridimensionnel à construire. | Avant : aire_rectangle autre couples et double ; après : décimal, permutation et zéro. |
| Q4, 22–27 ; réponse `td5-c0b6f24885a8` | Définir maximum3 avec comparaisons/conditions sans max. | Deux appels ; maximum valable aux trois positions, égalités et négatifs. | Cours `td5-ddfe392db1a0` avant Q4. Autonomie de décision ; conditions TD4 et return précoce rappelés. | Avant : prédiction plus_petit et cas sur papier ; après : positions, égalités, initialisation risquée à 0. |
| Q5, 28–33 ; réponse `td5-6dbaa909e188` | Construire normaliser : strip/lower, espaces intérieurs conservés. | Appel Bonjour TAL ; chaîne retournée. | Cours `td5-477920d9bfde` avant Q5. Réinvestissement ; méthodes explicitées avant usage, aucune chaîne résultat fournie dans réponse. | Avant : MUSÉE et espaces seuls ; après : vide, blancs et trois espaces intérieurs. |
| Q6, 34–39 ; réponse `td5-2f1888b22703` | Construire annoncer_atelier en appelant normaliser de Q5. | Préfixe exact Au programme : suivi du thème normalisé ; préfixe conservé si vide. | Cours `td5-0aeb95f3d5f7` avant Q6. Composition à construire ; données/cible textuelle bornées, pas de code solution. | Avant : ATELIER stocké + préfixe libre ; après : autre thème/vide, longueur, print versus valeur. |

Hors questions : introduction et transitions relues ; destinataire étudiant, données du parcours et finalité expliquées. Bilan : essai repris, explication et difficulté restante ; réexécution dans l’ordre et sorties conservées. Restitution `tal-submission` relue : URL publique substituable et trois étapes de dépôt, pas de solution ni adresse privée enregistrée.

## TD5-bis_S1_parametres_portee.ipynb

| Question / cellules lues | Action et données | Production à construire / afficher | Cours antérieur et statut de la tâche | Essais et vérifications obligatoires relus |
|---|---|---|---|---|
| Q1, 4–9 ; réponse `td5-a8015d05a021` | Définir etiquette(categorie, contenu) par concaténation. | Deux appels inversés, explication du changement de sens. | Cours `td5-8f9390643548` avant Q1. Guidé ; distinction paramètre/argument et appel nommé enseignée. | Avant : entourer arguments variés/inversés ; après : nommés dans ordre inverse et contenu vide. |
| Q2, 10–15 ; réponse `td5-919580f4e394` | Définir preparer_local en réaffectant le paramètre texte en minuscules. | Appel MUSÉE et variable extérieure Archives ; aucun global. | Cours `td5-1999ab5b0650` avant Q2. Observation guidée ; sorties musée/Archives explicitement encadrées comme vérification de portée, pas solution de fonction. | Avant : resultat extérieur puis suivant ; après : autre chaîne, retour et variable extérieure distingués. |
| Q3, 16–21 ; réponse `td5-00f6bda8e5fd` | Définir volume_defaut avec défaut 10 pour trois dimensions. | Appels 0/1/2/3 arguments dans ordre fourni, comparer prédictions. | Cours `td5-60707c75c07a` avant Q3. Réinvestissement ; syntaxe défaut expliquée avant, défauts immuables. | Avant : ajouter et défaut/nommé ; après : hauteur zéro, largeur deux, dimension décimale. |
| Q4, 22–27 ; réponse `td5-6ab5b1e6e1ed` | Définir saluer(personne, formule=Bonjour). | Appel avec défaut et autre avec Bonsoir. | Cours `td5-dbd981d0eb71` avant Q4. Guidé ; distinguer chaîne vide explicite et argument absent. | Avant : ranger avec/sans dossier ; après : autre personne, Salut et formule vide. |
| Q5, 28–33 ; réponse `td5-17108ab0c532` | Définir traduire_mot avec lexique reçu ; normaliser et repli vers mot normalisé. | Appels language et Unknown ; résultats retournés, dictionnaire transmis. | Cours `td5-7a85c1e12dba` avant Q5. Fonction générique à construire ; get ou if expliqués, aucune variable extérieure imposée. | Avant : tests clés casse/espaces et inconnue ; après : BOOK/Mystery/vide puis second lexique. |
| Q6, 34–39 ; réponse `td5-768dd4ed8f58` | Construire traduire_ou_signaler, avec repli facultatif distinct du mot inconnu. | Trois cas : second lexique, absence défaut et absence choisie. | Cours `td5-12fc8a22796e` avant Q6. Composition des acquis ; signaler valeur vide légitime versus absence ; paramètres obligatoires clarifiés. | Avant : lire_code table différente/valeur vide ; après : dictionnaire vide, entrée vide et traduction vide connue. |

Hors questions : introduction et transitions relues ; destinataire étudiant, données du parcours et finalité expliquées. Bilan : essai repris, explication et difficulté restante ; réexécution dans l’ordre et sorties conservées. Restitution `tal-submission` relue : URL publique substituable et trois étapes de dépôt, pas de solution ni adresse privée enregistrée.

## TD5-ter_S1_composition_texte.ipynb

| Question / cellules lues | Action et données | Production à construire / afficher | Cours antérieur et statut de la tâche | Essais et vérifications obligatoires relus |
|---|---|---|---|---|
| Q1, 6–11 ; réponse `td5-d919ce357914` | Construire compte_caractere par boucle/compteur, sans count ni normalisation. | Deux comptes e/texte et é/été. | Cours `td5-b1ee9d2c2816` avant Q1. Guidé sur compteur ; condition de correspondance à construire ; pas de fuite résultat complet. | Avant : compter_elements et liste vide ; après : absent/vide, e versus é, appels répétés. |
| Q2, 12–17 ; réponse `td5-3bab7eec99dc` | Construire nombre_mots en appelant normaliser et split sans argument. | Compte sur phrase fournie ; zéro vide/blancs. | Cours `td5-4a22205ddc8a` avant Q2. Guidé ; mot explicitement fragment, sans promesse linguistique. | Avant : composition encadrer/etiqueter, MUSÉE OUVERT et blancs ; après : vide/espaces multiples/apostrophe-ponctuation. |
| Q3, 18–23 ; réponse `td5-9165ae9c875c` | Construire traduire_phrase en appelant traduire_mot sur chaque fragment puis join. | Traduction Language data ; lexique paramètre. | Cours `td5-4994da4fde3e` avant Q3. Choix boucle/append ou compréhension TD4 rétabli ; fonctions de base fournies pour session vide. | Avant : séparateurs et tests traduire_mot ; après : inconnu, espaces multiples, vide et autre lexique. |
| Q4, 24–29 ; réponse `td5-fdab210aa19b` | Composer resume_texte avec normaliser et nombre_mots. | Trois clés exactes ; tous comptes sur texte normalisé, ordre libre. | Cours `td5-8b435096b567` avant Q4. Fonction à construire ; valeurs attendues des tests après réponse, servent critères de vérification. | Avant : dictionnaire decrire_etiquette et [:1] sur vide, longueur manuelle ; après : ARCHIVE ORALE/vide/espaces multiples. |
| Q5, 30–35 ; réponse `td5-9df79569a494` | Construire mesurer_traduction avec traduction et deux comptes. | Trois clés exactes ; lexique_expressions pour data book. | Cours `td5-19fde84f963f` avant Q5. Exemple/essai désormais distincts de la réponse évaluée ; composition générique reste à construire. | Avant : city map avec centre urbain/carte, compte source/cible ; après : inconnu, vide, lexique vide et limite traduction. |
| Q6, 36–41 ; réponse `td5-3c9aec2b857b` | Construire resumer_corpus en réutilisant resume_texte pour une liste de chaînes. | Liste de résumés ordonnée, doublons conservés, source intacte. | Cours `td5-21420a1910fd` avant Q6. Problème autonome annoncé ; principe illustré, assemblage fonctionnel restant à choisir. | Avant : relever_longueurs/vide puis comparer liste et set ; après : vide/répétitions/appels répétés/source affichée. |

Hors questions : introduction et transitions relues ; destinataire étudiant, données du parcours et finalité expliquées. Bilan : essai repris, explication et difficulté restante ; réexécution dans l’ordre et sorties conservées. Restitution `tal-submission` relue : URL publique substituable et trois étapes de dépôt, pas de solution ni adresse privée enregistrée.

## TD6-one_S1_fichiers_texte.ipynb

| Question / cellules lues | Action et données | Production à construire / afficher | Cours antérieur et statut de la tâche | Essais et vérifications obligatoires relus |
|---|---|---|---|---|
| Q1, 6–10 ; réponse `td6-q1-answer` | Lire affiliations_s1.txt UTF-8 avec with/open/read. | texte_affiliations ; longueur après bloc, expliquer lecture/fermeture. | Cours `td6-cours-q1-prompt` avant Q1. Manipulation guidée ; Path seulement préparation fournie ; cinq lignes historiques inchangées. | Avant : compter fins de lignes de atelier_lecture et relire autre variable. |
| Q2, 11–15 ; réponse `td6-q2-answer` | Filtrer les lignes utiles de texte_affiliations sans modifier graphies/ordre. | lignes complète et longueur. | Cours `td6-cours-q2-prompt` avant Q2. Réinvestissement ; splitlines et usage de strip comme test expliqués. | Avant : texte atelier/vide/blancs/musée et boucle de filtre. |
| Q3, 16–20 ; réponse `td6-q3-answer` | Écrire deux lignes exactes avec fins de ligne dans note_lecture.txt puis relire. | note_relue et repr ; expliquer intérêt relecture. | Cours `td6-cours-q3-prompt` avant Q3. Guidé ; write, w, fins de ligne et repr enseignés avant ; clarification essai tracée dans constats. | Avant : note_essai deux lignes puis observation de remplacement mode w. |
| Q4, 21–25 ; réponse `td6-q4-answer` | Nettoyer lignes_blanches.txt en gardant espaces des lignes utiles. | lignes_utiles, fichier lignes_utiles.txt, texte_utile_relu et repr. | Cours `td6-cours-q4-prompt` avant Q4. Réinvestissement ; jointure newline expliquée, fin finale explicitement exigée. | Avant : texte libre avec blancs, comparer filtrage brut et strip ; vérifier Salle A garde espaces. |
| Q5, 26–31 ; réponse `td6-q5-answer` | Trouver ligne maximale de phrases_s1.txt sans compter fin de ligne. | ligne_plus_longue et longueur ; expliquer initialisation. | Cours `td6-cours-q5-prompt` avant Q5. Problème autonome ; pas d’égalité dans données, vide défini, méthode de candidat enseignée. | Avant : candidat longueur puis texte sur trois chaînes et vide ; après : fichier vide. |
| Q6, 32–37 ; réponse `td6-q6-answer` | Transformer texte_espaces.txt en triplant chaque espace sans changer autres caractères. | texte_espaces_triples.txt, texte_triple_relu et repr. | Cours `td6-cours-q6-prompt` avant Q6. Problème autonome ; replace enseigné, choix enchaînement lecture/transformation/écriture/relecture. | Avant : remplacer e/E puis espace/tiret sur autre texte ; après : fichier vide/source conservée. |

Hors questions : introduction et transitions relues ; destinataire étudiant, données du parcours et finalité expliquées. Bilan : essai repris, explication et difficulté restante ; réexécution dans l’ordre et sorties conservées. Restitution `tal-submission` relue : URL publique substituable et trois étapes de dépôt, pas de solution ni adresse privée enregistrée.

## TD6-bis_S1_donnees_delimitees.ipynb

| Question / cellules lues | Action et données | Production à construire / afficher | Cours antérieur et statut de la tâche | Essais et vérifications obligatoires relus |
|---|---|---|---|---|
| Q1, 6–10 ; réponse `td6-q1-answer` | Relire cinq affiliations brutes et découper au premier point-virgule. | enregistrements, premier couple et liste entière dans ordre utile. | Cours `td6-cours-q1-prompt` avant Q1. Guidé ; lecture rappelée de TD6-one, graphies explicitement conservées. | Avant : galerie photo/aile nord/étage et comparaison strip ; expliquer maxsplit. |
| Q2, 11–15 ; réponse `td6-q2-answer` | Écrire les trois fiches fournies dans personnes_s1.txt avec champs délimités. | fiches_relues et repr ; trois fiches/code 06000 intact. | Cours `td6-cours-q2-prompt` avant Q2. Guidé ; join et fins de ligne réinvestis, ordre nom/prénom/code explicite. | Avant : autre fiche zéro initial, recomposer puis découper ; expliquer type chaîne. |
| Q3, 16–21 ; réponse `td6-q3-answer` | Relire personnes_s1.txt de Q2 et sélectionner code 83000. | personnes_83000, couples nom/prénom sans code, ordre du fichier. | Cours `td6-cours-q3-prompt` avant Q3. Réinvestissement ; indice/condition expliqués, dépendance Q2 explicite. | Avant : deux fiches libres code présent/absent ; après : code 75000, liste vide. |
| Q4, 22–27 ; réponse `td6-q4-answer` | Définir normaliser_personne puis appliquer aux quatre Durand Alice. | Quatre graphies identiques ; expliquer limite normalisation versus identité réelle. | Cours `td6-cours-q4-prompt` avant Q4. Fonction à construire ; strip/split/join/title enseignés avant essais exécutés. | Avant : trois graphies Lamy Zoé ; après : mêmes et vide, cas réel trompeur. |
| Q5, 28–33 ; réponse `td6-q5-answer` | Regrouper enregistrements de Q1 avec normaliser_personne de Q4. | affiliations_par_personne ; Durand puis dictionnaire complet, Martin compris. | Cours `td6-cours-q5-prompt` avant Q5. Autonomie de groupement ; dictionnaire de sets et clé absente enseignés. | Avant : salles par atelier/ajout répété ; après : personne par personne et affiliation déjà présente. |
| Q6, 34–38 ; réponse `td6-q6-answer` | Reprendre chaîne complète depuis affiliations_atelier.txt fourni, sans perdre ; dans affiliation. | groupes_atelier, tous groupes normalisés, ignorer lignes blanches. | Cours `td6-cours-q6-prompt` avant Q6. Problème autonome ; données fournies seulement, parsing/normalisation/groupement à construire. | Avant : appartenance Studio versus Studio;annexe ; après : comparer occurrences et distincts. |

Hors questions : introduction et transitions relues ; destinataire étudiant, données du parcours et finalité expliquées. Bilan : essai repris, explication et difficulté restante ; réexécution dans l’ordre et sorties conservées. Restitution `tal-submission` relue : URL publique substituable et trois étapes de dépôt, pas de solution ni adresse privée enregistrée.

## TD6-ter_S1_csv.ipynb

| Question / cellules lues | Action et données | Production à construire / afficher | Cours antérieur et statut de la tâche | Essais et vérifications obligatoires relus |
|---|---|---|---|---|
| Q1, 8–12 ; réponse `td6-q1-answer` | Écrire documents_s1.csv avec en-tête et deux documents exacts, puis csv.reader. | documents_relus, en-tête compris ; nombres relus chaînes. | Cours `td6-cours-q1-prompt` avant Q1. Guidé ; csv importé et writer/reader/writerow/list/newline expliqués avant usage. | Avant : ateliers CSV puis autre fichier d’essai et types des capacités. |
| Q2, 13–17 ; réponse `td6-q2-answer` | Lire lieux_s1.csv avec virgule interne à un lieu. | lieux_relus avec en-tête, deux colonnes par ligne. | Cours `td6-cours-q2-prompt` avant Q2. Guidé ; virgule de champ versus séparateur explicités, accents conservés. | Avant : fichier virgule dans second champ, texte versus reader ; interpréter guillemets. |
| Q3, 18–23 ; réponse `td6-q3-answer` | Sélectionner code 83000 dans personnes_s1.csv. | noms_83000 en chaînes Nom Prénom, ordre source, en-tête exclu. | Cours `td6-cours-q3-prompt` avant Q3. Réinvestissement ; [1:] et codes chaînes expliqués avant, pas conversion entier. | Avant : mini tableau autre codes présents/absents ; après : code 75000. |
| Q4, 24–28 ; réponse `td6-q4-answer` | Reconstruire groupes depuis cinq lignes brutes de affiliations_s1.txt. | affiliations_par_personne entier, justification des groupes par lignes sources. | Cours `td6-cours-q4-prompt` avant Q4. Problème autonome ; normaliser_personne fourni, groupement à refaire ; session vide équipée. | Avant : sorted des clés et sets de salles ; comparer collection initiale et liste triée. |
| Q5, 29–33 ; réponse `td6-q5-answer` | Exporter Q4 sous en-tête historique exact et affiliations jointes par barre verticale. | affiliations_uniques.csv, affiliations_relues et texte CSV repr fourni en complément. | Cours `td6-cours-q5-prompt` avant Q5. Réinvestissement ; ordre libre, sorted facultatif ; texte brut conservé pour couverture historique. | Avant : catégories cartes/photos puis autre dictionnaire et CSV d’essai ; après : comparer comptes/sets et séparateurs. |
| Q6, 34–39 ; réponse `td6-q6-answer` | Exporter groupes_nouveaux avec accents/virgule interne et tri imposé. | affiliations_nouvelles.csv, nouveaux_relus ; trois colonnes par ligne et comptes exacts. | Cours `td6-cours-q6-prompt` avant Q6. Problème autonome ; données seules fournies, toute écriture/relecture à construire. | Avant : retrouver virgule de Q2 ; après : lire texte brut et expliquer guillemets/personne. |

Hors questions : introduction et transitions relues ; destinataire étudiant, données du parcours et finalité expliquées. Bilan : essai repris, explication et difficulté restante ; réexécution dans l’ordre et sorties conservées. Restitution `tal-submission` relue : URL publique substituable et trois étapes de dépôt, pas de solution ni adresse privée enregistrée.

## Conservation comparée, autonomie et français

TD3 historique : Q1 est repris TD3-one Q2 ; Q2 dans TD3-bis Q1 ; Q3/Q4 fusionnés sans perte des affichages ni du parcours dans TD3-ter Q1 ; Q5 dans TD3-ter Q4 ; Q6 dans TD3-ter Q6 avec seconde différence ajoutée. Les exemples et essais de villes/codes/animaux/couleurs/langues restent actifs. Le comparatif des quatre structures encadre la série et revient en synthèse ; la non-modification des positions d’un tuple n’est pas assimilée à une exactitude des données.

TD5 historique : Q1/Q2 dans TD5-one Q1/Q5 ; défaut/saluer dans TD5-bis Q3/Q4 ; Q4 dans TD5-bis Q5 ; Q3/Q5/Q6 dans TD5-ter Q2/Q3/Q4. Les paramètres, print/return/None, portée locale, inconnus, second lexique, espaces intérieurs, cas vide, [:1] et cohérence des trois comptes sont bien repris avec essais. Le choix boucle/compréhension de TD5-ter Q3 demeure possible après reprise : la compréhension est effectivement enseignée au TD4 cellule 36.

TD6 historique : préparation cinq lignes inchangée ; Q1/Q2 dans TD6-one Q1/Q2 ; Q3/Q4/Q5 dans TD6-bis Q1/Q4/Q5 ; Q6 dans TD6-ter Q5, précédée d’une reconstruction autonome Q4. Les graphies brutes, premier couple et liste entière, quatre variantes Durand, toutes les personnes, ensemble distinct, en-tête et compte sont conservés. L’affichage brut repr de l’export est fourni en complément de csv.reader ; ceci conserve l’observation du fichier sans demander pathlib dans la réponse.

Les exemples distincts ont parfois une structure proche de la réponse, ce qui est cohérent avec leur fonction de préparation guidée. Ils ne sont pas des cellules-réponses préremplies. Les problèmes finaux demandent encore un transfert : copie indépendante, recomposition de tuple, inversion/ensembles, maximum de trois valeurs, composition sur corpus, chaîne de traitement d’un autre fichier, export comportant virgule/accent. Les demandes de vérification ne promettent pas qu’un affichage prouve la compréhension.

Les résultats explicites de certains essais (zéro sur vide, 12.0 pour un volume, portée musée/Archives, 13 caractères/2 fragments) sont encadrés par la tâche de test et exigent une fonction générique ; ils ne remplacent pas la définition à construire. Le défaut de séparation des données de TD5-ter Q5 a été corrigé : l’essai utilise désormais city map, l’exercice data book. Aucun résultat calculé n’est préinscrit dans une cellule-réponse.

Aucun minutage ni notice sur les valeurs d’identification dans les nouveaux cahiers. Pas de présentation répétée de Gemini. La restitution reste une action de dépôt ; les bilans demandent de relire les critères locaux. Les références Swinnen précisent les adaptations et ne lui attribuent ni ensembles ni module csv. Les noms de méthodes Python restent tels quels ; vocabulaire français expliqué avant réemploi, commentaires et unités d’âge/taille explicités. Les mentions de limites (normalisation/identité, fragments/mots, dictionnaire/traduction, perte de fréquence) sont orientées vers l’interprétation par l’étudiant.

## Constats et corrections

| ID | Gravité | Emplacement / difficulté | Reprise et critère vérifiable | État |
|---|---|---|---|---|
| TAL-EDIT-S1SW-001 | Mineure | TD3-bis Q5 : accord « espaces indiquées ». | « espaces indiqués ». | Corrigé par le Designer ; relu. |
| TAL-EDIT-S1SW-002 | Mineure | TD5-bis essai Q6 : un seul paramètre obligatoire annoncé alors que deux le sont. | Pluriel « paramètres obligatoires ». | Corrigé ; relu. |
| TAL-EDIT-S1SW-003 | Majeure sur autonomie, résolue | TD5-ter essai Q5 employait mêmes données et lexique que Q5. | Essai sur données distinctes en conservant comparaison de compte. | Corrigé : city map / centre urbain / carte ; relu. |
| TAL-EDIT-S1SW-004 | Mineure, résolue | TD3-one Q6 : test liste vide pouvait être compris comme modification indice 0. | Limiter test vide à copie, sans exiger remplacement inexistant. | Clarification explicite dans l’énoncé ; relue. |
| TAL-EDIT-S1SW-005 | Mineure | TD6-one essai Q3 : « ajouter une troisième ligne » en mode w pouvait signifier réécrire trois lignes, empêchant observation de remplacement. | Rouvrir en w et écrire seulement une nouvelle ligne ; observer disparition des premières. | Clarification demandée au Designer ; vérification finale ci-dessous. |
| TAL-EDIT-S1SW-006 | Bloquante jusqu’à synchronisation | TD5-ter Q3 réautorise compréhension, scope tuteur devait suivre. | Inscrire compréhension dans périmètre Q3 puis synchroniser manifeste/profil/deux contextes. | Résolu : compréhension présente dans le manifeste, profil et doubles contextes ; relu. |

## Tuteur, contrat et limites de preuve

Les contextes complets ont été lus, ainsi que tous les périmètres des 54 questions et les profils structurés. Le socle impose une question puis attente, exemple distinct si blocage, langage naturel S1 sans code, sans recette complète ni résultat attendu. Les bibliothèques sont limitées à csv dans TD6-ter aux questions correspondantes ; pathlib reste préparation fournie. Les connaissances déclarées correspondent aux explications réellement antérieures : for est introduit TD3-one Q3, déballage TD3-bis Q4, ensembles TD3-ter Q4/Q5, def TD5-one Q1, défaut TD5-bis Q3, csv TD6-ter Q1 et tri TD6-ter Q4. Aucun cumul de permission par union des exercices suivants n’est demandé au tuteur.

La cohérence machine (égalité des contextes, SHA-256 et session manifeste) est contrôlée séparément de cette lecture. La présence du texte caché ne démontre pas le comportement effectif de Gemini : essai Colab/tuteur non réalisé dans cette revue. Pas d’essai humain en classe ni de mesure de durée. La charge ajoutée demeure une décision de répartition enseignante ; aucune promesse d’achèvement dans l’ancien volume horaire n’apparaît dans les cahiers.

Les neuf identifiants et contrats sont nouveaux ; les trois historiques sont conservés. La revue éditoriale ne valide pas le barème ou l’implémentation des correcteurs. Exécution des modèles : rôle Étudiant-Modèle séparé ; cette revue ne s’attribue pas son exécution et n’a modifié aucun modèle, test ou correcteur. Le verdict pédagogique et la couverture finale appartiennent au rapport indépendant du Pedagogy-Reviewer.

## Vérification finale et verdict

Contrôles indépendants exécutés par lecture JSON des neuf cahiers et du manifeste final :

- 9/9 contextes Markdown exactement égaux aux contextes Colab ; 9/9 empreintes de contexte conformes au profil ; 9/9 sessions du profil égales aux sessions du manifeste.
- 9/9 premières cellules réunissent titre visible et contexte caché ; aucune nouvelle cellule exclusivement cachée ; aucune sortie ni numéro d’exécution enregistré dans les cellules de code.
- 9/9 annexes légales portent une empreinte identique et un bloc details repliable. Leur présence n’ajoute pas un prérequis pédagogique.
- TD5-ter Q3 contient désormais « compréhension de liste » dans le manifeste, le profil et les deux contextes synchronisés. La contrainte est résolue.
- Affichage texte brut repr de TD6-ter Q5 relu : code commenté fourni avec instruction explicite de le décommenter, après export étudiant.

Verdict éditorial : **ACCEPT**. Lisibilité : **LISIBILITÉ_ÉTUDIANTE_VALIDÉE** pour les neuf cahiers et les 54 questions sur les empreintes indiquées ci-dessus. Aucun blocage ouvert. Le mineur TD6-one essai Q3 n'empêche pas d'effectuer l'exercice ; sa clarification est recommandée pour observer sans ambiguïté le remplacement par w.

Ce verdict reste distinct de **COUVERTURE_PÉDAGOGIQUE_CONSERVÉE** et des revues technique/gouvernance. Relais : root/Integration-Master, avec revue pédagogique indépendante et essais Étudiant-Modèle à joindre avant décision du mainteneur. Ni fusion ni déploiement réalisés par ce rôle.

Addendum final — Les premières cellules TD3-ter et TD5-ter portent maintenant les titres visibles `TD3.ter` et `TD5.ter`, conformément à la graphie demandée. Titres relus ; sessions du manifeste égales aux profils, contextes Markdown/Colab identiques et empreintes de contexte conformes pour les deux cahiers. Aucun changement de notion. Empreintes de fichier actualisées ci-dessus ; verdict éditorial inchangé.
