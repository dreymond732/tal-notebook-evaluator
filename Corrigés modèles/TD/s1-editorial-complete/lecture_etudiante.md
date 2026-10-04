# Lecture étudiante — Révision complète S1

Mission : lecture préalable, sans résolution, exécution ni soumission. Aucune identité utilisée. Accès limité aux sept sujets S1 et aux règles du rôle ; aucun correcteur, test ou corrigé consulté. Les réponses imprimées dans les exemples sont fournies par le sujet ; les réponses aux exercices restent à construire. Les indices de cellules ci-dessous commencent à zéro et identifient l'état relu.

## TD1 — Variables et types (6 questions)

Lecture : toutes les cellules visibles 1–37, code fourni inclus. La cellule 0 contient des instructions cachées qui ne remplacent pas le cours. Les cellules 2 et 4 expliquent exécution, ordre, commentaires, emplacement des réponses et activation des affichages. Rien ne demande de connaître une bibliothèque.

| Question | Données comprises | Travail et production attendus | Notions apprises dans le sujet | Ambiguïté ou manque |
|---|---|---|---|---|
| Q1 | Prix 0.12 et 125 mots, fournis | Calculer `cout_total`, activer Q1, comparer au calcul manuel | Affectation et multiplication, cellules 5–8 | Aucun |
| Q2 | `note = 14.5` | Prédiction en commentaire et affichage du type | Types et `type`, cellules 11–13 | Aucun ; l'affichage est fourni, seule la prédiction est personnelle |
| Q3 | Variables Q1 | Deux comparaisons nommées ; affichage de deux booléens | `==`, `>=`, `>`, `and`, cellules 16–18 | Dépendance Q1 explicite |
| Q4 | Deux langues imposées | F-string et phrase exacte dans `phrase_presentation` | F-string, cellules 21–23 | Apostrophe typographique et ponctuation explicitement signalées |
| Q5 | Chaîne "80" | Conversion, addition de 20, résultat et type | `int` et différence somme/concaténation, cellules 26–28 | Aucun |
| Q6 | Phrase personnelle | Longueur, présence exacte de TAL, phrase conservée et justification en commentaire | `len`, `in`, casse, `repr`, cellules 31–33 | Sens de l'explication explicitement hors score |

Les consignes sont distinguées des cours et des exemples. Les essais sont identifiables comme travail supplémentaire demandé. Aucune tâche implicite découverte seulement après sa cellule de réponse. Durée affichée : 120 min ; plausible sur lecture, sans mesure réelle. Q6 réserve du temps à une production personnelle.

## TD2 — Chaînes et séquences (7 questions)

Lecture : toutes les cellules visibles 1–32. TD1 est la ressource antérieure autorisée effectivement lue. Les exemples sont suivis d'énoncés séparés. Chaque réponse comporte un emplacement pour l'explication.

| Question | Données comprises | Travail et production attendus | Notions apprises avant l'exercice | Ambiguïté ou manque |
|---|---|---|---|---|
| Q1 | `texte_brut` fourni avec espaces | Chaîne nettoyée, deux longueurs, explication de la conservation de la source | Immuabilité, méthode et `strip`, cellules 5–6 ; `len` TD1 Q6 | Aucun |
| Q2 | Résultat Q1 | Minuscules puis remplacement ; booléens de présence, source affichée et explication | `lower`, `replace`, cellules 9–10 ; `in` TD1 Q6 | L'énoncé invite correctement à discuter si l'ordre est indispensable sur ces données |
| Q3 | `mot = "tokenisation"` | Premier/dernier caractère, deux tranches, longueur et justification | Indices et borne exclue, cellules 13–14 | Aucun |
| Q4 | Phrase fournie | Liste, troisième et dernier éléments, longueurs/types et explication | `split`, liste et indice, cellules 17–18 ; types TD1 | Aucun |
| Q5 | `tokens` Q4 | Assemblage avec séparateur exact, reconstruction, comparaison et justification | `join` et `split(separateur)`, cellules 21–22 ; `==` TD1 | Dépendance explicite ; comparaison de listes expliquée dans l'énoncé |
| Q6 | Trois chaînes fournies | Nettoyer séparément, créer trois variables puis une liste ; comparer à la source | Opérations Q1–Q4, liste littérale cellules 25–26 | Boucle explicitement exclue et trois indices imposés ; pas de notion future nécessaire |
| Q7 | Phrase exacte fournie dans l'énoncé | Prédire puis découper ; commenter une limite à partir d'un fragment observé | `split` Q4 ; limites linguistiques annoncées cellule 17 | Pas de connaissance linguistique supplémentaire présupposée ; critères d'autoévaluation fournis |

