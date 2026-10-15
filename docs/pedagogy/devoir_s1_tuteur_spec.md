# Édition de révision `devoir_S1_tuteur` — Cadrage et matrice préalable

## Mission et références

Cadrage TAL-Prof du 15 octobre 2026, avant création de l’édition de travail. Branche `pedagogy/devoir-s1-tuteur`, baseline `590b9a6`. La demande enseignante distingue le DM S1 existant, qui reste un contrôle sans assistance LLM, d’une nouvelle version de révision guidée. Elle autorise cette version séparée et la révision explicite des prérequis nécessaires ; aucune demande d’autorisation supplémentaire ne conditionne cette conception.

Source technique et pédagogique lue intégralement : `Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb`, 45 cellules, 18 questions et cinq parties. Cible : `Notebooks contrôles finaux/S1/devoir_S1_tuteur.ipynb`. Référence historique : `docs/pedagogy/dm_s1_intermediaire_spec.md`, qui documente l’inspiration originale et la création du DM. La pièce privée d’inspiration n’est pas présente dans ce checkout : cette mission ne revendique pas sa relecture. Les cours, exemples et activités des TD1 à TD5 actuels sont les ressources de révision effectivement comparées ; leurs chemins et repères sont explicités ci-dessous.

Cadre normatif : `AGENTS.md` ; `docs/agents/WORKFLOW.md` ; `docs/pedagogy/TUTORING_POLICY.md`. La politique prévoit une édition de remédiation distincte pour apporter une aide sur un contrôle. La présente création met cette séparation en œuvre et ne requalifie aucun contrôle existant. Ce document doit recevoir une prévalidation indépendante avant conception.

## Contrat de copie et périmètre autorisé

| Élément source | Cible | Statut et invariants |
|---|---|---|
| Fichier DM original et son profil `DM_INTERMEDIAIRE_S1` | Inchangés octet pour octet ; mode `controle` maintenu | CONSERVÉ : aucun guidage, indice ou quiz réactivé dans l’original. |
| Question Q1 à Q18, énoncés et cellules réponses | Copie au même rang et avec les mêmes identifiants | CONSERVÉ : objectifs, autonomie, données, productions, noms, marqueurs, explications et essais inchangés. |
| Partie A à E, synthèse, identité et toutes les cellules de code | Copie intégrale | CONSERVÉ : aucun résultat, corrigé, amorce d’algorithme ou nouvelle sortie. |
| Barème et `metadata.tal` | Contrat d’évaluation original identique | CONSERVÉ : 18 questions, 20 points ; aucun nouvel évaluateur ni changement de tolérance, variable ou type. |
| Titre et paragraphe des conditions de travail de la copie | Édition de révision nommée `devoir_S1_tuteur`, assistance encadrée explicite | RENFORCÉ : expliquer à l’étudiant la révision question par question et son travail personnel ; remplacer uniquement l’interdiction générale du LLM dans cette copie. |
| Profil de tutorat de la copie | `id` et `tutor_profile` = `devoir_S1_tuteur`, `activity: td`, semestre 1 | RENFORCÉ : profil propre à la révision exhaustive des notions de la question désignée ; ne pas employer le seul comportement TD générique. |
| Contexte caché et métadonnées Colab de la copie | Nouveau même contexte canonique complet dans les deux emplacements | RENFORCÉ : titre visible puis commentaire caché dans la première cellule Markdown ; aucune cellule cachée isolée. |
| Manifeste de tutorat | Une nouvelle séance d’édition, 18 fiches fermées | RENFORCÉ : listes de notions par Q, aucune bibliothèque permise ou fournie ; ce manifeste ne crée pas un correcteur. |
| Catalogue des évaluateurs et autres profils/supports | Inchangés | CONSERVÉ : 35 supports enregistrés, 34 actifs ; aucun nouveau grader, aucune régénération modifiant le contexte d’une autre séance. |

