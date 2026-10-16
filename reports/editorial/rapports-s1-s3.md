# Revue éditoriale indépendante — rapports S1 et S3

Date : 16 octobre 2026. Branche : `code/rapports-pedagogiques-s1-s3` ; base technique `c81c38641ecddb66c5ea65c78eafbd2d8d3cbbc5`.

## Mission et indépendance

La même session a d'abord tenu le rôle TAL-Prof pour rédiger le cadrage. Le rôle TAL-Editorial-Reviewer intervient ensuite sur les textes produits par les autres agents : `app/s1_feedback.py`, `app/s3_feedback.py`, `app/templates/corrector_template.html`, `app/templates/s3_review_evidence.html`, et les nouveaux diagnostics des moteurs. Le plan `docs/pedagogy/plan_restitution_etudiante_s1_s3.md` est expressément exclu du verdict : le réviseur ne valide pas son propre texte.

Les deux anciens rapports HTML fournis ont été lus intégralement. Les exemples et explications produits ont été relus question par question et confrontés aux énoncés actuels. Les prérequis sont examinés au regard des données, fonctions et bibliothèques déjà employées dans les questions ; l'installation d'un import ne suffit pas à justifier une nouvelle compétence. Aucun notebook source n'est modifié par cette revue. Celle-ci ne prétend pas relire ni valider de nouveau l'intégralité des cours historiques et tuteurs, inchangés dans la mission.

## Verdict

`ACCEPT` — `LISIBILITÉ_ÉTUDIANTE_VALIDÉE` pour les textes des rapports et les 116 exemples des 19 TD/révisions actifs S1/S3, après résolution et relecture des constats ci-dessous. Les exemples illustrent le traitement calculé ; ils ne promettent pas un corrigé intégral des interprétations et transferts personnels. Ce verdict ne porte pas sur le plan produit antérieurement par le réviseur et ne remplace ni la validation pédagogique, ni la validation technique, ni la décision de fusion.

## Constats et reprises demandées

| Identifiant | Gravité / emplacement | Difficulté pour l'étudiant | Ordre de reprise et critère vérifiable | État |
|---|---|---|---|---|
| TAL-EDIT-001 | Bloquant, guide `corrector_template.html` | « restent à discuter avec votre enseignant » suggère une discussion individuelle systématique ; politique du TD : autoévaluation avec sollicitation possible. | Adresser la consigne à l'étudiant : relire avec les critères du TD, solliciter l'enseignant si difficulté persistante. | Corrigé et relu. |
| TAL-EDIT-002 | Majeur, lignes informatives hors score | Une observation ℹ️ apparaît comme un critère défaillant, « À vérifier », avec 0/0. | Afficher « À autoévaluer » et « Non noté » pour ces lignes, sans changer le score. | Corrigé et relu. |
| TAL-EDIT-003 | Majeur, S1 TD5 Q1–Q6 et TD7 Q4–Q6 | Un exemple avec l'appel principal peut être pris pour un travail complet et faire oublier les essais du sujet. | Rappeler la portée de l'exemple, les cellules d'essai et les cas limites déjà demandés ; ne pas inventer de nouvelles obligations. | Corrigé et relu : rappel ajouté aux six exemples TD5 et aux trois exemples TD7 concernés. |
| TAL-EDIT-004 | Bloquant, S3 TD0 Q1/Q3/Q5/Q6 | Exemples initiaux substituant un raccourci à la méthode demandée : Path pour `with`, absence de boucle de comparaison, Counter au lieu des fonctions à construire. | Restaurer les méthodes du sujet et leur réemploi, conserver les observations/transferts en rappel. | Méthodes corrigées et relues. |
| TAL-EDIT-005 | Bloquant, S3 TD2 Q2/Q5/Q7 | Le programme exemple initial omettait fonctions, filtres ou signature ; le lecteur aurait comparé sa réponse à une méthode différente de la consigne. | Reprendre fonctions réutilisables, exclusions, filtre des mots vides et catégories attendues ; vérifier la cohérence du code et de l'explication. | Corrigé et relu : fonctions, signatures, filtres et cohérence de Q7 restaurés. |
| TAL-EDIT-006 | Majeur, S3 TD1.a Q4, TD2 Q1/Q6 | La figure demandée manquait ou les noms de bibliothèques apparaissaient sans contexte. | Fournir l'appel d'affichage et les imports utiles ; identifier les variables préparées dans le notebook. | Corrigé et relu : displaCy, imports Matplotlib/WordCloud et rappel général des cellules précédentes. |
| TAL-EDIT-007 | Majeur, S3 TD1.c Q2/Q3 | Texte d'essai initial sans organisation malgré la consigne personne/organisation/lieu ; similarité présentée sous un nom de pipeline différent de celui du sujet. | Fournir un exemple répondant aux trois types de mention et réemployer `nlp_sim` pour la similarité. | Corrigé et relu : Google ajouté, pipeline nlp_sim repris ; variantes et ambiguïté ajoutées en Q4. |
| TAL-EDIT-008 | Majeur, S3 TD1.a Q4, TD2 Q5/Q6, TD3 Q5 | Certaines chaînes sont des invitations à compléter, pas des interprétations achevées. Les appeler « résultat attendu » sans réserve ferait recopier une consigne comme réponse. | Distinguer le code du calcul et la production personnelle ; annoncer le caractère partiel de ces exemples et préciser ce que l'étudiant doit argumenter. | Distinction explicitement présente dans les explications ; code calculé et jugement personnel séparés. Pas de prétention à un corrigé linguistique complet. |
| TAL-EDIT-009 | Majeur, diagnostic S3 des champs manquants ; observation Q4 R0–R2 | Ancien et nouveau suffixes de rédaction étaient concaténés, sans espace ; ligne observation mêlait note explicative et code en réponse. | Une phrase utile unique et espacée pour le champ à compléter ; déplacer la portée hors de la réponse sans supprimer le code Q4 extrait. | Corrigé et relu dans `s3_audit.py` et `revision_s3.py`. |
| TAL-EDIT-010 | Bloquant, ordre des statuts dans le gabarit | L'ancien symbole ❌ pouvait prendre le pas sur l'état non vérifiable ou preuve manquante, donnant un libellé trompeur. | Faire prévaloir les états explicites sur les symboles historiques ; conserver les points. | Corrigé et relu : « Non vérifiable » ou « Résultat manquant ou inexploitable » sont prioritaires. |