Aucun blocage. La nuance entre résultat technique et interprétation personnelle est compréhensible sans promesse de correction individuelle. Les 120 min indiquées restent une hypothèse ; Q6 accumule plusieurs observations mais réemploie uniquement les opérations déjà présentées.

## TD3 — Collections (6 questions)

Lecture : toutes les cellules visibles 1–38. Ressources antérieures lues : TD1 et TD2. Les collections sont présentées avant leur emploi. Une première boucle est enseignée ici, sans renvoyer implicitement au futur TD4.

| Question | Données comprises | Travail et production attendus | Notions apprises avant l'exercice | Ambiguïté ou manque |
|---|---|---|---|---|
| Q1 | Liste `outils` fournie | Ajouter puis retirer ; affichage intermédiaire Q1a et final Q1 | `append`/`pop`, cellules 6–8 | Déplacement de Q1a explicitement demandé ; son ordre dans le squelette oblige à lire cette indication |
| Q2 | Trois langues et ordre imposés | Tuple, type, justification et tuple affiché | Tuple et accès par indice, cellules 11–13 | Sens de justification déclaré non autocorrigé |
| Q3 | Correspondances dans tableau cellule 20 | Dictionnaire de trois entrées, ajout séparé, traduction et dictionnaire complet | Dictionnaire/clé/valeur/affectation, cellules 16–18 | Les deux traductions admises de language sont explicites |
| Q4 | Lexique Q3 | Parcours `items`, liste de chaînes avec flèche et affichage après boucle | Boucle, indentation, déballage, accumulation et f-string, cellules 22–24 | Compris ; étape cognitive la plus dense, durée de 25 min à observer |
| Q5 | Liste de formes répétées | Ensemble, deux cardinalités, ensemble affiché et vérification manuelle | `set`, occurrences/formes, cellules 27–29 | Aucun ; ordre sans signification explicité |
| Q6 | Deux corpus fournis | Ensembles, intersection et différence orientée, affichage | Opérations d'ensemble, cellules 32–34 | Aucun ; orientation de la différence explicitée |

Aucun blocage ni passage incompris. Q4 dispose bien d'un cours exécutable et d'un essai, mais la lecture seule ne garantit pas la maîtrise du déballage et de l'accumulation en 25 min. Le total annoncé de 120 min est une estimation.


## TD4 — Boucles et comptages (7 questions)

Lecture : toutes les cellules visibles 1–43. TD1–TD3 lus comme ressources antérieures. La première boucle n'est donc pas supposée inconnue. Les conditions sont montrées avant les filtres.

| Question | Données comprises | Travail et production attendus | Notions apprises avant l'exercice | Ambiguïté ou manque |
|---|---|---|---|---|
| Q1 | Liste `mots` fournie | Boucle produisant une nouvelle liste en majuscules, ordre/source conservés | Parcours et accumulation TD3 Q4 ; `upper`, cellules 6–8 | Aucun |
| Q2 | Liste Q1 | Filtrer strictement au-delà de cinq caractères ; liste affichée | `if` imbriqué, cellules 11–13 ; `len` TD1 | Borne expressément vérifiée |
| Q3 | Liste Q1 | Présence de a sans casse mais graphie d'origine conservée | Casse et valeur testée/conservée, cellules 16–18 | Aucun |
| Q4 | Bornes 0–10 | Liste des positions paires par `range` | Bornes, pas et conversion en liste, cellules 21–23 | Modulo expliqué mais pas obligatoire ; choix possible lisible |
| Q5 | Départ 7, plafond 70 | Liste des multiples par `while`, anticipation de l'arrêt | État, condition, mise à jour, cellules 26–28 | Aucun ; ne pas tester volontairement une boucle infinie est explicite |
| Q6 | Liste issue du texte fourni | Dictionnaire d'effectifs, contrôle de somme | `get` et alternative `if/else`, cellules 31–33 | Le contrôle de somme peut se faire à la main ; aucune fonction `sum` imposée sans cours |
| Q7 | Liste Q1 | Compréhension retournant des longueurs sous filtre strict | Compréhension comparée à une boucle, cellules 36–38 | Référence de vérification Q2 explicite |