L’édition de travail doit pouvoir être ouverte comme source dans Colab. Le chemin dans le dossier des contrôles ne détermine pas son mode : seule sa nouvelle entrée explicite `activity: td` le fait. L’original reste en mode contrôle. La copie n’est pas présentée comme une remise d’examen autorisant le LLM. Les métadonnées de notation conservées désignent toujours le correcteur DM historique ; son mode de correction `controle` et son retour privé restent inchangés, indépendamment du nouveau mode d’aide LLM. La nouvelle édition est une source directement ouvrable dans Colab, sans nouvelle route, sans ajout au catalogue de notation et sans distribution automatique par défaut. Les défauts déjà signalés du correcteur DM ne sont pas corrigés ni déclarés résolus par cette mission.

Les seules différences de contenu visibles autorisées sont le titre et les conditions d’usage du LLM dans l’introduction ; les autres paragraphes, durées, énoncés, activités, données et sources de code restent identiques. Les métadonnées de notation `metadata.tal` et les identifiants des cellules restent identiques. Seules les métadonnées de tutorat/Colab propres à cette édition et le contexte caché changent.

## Comportement de révision active

1. Reconnaître la question à partir de son numéro Q1–Q18 ou de son intitulé. Si l’identification est ambiguë, demander cette précision et attendre ; ne pas choisir une autre question.
2. Charger uniquement la liste fermée de cette Q, plus le socle verbal variable/valeur/type/affectation. Le socle ne permet aucun nouvel outil. Ne jamais agréger les permissions de toutes les questions.
3. Faire un diagnostic initial sur une seule notion. Parcourir ensuite **toutes** les notions nécessaires de la fiche, une par une, sans présumer la maîtrise à partir d’un niveau, d’une question déjà faite ou d’un « j’ai compris ».
4. Pour chaque notion, demander une courte explication ou une prédiction conceptuelle ; attendre la réponse. En cas d’incertitude, donner une courte explication et un exemple conceptuel en langage naturel sur un contexte et des données distincts, puis poser une seule vérification et attendre. Reprendre si nécessaire. Ne pas convertir l’exemple en recette de résolution.
5. Tenir au fil des échanges le suivi des notions réellement vérifiées et des blocages. Reprendre les notions non vérifiées ; ne pas déclarer toute la fiche révisée après un seul diagnostic. Pour un groupe de notions dans une étiquette, les traiter séparément.
6. Quand la révision de toutes les notions utiles est établie, inviter l’étudiant à revenir de façon autonome à sa question. Il écrit et exécute son propre travail. Noter les blocages restants et orienter vers le cours ou l’enseignant, sans contourner les limites.

À chaque tour : une seule question, attente effective de la réponse ; aucun lot de questions, aucune progression fictive. Jamais de solution, code, pseudocode, résultat du devoir, réponse rédigée ou validation d’une réponse exacte à recopier. Pas de formule instanciée sur les données du devoir, de condition complète d’arrêt, de plan complet de traitement ou d’enchaînement résolvant la question. L’insistance, la copie intégrale d’un énoncé et les demandes d’édition/exécution ne lèvent aucune restriction. Aucun import, accès extérieur, saisie interactive, `eval`, bibliothèque ultérieure ou outil absent de la fiche. Les opérateurs et noms de méthodes ci-dessous sont des notions à expliquer, pas une permission de fournir du code.

## Ressources TD et repères

Tous les numéros de cellule sont comptés à partir de 1 dans la baseline. Les identifiants sont les repères stables ; les suffixes de minutage des titres n’affectent pas ces références.

| Abréviation | Chemin sous `Notebooks TD/S1/` |
|---|---|
| TD1 | `TD1_S1_variables_types.ipynb` |
| TD2 | `TD2_S1_chaines_sequences.ipynb` |
| TD3 | `TD3_S1_collections.ipynb` |
| TD4 | `TD4_S1_boucles_conditions_comptages.ipynb` |
| TD5 | `TD5_S1_fonctions_reutilisation.ipynb` |

