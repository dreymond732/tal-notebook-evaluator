# S3 — Révision des TD suivants et autocorrection technique

## Cadrage avant conception

Mission TAL-Prof du 3 octobre 2026, branche `pedagogy/s3-next-review`, après fusion de la PR25. Demande enseignante : « Passe en revue tous les TD suivants et crée les correcteurs nécessaires. » Le périmètre est **TD1B et TD2 à TD7**, soit sept supports et 46 questions. R1, R2 et TD1 viennent d'être révisés ; les contrôles ne sont pas transformés par ce lot. La demande précédente exige de limiter la relecture individuelle par l'enseignant, sans retirer les activités d'interprétation.

La référence technique initiale est `cdc52d08cc02c8880003d962d0631658f04392c1`. Pour TD2–TD7, la référence historique directement disponible et comparée est `2a36752`, aux mêmes chemins ; les ajouts intermédiaires de `ebb3458` et `4fe2e48` précisent les contrats v2 et étayent les questions. La comparaison cellule par cellule montre que les sept exercices historiques de chacun de ces TD sont présents ; les nouveaux repères et précisions sont à conserver. Le précédent cadrage `s3_progression_review_coverage.md` documente les renforcements intermédiaires.

Pour TD1B, comparer les versions `7fdfcd9` et `638b593`, ainsi que la couverture historique de `TD_0_Initiation_spacy.ipynb` consignée dans `s3_r2_spacy_editorial_coverage.md`. TD1B rétablit entités, extraction PER/ORG, similarité mots/phrases et règles. La présente mission n'annonce pas la restauration des activités historiques hors du parcours d'audit, telles que traduction, groupes nominaux ou classification : leur statut est expliqué dans `S3_COVERAGE_MATRIX.md`.

**Décision de conception proposée : aucune suppression, aucun transfert vers un support futur.** Les idées, données, prédictions, fonctions à construire, essais, interprétations, figures et exports restent présents et gardent leur caractère obligatoire. PMI (TD5 Q5) et recherche approchée avec `difflib` (TD7 Q3) restent facultatives, hors des deux heures. Les exemples fournis servent de démonstration sur d'autres données, sans remplir les cellules de réponse. Les notes destinées aux auteurs sont déplacées hors des supports ; elles ne constituent pas des objectifs étudiants.

## Progression et destinataire

Chaque passage visible s'adresse à l'étudiant. Séparer les explications de cours, les exemples fournis, la tâche à réaliser, la sortie attendue et la vérification. Une cellule peut contenir plusieurs fonctions clairement identifiables ; ne pas imposer une succession mécanique de six titres à chaque question. Les repères actuels « intégré au temps… sans nouvelle question notée » sont des notes de fabrication à retirer du cours, en conservant leur contenu utile. Expliquer le protocole avant de demander de le programmer.

Les TD2–TD7 annoncent actuellement une relecture de toutes les interprétations par l'enseignant. Remplacer cette promesse par des critères d'autoévaluation : **le score porte sur les résultats techniques ; les interprétations linguistiques ne sont pas autocorrigées**. Les étudiants conservent leurs observations, passages et explications ; ils peuvent les comparer aux critères et discuter en séance. Aucun appel à un LLM externe ni note de qualité linguistique automatique n'est introduit. Les retours entre pairs déjà prévus restent présents. La disparition d'une promesse de relecture systématique ne justifie pas d'enlever un commentaire demandé.

| Support | Acquis d'entrée et place dans le parcours | Fonctions à clarifier | Charge indicative conservée |
|---|---|---|---|
| TD1B | TD1, Python S1/S2 ; avant TD2 | Entités puis sélection, vecteurs puis scores, règle puis tests ; quatre activités réelles | Préparation 15 ; Q1–Q4 : 20/20/25/30 ; bilan 10 = 120 min |
| TD2 | TD1 pour Doc/tokens/POS ; fonctions, collections ; R2 si difficulté | Fréquences → exclusions → qualité → représentations → fonction générale | Préparation 10 ; Q1–Q7 : 10/20/15/10/15/15/20 ; export 5 = 120 min |
| TD3 | TD2 ; chaînes, tranches, fonctions ; positions du TD1 | Recherche exacte → expression → citation → qualification → preuve | Préparation 10 ; Q1–Q7 : 10/20/15/15/15/15/15 ; export 5 = 120 min |
| TD4 | TD3 pour concordances ; listes/ensembles, fonctions | Présence, marges, paires, union, distance et frontières sont des objets distincts | Préparation 8 ; Q1–Q7 : 12/14/14/17/15/18/16 ; bilan 6 = 120 min |
| TD5 | Fonctions et export TD4 ; division et conditions | Dénominateurs, proportions, taux, cas indéfinis, sensibilité | Même répartition que TD4 = 120 min |
| TD6 | TD4 positions/fenêtres ; TD5 taux ; Matplotlib TD2 | Construire les valeurs avant la figure, retrouver les passages après lecture distante | Même répartition que TD4 = 120 min |
| TD7 | TD2–TD6 : fonctions conservées, provenance, preuves et visualisations | Assemblage progressif de l'audit, sans attribuer au LLM un protocole reconstruit | Préparation 8 ; Q1–Q7 : 12/20/14/12/16/14/18 ; bilan 6 = 120 min |