Pas de blocage. Séance dense, notamment `while` et accumulation ; la plausibilité de 120 min n'est pas une observation de classe.

## TD5 — Fonctions (6 questions)

Lecture : toutes les cellules visibles 1–45. Les vérifications de fonctions occupent maintenant des cellules dédiées après chaque réponse ; elles se réexécutent donc après les définitions. Les entraînements préalables restent séparés.

| Question | Données comprises | Travail et production attendus | Notions apprises avant l'exercice | Ambiguïté ou manque |
|---|---|---|---|---|
| Q1 | Deux appels fournis et chaîne vide | Fonction retournant un entier, tests et affichages | `def`, paramètre, appel, `return`/`print`, `None`, cellules 5–8 ; `len` TD1 | Aucun |
| Q2 | Chaîne de l'appel, vide et espaces | Fonction retirant espaces de bord et normalisant casse | TD2, rappel et essais cellules 12–14 | Espaces intérieurs explicitement conservés |
| Q3 | Appel, vide et espaces multiples | Fonction composant `normaliser`, `split` et comptage | Composition et comportement vide, cellules 18–20 | Paramètre par défaut est enseigné dans l'essai sans être imposé à Q3 |
| Q4 | Lexique fourni et différents mots | Fonction avec lexique paramétré, traduction ou repli normalisé | Dictionnaire TD3, conditions TD4, recherche cellules 24–26 | Clé inconnue et dictionnaire extérieur distingués |
| Q5 | Phrase de l'appel puis cas limites | Découper, appeler Q4 pour chaque fragment, assembler et retourner | Boucle TD4, `join` TD2, rappel cellules 30–32 | Fonction antérieure requise nommée explicitement |
| Q6 | Texte de l'appel et deux tests | Dictionnaire à trois clés, tous comptes sur texte normalisé | Retour de dictionnaire cellules 36–38 ; fonctions Q1–Q3 | Tableau tranche explicitement brut/normalisé |

Pas de blocage. Les résultats doivent être construits à partir des paramètres, ce que le cours explique sans discours de concepteur. Les 120 min restent indicatives.

## TD6 — Fichiers et CSV (6 questions)

Lecture : toutes les cellules visibles 1–42. Les identités présentes dans la ressource font partie des données pédagogiques du sujet ; aucun fichier d'identités extérieures consulté. Préparation fournie distincte de ce que l'étudiant doit écrire.

| Question | Données comprises | Travail et production attendus | Notions apprises avant l'exercice | Ambiguïté ou manque |
|---|---|---|---|---|
| Q1 | Fichier préparé cellule 6 | Lecture avec fermeture, chaîne et longueur | `with open`, UTF-8, `read`, cellules 7–9 | Aucun ; fichier à recréer après session vide signalé |
| Q2 | Texte Q1 | Liste des lignes utiles, ordre conservé et cardinalité | `splitlines` et blanc/vide, cellules 12–14 ; filtrage TD4 | Aucun |
| Q3 | Lignes Q2 | Couples identité/affiliation, premier et totalité affichés | Découpage maximal cellules 17–19 ; boucles/collections TD3–TD4 | Liste ou tuple explicitement admis |
| Q4 | Quatre graphies | Fonction normalisant bords, espaces internes et casse, essais affichés | `split`/`join`/`title`, cellules 22–24 ; fonctions TD5 | Convention de nommage distinguée d'une identité réelle |
| Q5 | Enregistrements Q3, fonction Q4 | Dictionnaire d'ensembles d'affiliations, particulier et totalité affichés | Collections imbriquées et ajout ensembliste cellules 28–30 ; branchement TD4 | Combinaison autonome de notions déjà montrées, sans réponse fournie |
| Q6 | Dictionnaire Q5 | CSV UTF-8, en-tête exact et une ligne/personne, relecture | Module `csv`, modes, `writerow`, cellules 34–36 | Point corrigé : `join` accepte un ensemble de chaînes, expliqué cellule 34 |