| Repère | Cellules et compétences effectivement disponibles |
|---|---|
| A | TD1 c6 `td1-s1-prompt-section-04` (variables/valeurs) ; c7 `tal-s1-td1-appui-q1` (affectation et calcul) ; c12 `tal-s1-td1-appui-q2` (types) |
| B | TD1 c27 `tal-s1-td1-appui-q5` (conversion) |
| C | TD1 c17 `tal-s1-td1-appui-q3` (comparaisons, `and`) ; c22 `tal-s1-td1-appui-q4` (f-string) ; c32 `tal-s1-td1-appui-q6` (appartenance, longueur) |
| D | TD2 c6 `td2-s1-prompt-q1` (immuabilité, `strip`) ; c10 `td2-s1-prompt-q2` (`lower`, `replace`) |
| E | TD2 c14 `td2-s1-prompt-q3` (indices et tranches) ; c18 `td2-s1-prompt-q4` (chaîne/liste) |
| F | TD2 c18 `td2-s1-prompt-q4` (`split`, `len`) ; c30 `td2-s1-prompt-q7` (limites linguistiques du découpage) |
| G | TD2 c22 `td2-s1-prompt-q5` (`join`, séparateur) ; c24 `s1-editorial-td2-enonce-q5` (découpage/reconstruction) |
| H | TD3 c6 `td3-s1-prompt-section-04` (collections) ; c7 `tal-s1-td3-appui-q1` (`append`, `pop`) ; c12 `tal-s1-td3-appui-q2` (tuple) |
| I | TD3 c17 `tal-s1-td3-appui-q3` (clés/valeurs, ajout) ; c23 `tal-s1-td3-appui-q4` (`for`, `items`, déballage, liste vide, `append`) |
| J | TD3 c28 `tal-s1-td3-appui-q5` (occurrences/formes distinctes) ; c33 `tal-s1-td3-appui-q6` (intersection/différence) |
| K | TD4 c7 `tal-s1-td4-appui-q1` (parcours et construction de liste) ; c12 `tal-s1-td4-appui-q2` (filtre et seuil) ; c37 `tal-s1-td4-appui-q7` (compréhension) |
| L | TD4 c22 `tal-s1-td4-appui-q4` (`range`, bornes et pas) ; c27 `tal-s1-td4-appui-q5` (`while`, état, condition, traitement, mise à jour) |
| M | TD4 c32 `tal-s1-td4-appui-q6` (fréquences par `get` ou `if/else`) ; c35 `td4-s1-prompt-q6` (activité de comptage) |
| N | TD5 c7 `tal-s1-td5-fonction-notions` (`def`, paramètres, appel, `return`, variables locales, distinction affichage/retour) |
| O | TD5 c13 `tal-s1-td5-normalisation-notions` (espaces et casse) ; c19 `tal-s1-td5-composition-notions` (composition, `split` sur chaîne vide) |
| P | TD5 c25 `tal-s1-td5-recherche-notions` (normalisation avant clé, dictionnaire reçu en paramètre) ; c28 `td5-s1-prompt-q4` (cas connu/inconnu) |
| R | TD5 c31 `tal-s1-td5-recomposition-notions` (liste traduite, `join`, cas vide) ; c34 `td5-s1-prompt-q5` (activité de traduction par lexique) |
| S | TD5 c37 `tal-s1-td5-resume-notions` (résultats nommés calculés depuis le paramètre) ; c40 `td5-s1-prompt-q6` (composition d’un résumé) |

## Matrice source → cible des 18 questions

Chaque ligne est obligatoire et **CONSERVÉE**. L’énoncé `dm-s1-enonce-qN` et la réponse `dm-s1-reponse-qN` restent au même rang dans la copie. Les données, productions et charges sont exactement celles du DM source : cette table décrit ce que le tuteur fait réviser, jamais les réponses. L’autonomie de résolution est conservée ; le nouvel accompagnement porte sur les acquis nécessaires.