## Lecture de la présentation commune

La présentation sépare désormais les questions, le code retrouvé et les sorties sauvegardées, le diagnostic et l'action utile, l'exemple de code avec explication, le statut textuel et les points. La colonne de réponse ne présente plus le diagnostic comme s'il venait du notebook dès lors que les champs d'extraction existent. La portée du score est hors du tableau. « Score formatif provisoire » n'est pas annoncé comme une validation finale du travail.

Les numéros de cellules donnent un repère dans la copie. L'extraction montre les commentaires préremplis tels qu'ils existent : le libellé « retrouvé » ne prétend pas identifier l'auteur de chaque ligne. Les sorties absentes sont nommées comme telles. Les productions complémentaires et figures sont consultables ou signalées, sans les transformer en correction linguistique. Dans la vue étudiante, l'annexe s'adresse à « votre notebook » ; les codes internes de cellule ne structurent plus sa consigne. Une figure sauvegardée est annoncée comme un affichage à ouvrir dans le notebook ; sa présence n'est pas une preuve de pertinence.

L'ouverture des exemples reste un choix de l'étudiant dans le TD. La formulation doit permettre une solution différente valide ; les phrases personnelles et jugements linguistiques restent explicitement des exemples ou des productions à adapter. Les instructions destinées aux agents ne sont pas introduites dans les commentaires du code exemple. Les limites sur l'exécution réelle et les sorties périmées sont présentées comme des actions utiles : réexécuter, enregistrer, soumettre de nouveau.

## Repères de contexte et prérequis

Les exemples s'essaient dans le notebook correspondant après sa préparation, pas dans un interpréteur vide. Le guide annonce explicitement cette dépendance. Les repères de cellules de l'inventaire ci-dessous concernent les sources `Notebooks TD/S1/` et `Notebooks TD/S3/`, retrouvables par le catalogue `app/notebook_catalog.json`.

| Groupe de questions | Contexte retenu dans la lecture | Distinction maintenue |
|---|---|---|
| S1 TD1 Q1–Q6 | Cours et exemples précédant chaque exercice ; variables Q1 reprises Q3 | Exemple calculé, phrase personnelle Q6 différente d'une réponse unique obligatoire |
| S1 TD2 Q1–Q7 | strip, lower, replace, indices et tranches, split/join introduits successivement ; liste à trois indices traitée explicitement | Pas de boucle introduite pour contourner le niveau Q6 ; commentaire Q7 proposé comme illustration |
| S1 TD3 Q1–Q6 | Liste, tuple, dictionnaire, items et ensembles du TD ; lexique Q3 repris Q4 | Ordre de liste conservé ; ordre d'ensemble libre ; justification de tuple à autoévaluer |
| S1 TD4 Q1–Q7 | for, if, range, while, compte et compréhension introduits avant leur exercice ; liste mots Q1 reprise | Méthode demandée montrée, pas seulement la valeur de sortie |
| S1 TD5 Q1–Q6 | Fonctions/return du TD ; normaliser Q2, nombre_mots Q3 et traduire_mot Q4 réemployées | Appel principal illustré ; autres essais du sujet toujours à réaliser |
| S1 TD6 Q1–Q6 | Préparation du fichier, lecture UTF-8, lignes Q2, enregistrements Q3, normalisation Q4, regroupement Q5 | CSV fourni comme texte enregistré, sans exécuter un fichier de copie sur le serveur |
| S1 TD7 Q1–Q7 | re et motifs successifs ; nettoyer_texte Q5 repris Q6 | Règles de forme distinctes d'une analyse linguistique ou d'une validité calendaire |
| S3 TD0 Q1–Q7 | Fichiers préparés, with/open, listes et dictionnaires S1 ; fonctions construites Q5 puis Q6 | Le résultat fixe du microcas ne remplace pas les transferts Faguet et synthèses |
| S3 R0 Q1–Q4 | Fonctions Python et split ; frequences Q3 réemployée Q4 | Compter une clé ponctuée ne prouve pas une analyse linguistique |
| S3 R1 Q1–Q4 | nlp/doc puis attributs text/lemma_/pos_ ; doc Q1 réemployé | Liste de verbes vide autorisée si prédiction du modèle ; bonus non rendu obligatoire |
| S3 R2 Q1–Q4 | Counter et Doc cadrés dans la révision ; fonction réservant stopwords puis révisée Q3 | Aucune exclusion en Q1 ; filtre spaCy et exclusion personnelle distincts en Q3/Q4 |
| S3 TD1.a Q1–Q6 | nlp/doc préparés ; attributs et displaCy introduits dans le TD ; texte_td0 Q5 | Modèle, jugement du lecteur et trace du code restent distincts ; extrait libre Q6 |
| S3 TD1.c Q1–Q4 | Pipelines entités et similarité préparés sous noms distincts ; entity_ruler et labels du TD | Interprétation des entités/scores ouverte ; règles exactes distinguées de leur justesse contextuelle |
| S3 TD2 Q1–Q7 | doc_corpus Q1, fonctions et exclusions Q2/Q3, figures prévues dans le TD, généralisation Q7 | Fonction sur son argument ; filtres identiques ; interprétation manuelle non automatisée |
| S3 TD3 Q1–Q7 | Corpus original et notice préparés ; concordances Q2, spaCy connu ; PhraseMatcher introduit dans le sujet | Original et normalisation séparés ; identité exacte distincte de proximité et fidélité du sens |
| S3 TD4 Q1–Q7 | Fonctions successives marge/cooccurrence/union/fenêtre ; mesures composées Q7 | Unités et frontières distinguées ; transfert et commentaires rappelés |
| S3 TD5 Q1–Q7 | Mesures TD4 ; proportions, dénominateurs, taux et couverture du TD | Absence de dénominateur distincte de zéro ; aucun test statistique ou logarithme imposé |
| S3 TD6 Q1–Q7 | Positions et fenêtre TD4/TD5 ; segmentation/taux Q2/Q3 ; Matplotlib du parcours | Microcas illustré ; matrices, passages et relecture humaine restent requis par le sujet |
| S3 TD7 Q1–Q7 | Réemploi TD3–TD6 ; moteur d'expressions et garde de protocole détaillés | Cas nouveau sans ajuster le moteur ; absence de protocole distincte de réfutation numérique |