Les durées sont prévisionnelles, non mesurées. TD7 est particulièrement dense : les fonctions antérieures doivent être disponibles et les notes/tableaux s'assemblent au fil des questions. Aucun exercice ne passe silencieusement en option pour tenir les deux heures. Si la séance révèle une surcharge, elle devra être rapportée à l'enseignant avant de changer sa durée ou sa couverture.

## Matrice par question : historique → actuel → cible

Chaque ligne désigne le même exercice dans la source historique et dans la référence technique, sauf TD1B ajouté récemment. Les identifiants de consigne et réponse constituent les ancres à conserver. Le statut **RENFORCÉ** signifie une clarification/explication, sans augmentation implicite des exercices obligatoires ; **CONSERVÉ** maintient aussi l'autonomie et les données ouvertes. La colonne « notions » prescrit un cours/rappel et, pour une opération nouvelle, un exemple distinct **avant** la tâche.

### TD1B — Entités, similarité et règles

| Question / ancre | Acquis et notions introduites avant la tâche | Activité, données, production et autonomie à conserver | Cible / correction |
|---|---|---|---|
| Q1 `td1b-q1-consigne` | Doc/parcours ; Span, `ents`, `text`, `label_`, catégories du modèle | Prédire informations Apple/Allemagne/montant/date ; analyser texte fixe ; liste ordonnée complète `entites_q1` ; confronter humain et modèle sans ajouter une DATE absente | **CONSERVÉ** ; contrôler les annotations enregistrées et la provenance du texte ; ne pas noter l'accord linguistique |
| Q2 `td1b-q2-consigne` | Q1, condition d'appartenance ; distinction détection/extraction, faux positif | Texte Macron/Musk/Paris/Google/Tesla, sortie complète puis filtre PER/ORG ; réutilisation sur texte personnel avec personne/organisation/lieu ; expliquer sélection et limites | **CONSERVÉ** ; vérifier filtre, ordre/répétitions et réemploi observable ; ne pas imposer les entités du texte personnel |
| Q3 `td1b-q3-consigne` | Vecteurs du modèle md, `has_vector`, `similarity`, score non probabiliste | Prédire puis comparer chien/chat et chien/voiture ; phrases chat/tapis et chien/canapé ; modification libre de sens ; scores étiquetés, vérification vecteurs et interprétation | **CONSERVÉ** ; contrôler comparaisons fixes et cohérence de la variation, sans ordre ni seuil sémantique prescrit |
| Q4 `td1b-q4-consigne` | Pipeline dédié, `pipe_names`, `add_pipe`, `add_patterns`, règles exactes et labels | Université de Toulon avant/après ; ajout ORG, LOC et DATE ; au moins cinq textes incluant variante et ambiguïté ; attendus avant exécution, observations et limites | **CONSERVÉ** ; contrôler structure des règles, présence du composant et traces d'essais ; aucun jugement automatique sur pertinence linguistique |

Les quatre réponses `td1b-qN-reponse`, observations et bilan restent entiers. **CHANGEMENT_DE_CONTRAT** : ajout d'un correcteur technique, de traces structurées et d'une version distinguant les anciennes copies sans ces traces. La version 2 historique ne doit pas recevoir une fausse note nulle pour des traces qu'elle ne demandait pas ; elle doit être refusée selon la règle « mauvaise version du notebook ». Le format exact retenu avec l’Architecte est précisé ci-dessous ; le barème est de quatre points techniques, un par question, sans point d’interprétation. L'ajout de traces peut être fourni comme affichage de valeurs construites par l'étudiant ; il ne doit pas transformer quatre activités ouvertes en reproduction de listes figées.

### TD2 — Fréquences, filtres et objets de recherche