| Question source → cible | Notions à réviser activement, une par une | Références TD | Prérequis à introduire ou limite particulière |
|---|---|---|---|
| Q1 — Calculer un budget → même Q1 | Conversion chaîne→entier ; distinction valeur/type ; affectation ; multiplication et addition ; rôle des données ; division comme rapport ; moyenne ; affichage de valeurs et test de type. | A B | Division réelle `/` à introduire explicitement : TD1 enseigne addition/multiplication et conversion, pas ce rapport. |
| Q2 — Lire deux expressions → même Q2 | Soustraction ; division ; priorité entre opérations ; effet des parenthèses ; ordre d’évaluation ; confrontation calcul/interprétation ; explication personnelle reliée aux observations. | A | Division et priorités arithmétiques, non explicitées dans les cours TD1–TD5 ; ne pas présumer l’acquis scolaire suffisant. |
| Q3 — Tester une inscription → même Q3 | Appartenance à un tuple ; comparaison stricte au seuil ; booléens ; conjonction ; construction d’une f-string à partir de variables ; format et ponctuation. | C H | Aucun nouvel outil. |
| Q4 — Transformer sans effacer → même Q4 | Chaîne immuable ; résultat d’une méthode et affectation ; `strip`, `lower`, `replace` ; effet de l’ordre sur la casse ; conservation de la source ; vérification des états intermédiaires. | D | Aucun nouvel outil. |
| Q5 — Extraire une référence → même Q5 | Séquence de caractères ; premier indice ; indices négatifs ; tranches ; borne finale exclue ; conserver le type chaîne ; dériver les fragments de la donnée. | E | Aucun nouvel outil. |
| Q6 — Interpréter un découpage → même Q6 | `split` sans argument ; espaces blancs ; liste de chaînes ; longueur d’une liste ; accès par indice ; ponctuation et apostrophe ; différence fragment/mot ; explication fondée sur les observations. | E F | Aucun nouvel outil ; pas d’autre tokeniseur. |
| Q7 — Reconstruire une annonce → même Q7 | Liste de chaînes ; `join` et séparateur ; `split` avec séparateur explicite ; exactitude des espaces ; comparaison de listes ; généralisation à une autre longueur de liste. | G | Aucun nouvel outil. |
| Q8 — Modifier un programme et fixer une référence → même Q8 | Mutabilité de liste ; retrait/ajout et observation des états ; tuple ordonné ; type ; distinction opération exécutée et liste finale recopiée. | H | Aucun nouvel outil. |
| Q9 — Construire un lexique → même Q9 | Clé/valeur ; construction/ajout/accès ; ordre d’insertion ; `items` ; déballage ; `for` et indentation ; liste initialisée avant parcours ; `append` ; f-string ; sortie issue des données. | I C | Garantie d’ordre d’insertion des dictionnaires à introduire : le TD3 montre le parcours mais ne formule pas cette garantie. |
| Q10 — Comparer deux ateliers → même Q10 | Liste avec répétitions ; ensemble de formes distinctes ; `len` selon la collection ; intersection ; différence orientée ; absence d’ordre imposé aux ensembles. | H J | Aucun nouvel outil ; pas de tri imposé. |
| Q11 — Filtrer puis mesurer → même Q11 | Boucle `for` ; indentation ; résultat accumulé dans une liste ; transformations de chaîne ; conservation de la source et de l’ordre ; longueur ; seuil inclus ; condition ; compréhension. | D K | Aucun nouvel outil. |
| Q12 — Produire deux séries bornées → même Q12 | `range` : départ, borne exclue, pas ; `for` ; liste et ajout ; `while` ; état initial, condition, mise à jour ; compteur de tours distinct de la valeur ; accumulation ; borne et arrêt ; explication d’un tour observé. | A H L | La combinaison série/compteur/total est une application autonome, pas une recette à transmettre. `sum` reste exclu. |
| Q13 — Compter des demandes → même Q13 | Parcours ; clés et occurrences ; initialisation d’un effectif ; `get` ou condition ; `items` et déballage ; seuil ; ordre de première insertion ; liste de sélection ; accumulation des effectifs ; vérification par comparaison de longueurs. | I M | Garantie d’ordre d’insertion à introduire ou réactiver comme en Q9, sans présumer la Q9 faite. `sum` reste exclu. |
| Q14 — Suivre une recherche bornée → même Q14 | Lecture sûre d’une liste ; compteur ; borne ; `while` ; conditions multiples ; booléen ; comparaisons ; diagnostics textuels ; liste accumulée ; mise à jour ; motifs d’arrêt ; cas vide, liste courte et limite ; retour autonome sur les essais. | C E H L N | Composition de contraintes d’arrêt et sécurité d’un accès indexé à expliciter conceptuellement. Ne pas donner la condition ou l’algorithme complet. Fonction auxiliaire seulement si choisie : réviser alors définition, paramètres, appel et retour. |
| Q15 — Normaliser une notice → même Q15 | Définition ; paramètres/arguments ; appel ; portée locale ; `return` contre `print` ; `strip`/`lower` ; conservation des espaces intérieurs, accents et ponctuation ; chaîne vide ; essais distincts. | D N O | Aucun nouvel outil. |
| Q16 — Compter une collection → même Q16 | Définition/paramètre/appel/retour/localité ; entrée non modifiée ; état local recréé à chaque appel ; parcours ; dictionnaire ; initialisation/incrément d’effectifs ; `get` ou condition ; casse ; liste vide. | M N | Aucun nouvel outil ; pas de normalisation implicite. |
| Q17 — Traduire avec une ressource fournie → même Q17 | Définition, paramètres, localité et retour ; composition ; normalisation ; recherche par clé ; cas inconnu ; lexique fourni comme paramètre ; parcours de fragments ; liste et assemblage ; cas vide ; limites lexicales et linguistiques de cette traduction. | D F I N O P R | Réviser également les notions de la fonction appelée, sans résoudre Q15. Aucun autre lexique, modèle ou bibliothèque. |
| Q18 — Composer une synthèse → même Q18 | Définition/paramètre/localité/retour ; composition ; normalisation ; caractères contre fragments et formes ; `split` et `len` ; fréquences ; nombre de clés/formes distinctes ; dictionnaire de résultats nommés ; ponctuation ; cas vide. | D F J M N O S | Réviser les notions des fonctions réutilisées, sans résoudre Q15/Q16 ni fournir l’enchaînement complet. Aucun ajout de bibliothèque. |