## Preuve de lecture par question

L'inventaire ci-dessous indique les cellules de réponse des sujets de référence, les notions/dépendances que le lecteur doit retrouver et le contenu des exemples inspectés. Les cellules sont numérotées à partir de 1 dans le fichier. Tous les exemples sont des éléments de restitution après soumission ; ils ne sont pas ajoutés aux cellules d'exercice et ne changent pas le statut autonome ou facultatif de ces activités.



### S1

| Sujet / question | Cellule réponse | Exemple et explication inspectés |
|---|---|---|
| `td1-s1` Q1 | 11, `td1-s1-answer-q1` | `prix_par_mot = 0.12` — Multipliez le prix unitaire par le nombre de mots : le coût est 15 euros. |
| `td1-s1` Q2 | 16, `td1-s1-answer-q2` | `# Prédiction : un nombre décimal a ici le type float.` — type(note) affiche le type de la valeur, ici float. |
| `td1-s1` Q3 | 21, `td1-s1-answer-q3` | `meme_nombre = nb_mots == 125` — Réutilisez les données de Q1. == compare deux valeurs ; and exige que les deux conditions soient vraies. Les deux réponses valent ici True. |
| `td1-s1` Q4 | 26, `td1-s1-answer-q4` | `langue_source = "français"` — Les accolades insèrent les deux variables. Conservez les espaces, l’apostrophe et le point final de la phrase demandée. |
| `td1-s1` Q5 | 31, `td1-s1-answer-q5` | `volume_saisi = "80"` — Convertissez la chaîne en entier avant l’addition : le résultat est 100, de type int. |
| `td1-s1` Q6 | 36, `td1-s1-answer-q6` | `phrase = "Le TAL aide."` — Cet exemple utilise une phrase possible ; gardez votre propre choix. len compte tous les caractères, et in distingue les majuscules des minuscules. repr rend la donnée choisie visible. |
| `td2-s1` Q1 | 9, `td2-s1-answer-q1` | `texte_brut = "   Le TAL transforme des textes.   "` — Les longueurs sont 35 puis 29. strip produit une nouvelle chaîne : texte_brut reste disponible. |
| `td2-s1` Q2 | 13, `td2-s1-answer-q2` | `texte_minuscule = texte_propre.lower()` — Après Q1, mettez en minuscules puis remplacez textes par corpus. Les recherches donnent True puis False. Ici, textes est déjà en minuscules : inverser ces deux opérations donnerait le même résultat. |
| `td2-s1` Q3 | 17, `td2-s1-answer-q3` | `mot = "tokenisation"` — La borne de fin est exclue : [0:4] donne toke et [1:5] donne oken. Ces tranches ne changent pas les 12 caractères de mot. |
| `td2-s1` Q4 | 21, `td2-s1-answer-q4` | `phrase = "La traduction automatique aide parfois"` — La liste compte cinq éléments. tokens[2] est le troisième élément, automatique ; phrase[2] serait un caractère de la chaîne. |
| `td2-s1` Q5 | 25, `td2-s1-answer-q5` | `phrase_avec_barres = " / ".join(tokens)` — Réutilisez tokens de Q4. Le séparateur exact, espaces compris, permet de retrouver la même liste ; la comparaison vaut True. |
| `td2-s1` Q6 | 29, `td2-s1-answer-q6` | `exemples = ["  Bonjour  ", "TAL", "  Corpus Français"]` — Traitez les trois chaînes séparément avec les notions de ce TD. Les accents et les espaces intérieurs sont conservés ; la liste exemples n’est pas modifiée. |
| `td2-s1` Q7 | 31, `td2-s1-answer-q7` | `phrase_limite = "L’analyse, c’est utile !"` — Voici une interprétation possible. Reliez votre propre commentaire aux fragments observés : split sépare selon les espaces, pas selon une analyse linguistique. La présence d’un commentaire ne valide pas son contenu. |
| `td3-s1` Q1 | 11, `td3-s1-answer-q1` | `outils = ["corpus", "lexique", "concordancier"]` — Placez le premier affichage après append et avant pop : il montre quatre éléments. Après le retrait du dernier, la liste retrouve ses trois éléments initiaux. |
| `td3-s1` Q2 | 16, `td3-s1-answer-q2` | `langues_romanes = ("français", "italien", "espagnol")` — Le tuple conserve l’ordre et ne permet pas de remplacer ses éléments. Adaptez la justification à votre compréhension ; sa présence ne suffit pas à valider son sens. |
| `td3-s1` Q3 | 22, `td3-s1-answer-q3` | `lexique = {"book": "livre", "language": "langage", "data": "données"}` — Ajoutez corpus par sa clé puis consultez language. La traduction langue est également admise ; réutilisez votre choix en Q4. |
| `td3-s1` Q4 | 27, `td3-s1-answer-q4` | `entrees_lexique = []` — Après Q3, items fournit chaque paire clé-valeur. La liste doit conserver les quatre correspondances ; l’ordre des entrées est libre. |
| `td3-s1` Q5 | 32, `td3-s1-answer-q5` | `formes = ["texte", "corpus", "texte", "donnée", "corpus", "analyse"]` — La liste compte six occurrences et l’ensemble quatre formes distinctes. L’ordre d’affichage d’un ensemble n’est pas un critère de réussite. |
| `td3-s1` Q6 | 37, `td3-s1-answer-q6` | `corpus_a = ["texte", "analyse", "langue", "corpus"]` — L’intersection contient langue et corpus ; la différence de a avec b contient texte et analyse. La différence dépend du sens de la comparaison. |
| `td4-s1` Q1 | 11, `td4-s1-answer-q1` | `mots = ["TAL", "corpus", "analyse", "IA"]` — Parcourez les mots et ajoutez chaque transformation à la nouvelle liste, dans le même ordre. |
| `td4-s1` Q2 | 16, `td4-s1-answer-q2` | `mots_longs = []` — Réutilisez mots de Q1. Le test strictement supérieur à 5 conserve corpus et analyse. |
| `td4-s1` Q3 | 21, `td4-s1-answer-q3` | `mots_avec_a = []` — Réutilisez mots de Q1. Testez une version en minuscules, puis conservez la forme initiale : TAL, analyse et IA. |
| `td4-s1` Q4 | 26, `td4-s1-answer-q4` | `positions_paires = list(range(0, 11, 2))` — range exclut sa borne de fin. Avec 11 et un pas de 2, les positions vont de 0 à 10 inclus. |
| `td4-s1` Q5 | 31, `td4-s1-answer-q5` | `multiples = []` — Ajoutez le multiple avant de l’augmenter. L’incrément garantit que la boucle finit ; <= inclut 70. |
| `td4-s1` Q6 | 36, `td4-s1-answer-q6` | `mots_a_compter = "le TAL traite le langage et le texte".lower().split()` — Une première occurrence crée une entrée ; les suivantes augmentent son compteur. le apparaît trois fois ; chaque autre forme apparaît une fois. |
| `td4-s1` Q7 | 41, `td4-s1-answer-q7` | `longueurs_mots_longs = [len(mot) for mot in mots if len(mot) > 5]` — Réutilisez mots de Q1. La compréhension filtre les mots puis conserve leur longueur : 6 et 7. |
| `td5-s1` Q1 | 11, `td5-s1-answer-q1` | `def longueur_texte(texte):` — return fournit le résultat à l’appelant. La même fonction donne 3 puis 6 selon l’argument reçu. L’exemple illustre l’appel principal. Réalisez aussi les cas d’essai prévus dans le TD, notamment les entrées vides, les espaces ou les mots inconnus lorsque l’exercice les demande. |
| `td5-s1` Q2 | 17, `td5-s1-answer-q2` | `def normaliser(texte):` — strip retire les espaces de bord ; lower convertit les lettres en minuscules. Retournez la chaîne obtenue. L’exemple illustre l’appel principal. Réalisez aussi les cas d’essai prévus dans le TD, notamment les entrées vides, les espaces ou les mots inconnus lorsque l’exercice les demande. |
| `td5-s1` Q3 | 23, `td5-s1-answer-q3` | `def nombre_mots(texte):` — Après Q2, composez les traitements : normalisation, découpage, puis comptage des cinq éléments. L’exemple illustre l’appel principal. Réalisez aussi les cas d’essai prévus dans le TD, notamment les entrées vides, les espaces ou les mots inconnus lorsque l’exercice les demande. |
| `td5-s1` Q4 | 29, `td5-s1-answer-q4` | `lexique = {"language": "langage", "data": "données", "book": "livre"}` — Après Q2, normalisez la clé avant la recherche. get conserve le mot normalisé lorsqu’il est absent : Unknown devient unknown. L’exemple illustre l’appel principal. Réalisez aussi les cas d’essai prévus dans le TD, notamment les entrées vides, les espaces ou les mots inconnus lorsque l’exercice les demande. |
| `td5-s1` Q5 | 35, `td5-s1-answer-q5` | `def traduire_phrase(phrase, lexique):` — Réutilisez traduire_mot et lexique de Q4 pour chaque mot, puis assemblez les traductions avec un espace. L’exemple illustre l’appel principal. Réalisez aussi les cas d’essai prévus dans le TD, notamment les entrées vides, les espaces ou les mots inconnus lorsque l’exercice les demande. |
| `td5-s1` Q6 | 41, `td5-s1-answer-q6` | `def resume_texte(texte):` — Réutilisez les fonctions de Q2 et Q3. Le résumé contient le texte normalisé, ses 13 caractères et ses 3 mots. L’exemple illustre l’appel principal. Réalisez aussi les cas d’essai prévus dans le TD, notamment les entrées vides, les espaces ou les mots inconnus lorsque l’exercice les demande. |
| `td6-s1` Q1 | 12, `td6-s1-answer-q1` | `with open("affiliations_s1.txt", encoding="utf-8") as fichier:` — Exécutez d’abord la préparation du fichier fournie dans le TD. with ferme le fichier après lecture ; le texte fourni contient 156 caractères. |
| `td6-s1` Q2 | 17, `td6-s1-answer-q2` | `lignes = []` — Après Q1, splitlines sépare les lignes. Le test ligne.strip() écarte les lignes vides ou composées seulement d’espaces. Les cinq lignes de données sont conservées. |
| `td6-s1` Q3 | 22, `td6-s1-answer-q3` | `enregistrements = []` — Après Q2, séparez chaque ligne une seule fois au point-virgule. Gardez les cinq couples personne-affiliation dans l’ordre du fichier. |
| `td6-s1` Q4 | 27, `td6-s1-answer-q4` | `def normaliser_personne(identite):` — split puis join ramènent les espaces à un seul ; title harmonise ici la casse. Les quatre essais donnent Durand Alice. Cette règle simple n’est pas une règle générale pour tous les noms. |
| `td6-s1` Q5 | 33, `td6-s1-answer-q5` | `affiliations_par_personne = {}` — Après Q3 et Q4, normalisez avant de regrouper. Chaque ensemble élimine les affiliations répétées : Durand Alice en a deux et Martin Bob une. |
| `td6-s1` Q6 | 39, `td6-s1-answer-q6` | `import csv` — Après Q5, écrivez l’en-tête et une ligne par personne. La virgule sépare les colonnes ; / sépare les affiliations à l’intérieur d’une colonne. L’ordre des personnes et des affiliations est libre. |
| `td7-s1` Q1 | 13, `td7-s1-answer-q1` | `import re` — search cherche dans tout le texte. IGNORECASE permet de trouver tal malgré la différence de casse ; bool donne True. |
| `td7-s1` Q2 | 18, `td7-s1-answer-q2` | `texte_nombres = "Version 2 : 14 corpus, 3 langues et 250 phrases."` — Après l’import de re, + regroupe les chiffres consécutifs. findall conserve l’ordre et renvoie des chaînes : 2, 14, 3 et 250. |
| `td7-s1` Q3 | 23, `td7-s1-answer-q3` | `texte_mots = "L’analyse, c’est déjà 2 étapes !"` — Après l’import de re, la classe étendue conserve les lettres accentuées. Apostrophes, chiffres et ponctuation séparent les fragments. Comparez une différence observée dans votre propre commentaire. |
| `td7-s1` Q4 | 28, `td7-s1-answer-q4` | `journal = "Le 03/09/2026, Alice a relu 12 segments."` — Après l’import de re, les quantités exactes reconnaissent la forme JJ/MM/AAAA. Le nombre 12 reste présent. Reconnaître cette forme ne vérifie pas la validité d’une date dans le calendrier. Cet appel ne remplace pas les autres essais et les commentaires demandés dans le TD. |
| `td7-s1` Q5 | 34, `td7-s1-answer-q5` | `def nettoyer_texte(texte):` — Après l’import de re, respectez l’ordre : minuscules, dates, chiffres, espaces. Le marqueur ajouté après lower reste en majuscules ; le point final reste présent. Cet appel ne remplace pas les autres essais et les commentaires demandés dans le TD. |
| `td7-s1` Q6 | 40, `td7-s1-answer-q6` | `def analyser_texte(texte):` — Réutilisez nettoyer_texte de Q5 et l’import de re. Comptez les fragments extraits : le et tal apparaissent deux fois. Sur un autre texte contenant une date, le motif extrairait aussi DATE du marqueur. Cet appel ne remplace pas les autres essais et les commentaires demandés dans le TD. |
| `td7-s1` Q7 | 46, `td7-s1-answer-q7` | `limite_regex = "Dans il est avocat et un avocat mûr, la même forme désigne un métier ou un fruit ; le contexte et une analyse sémantique aideraient à choisir le sens."` — Voici un exemple possible : un cas concret, une ambiguïté que la seule forme ne résout pas et une information linguistique utile. Le correcteur constate seulement la présence d’une réponse ; relisez vous-même son argumentation. |