| Q / consigne actuelle | Notions à cadrer avant la question | Production, essais et interprétation conservés | Statut |
|---|---|---|---|
| Q1 `0910116a4331` | Lecture UTF-8, chaîne/Doc, caractères/tokens/phrases | Lire `corpus_td2.txt`, trois comptages, dix premiers tokens non ponctuation forme/lemme/POS, vérifier provenance et noter écart forme/lemme | **RENFORCÉ**, exemple de lecture exécutable distinct |
| Q2 `6b03a2dee4a6` | `Counter`, retour, argument texte, exclusions `None`, POS, `is_stop` | Construire deux fonctions noms/verbes, tester phrase répétée et corpus, top5 et somme, justifier VERB sans AUX ; dictionnaires complets | **RENFORCÉ**, cours séparé de la consigne et aucun résultat prérempli |
| Q3 `dbb99a0dfe33` | Exclusion de lemme et invariance des comptes restants | Choix personnel d'un nom présent, justifier, comparer avant/après, invariants, effet de femme/homme sur objet de Faguet | **RENFORCÉ**, choix libre conservé ; cohérence Q3→Q6 |
| Q4 `97e0baba0c8c` | Distribution POS, tri décroissant et ex aequo | Compter hors ponctuation/espaces, top3, somme, observation et limite thématique ; ordre libre à égalité | **CONSERVÉ**, vérifications explicites |
| Q5 `e1fafdbee7f2` | NOUN/VERB/ADJ, stopwords ; `PhraseMatcher`, formes/lemmes/expressions | Liste complète ordonnée avec répétitions ; cinq occurrences distinctes observées, jugement sans écraser modèle ; intelligence/intelligentes/bon sens ; lecture du motif seulement | **RENFORCÉ**, tutoriel de l'expression distinct de la tâche d'inspection |
| Q6 `8bac30105f01` | `WordCloud.generate_from_frequencies`, Matplotlib, unités et limites | Nuage et barres issus mêmes noms filtrés, placement fixé, cas filtre vide avec reprise Q3, hypothèse et concordance future | **RENFORCÉ**, démonstration exécutable, deux figures maintenues |
| Q7 `2ef5275cac37` | Réemploi fonctions paramétrées, catégories multiples, cas vide | Fonction `frequences_pos`, égalités avec spécialisées, réunion catégories, textes/exclusions vides, transfert 5000 caractères Faguet séparé trace microcorpus ; lisibilité/généralité | **CONSERVÉ**, transfert autonome maintenu |

### TD3 — Concordances et fidélité des citations

| Q / consigne actuelle | Notions à cadrer avant la question | Production, essais et interprétation conservés | Statut |
|---|---|---|---|
| Q1 `ede8b619b42d` | Provenance, empreinte, convention ; conversation séquentielle | Fiche corpus, six affirmations, trois prompts, paramètres absents ; pourquoi pas répétitions indépendantes et fourchettes non références | **RENFORCÉ**, lecture de ressource guidée et séparée du cours |
| Q2 `6dfa6e72ddd7` | `find`/indice reprise, tranches bornées, absence/erreur, `raise` et `except ValueError` | Fonction concordances toutes occurrences non chevauchantes ; bords/répétition/sous-chaîne/texte vide/motif vide ; attendu manuel avant calcul ; source_test puis trois contextes intelligence Faguet | **RENFORCÉ**, exemples exécutables sans fonction solution |
| Q3 `b3861304ce29` | Fragment, token entier, lemme, `PhraseMatcher` repris TD2 | Comparer lit/lire sur lecteurs/lectrice ; positions et formes ; cas Faguet ; motif bon sens ; expliquer intelligence/intelligentes | **RENFORCÉ**, modèle d'expression expliqué puis adaptation réelle |
| Q4 `aa31f6af9aeb` | Recherche exacte, casse/apostrophes/ponctuation | Trois citations, indice ou -1, tranche vérifiée ; absence exacte distincte absence de l'idée | **CONSERVÉ**, autonomie de réemploi |
| Q5 `a81cf330c3da` | Normalisation typographique, position originale vs normalisée | Citations absentes, fragment légalement de C1, comparaison mot à mot ; passage exact et position source ; typographie/substitution/non-localisation ; original LLM conservé | **RENFORCÉ**, exemple séparé de toute conclusion imposée |
| Q6 `8373304e4726` | Rapprochement thématique vs fidélité | Deux passages professions, mots communs, règle de lecture ; deux cas personnels exact/altéré avec attendu préalable et comparaison observée | **CONSERVÉ**, création autonome sans bibliothèque nouvelle |
| Q7 `abcdbeabe3b2` | Concordance comme preuve ; convention proposée | G1 intelligence ou G2 aptitude(s), au moins trois occurrences distinctes, positions/source exactes ; portée et limites fenêtre/agrégation absentes ; convention TD4 déclarée proposition | **CONSERVÉ**, pas trois fenêtres du même pivot |

### TD4 — Définir et vérifier les cooccurrences