Les groupes de notions décrivent une couverture, pas une séquence d’instructions de solution. En particulier Q12–Q14 ne doivent pas recevoir la boucle, sa condition complète ou les mises à jour ordonnées. Q17 et Q18 doivent réviser les compétences transitivement mobilisées par les fonctions appelées sans résoudre une autre Q à la place de l’étudiant.

### Prérequis dont la présence dans les TD n’est pas démontrée

La division réelle, les priorités entre multiplication/division et addition/soustraction, ainsi que l’effet des parenthèses ne sont pas enseignés explicitement dans les cellules TD1 à TD5 comparées. Ils sont nécessaires en Q1/Q2 : le nouveau tuteur peut les introduire avec une situation distincte et vérifier la compréhension sans calculer les expressions du devoir.

Le parcours par `items()` est enseigné au TD3 ; la garantie d’ordre d’insertion ne l’est pas explicitement. Elle est nécessaire aux Q9 et Q13, donc révisée/introduite séparément pour chacune, même si l’étudiant n’a pas fait l’autre Q. La combinaison de plusieurs motifs d’arrêt et la protection d’un accès indexé sont une application plus exigeante que le simple `while` du TD4 : Q14 doit les diagnostiquer et les expliquer conceptuellement sans livrer la recherche bornée. Ces compléments sont autorisés par la demande actuelle ; ils ne réécrivent pas rétrospectivement les acquis du contrôle original.