### S3

| Sujet / question | Cellule réponse | Exemple et explication inspectés |
|---|---|---|
| `td0-s3` Q1 | 9, `e8a48edb5ed9` | `with open("corpus_td0.txt", encoding="utf-8") as fichier:` — Lisez le fichier en UTF-8 avant de compter ses caractères, y compris espaces et retours à la ligne. |
| `td0-s3` Q2 | 12, `57598382bdb7` | `mots_bruts = texte.split()` — split() découpe sur les espaces et conserve la ponctuation attachée aux mots. Cette liste est un découpage brut. |
| `td0-s3` Q3 | 14, `0f76c3c59928` | `compteur = 0` — Comptez les éléments de la liste ; un mot répété contribue à chaque occurrence. |
| `td0-s3` Q4 | 17, `e9b18e8b65f8` | `formes_distinctes = set(mots_bruts)` — Un ensemble ne conserve chaque chaîne qu’une fois. La casse et la ponctuation distinguent encore les formes. |
| `td0-s3` Q5 | 22, `741502c4fe30` | `def frequences_brutes(liste_mots):` — La fonction incrémente le dictionnaire pour chaque forme exacte ; la somme des effectifs retrouve le nombre d’occurrences. |
| `td0-s3` Q6 | 24, `3f10c1bdf6b3` | `def frequences_minuscules(texte):` — Passez en minuscules avant le découpage. Cette transformation ne retire pas la ponctuation et ne lemmatise pas. |
| `td0-s3` Q7 | 26, `754a2ce1198c` | `microcas = "L’analyse, c’est utile !"` — Observez les éléments exacts de la liste. Votre synthèse doit expliquer les limites de split(), pas seulement annoncer que le résultat est correct. Sa qualité se vérifie avec les critères du sujet, sans point automatique. |
| `td-r0-s3` Q1 | 8, `r0-q1-reponse` | `def compter_mots(texte):` — La fonction reçoit le texte en paramètre et renvoie le nombre d’éléments issus de split(). Testez aussi le cas vide. |
| `td-r0-s3` Q2 | 10, `r0-q2-reponse` | `mots_normalises = texte.lower().split()` — La minuscule précède le découpage ; la ponctuation reste attachée aux chaînes. |
| `td-r0-s3` Q3 | 14, `r0-q3-reponse` | `def frequences(texte):` — get(mot, 0) initialise le premier compte ; chaque répétition ajoute une unité. Comparez le test au calcul manuel. |
| `td-r0-s3` Q4 | 16, `r0-q4-reponse` | `bilan_limite = {"comptes": frequences("Python Python."),` — Réutilisez la fonction de Q3. La différence entre les deux clés fournit un exemple concret de la limite observée. |
| `td1-s3` Q1 | 18, `f0868b90c1ec` | `annotations = []` — Parcourez doc dans l’ordre. Les bornes doivent restituer exactement chaque forme dans texte ; les étiquettes sont les prédictions du modèle chargé. |
| `td1-s3` Q2 | 22, `6f8e948b3277` | `phrases = []` — Chaque phrase conserve son texte et son nombre de tokens, ponctuation comprise. Comparez avec votre segmentation manuelle. |
| `td1-s3` Q3 | 26, `0d6d764a0ba2` | `noms, verbes, mots_pleins = [], [], []` — Filtrez les tokens puis prélevez leurs lemmes. Conservez l’ordre et les répétitions ; la liste des mots pleins applique aussi le filtre des mots vides. |
| `td1-s3` Q4 | 30, `6026f523bc1f` | `from spacy import displacy` — Exemple de repérage d’un verbe et de l’un de ses dépendants dans la première phrase. Précisez votre interprétation en nommant les deux tokens et en discutant la relation observée ; la syntaxe seule ne résout pas la question du locuteur. |
| `td1-s3` Q5 | 34, `951832c4e554` | `doc_td0 = nlp(texte_td0)` — Appliquez les trois règles au même texte. Gardez les tokens d’espacement hors du troisième compte ; dans votre commentaire, expliquez deux écarts précis avec les unités réellement obtenues. |
| `td1-s3` Q6 | 36, `4b47b9af0c87` | `extrait = "Les étudiantes analysent des corpus français. Elles comparent ensuite les résultats et rédigent une interprétation."` — Exemple sur deux phrases du sujet. Pour votre transfert, choisissez votre propre extrait de deux à quatre phrases, contrôlez ses cinq premières annotations et formulez une question qui lui convient. |
| `td-r1-s3` Q1 | 11, `r1-q1-reponse` | `doc = nlp(texte)` — nlp transforme la chaîne en Doc ; len(doc) compte ses tokens, ponctuation comprise. |
| `td-r1-s3` Q2 | 17, `r1-q2-reponse` | `annotations = []` — Chaque tuple associe forme, lemme et catégorie d’un même token. Inspectez les prédictions avant de formuler votre observation. |
| `td-r1-s3` Q3 | 21, `r1-q3-reponse` | `noms = []` — Sélectionnez les tokens de catégorie NOUN puis ajoutez leur lemme ; ne filtrez pas une liste de chaînes privées de leurs attributs. |
| `td-r1-s3` Q4 | 23, `r1-q4-reponse` | `verbes = []` — Conservez les catégories effectivement prédites. Si la liste est vide, revenez aux annotations de Q2 et discutez les erreurs possibles du modèle. |
| `td-r2-s3` Q1 | 11, `r2-q1-reponse` | `from collections import Counter` — La fonction calcule les effectifs des lemmes nominaux. À ce stade, stopwords est prévu dans la signature mais le filtrage sera ajouté en Q3. |
| `td-r2-s3` Q2 | 15, `r2-q2-reponse` | `doc = nlp(texte)` — Ce tableau expose les prédictions qui ont déterminé les fréquences. Une étiquette inattendue appelle une vérification dans le contexte. |
| `td-r2-s3` Q3 | 21, `r2-q3-reponse` | `def frequences_lemmas(texte, stopwords=None):` — Distinguez mots vides du modèle et exclusions supplémentaires. Comparez avant/après avec le même texte ; les lemmes conservés gardent leurs effectifs. |
| `td-r2-s3` Q4 | 25, `r2-q4-reponse` | `classements = {"avant": frequences_lemmas(texte).most_common(),` — Réutilisez la fonction révisée. Comparez les rangs et les effectifs ; le tri seul ne démontre pas la pertinence linguistique du classement. |
| `td2-s3` Q1 | 11, `418a064ebdbf` | `with open("corpus_td2.txt", encoding="utf-8") as fichier:` — Lisez le fichier puis annotez son contenu. Conservez les dix premières annotations hors ponctuation et espaces ; le compte total inclut tous les tokens. |
| `td2-s3` Q2 | 16, `67c5c98fd3c1` | `from collections import Counter` — Comptez les lemmes après sélection de la catégorie. Ne comptez pas seulement les formes différentes : les répétitions augmentent l’effectif. |
| `td2-s3` Q3 | 22, `fcf3b662854d` | `exclusions = ["notice"]` — Exemple d’exclusion explicite sur le corpus fourni. Le dictionnaire après conserve exactement les autres effectifs ; justifiez votre propre choix. |
| `td2-s3` Q4 | 25, `e0f8f66130f9` | `from collections import Counter` — Triez les catégories selon leurs effectifs. Les ex æquo peuvent avoir plusieurs ordres ; inspectez les tokens qui justifient les comptes. |
| `td2-s3` Q5 | 29, `ec2180a45a4a` | `tokens = [t for t in doc if not t.is_punct and not t.is_space]` — Ce code prépare cinq occurrences pour votre contrôle manuel. Remplacez chaque invitation par un jugement argumenté ; le programme ne peut pas rédiger cette vérification à votre place. |
| `td2-s3` Q6 | 33, `fd7ae731fa55` | `import matplotlib.pyplot as plt` — Les deux figures utilisent les mêmes fréquences filtrées. Rédigez ensuite une hypothèse et sa vérification dans le texte ; le score ne certifie ni les images ni l’interprétation. |
| `td2-s3` Q7 | 35, `f20324e1bcaa` | `from collections import Counter` — Paramétrez les catégories et comparez avec les deux fonctions indépendantes de Q2. Testez aussi le texte vide et le transfert sur les 5 000 premiers caractères de Faguet. La combinaison additionne les effectifs lorsqu’un même lemme apparaît dans les deux catégories. |
| `td3-s3` Q1 | 12, `6718b4974b81` | `champs = ["unite", "fenetre", "normalisation", "agregation"]` — Reliez chaque information aux fichiers fournis. Les paramètres absents restent absents : ne les reconstruisez pas à partir des nombres annoncés. |
| `td3-s3` Q2 | 19, `35be237012b3` | `def concordances_exactes(source, motif, largeur=20):` — La recherche avance à la fin du résultat précédent, sans chevauchement. Testez séparément les bords, le fragment dans un mot, le texte vide et le motif vide, puis explorez Faguet. |
| `td3-s3` Q3 | 25, `fa88bc41845b` | `source = "Les lecteurs lisent. Une lectrice lit."` — Comparez les listes réellement obtenues ; ne remplacez pas une prédiction du modèle pour obtenir l’écart espéré. Le transfert et le PhraseMatcher restent à appliquer à Faguet. |
| `td3-s3` Q4 | 27, `97d7d4a5cc8a` | `lignes = []` — Cherchez dans le texte original, retours à la ligne compris. Une recherche normalisée ne doit pas modifier le verdict d’identité exacte. |
| `td3-s3` Q5 | 32, `b31d99ea1907` | `position = texte_faguet.find("légalement")` — Cet exemple localise un candidat autour du fragment distinctif. Ajustez son étendue et rédigez votre qualification ; conservez la citation Gemini intacte. |
| `td3-s3` Q6 | 34, `b711b3f23e0a` | `tests = [` — Les attentes sont fixées avant la recherche. Créez vos propres deux cas et comparez aussi les deux passages contenant professions demandés dans le sujet. |
| `td3-s3` Q7 | 36, `3f1aba846994` | `doc_preuves = nlp(texte_faguet)` — Le filtre porte sur le token entier. Les trois preuves doivent couvrir trois occurrences différentes ; vérifiez si les fenêtres retenues permettent réellement d’interpréter les passages. |
| `td4-s3` Q1 | 12, `s3-td4-06` | `def marge(contextes, terme):` — Chaque contexte contribue une fois au plus à la marge, même si chat est répété. Appliquez ensuite la fonction aux phrases de Faguet en déclarant le filtre des tokens. |
| `td4-s3` Q2 | 18, `s3-td4-09` | `def cooc_phrases(contextes, pivot, associe):` — Une paire compte une fois par phrase. Vérifiez symétrie, marges et pivot absent ; retrouvez ensuite les phrases communes des deux paires de Faguet. |
| `td4-s3` Q3 | 23, `s3-td4-12` | `def cooc_phrases(contextes, pivot, associe):` — Une phrase avec les deux associés contribue deux fois à la somme et une fois à l’union. Gardez ces conventions distinctes en examinant la ligne Intelligence. |
| `td4-s3` Q4 | 29, `s3-td4-15` | `def cooc_fenetre(tokens, pivot, associe, k):` — Comptez les paires de positions, pas seulement les pivots couverts. Pour Faguet, conservez ponctuation et mots vides dans le flux de distance. |
| `td4-s3` Q5 | 33, `s3-td4-18` | `def cooc_fenetre(tokens, pivot, associe, k):` — La concaténation autorise une paire qui traverse la frontière. Comparez ensuite vos trois unités dans Faguet en conservant leurs définitions et leurs preuves. |
| `td4-s3` Q6 | 38, `s3-td4-21` | `annotations = [{"forme": "chat", "lemme": "chat"}, {"forme": "chats", "lemme": "chat"},` — Cette table manuelle isole le changement de représentation. Sur Faguet, vérifiez cinq annotations et gardez les autres choix constants lors de la comparaison. |
| `td4-s3` Q7 | 43, `s3-td4-24` | `def marge(contextes, terme):` — Assemblez les fonctions pour produire les quatre effectifs du microcas. L’export demandé doit aussi contenir les protocoles et passages de vos deux paires réelles. |
| `td5-s3` Q1 | 13, `s3-td5-06` | `def proportion(effectif, denominateur):` — La proportion conditionnelle divise par les phrases avec pivot ; la base divise par toutes les phrases. Complétez avec votre schéma des huit cases et votre paire de Faguet. |
| `td5-s3` Q2 | 17, `s3-td5-09` | `def proportion(effectif, denominateur):` — Comparez chaque proportion à sa propre base : l’associé le plus fréquent près du pivot n’est pas nécessairement le plus concentré relativement à sa présence globale. |
| `td5-s3` Q3 | 22, `s3-td5-12` | `def pour_mille(effectif, taille):` — Le taux utilise la taille du segment, pas celle de l’autre extrait. Appliquez la même unité aux deux moitiés contiguës de Faguet et conservez les indices. |
| `td5-s3` Q4 | 26, `s3-td5-15` | `def proportion(effectif, denominateur):` — L’inversion conserve la cooccurrence et change le dénominateur. Vérifiez les quatre cases du tableau 2 × 2 et explicitez les deux populations dans votre commentaire. |
| `td5-s3` Q5 | 32, `s3-td5-18` | `def proportion(effectif, denominateur):` — Zéro sur cinq est défini et vaut zéro ; zéro sur zéro n’est pas défini. Conservez les effectifs pour discuter aussi les petits nombres. |
| `td5-s3` Q6 | 38, `s3-td5-21` | `def couverture_pivots(tokens, pivot, associe, k):` — Chaque position du pivot contribue au plus une fois. Comparez fenêtres 5, 10 et 25 dans Faguet avec le même flux non filtré et les effectifs couverts/total. |
| `td5-s3` Q7 | 42, `s3-td5-24` | `def proportion(effectif, denominateur):` — Le résultat du microcas garde numérateur et dénominateur. Votre export et votre paragraphe doivent également distinguer observation, interprétation possible et limites du protocole. |
| `td6-s3` Q1 | 15, `s3-td6-07` | `def positions(tokens, forme):` — Divisez les indices par la taille du flux complet. Pour votre dispersion de Faguet, conservez les indices spaCy d’origine et reliez les zones à des passages. |
| `td6-s3` Q2 | 20, `s3-td6-10` | `def segmenter(tokens, nb_segments):` — Les bornes couvrent tout le flux sans chevauchement. Testez aussi onze tokens ; les dix segments de Faguet conservent leurs bornes et dénominateurs alphabétiques. |
| `td6-s3` Q3 | 26, `s3-td6-13` | `segments_test = [["chat", "lit"], ["plume", "chat", "lit", "ici"]]` — Les deux segments ont des tailles différentes. Pour la carte de Faguet, calculez les taux avec les tailles alphabétiques et gardez une échelle commune aux lignes. |
| `td6-s3` Q4 | 31, `s3-td6-16` | `def cooc_fenetre(tokens, pivot, associe, k):` — Reprenez exactement le compte de paires du TD4. Présentez séparément la couverture du TD5 ; ces mesures n’ont pas la même unité. |
| `td6-s3` Q5 | 37, `s3-td6-19` | `tokens = ["avant", "chat", "puis", "plume", "après"]` — La fin exclue inclut le token situé une place après le pivot. Le join appartient au microcas ; les passages de Faguet doivent être extraits de la source originale par leurs bornes caractères. |
| `td6-s3` Q6 | 42, `s3-td6-22` | `resultat_q6 = {"etiquettes": ["segment 1", "segment 2"], "valeurs": resultat_q3["chat"]}` — Réutilisez les taux calculés en Q3. La tâche complète comprend aussi la matrice de cooccurrences de Faguet, sa diagonale conventionnelle et la relecture de la figure. |
| `td6-s3` Q7 | 49, `s3-td6-25` | `segments_test = [["chat", "lit"], ["plume", "chat", "lit", "ici"]]` — Additionnez les effectifs et les tailles avant de diviser. L’export final doit aussi relier les visualisations aux trois passages et à vos deux lectures argumentées. |
| `td7-s3` Q1 | 15, `s3-td7-08` | `def champs_manquants(affirmation):` — Une absence de protocole empêche la comparaison directe ; elle ne prouve pas un nombre faux. Gardez séparées les six annonces originales et vos propositions. |
| `td7-s3` Q2 | 21, `s3-td7-11` | `def contient_expression(tokens, expression):` — Le moteur reconnaît des expressions contiguës et garde les indices de preuve. Dans Faguet, ignorez seulement les tokens d’espacement pour ces expressions et conservez les positions d’origine. |
| `td7-s3` Q3 | 26, `s3-td7-14` | `def verifier_exactement(source, citation):` — Une variante proche reste absente comme chaîne exacte. Pour les trois citations réelles, distinguez identité, candidat proche et absence de localisation, en conservant chaque différence. |
| `td7-s3` Q4 | 32, `s3-td7-17` | `def comparer_intervalle(valeur, borne_basse, borne_haute):` — Les bornes sont inclusives. Avant toute application aux annonces réelles, vérifiez que corpus, unité, normalisation et agrégation permettent cette comparaison. |
| `td7-s3` Q5 | 36, `s3-td7-20` | `def contient_expression(tokens, expression):` — Les deux mesures appliquent les mêmes termes à deux agrégations. Définissez aussi les alternatives et expressions des six annonces réelles, sans choisir une convention pour retrouver Gemini. |
| `td7-s3` Q6 | 41, `s3-td7-23` | `def contient_expression(tokens, expression):` — La définition est rappelée ici pour rendre l’exemple lisible : dans votre notebook, réutilisez le même moteur figé en Q2 sans le modifier. Il traite un nouveau corpus. Ajoutez les attentes manuelles du voisin et les cas limites ; les tests de comptage ne valident pas les annotations linguistiques. |
| `td7-s3` Q7 | 46, `s3-td7-26` | `def champs_manquants(affirmation):` — La garde précède le calcul et la comparaison. Cet exemple traite les deux protocoles du microcas ; votre livrable complet relie aussi six annonces, citations, mesures, figures, tests, passages et synthèse argumentée. |
| `td1b-s3` Q1 | 14, `td1b-q1-reponse` | `def entites(texte, pipeline):` — Conservez les entités réellement proposées par le modèle md fixé. Discutez ensuite les éléments que vous aviez anticipés ; une absence peut venir du modèle. |
| `td1b-s3` Q2 | 18, `td1b-q2-reponse` | `def entites(texte, pipeline):` — Le filtrage s’applique aux prédictions sans changer leurs labels. Remplacez le texte d’essai par le vôtre, puis interprétez les erreurs éventuelles à partir des mentions observées. |
| `td1b-s3` Q3 | 24, `td1b-q3-reponse` | `nlp_sim = spacy.load("fr_core_news_md")` — Calculez les scores avec le modèle md. Comparez les valeurs observées et votre modification ; une forte similarité ne garantit ni équivalence des phrases ni fidélité au sens. |
| `td1b-s3` Q4 | 31, `td1b-q4-reponse` | `def entites(texte, pipeline):` — Rechargez les modèles pour éviter de multiplier les règles à chaque exécution. Cet exemple couvre les quatre règles et propose une variante de casse et un usage fictif ambigu. Examinez leurs effets réels ; une expression identique peut changer de rôle selon le contexte. |