| Q / consigne actuelle | Notions à cadrer avant la question | Production, essais et interprétation conservés | Statut |
|---|---|---|---|
| Q1 `s3-td4-05` | Présence/marge/occurrence, ensemble et N | Prédiction chat, fonction marge + vide ; chat/livre/N microcorpus ; phrases Faguet en formes minuscules alpha, intelligence/professions | **RENFORCÉ**, définition avant construction |
| Q2 `s3-td4-08` | Cooccurrence booléenne, symétrie/bornes, `assert` | Fonction trois paires, tests symétrie/marges/pivot absent ; deux paires Faguet et phrases preuves ; ni lien grammatical ni adhésion induits | **RENFORCÉ**, exemple assert distinct |
| Q3 `s3-td4-11` | Somme de paires vs union de contextes | Prédire deux mesures ; fonction union sans doublons ; réemploi Q2 ; lire ligne Intelligence Gemini et champs manquants | **RENFORCÉ**, tableau pédagogique conservé |
| Q4 `s3-td4-14` | Positions token/char, distance, `enumerate`, fenêtre valide | Fonction fenêtre, refuser k<1 ; paires manuelles k1/k3 ; Faguet k5/k10 flux intégral ponctuation/stopwords conservés ; positions preuves | **RENFORCÉ**, conventions avant tâche |
| Q5 `s3-td4-17` | Frontière phrase/paragraphe/flux | Microcas chat et livre séparés ; flux vs phrase ; Faguet trois mesures différentes ; copie retours normalisés pour paragraphes, original pour positions ; cas frontière ou absence déclarée | **CONSERVÉ**, unités comparées sans fausse erreur |
| Q6 `s3-td4-20` | Forme/lemme/famille, expression contiguë | Référence manuelle chat/chats/chaton ; fonction par clé ; cinq observations Faguet ; comparaisons protocole constant ; bon sens/femme forte, espaces ignorés pour expression uniquement | **RENFORCÉ**, séparation expression et distance explicitée |
| Q7 `s3-td4-23` | Composition fonctions, preuve et protocole | Fonction mesurer_phrase, marges/cooc/N, bornes et vide ; export deux paires Faguet avec unités et contextes ; trois phrases bilan et fonctions conservées | **CONSERVÉ**, assemblage autonome |

### TD5 — Fréquences et associations

| Q / consigne actuelle | Notions à cadrer avant la question | Production, essais et interprétation conservés | Statut |
|---|---|---|---|
| Q1 `s3-td5-05` | Marges, conditionnelle/base, quatre cases, arrondi | Dessiner huit contextes compatibles ; fonction proportions ; trace cas N8/marges3&4/cooc2 ; paire TD4 et dénominateurs explicités | **RENFORCÉ**, tableau de cours distinct conservé |
| Q2 `s3-td5-08` | Fréquence vs concentration relative | Cas A/B, conditionnelles et bases ; comparaison nuancée sans significativité ; Faguet un pivot/deux associés, citations/négations/opinions | **CONSERVÉ**, autonomie d'application |
| Q3 `s3-td5-11` | Taux pour mille, population comparable | Fonction avec taille nulle ; court100/4 et long400/8 ; deux moitiés alpha Faguet indices conservés, pas chapitres ; limites effectifs seuls | **RENFORCÉ**, explication avant programmation |
| Q4 `s3-td5-14` | Symétrie cooc vs conditionnelle, tableau 2×2 | Deux sens cas N8 ; fonction/tests marges égales/inégales ; Faguet deux commentaires populations ; quatre effectifs et somme, pas test statistique | **CONSERVÉ** |
| Q5 `s3-td5-17` | Zéro vs indéfini, `None`, quantité d'observations | Proportion sûre, tests 0/0 et 0/5 ; comparaison 1/1 vs20/20 ; terme rare et phrases Faguet, limites ; PMI facultative après prérequis | **RENFORCÉ**, arrondi conditionnel expliqué ; option inchangée |
| Q6 `s3-td5-20` | Position de pivot couverte au plus une fois | Fonction couverture ; k1/k3 chat/livre ; Faguet k = 5, 10, 25 numérateur/dénominateur ; dépendance au protocole sans attribuer au LLM | **RENFORCÉ**, contraste paires/couverture conservé |
| Q7 `s3-td5-23` | Résultat, unité, provenance et portée | Trace issue Q1 ; export deux paires avec marges, proportions, fenêtres et preuves ; paragraphe observation/explication/limite ; ligne Gemini et convention personnelle | **CONSERVÉ**, synthèse ouverte |

### TD6 — Visualisations