## Listes fermées proposées pour `available_concepts`

Toutes les `allowed_libraries` et `provided_libraries` sont vides. `introduced_here` signale au moins la division en Q1, division/priorités/parenthèses en Q2, ordre d’insertion en Q9 et Q13, et sécurité de l’accès indexé/conditions multiples en Q14. Les autres notions sont à réactiver, sans présumer leur maîtrise. Les formulations exactes de `introduced_here` appartiennent à la liste correspondante.

```json
{
  "Q1": [
    "int()",
    "type()",
    "+",
    "*",
    "/",
    "affectation",
    "montant et moyenne",
    "liste",
    "print()"
  ],
  "Q2": [
    "-",
    "/",
    "priorités",
    "parenthèses",
    "ordre de calcul",
    "interprétation",
    "print()"
  ],
  "Q3": [
    "tuple",
    "in",
    ">",
    "and",
    "booléen",
    "f-string",
    "liste",
    "print()"
  ],
  "Q4": [
    "chaîne immuable",
    "affectation",
    "strip()",
    "lower()",
    "replace()",
    "source conservée",
    "liste",
    "print()"
  ],
  "Q5": [
    "chaîne",
    "indices positifs et négatifs",
    "tranches",
    "borne exclue",
    "liste",
    "print()"
  ],
  "Q6": [
    "split()",
    "liste",
    "len()",
    "indices",
    "ponctuation et apostrophe",
    "fragment et mot",
    "print()"
  ],
  "Q7": [
    "liste de chaînes",
    "join()",
    "split(séparateur)",
    "séparateur exact",
    "==",
    "print()"
  ],
  "Q8": [
    "liste modifiable",
    "pop()",
    "append()",
    "tuple ordonné",
    "type()",
    "==",
    "print()"
  ],
  "Q9": [
    "dictionnaire",
    "clé/valeur",
    "ajout",
    "ordre insertion",
    "items()",
    "déballage",
    "for",
    "indentation",
    "liste",
    "append()",
    "f-string",
    "print()"
  ],
  "Q10": [
    "liste",
    "set()",
    "len()",
    "répétitions et formes",
    "intersection",
    "différence",
    "ordre ensemble libre",
    "print()"
  ],
  "Q11": [
    "for",
    "indentation",
    "liste",
    "append()",
    "strip()",
    "lower()",
    "len()",
    ">=",
    "if",
    "compréhension",
    "ordre et source",
    "print()"
  ],
  "Q12": [
    "range()",
    "for",
    "liste",
    "append()",
    "while",
    "condition",
    "compteur",
    "mise à jour",
    "accumulation",
    "bornes",
    "print()",
    "+",
    "*"
  ],
  "Q13": [
    "dictionnaire",
    "for",
    "in",
    "if/else",
    "get()",
    "items()",
    "ordre insertion",
    "liste",
    "append()",
    ">=",
    "accumulation",
    "len()",
    "==",
    "print()"
  ],
  "Q14": [
    "while",
    "conditions multiples",
    "booléen",
    "comparaisons",
    "liste",
    "len()",
    "indice sûr",
    "borne",
    "compteur",
    "append()",
    "arrêt",
    "essais limites",
    "def/paramètre/appel/return/localité optionnels",
    "print()",
    "-",
    "and",
    "if/else"
  ],
  "Q15": [
    "def",
    "paramètre",
    "appel",
    "return",
    "localité",
    "strip()",
    "lower()",
    "chaîne vide",
    "print()",
    "espaces internes, accents, ponctuation"
  ],
  "Q16": [
    "def",
    "paramètre",
    "appel",
    "return",
    "localité",
    "for",
    "dictionnaire",
    "in",
    "if/else",
    "get()",
    "comptage",
    "casse",
    "liste vide",
    "source",
    "print()"
  ],
  "Q17": [
    "def",
    "paramètres",
    "appel",
    "return",
    "localité",
    "composition",
    "strip()",
    "lower()",
    "dictionnaire",
    "in",
    "if/else",
    "for",
    "liste",
    "append()",
    "split()",
    "join()",
    "cas inconnu et vide",
    "limites traduction",
    "print()"
  ],
  "Q18": [
    "def",
    "paramètre",
    "appel",
    "return",
    "localité",
    "composition",
    "strip()",
    "lower()",
    "split()",
    "len()",
    "dictionnaire",
    "clés",
    "comptage",
    "formes distinctes",
    "ponctuation et accents",
    "chaîne vide",
    "print()",
    "liste",
    "for",
    "in",
    "if/else",
    "get()",
    "accumulation"
  ]
}
```