## Limites de cette revue

La lecture ne certifie pas l’exécution effective des exemples spaCy sur les modèles installés ni la conformité générale de toute solution alternative. Elle ne remplace pas la revue pédagogique, la revue de code, les essais de rendu et la vérification de non-divulgation des contrôles. Le rapport ne revendique aucun essai en classe, aucune fusion et aucun déploiement. Les douze futurs TD one/bis/ter des PR ouvertes ne sont pas couverts par ce verdict : leurs sujets stabilisés demanderont des exemples et une relecture propres.

## Lecture des aperçus et traçabilité

Les fichiers définitifs `docs/examples/rapport_td1_s1.html` (succès 6/6) et `docs/examples/rapport_td1_s3.html` (0/6 avec code et NameError sauvegardée), explicitement signalés comme synthétiques, ont été lus intégralement sous forme de texte HTML structuré. Les deux aperçus ont été relus après les dernières reprises : guide des prérequis présent, suffixes lisibles, état de résultat manquant explicite. Les sources ont également été relues après ces reprises. Aucun rendu navigateur interactif n'a été réalisé : Chromium indisponible dans l'environnement, selon le constat d'intégration. La lisibilité responsive et le fonctionnement visuel au clic demeurent donc à confirmer en navigateur ; la lecture des conditions du gabarit n'est pas présentée comme un essai visuel.