| Q / consigne actuelle | Notions à cadrer avant la question | Production, essais et interprétation conservés | Statut |
|---|---|---|---|
| Q1 `s3-td6-06` | Dispersion, position i/N, `eventplot` | Microcas positions/relatives ; fonction positions ; trois pivots Faguet flux intégral ; légende, zone dense/pauvre et deux passages | **RENFORCÉ**, exemple graphique exécutable |
| Q2 `s3-td6-09` | Segments contigus, bornes fin exclue, tailles nulles | Microcas4segments ; fonction générale + essai sur 11 tokens ; Faguet en dix segments, bornes flux intégral et tailles alpha ; somme globale ; export bornes | **RENFORCÉ**, vide traité sans taux inventé |
| Q3 `s3-td6-12` | Matrice lignes/colonnes, unités, `imshow` et colorbar | Taux chat/plume2segments ; Faguet : trois pivots, dix segments, bruts conservés ; échelle commune ; case à relire sans inférence thématique automatique | **RENFORCÉ**, cours table→figure avant consigne |
| Q4 `s3-td6-15` | Sensibilité, paires vs couverture | Réemploi fenêtre TD4 microcas k = 1, 2, 3 ; deux paires Faguet k = 5, 10, 25 table puis courbes ; couverture séparée ; expliquer classement et paires ajoutées | **CONSERVÉ**, plusieurs unités jamais confondues |
| Q5 `s3-td6-18` | Indices token/char, tranches, contexte source | Microcas join borné ; au moins trois occurrences ou toutes dans case de Q3 ; Faguet original exact, contexte négation/citation/opinion, fichier et indices | **RENFORCÉ**, exemple de position et fidèle citation |
| Q6 `s3-td6-21` | Valeurs partagées figure/table, légende vérifiable | Réemploi taux de Q3 et barres ; matrice de cooccurrences pour trois pivots, diagonale à zéro conventionnelle, preuves hors diagonale ; légende complète ; voisin relit et correction concrète | **RENFORCÉ**, démonstration distincte, relecture entre pairs conservée |
| Q7 `s3-td6-24` | Somme effectifs et tailles avant taux, savefig | Agrégat microcas ; export bornes/taux/positions/sensibilité/preuves +figures ; deux paragraphes distant/proche ; figure et table pour l’audit | **CONSERVÉ**, autonomie de synthèse |

### TD7 — Audit final

| Q / consigne actuelle | Notions à cadrer avant la question | Production, essais et interprétation conservés | Statut |
|---|---|---|---|
| Q1 `s3-td7-07` | Définition opératoire, quatre paramètres absents | Microannonce et statut ; six lignes originales conservées et dictionnaires de protocole proposés distincts ; étapes de provenance | **RENFORCÉ**, modèle de structure expliqué |
| Q2 `s3-td7-10` | Expressions contiguës, union, preuves et marges | Fonctions contient_expression/mesurer ; microcas et bornes ; essai expression/noncontigu ; Faguet formes+positions originales, espaces seuls ignorés expressions ; une ligne auditée | **RENFORCÉ**, architecture décomposée sans fournir moteur |
| Q3 `s3-td7-13` | Citation exacte vs normalisée, positions originales | Fonction et microcas exact/altéré ; trois citations Faguet ; candidat proche ou non localisé, différences/positions ; C1 ; difflib facultatif | **CONSERVÉ**, activité de lecture maintenue |
| Q4 `s3-td7-16` | Comparabilité avant intervalle, bornes inclusives | Fonction intervalle, essais3/5 et bornes2/4 ; garde paramètres absents ; ligne réelle statut original vs recomptage exploratoire | **RENFORCÉ**, statut différent de vérité générale |
| Q5 `s3-td7-19` | Union vs somme paires, expressions alternatives | Mode somme, microcas ; dictionnaires six lignes formes/variantes déclarées ; six recomptages et marges/preuves ; visualisation du TD6 d’une ligne | **CONSERVÉ**, toutes les lignes conservées |
| Q6 `s3-td7-22` | Essai indépendant, référence manuelle, caslimites | Nouveau microcorpus livre/plume manuel avant exécution ; voisin crée un autre cas répété/noncontigu ; vide/pivot absent/associé seul ; cinq observations spaCy ; lot exporté | **RENFORCÉ**, tableau attendu/observé distinct sans solution |
| Q7 `s3-td7-25` | Assemblage progressif, provenance et argumentation | Fonction auditer + recomptage séparé ; deux annonces même intervalle définie/indéfinie ; export des six lignes, preuves, citations et lot manuel ; tableau ; synthèse de 200–300 mots, figure et trois passages | **CONSERVÉ**, critères d'autoévaluation à la place de promesse de lecture par l’enseignant |

## Tutorats, bibliothèques et évaluateurs

Le double contexte complet identique demeure obligatoire, dans la première cellule Markdown et dans les métadonnées Colab. Une demande de résolution entraîne une question ciblée et une attente. Seuls les acquis présents avant la question sont autorisés. Les modules employés dans une préparation fournie ne deviennent pas des bibliothèques de solution.