Le travail de Q5 est autonome et plus complexe que son exemple, mais les opérations composantes ont été vues. La clarification sur les types acceptés par `join` a été relue ; le manque signalé est levé.

## TD7 — Regex et pipeline (7 questions)

Lecture : toutes les cellules visibles 1–49. Module présenté cellule 5 et import fourni cellule 6 ; aucune installation à deviner.

| Question | Données comprises | Travail et production attendus | Notions apprises avant l'exercice | Ambiguïté ou manque |
|---|---|---|---|---|
| Q1 | Texte fourni | Recherche TAL sans casse, booléen | `search`, `bool`, `IGNORECASE`, cellules 8–10 | Aucun |
| Q2 | Texte fourni | Liste de séquences de chiffres sous forme de chaînes | Classe, `+`, `findall`, cellules 13–15 | Type et ordre explicites |
| Q3 | Texte français fourni | Suites de lettres accentuées et comparaison commentée à `split` | Classes et frontières, cellules 18–20 ; `split` TD2 | Convention apostrophes/ponctuation clairement fixée |
| Q4 | Journal fourni | Remplacer dates de forme définie et conserver autres caractères | `sub`, quantificateurs, cellules 23–25 | Validation calendaire non demandée |
| Q5 | Appel puis tests vide/espaces/date | Fonction de quatre transformations dans l'ordre imposé | TD5 fonctions, TD6 espaces, regex Q2/Q4, ordre cellules 29–31 | Marqueur et ponctuation explicités |
| Q6 | Appel puis autres entrées | Fonction retournant trois clés : texte, liste et effectifs | Comptage TD4, composition TD5, rappel cellules 35–37 | DATE dans les fragments signalé et à commenter ; pas à supprimer tacitement |
| Q7 | Situation française choisie | Chaîne explicitant une limite, information linguistique utile et affichage | Limites forme/sens/fonction cellules 41–43 | Point corrigé : exemple concret de porte nom/verbe, cellule 41 ; cas personnel distinct demandé |

Les 120 min sont une estimation ; Q5/Q6 concentrent le réinvestissement. Q7 dispose désormais de critères d'autoévaluation et d'un exemple linguistique concret distinct du cas personnel attendu.

## Clôture de la lecture exhaustive

45 questions relues et documentées. Les deux clarifications demandées ont été relues dans la version finale : `join` sur ensemble en TD6 et cas concret forme/fonction en TD7. Les onze cellules de vérification ajoutées après les réponses en TD5–TD7 ont été relues : les essais n'obligent plus à écrire un appel au-dessus de la définition à conserver lors d'une réexécution de haut en bas. Les renvois et l'organisation générale ont été contrôlés à nouveau.

**Verdict de lecture étudiante : favorable, sans blocage restant.** Chaque question donne des données ou un choix explicitement personnel, un travail et une production identifiables, avec des appuis antérieurs effectivement lus. Aucun passage visible incompris après ces clarifications. Les cours, exemples et travaux sont distincts. Les promesses de relecture individuelle systématique sont absentes.

Aucune réponse construite, exécutée ou soumise. Aucun correcteur ou test consulté. Ce verdict ne valide ni les correcteurs, ni l'exécution réelle, ni la prise en compte du tuteur par Colab, ni la durée en classe. Les séquences denses TD3 Q4, TD6 Q5–Q6 et TD7 Q5–Q6 restent à observer lors d'un usage réel.