Empreintes SHA-256 des fichiers relus à la clôture ; tout changement ultérieur significatif demande une reprise ciblée de la revue :

| Fichier | SHA-256 |
|---|---|
| `app/s1_feedback.py` | `83717460208316f5df2380b0a208e074f63caa5b80c0d075d5afbe7706f8e55e` |
| `app/s3_feedback.py` | `6cb8c59e24f3180d9927135aad4d0a4d3f1b7bf25161ca875d769dd4d79f1b47` |
| `app/templates/corrector_template.html` | `bcd26e0758700b3d622f4b4688545dab198fc648e46141024466f365413d6b55` |
| `app/templates/s3_review_evidence.html` | `e637d3e5d65c6e1debbeea9d5d9d680514a1052611b5c59ff3394ee4a8a536d0` |
| `app/s1_revision.py` | `7c4541d442100f861346188063057117855ca1cd8b9e34663ae5029ef032d243` |
| `app/s3_audit.py` | `9fe262f5f7067cc26c127f768c48e700c4bffc9150dc64678f5b3f1d1ea4e426` |
| `app/revision_s3.py` | `b9388081e20d2edb166351cb8cd3639881716b01f3c20d08069a2d0f9c4d7dd5` |
| `docs/examples/rapport_td1_s1.html` | `b71182c3ff00dbd7515a881a045b237ff810ceec17a688493ef4f2aeb0a11282` |
| `docs/examples/rapport_td1_s3.html` | `f11344d6645968c826ef679d9653c743baeb72062697015b3a97575184b04c82` |