- TD1B : `spacy` ; NER Q1, filtre Q2, similarité Q3 seulement, règles Q4 seulement. Les traces JSON fournies ne justifient pas un nouveau cours obligatoire sur la sérialisation.
- TD2 : `spacy`, `collections.Counter` ; lecture UTF-8 par `open`, déjà enseignée ; `pathlib` reste réservé à la préparation fournie ; `spacy.matcher.PhraseMatcher` expliqué Q5 ; `wordcloud` et `matplotlib.pyplot` à partir de Q6. Les permissions du manifeste doivent refléter les notions réellement expliquées, sans anticiper les méthodes de TD3.
- TD3 : `spacy`, `json`, `spacy.matcher.PhraseMatcher` Q3 ; pas de bibliothèque de similarité pour Q6. Empreinte/téléchargement restent préparation fournie.
- TD4/TD5 : `spacy`, `json` et Python déjà travaillé. `math.log2` reste hors tronc commun et réservé au prolongement PMI conditionné.
- TD6 : réemploi de `matplotlib.pyplot`, `spacy`, `json` ; ne pas introduire NumPy/pandas/seaborn pour raccourcir les exercices.
- TD7 : `spacy`, `json`, Matplotlib pour réemploi TD6 ; `difflib` seulement dans le prolongement annoncé. Aucune API LLM ni nouvelle bibliothèque.

TD2–TD7 ont déjà des correcteurs v2 : **les vérifier et les compléter seulement pour un défaut démontré**, sans créer six doublons ni transformer l'évaluation technique en note d'interprétation. Les productions ouvertes restent assorties de critères d'autoévaluation concrets. Les tests ne doivent pas exiger un préfixe textuel ancien au détriment d'une réécriture lisible ; leur protection doit porter sur la conservation des questions, données, réponses, marqueurs et acquis, accompagnée des revues indépendantes.

## Acceptation attendue

La conception attend la validation indépendante de cette matrice. Après écriture : relever les cellules ajoutées/réécrites et la conservation par question ; vérifier les réponses et traces, métadonnées, restitution avec placeholder et séparateur ; vérifier les tuteurs avec le manifeste ; relire chaque passage et chaque commentaire. Les verdicts pédagogique et éditorial doivent être distincts. L'auditeur technique examine tout changement de correcteur et la migration TD1B. Le score automatique doit annoncer sa portée réelle. Les tests locaux et CI ne remplacent ni la lecture étudiante ni l'observation d'une séance réelle.

## Compléments de cadrage reçus avant conception

Les trois Designers ont lu intégralement leurs lots, sans les modifier, et confirmé les 42 activités TD2–TD7. TAL-Pedagogy-Reviewer a effectué une première comparaison indépendante historique/technique avant de relire cette matrice. Les précisions suivantes complètent le cadrage, sans supprimer d'objectif.

- TD2 Q1 : l'exemple historique utilisait `Path.read_text`/`write_text` alors que le tuteur n'autorise pas pathlib dans les réponses. La lecture/écriture UTF-8 est conservée avec `open`, déjà enseigné ; l'objectif est lire le fichier, non imposer cette API.
- TD3 Q1 : donner l'accès explicite aux fichiers de provenance et au README figé ; ne pas supposer qu'un README absent du téléchargement a été lu. Garder la fiche à construire par l'étudiant.
- TD4 Q3 : retirer `any()` des permissions du tuteur puisque l'opération n'a pas été introduite et que boucles/conditions suffisent. Cela ne retire aucune activité ni stratégie demandée.
- TD6 : rendre exécutables les exemples Matplotlib déjà présents ; expliquer la figure, les axes, `eventplot`, `imshow`, `colorbar`, `plot`, `bar` et `savefig` avant leurs emplois respectifs. `plt.figure` pour isoler les graphiques est une opération déjà montrée au TD2.
- TD6 Q6 : la phrase historique sur le remplacement d'une ancienne variante est une note de conception ; la matrice de cooccurrences, ses conventions, la figure et la vérification entre pairs restent demandées.

### Contrat TD1B retenu avec l'Architecte

Version **3**, quatre points techniques formatifs. Les anciennes copies version 2, qui ne demandaient pas ces traces, sont refusées explicitement avec « mauvaise version du notebook ». Chaque réponse garde son ID et reçoit un affichage fourni `S3_TD1B_Qn:` suivi de JSON assemblé à partir des résultats métiers construits par l'étudiant. JSON a déjà été rencontré au TD1 ; l'assemblage fourni n'ajoute pas un cinquième exercice. Aucune analyse spaCy n'est fournie dans les réponses.

| Question | Structure retenue | Portée exacte de l'autocorrection |
|---|---|---|
| Q1 | `texte`, `entites` | Texte fixe et liste complète ordonnée de couples forme/label, comparaison aux prédictions réellement relevées de md 3.8.0 |
| Q2 | `texte`, `entites`, `selection`, `essai: {texte, entites, selection}` | Référence fixe puis cohérence du filtre PER/ORG pour le texte personnel ; aucune certification des catégories personnelles |
| Q3 | `vecteurs: {chien, chat, voiture}`, `scores: {chien_chat, chien_voiture, phrases}`, `variation: {original, modifie, score}` | Comparaisons fixes réellement relevées et tolérance numérique documentée ; textes de variation distincts et score fini ; aucune qualité sémantique ni ordre imposé |
| Q4 | `texte`, `avant`, `apres`, `pipeline`, `regles: [{label, pattern}]`, `essais: [{texte, sans_regles, avec_regles}]` | Cas Toulon, ordre composant avant ner, quatre expressions dont ORG/LOC/DATE, au moins cinq textes distincts et cohérence des traces ; pertinence linguistique des règles non notée |