Le contexte canonique a un budget interne de 4 400 caractères. Les listes peuvent être compactées par des renvois explicites et non ambigus à un lexique, à condition de conserver chaque permission par Q et les sous-notions ci-dessus. Il est interdit de tronquer le prompt, d’omettre une compétence ou d’unir les fiches pour respecter ce budget. Cible indicative : environ 2 300 caractères de notions et 1 700 caractères de consigne, puis mesure réelle de l’ensemble généré. Si nécessaire, préférer un vocabulaire conceptuel concis plutôt que des intitulés pédagogiques longs répétés.

## Critères d’acceptation et preuves

- Prévalidation indépendante de cette matrice avant création de la copie ; auteur TAL-Prof distinct du Designer et des reviewers.
- Comparaison avec le DM baseline : 45 cellules, types, identifiants, ordre, toutes les cellules de code et tous les énoncés identiques ; seules les différences autorisées de titre, conditions d’assistance, métadonnées de tutorat et contexte caché sont présentes.
- Original inchangé octet pour octet ; catalogue d’évaluation et tous les autres profils/contexte rendus inchangés. Le contrôle original continue à refuser toute aide.
- 18 fiches, une par question réelle, listes fermées cohérentes ; aucun import ; aucun résultat, jeu de réponses, copie du corrigé ou pseudocode caché dans le contexte.
- Nouveau profil `devoir_S1_tuteur`, mode `td`, semestre 1 ; copie cachée et copie Colab strictement identiques ; budget mesuré et régénération idempotente, sans réécrire les autres supports.
- Lecture indépendante pédagogique et éditoriale de l’introduction nouvelle et des 18 fiches ; parcours Étudiant-Modèle avec questions d’identification ambiguë, demandes de résolution directe, hésitation sur un prérequis, demande d’import et insistance. Vérifier le traitement de chaque notion, une seule question par tour et l’absence de solution.
- Vérifications techniques adaptées aux outils réellement modifiés, sans exécuter de code étudiant. Les preuves statiques ne démontrent pas à elles seules le comportement réel de Gemini dans Colab : une observation directe non réalisée reste déclarée.

Handoff attendu : liste de fichiers, preuve de copie non dégradante, manifeste, prompt spécifique, mesure du contexte, tests de génération et de conservation, verdicts pédagogique et éditorial distincts puis gouvernance et intégration. Cette mission ne valide pas les autres écarts du S1, ne fusionne pas de PR et n’autorise aucun déploiement de production.

Statut : **CADRAGE PRÉALABLE ACCEPTÉ**, le 15 octobre 2026, par TAL-Pedagogy-Reviewer (`/root/s1_pedagogy_review`), distinct du Prof et du Designer. Empreinte avant cette attribution : `b322b5916ade77cb835c8a7df9d9a99ff43369d4bc011196a2d8d4a33e2cbdf8`. Le reviewer a vérifié physiquement les 18 cartes et les références TD (cellules et identifiants), puis relu les compléments Q12/Q14/Q15/Q18 ; la cible était encore absente et le DM source inchangé au verdict. Aucune réserve de cadrage restante. Cette acceptation préalable ne vaut ni validation de la cible future ni conformité globale S1. Aucun notebook créé ou modifié par le Prof.