La vérification des sorties libres peut établir structure, cohérence et provenance textuelle, jamais leur vérité linguistique. Le correcteur ne doit ni exécuter le code étudiant ni compter une simple présence de prose comme preuve de qualité. Les anticipations, choix de textes, ambiguïtés, variantes et commentaires demeurent dans les cellules d'observation et l'autoévaluation.

Pour Q4, un essai simple sans chevauchement doit permettre d'observer chaque règle exacte avec son label. Les variantes et ambiguïtés restent également demandées parmi les cinq textes ou au-delà : la vérification du fonctionnement de la règle ne remplace pas son examen critique. Le modèle statistique ne prédit pas DATE ; ce label personnalisé peut apparaître après les règles, pas être présenté comme une prédiction antérieure. Une règle exacte doit être réellement représentée dans les sorties de ses essais, pas seulement écrite dans la liste des règles.

### Validation préalable

Le 3 octobre 2026, TAL-Pedagogy-Reviewer indépendant (`next_ped_review`) a lu la matrice et les 42 questions TD2–TD7 dans les deux références ; verdict **ACCEPT du cadrage avant conception** communiqué à l'intégration. La couverture des quatre activités TD1B est également acceptée ; les critères précis du correcteur v3 sont examinés séparément avec l'Architecte. Ce verdict autorise la conception et ne préjuge pas des supports produits.

Le même réviseur a ensuite confirmé **ACCEPT du cadrage TD1B version 3**, après lecture du schéma exact, des quatre points techniques et de la vérification de chaque règle sur un essai simple. Les sept supports ont donc leur cadrage validé avant conception.

## Réalisation après conception — relevé pour les revues

Le cadrage a été suivi par sept supports : **311 cellules et 46 questions**. Les six TD2–TD7 conservent leurs sept cellules de réponse, leurs traces v2 et leurs activités historiques ; TD1B conserve ses quatre activités et passe à la version 3 avec correction technique. Aucun contrôle n'a reçu de notion supplémentaire par cette révision. Ce relevé décrit les fichiers écrits, sans constituer une auto-validation par leur producteur.

| Support | Cellules / questions | Exemples de code fournis et exécutables |
|---|---:|---|
| TD1B | 36 / 4 | `td1b-q1-exemple`, `td1b-q2-exemple`, `td1b-q3-exemple`, `td1b-q4-exemple`, `td1b-q4-exemple-essais` |
| TD2 | 39 / 7 | `td2-exemple-lecture`, `td2-exemple-counter`, `td2-exemple-filtre`, `td2-exemple-expression`, `td2-exemple-figures` |
| TD3 | 40 / 7 | `td3-exemple-find`, `td3-exemple-contexte`, `td3-exemple-reprise`, `td3-exemple-erreur`, `td3-exemple-lemme`, `td3-exemple-expression`, `td3-exemple-normalisation` |
| TD4 | 47 / 7 | `s3-td4-json-example`, `s3-td4-example-q1`, `s3-td4-example-q2`, `s3-td4-example-q4`, `s3-td4-example-q6` |
| TD5 | 46 / 7 | `s3-td5-json-example`, `s3-td5-example-q1`, `s3-td5-example-q3`, `s3-td5-example-q5`, `s3-td5-example-q6` |
| TD6 | 53 / 7 | `s3-td6-json-exemple`, `s3-td6-q1-exemple-1`, `s3-td6-q3-exemple-1`, `s3-td6-q4-exemple-1`, `s3-td6-q5-exemple-source`, `s3-td6-q6-exemple-1`, `s3-td6-q7-exemple-sauvegarde` |
| TD7 | 50 / 7 | `s3-td7-json-exemple`, `s3-td7-q1-exemple-champs`, `s3-td7-q2-exemple-tranche`, `s3-td7-q3-exemple-1`, `s3-td7-q4-exemple-intervalle` |

Les **39 exemples de code** emploient des données distinctes des réponses. Le transfert de fences Markdown vers des cellules exécutables conserve la fonction pédagogique de démonstration. Les interprétations disposent de critères concrets de vérification personnelle ; les passages sur Faguet, les essais limites, les figures et les exports restent demandés. Les notes de fabrication et promesses de relecture systématique sont retirées. La restitution HTML reste séparée visuellement et son URL demeure un placeholder dans Git.

Le manifeste final aligne les bibliothèques sur les explications effectivement présentes avant chaque question. Il retire les permissions non enseignées `any()` (TD4 Q3 / TD5 Q6), `scatter` et `axvline` (TD6), place `savefig` seulement en Q7 du TD6, et autorise les méthodes effectivement expliquées : comptage et compréhension de dictionnaire TD2, PhraseMatcher et positions de Span TD3, puis réemploi des tokens pour les mots entiers en Q7. JSON dans TD1B demeure un affichage fourni. Les titres de certains exercices dans le manifeste sont abrégés pour le budget interne sans retirer les notions. Les contextes générables comptent respectivement 4028, 4374, 4287, 4343, 4248, 4345 et 4358 caractères : aucun n'est tronqué. La génération des deux copies relève de l'intégration et sa vérification reste distincte de la revue rédactionnelle.

## Bilan final des revues et vérifications

Le 3 octobre 2026, les avis indépendants définitifs portent sur les **311 cellules et 46 questions**, ainsi que le README S3 :

- TAL-Pedagogy-Reviewer (`next_ped_review`) : **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**. Les activités et l'autonomie des versions comparées sont conservées, sans déplacement vers un support futur. Les sept doubles contextes du tuteur ont été vérifiés après synchronisation.
- TAL-Editorial-Reviewer (`next_editorial_review`) : **ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE**, dans `reports/editorial/s3-next-review.md`. Lecture exhaustive des consignes, cours, commentaires de code, exemples et bilans ; aucune promesse de relecture systématique ni blocage éditorial restant.
- TAL-Étudiant-Modèle : lecture des 46 questions, sans exécution de code étudiant ni accès aux correcteurs ; note `Corrigés modèles/TD/s3-next-review/lecture_etudiante.md`. La réserve TD6 Q5 est levée : changer de case en le déclarant permet de retrouver effectivement un contexte avec négation, citation ou opinion rapportée. La relecture entre pairs de Q6 conserve une preuve même si le voisin ne demande pas de modification.
- TAL-Code-Auditor : avis **ACCEPT**, 136 tests ciblés et 228 mutations rapportés ; correction TD1B v3 et maintien des contrats TD2–TD7 examinés indépendamment.

L'intégration rapporte **293 tests réussis**, **39 exemples fournis exécutés avec succès**, **35 profils de tutorat vérifiés**, et **34 supports de distribution préparés et contrôlés**. Ces résultats ne sont pas présentés comme des exécutions personnelles du TAL-Prof : son contrôle direct porte sur la lecture des matrices et profils, le rendu des sept contextes sous budget et la concordance des empreintes finales avec le rapport éditorial. Le catalogue a été relu directement : 35 entrées, 34 actives et 34 correcteurs automatiques, dont `td1b-s3` version 3.

### Empreintes des fichiers effectivement revus

| Support | Cellules / questions | SHA-256 |
|---|---:|---|
| TD1B | 36 / 4 | `7f740064aecb0d877d1e407429c4e26ded1ac6a7b89637049a8fd4a9594c6daa` |
| TD2 | 39 / 7 | `ff5fd1d037eb8c4e7c5b5495e0903d4ba2a8844678ececad28462e7c1c17f6f9` |
| TD3 | 40 / 7 | `1ec40c816a269a79c925eaab48b2d4db16c5b6a64c48640f44367a2d6ca77e95` |
| TD4 | 47 / 7 | `dc8d1b7240f1be8ec6a57f314bdf5cb50742487849e622d3e14f8d2f8e9aa2f7` |
| TD5 | 46 / 7 | `b9beee85f8e11b4c676c7507d649644f0d61a17b8ed1b7d33978e11f1412e74c` |
| TD6 | 53 / 7 | `828aabddf5410bda7dfea9c0bc7f7e0ee8e365e47c1a9bb17687a96a494d0f73` |
| TD7 | 50 / 7 | `bf1a04b5193d52bd1dcf9ecad40d512b816d31b1259906eddd8c13443ada384f` |

Les sept supports passent à **REVU** dans l'inventaire ; ce statut ne vaut ni décision de fusion ni mise en production. La gouvernance et l'intégration rassemblent séparément leurs preuves, puis le mainteneur décide de la fusion et du déploiement.

**Limites maintenues :** aucune durée réelle n'est mesurée en classe ; TD7 reste dense et dépend des fonctions construites auparavant. L'exécution réussie d'un exemple fourni ne garantit pas la réussite des étudiants. La présence du double tuteur ne garantit pas son respect par Colab. Les correcteurs analysent des traces enregistrées sans exécuter le code étudiant : ils n'établissent ni l'authenticité des calculs ni la qualité de l'interprétation linguistique. Les activités ouvertes restent demandées et autoévaluées ; leur conservation ne crée pas une obligation de relecture individuelle systématique. Les autres supports, notamment les contrôles, restent à reprendre dans leur propre lot.
