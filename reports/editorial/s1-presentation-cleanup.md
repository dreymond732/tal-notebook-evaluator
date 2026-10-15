# S1 — Revue éditoriale indépendante du nettoyage de présentation

## Périmètre et références

Mission du 15 octobre 2026 : vérifier le nettoyage de présentation des sept TD S1 avant la PR demandée par l'enseignant. Branche : `pedagogy/s1-nettoyage-presentation`. Rôle : **TAL-Editorial-Reviewer**, distinct du TAL-Prof et du TAL-Pedagogy-Designer ayant produit les fichiers. Référence technique examinée : `590b9a6`, comparée à la version de travail identifiée par les empreintes finales ci-dessous.

Lecture exhaustive des **293 cellules et 45 questions**, de la première à la dernière cellule de chaque TD, y compris les commentaires de code, les essais, les vérifications et la restitution HTML. Les sources ne contiennent aucune sortie enregistrée à interpréter. Les indices de ce rapport commencent à **zéro**, contrairement à ceux de la matrice préalable qui commencent à un. Les IDs techniques restent identiques.

Références normatives relues : `AGENTS.md`, fiche `docs/agents/TAL-Editorial-Reviewer.md`, fiche de revue `docs/agents/EDITORIAL_REVIEW_TEMPLATE.md`. Cadrage : `docs/pedagogy/s1_presentation_cleanup_coverage.md`, accepté indépendamment par le Pedagogy-Reviewer avant l'intervention du Designer. Le handoff du Designer `/tmp/s1-cleanup-designer.md` a été confronté aux fichiers réels, sans être considéré comme une validation indépendante.

La comparaison de conservation porte sur les mêmes fichiers au commit `590b9a6`. Les références historiques plus anciennes et les sources privées 2025 restent documentées dans `docs/pedagogy/s1_editorial_complete_coverage.md`. Elles ne sont pas présentées comme relues pour ce nettoyage ; une restauration exhaustive des originaux ne peut être déduite de cette opération de présentation. Les observations et le verdict global de l'audit S1 du 14 octobre restent inchangés pour les DM, contrôles, corrigés et lacunes historiques hors de cette livraison.

Chaque passage des sept TD s'adresse à l'étudiant. Aucun corrigé DM enseignant ne figure dans ce périmètre. Le rôle éditorial a écrit uniquement le présent rapport ; aucun support, profil tuteur, document normatif, test ou correcteur n'a été modifié par ce rôle.

## Fichiers relus et verdicts par support

Les chemins ci-dessous sont sous `Notebooks TD/S1/`. Tous sont des TD S1, avec les identifiants tuteur `TD1_S1` à `TD7_S1`. Les cellules initiales ont l'ID `tal-tutor-instructions`, les restitutions l'ID `tal-submission`.

| Fichier | Plage relue | Questions | Verdict éditorial du nettoyage | Lisibilité |
|---|---:|---:|---|---|
| `TD1_S1_variables_types.ipynb` | 0–37, soit 38 cellules | 6 | ACCEPT | LISIBILITÉ_ÉTUDIANTE_VALIDÉE |
| `TD2_S1_chaines_sequences.ipynb` | 0–32, soit 33 cellules | 7 | ACCEPT | LISIBILITÉ_ÉTUDIANTE_VALIDÉE |
| `TD3_S1_collections.ipynb` | 0–38, soit 39 cellules | 6 | ACCEPT | LISIBILITÉ_ÉTUDIANTE_VALIDÉE |
| `TD4_S1_boucles_conditions_comptages.ipynb` | 0–43, soit 44 cellules | 7 | ACCEPT | LISIBILITÉ_ÉTUDIANTE_VALIDÉE |
| `TD5_S1_fonctions_reutilisation.ipynb` | 0–45, soit 46 cellules | 6 | ACCEPT | LISIBILITÉ_ÉTUDIANTE_VALIDÉE |
| `TD6_S1_fichiers_csv.ipynb` | 0–42, soit 43 cellules | 6 | ACCEPT | LISIBILITÉ_ÉTUDIANTE_VALIDÉE |
| `TD7_S1_expressions_regulieres_pipeline.ipynb` | 0–49, soit 50 cellules | 7 | ACCEPT | LISIBILITÉ_ÉTUDIANTE_VALIDÉE |

## Lecture des changements de présentation

### Procédure générale et tuteur dans le premier TD

La cellule 4 du TD1, `tal-s1-td1-intro-v2`, réunit désormais les instructions générales nécessaires : travailler sur une copie, conserver les cellules et les libellés, séparer essais et réponses, prédire puis exécuter les exemples, réaliser les essais obligatoires, activer `# print` après la création des variables, enregistrer les sorties et déposer le fichier. Le rappel « Faites ces essais même s'ils ne contribuent pas au score automatique » conserve leur statut obligatoire.

Cette cellule distingue le retour technique de la vérification personnelle : « le score ne valide pas leur sens ». Elle présente Gemini une seule fois dans les sept TD : « Le tuteur Gemini peut vous aider à raisonner sur les notions déjà étudiées ou présentées avant l'exercice concerné. » La suite précise les questions, les courtes explications en langage naturel et l'absence de code ou de réponse fournis. Le texte visible est cohérent avec la limite S1 ; il ne prétend pas garantir le comportement réel de Colab.

Le guide général d'autoévaluation n'est pas reconstruit dans les TD suivants. Les instructions locales restantes indiquent où écrire, quel exemple observer, quand effectuer un essai ou quel fichier déposer. Elles ne répètent pas le protocole global du correcteur. Les critères propres aux interprétations, même lorsqu'ils mentionnent le retour automatique, restent nécessaires et ont été conservés.

### Retraits limités et passages conservés

| Support / cellules modifiées, indices zéro | Observation de lecture et comparaison au parent |
|---|---|
| TD1 : 2, 4, 6, 11, 16, 21, 26, 31, 36 | Retrait de la notice d'identification, des budgets et des suffixes de durée ; le cours sur `#`, la prise en main du notebook, les prédictions et la synthèse valeur/type/affectation restent présents. L'explication générale est regroupée en C4. |
| TD2 : 1, 2, 3, 4, 5, 9, 13, 17, 21, 25, 29, 31 | Budget et durées retirés. Le commentaire de notice `# Complétez les informations entre les guillemets.` disparaît en C3 ; les quatre affectations et `# Mes réponses au rappel du TD1 :` restent présents. C2 conserve les questions actives sur variable, valeur, type, `=`, `==`, `len()` et le renvoi au TD1. C31 conserve Q1–Q7, Q1b–Q7b et la synthèse propre aux chaînes. |
| TD3 : 2, 4, 6, 11, 16, 22, 27, 32, 37 | Retrait des notices, du budget, des durées et de l'exposé général de retour automatique. Le partage du lexique entre Q3 et Q4, les exemples distincts, les essais, les prédictions et le choix argumenté des collections restent lisibles. |
| TD4 : 4, 6, 11, 16, 21, 26, 31, 36, 41 | Retrait du budget, de l'identification, des durées et du paragraphe global retour/tuteur. Les prédictions, les essais, les commentaires et la synthèse bornes/filtres/initialisation restent demandés. |
| TD5 : 4, 42 | Tableau horaire, notice d'identification et présentation générale répétée supprimés. C4 conserve l'avertissement d'effectuer les vérifications de fonction après la réponse. C42 conserve le choix d'un test à expliquer, la difficulté ouverte et l'enregistrement des sorties. |
| TD6 : 4, 39 | Même allègement limité. La préparation du fichier, la notion d'identité des personnes dans les données, la normalisation et tous les essais après réponse restent présents. Le retrait de la notice du formulaire ne touche pas l'identité étudiée en Q4. |
| TD7 : 4, 46 | Même allègement limité. L'introduction de `re`, les conventions des fragments, l'ordre du pipeline, les cas vides, les commentaires linguistiques et la synthèse sont conservés. |

La prose a été relue pour sa fonction : cours, exemple, entraînement, réponse à construire, vérification et restitution restent distinguables sans ajout d'un gabarit de rubriques à chaque exercice. Le nettoyage n'introduit pas de note destinée au mainteneur ou au concepteur. Le commentaire de restitution « URL injectée lors du déploiement » est l'exception canonique explicitement conservée par le cadrage ; les sept cellules de restitution restent strictement identiques au parent.

## Preuves par question et par activité

Les tables suivantes couvrent chaque question, ses notions préalables, la production et les essais obligatoires. Dans la colonne « Repères », l'ID de la réponse est donné intégralement ; les autres indices situent le cours, l'exemple et l'entraînement effectivement relus. Chaque énoncé indique la cellule de réponse ou les affichages fournis. Les données et affichages de ces cellules sont fournis ; le traitement et les explications restent à construire par l'étudiant. Les contenus locaux sont inchangés : seuls certains titres perdent leur durée.

### TD1 — Variables et types

| Q / repères | Action, données et production | Acquis et activité préalable | Ambiguïté / conservation |
|---|---|---|---|
| Q1, énoncé 9, réponse 10 `td1-s1-answer-q1` | Calculer le coût de 125 mots à 0.12 dans `cout_total`, afficher Q1 et comparer au calcul manuel. | C5–7 : variable, affectation, multiplication, affichage. Essai C8 : recalculer après modification du nombre de cahiers et expliquer. | Clair ; énoncé, exemple, essai et réponse identiques. Seul le titre C6 perd son minutage. |
| Q2, 14→15 `td1-s1-answer-q2` | Prédire puis afficher le type de `note=14.5`, consigner la prédiction. | C11–12 : types int/float/str/bool et `type`. C13 : comparer 6, 6.0, "6" et choisir le type d'un titre. | Clair ; les trois essais et la justification restent obligatoires. |
| Q3, 19→20 `td1-s1-answer-q3` | Reprendre les données Q1, construire deux booléens et afficher Q3. | C16–17 : comparaisons et `and`. C18 : essais inscrits18/19, distinction `<` et `<=`. | Dépendance Q1 explicite, aucun résultat à recopier fourni. |
| Q4, 24→25 `td1-s1-answer-q4` | Produire la phrase exacte avec les deux langues et une f-string, afficher Q4. | C21–22 : interpolation ; C23 : créer puis modifier une autre annonce et expliquer les accolades. | Noms, apostrophe, espaces et point final conservés. |
| Q5, 29→30 `td1-s1-answer-q5` | Convertir "80", ajouter 20, afficher `volume_corrige` et son type Q5. | C26–27 : conversion, addition et concaténation ; C28 : essais "42" et 3 avec variables nouvelles. | La distinction entre écriture affichée et conversion reste enseignée. |
| Q6, 34→35 `td1-s1-answer-q6` | Choisir sa phrase, afficher longueur/présence de TAL Q6 et source `repr` Q6b, expliquer. | C31–32 : len/in/casse/repr ; C33 : essai distinct TAL/tal. | C34 conserve « le retour automatique ne juge pas sa qualité rédactionnelle » ; choix personnel et interprétation préservés. |

Hors questions : introduction TAL C1, prise en main C2, identification C3, guide C4, synthèse C36 et restitution C37 relus. C36 demande toujours un essai où la prédiction était fausse et un exemple pour chacune des distinctions conceptuelles. Le retrait du rappel global du correcteur n'enlève aucune de ces activités.

### TD2 — Chaînes et séquences

| Q / repères | Action, données et production | Acquis et activité préalable | Ambiguïté / conservation |
|---|---|---|---|
| Q1, 7→8 `td2-s1-answer-q1` | Retirer les espaces de bord de `texte_brut`, afficher texte Q1 et deux longueurs Q1b, expliquer la source conservée. | TD1 variables/len ; C5–6 : méthode, immuabilité et strip sur une autre étiquette. | Toutes les observations et prédictions restent présentes. |
| Q2, 11→12 `td2-s1-answer-q2` | Lower puis remplacer textes par corpus, Q2/Q2b, conserver et vérifier la source, justifier l'ordre. | C9–10 : lower/replace ; `in` TD1 C31. | La question sur l'ordre pour ces données précises et la comparaison au livre restent demandées. |
| Q3, 15→16 `td2-s1-answer-q3` | Extraire premier/dernier/debut/milieu de tokenisation, Q3/Q3b, vérifier la source et expliquer les bornes. | C13–14 : indices, négatifs et tranche ; indices d'archive à prédire sur brouillon. | Bornes exclues et comparaison des deux tranches conservées. |
| Q4, 19→20 `td2-s1-answer-q4` | Découper la phrase, afficher tokens/3e/dernier/longueur, examiner types et unités. | C17–18 : split, liste de chaînes, espaces successifs ; indices Q3. | Distinction caractère/élément explicitement demandée, sans introduire les boucles. |
| Q5, 23→24 `td2-s1-answer-q5` | Join avec " \| ", redécouper exactement, afficher Q5/Q5b et comparer les listes. | C21–22 : join/split séparateur ; prédiction du nombre de séparateurs. Dépend de tokens Q4. | Rôle des espaces autour de la barre et limite de split simple conservés. |
| Q6, 27→28 `td2-s1-answer-q6` | Traiter trois chaînes par indices explicites, créer la nouvelle liste Q6 et afficher la source Q6b. | C25–26 : liste littérale ; strip/lower/indices Q1–3. | Aucune boucle anticipée ; observations sur espaces intérieurs, accents et source inchangées. |
| Q7, 29→30 `td2-s1-answer-q7` | Prédire et observer le split de la phrase exacte ; tokens Q7b et commentaire argumenté Q7. | Split Q4 ; ponctuation, apostrophe et fragments observés dans l'énoncé. | « Le fond de votre explication n'est pas autocorrigé » reste en C29 ; données, critères et production intacts, seul le titre perd la durée. |

Hors questions : C1–4 et C31–32 relus. Le rappel actif des acquis du TD1 est conservé dans son intégralité ; le commentaire supprimé de la cellule d'identification ne portait aucune réponse ni notion. La synthèse demande toujours la distinction chaîne/liste, la borne exclue et une limite de split ; le dépôt reste spécifique au TD2 avec toutes les traces complémentaires.

### TD3 — Collections

| Q / repères | Action, données et production | Acquis et activité préalable | Ambiguïté / conservation |
|---|---|---|---|
| Q1, 9→10 `td3-s1-answer-q1` | Append tokeniseur, montrer Q1a avant pop puis Q1 après retrait. | Listes TD2 ; C6–7 append/pop ; C8 reproduit les trois états avec des villes. | Position des deux affichages explicitée ; aucun état intermédiaire supprimé. |
| Q2, 14→15 `td3-s1-answer-q2` | Tuple des trois langues, choix argumenté Q2 et valeur Q2b. | C11–12 : ordre et mutabilité ; C13 : deux codes, dernier élément et choix liste/tuple. | Les critères du fond non autocorrigé restent dans l'énoncé. |
| Q3, 19–20→21 `td3-s1-answer-q3` | Lexique bilingue trois entrées puis corpus, traduction Q3 et dictionnaire Q3b. | C16–17 : clé/valeur/affectation ; C18 : dictionnaire d'animaux, ajout et réaffectation. | Toutes les traductions admises et la réserve de contexte linguistique restent présentes. |
| Q4, 25→26 `td3-s1-answer-q4` | Parcourir les items du lexique Q3, construire les fiches `anglais -> français`, Q4 final. | C22–23 : premier for, indentation, déballage, append hors réinitialisation ; f-string TD1. C24 : réemploi sur les animaux. | Premier parcours réellement enseigné avant la question ; dépendance Q3 explicite. |
| Q5, 30→31 `td3-s1-answer-q5` | Construire le vocabulaire des six occurrences, Q5 deux comptes et Q5b ensemble. | C27–28 : set/len/casse ; C29 : nouvelle occurrence de poésie et interprétation des comptes. | L'ordre d'affichage n'est pas confondu avec le contenu ; contrôle manuel conservé. |
| Q6, 35→36 `td3-s1-answer-q6` | Comparer les deux corpus par ensembles, communs et seulement_a Q6. | C32–33 : intersection et différence ; C34 : langues communes, deux différences et perte des fréquences. | L'asymétrie de la différence et les interprétations restent présentes. |

Hors questions : C1–5 et C37–38 relus. L'énoncé de progression C2 indique toujours que Q3 et Q4 partagent le lexique. La synthèse C37 conserve les trois choix de structures à justifier, la reprise d'un essai et la comparaison des ensembles.

### TD4 — Boucles, conditions et comptages

| Q / repères | Action, données et production | Acquis et activité préalable | Ambiguïté / conservation |
|---|---|---|---|
| Q1, 9→10 `td4-s1-answer-q1` | Transformer mots en majuscules par for, source et ordre conservés, Q1. | For TD3 C22 ; C6–7 upper et accumulation ; C8 essais sur trois villes. | Explication de l'initialisation hors boucle toujours demandée. |
| Q2, 14→15 `td4-s1-answer-q2` | Filtrer strictement au-delà de cinq caractères dans mots_longs Q2. | C11–12 : if imbriqué ; C13 : filtre <=3 et cas limite de cinq caractères. | Source Q1 et frontière stricte explicites. |
| Q3, 19→20 `td4-s1-answer-q3` | Retenir les mots contenant a sans casse pour le test, garder leur graphie, Q3. | C16–17 : test normalisé et valeur conservée ; C18 essais e/é et o. | Normalisation du test et modification de la source restent distinguées. |
| Q4, 24→25 `td4-s1-answer-q4` | Produire la liste des entiers pairs de 0 à 10 inclus avec range, Q4. | C21–22 : bornes/pas/modulo ; C23 essais inverses et restes de 8/9/10. | Toutes les prédictions et l'explication de la borne exclue restent présentes. |
| Q5, 29→30 `td4-s1-answer-q5` | While des multiples de 7 jusqu'à 70, liste Q5 et prédiction d'arrêt. | C26–27 : état/condition/mise à jour ; C28 liste 2/4/6/8 et première valeur rejetée. | Arrêt et essai non exécuté de boucle sans mise à jour conservés. |
| Q6, 34→35 `td4-s1-answer-q6` | Compter la liste fournie dans un dictionnaire de fréquences, Q6 et somme de contrôle. | C31–32 : get ou if/else ; C33 : prédire les états oui/non et expliquer l'initialisation. | Les deux méthodes restent exposées et autorisées ; aucune nouvelle fonction sum imposée. |
| Q7, 39→40 `td4-s1-answer-q7` | Compréhension des longueurs des mots>5, liste Q7, comparaison à Q2. | C36–37 : compréhension et boucle équivalente ; C38 : carrés des valeurs>2, comparaison des démarches. | Filtre et valeur retournée distingués ; tâche intacte. |

Hors questions : C1–5,41–43 relus. La synthèse reste centrée sur bornes, filtres et initialisation. La phrase conditionnelle héritée sur les essais de fonction en C4 n'introduit aucune fonction à créer dans ce TD : les réponses, les entraînements et leurs emplacements sont explicites. Ce nettoyage n'a ajouté aucune obligation de fonction au TD4.

### TD5 — Fonctions

| Q / repères | Action, données et production | Acquis et activité préalable | Ambiguïté / conservation |
|---|---|---|---|
| Q1, 9→10 `td5-s1-answer-q1` | Définir longueur_texte, retourner un entier, Q1 sur TAL/corpus puis vide. | Len TD1 ; C6–7 def/paramètre/appel/localité/None/return ; entraînement annoncer C8. | Test vide C11 réellement après la définition étudiante ; distinction afficher/retourner intacte. |
| Q2, 15→16 `td5-s1-answer-q2` | Normaliser bords/casse sans modifier les espaces intérieurs, afficher Q2 et tester vide/espaces. | Strip/lower TD2 ; C12–13 transformations ; C14 essais MUSÉE/espaces. | Vérifications C17 conservées après la réponse. |
| Q3, 21→22 `td5-s1-answer-q3` | Compter les fragments en appelant normaliser, afficher Q3, essais vide/espaces multiples. | C18–19 : composition, défaut et split vide ; C20 exercice saluer avec un/deux arguments. | Les deux dimensions, composition demandée et entraînement au défaut, restent couvertes ; vérification C23. |
| Q4, 27→28 `td5-s1-answer-q4` | Traduire via le lexique paramètre après normalisation ; inconnu normalisé ; deux affichages Q4. | Dictionnaires TD3, if/else TD4 ; C24–26 clés, espaces, casse et essais connus/inconnus. | Tests BOOK/Mystery/vide C29 après réponse, autre dictionnaire possible ; clair. |
| Q5, 33→34 `td5-s1-answer-q5` | Traduire chaque fragment par Q4, reconstruire avec un espace et retourner la chaîne, Q5. | For TD4, join TD2 ; C30–31 séparateurs/liste vide, essai C32. | Réemploi sans recopier Q4, tests inconnus/espaces/vide C35 conservés. |
| Q6, 39→40 `td5-s1-answer-q6` | Retourner le résumé à trois clés, nombre de caractères du texte normalisé, Q6. | C36–37 dictionnaire de résultats et tranche vide ; C38 explication de [:1]. | Tests ARCHIVE ORALE/vide C41, cohérence des champs et commentaire obligatoires. |

Hors questions : C1–5,42–45 relus. Le choix d'un test utile, son explication dans C43 et la difficulté ouverte sont conservés ; les sorties doivent toujours être enregistrées. L'avertissement local de C4 sur les vérifications après définition correspond aux six cellules C11/17/23/29/35/41.

### TD6 — Fichiers et CSV

| Q / repères | Action, données et production | Acquis et activité préalable | Ambiguïté / conservation |
|---|---|---|---|
| Q1, 10→11 `td6-s1-answer-q1` | Lire affiliations_s1.txt avec with/open UTF8 ; texte et longueur Q1. | Préparation fournie C5–6 ; C7–8 : lecture/fermeture ; C9 : relire le fichier exemple et comparer. | La préparation Path reste fournie ; elle n'est pas transformée en compétence de réponse. |
| Q2, 15→16 `td6-s1-answer-q2` | Splitlines, retirer les lignes vides/espaces, conserver l'ordre et afficher le nombre Q2. | C12–13 : fins de ligne et test strip ; C14 : boucle de filtrage du texte exemple. | Dépendance Q1 et cas limite de ligne d'espaces conservés. |
| Q3, 20→21 `td6-s1-answer-q3` | Lire les lignes Q2 par split(';',1), liste ordonnée de couples, Q3/Q3b. | C17–18 : maxsplit ; C19 : exemple à plusieurs points-virgules et espaces. | Les couples peuvent être liste ou tuple ; deux chaînes et graphies sources exigées. |
| Q4, 25→26 `td6-s1-answer-q4` | Normaliser personne, espaces intérieurs et title ; Q4/Q4b sur variantes de Durand. | Fonctions TD5 ; C22–23 : split/join/title et limite d'identité ; essai Lamy Zoé C24. | Vérification C27 après réponse ; distinction graphie/identité non supprimée avec la notice du formulaire. |
| Q5, 31→32 `td6-s1-answer-q5` | Regrouper les affiliations en ensembles par personne normalisée ; Durand Q5 et dictionnaire Q5b. | C28–29 : set vide/add ; C30 : Studio ajouté deux fois ; dict/sets TD3, fonction Q4. | Vérifier toutes les personnes C33 reste demandé ; ordre libre inchangé. |
| Q6, 37→38 `td6-s1-answer-q6` | Écrire CSV UTF8/newline, trois colonnes, une ligne par personne et séparateur interne ; relire Q6. | C34–35 : utilité/module/objet writer/writerow/exemple ; C36 : créer un autre CSV, relire et distinguer en-tête/données. | Données Q5, nombre d'affiliations, ordres libres et affichage repr fourni conservés. |

Hors questions : C1–6,39–42 relus. Le parcours de découverte de csv reste progressif : utilité, import, objet et méthode, exemple exécuté par l'étudiant, manipulation distincte puis réemploi. La synthèse garde le choix d'un test et son explication C40. Aucun service externe ni nouvelle bibliothèque n'est ajouté.

### TD7 — Regex et pipeline

| Q / repères | Action, données et production | Acquis et activité préalable | Ambiguïté / conservation |
|---|---|---|---|
| Q1, 11→12 `td7-s1-answer-q1` | Rechercher TAL sans casse et stocker le booléen tal_present Q1. | C5–6 : utilité/import re ; C8–9 : raw/search/None/bool/IGNORECASE/match/point ; C10 essais archive/absence. | L'import fourni n'est pas assimilé au cours : l'explication précède le travail demandé. |
| Q2, 16→17 `td7-s1-answer-q2` | Extraire toutes les séquences de chiffres en chaînes ordonnées, Q2. | C13–14 : classe et quantificateur+ ; C15 essais Lot7/36/absence et explication. | Type chaîne sans conversion explicite, ordre conservé ; clair. |
| Q3, 21→22 `td7-s1-answer-q3` | Suites de lettres accentuées et commentaire comparant split, Q3. | C18–19 : classes étendues et convention d'unité ; C20 essais île/apostrophe. | Critères du commentaire et limite de convention universelle inchangés. |
| Q4, 26→27 `td7-s1-answer-q4` | Substituer les dates de forme JJ/MM/AAAA par [DATE], autres caractères intacts, Q4. | C23–24 sub et quantités exactes ; C25 exemple complet/incomplet distinct. | Test de forme C28 après réponse ; forme/calendrier distingués. |
| Q5, 32→33 `td7-s1-answer-q5` | Fonction ordonnée lower/date/chiffres/espaces, chaîne retournée Q5 et conséquence de l'ordre. | Fonctions TD5 ; C29–30 ordre et casse du marqueur, prédictions C31. | DATE reste majuscule ; tests vide/espaces/date C34 après définition, ponctuation non visée conservée. |
| Q6, 38→39 `td7-s1-answer-q6` | Réutiliser Q5 et convention Q3, compter puis retourner trois clés, Q6. | TD4 fréquences, TD5 composition ; C35–36 pipeline/comptage et prédiction C37. | Test vide/autre texte C40, cohérence des effectifs et commentaire sur DATE toujours exigés. |
| Q7, 44→45 `td7-s1-answer-q7` | Limite regex personnelle : cas français, information linguistique manquante, réponse Q7. | C41–42 : forme/sens, exemple porte, * et+ ; C43 essai a5b, fragments vides, autre phénomène. | « Le retour automatique constate la présence d'une réponse ; il ne valide pas cette analyse » conservé mot pour mot. |

Hors questions : C1–8,46–49 relus. Introduction du module, fonctions/objets nécessaires et exemples précèdent leurs réemplois ; aucune liste de résultats n'a remplacé la découverte. C46–47 conservent le test utile à expliquer et la difficulté ouverte. Les conventions linguistiques et interprétations ne sont pas réduites.

## Constats, conservation et preuves distinctes

Aucun nouveau constat bloquant ou demande de reprise éditoriale dans le périmètre autorisé. Les anciennes notices du TD2 modèle, les contradictions du contrôle et les lacunes de prérequis du DM ne sont ni modifiées ni déclarées résolues. Le présent ACCEPT porte sur les sept TD identifiés, pas sur tous les supports S1.

| Point contrôlé | Résultat et preuve |
|---|---|
| Minutages et identification | Lecture de toutes les cellules visibles : plus de budgets, tableaux horaires, durées ni notices détaillant les champs du formulaire. Les quatre affectations de chaque TD restent inchangées. |
| Procédure unique et Gemini | Présentation générale en TD1 C4 ; aucune présentation de Gemini dans TD2–7. Les anciens paragraphes globaux du retour automatique ont disparu ailleurs. Les vérifications locales et restitutions nécessaires restent disponibles. |
| Limites locales essentielles | TD1 C34 Q6 et C33 essai, TD2 C29 Q7, TD7 C44 Q7 ; texte identique au parent, sauf retrait du minutage du titre TD2 C29. Les productions, les critères du fond et les commentaires restent demandés. |
| Activités conservées | 45 réponses, 44 exemples, 52 cellules d'essai/vérification/synthèse, deux préparations et sept restitutions identiques au parent. Les activités mêlées aux énoncés et réponses ont aussi été relues dans les 45 lignes ci-dessus. Aucune activité déplacée dans un support futur ou rendue facultative. |
| Seul changement de code | TD2 C3 : retrait exact du commentaire de notice. Quatre affectations, commentaire de rappel, AST, métadonnées et sorties inchangés. Toutes les autres sources de code sont strictement identiques. |
| Tuteur en double | Sept premières cellules complètes identiques au parent, titre visible puis HTML caché. Texte entre les marqueurs identique exactement au contexte Colab, sans normalisation du texte. Profils structurés égaux aux séances du manifeste, métadonnées racines intégralement identiques. |
| Périmètre des notions | Lecture des cours préalables dans les tables : aucune permission nouvelle ; TD1–5 sans bibliothèque, csv seulement TD6 Q6, re introduit avant TD7. Path et IPython restent des outils fournis. Les règles S1 interdisent code, solution et modification de cellules par le tuteur. |
| Contrat et distribution | Structure, ordre, IDs, rôles, questions, métadonnées, sorties et exécutions inchangés. Les sept restitutions conservent exactement `__TAL_PUBLIC_URL__` et leur HTML, sans adresse privée ni sortie enregistrée. L'injection de distribution relève de la vérification technique séparée. |

Vérifications auxiliaires exécutées indépendamment : lecture du diff intégral produit cellule par cellule contre `git show 590b9a6:<chemin>` ; assertions JSON sur structure, métadonnées, cellules protégées et sources ; comparaison de l'AST de l'unique cellule de code modifiée ; égalité exacte des contextes HTML/Colab et des profils/manifeste sur les sept fichiers ; vérification complémentaire de l'absence de durées et de notices dans le texte visible ; calcul des empreintes ci-dessous. Ces contrôles ont réussi. Ils accompagnent la lecture exhaustive et ne la remplacent pas.

Aucune cellule de réponse, aucun corrigé ni exemple n'a été exécuté par ce rôle pour cette revue. L'exécution humaine en classe, la durée réelle et le comportement effectif de Gemini/Colab sont **NON_TESTÉS**. Aucun score automatique n'est présenté comme preuve de compréhension. Le verdict pédagogique `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`, la revue technique et la gouvernance sont des avis distincts à recueillir dans le workflow ; ils ne sont pas déduits de cet avis éditorial.

Le rapport indépendant `Corrigés modèles/TD/s1-presentation-cleanup/lecture_etudiante.md` a été lu intégralement avant ce relais. Il porte sur les mêmes sept empreintes, les 293 cellules et les 45 questions, sans accès aux corrigés, matrices, correcteurs ou tests, et sans résolution ni exécution. Il confirme que les données, productions et critères sont compréhensibles, que le guide général et Gemini sont présentés au TD1 et qu'aucune nouvelle ambiguïté précise n'empêche d'engager une question. Il relève le commentaire technique des cellules finales sans demander sa modification dans cette mission : sa conservation canonique est explicitement prévue par le cadrage. Cette lecture complète l'avis éditorial sans constituer un essai auprès de vrais étudiants.

## Empreintes de la version relue

| Support | SHA-256 |
|---|---|
| TD1 | `94abfa27d9b6a21395f60c91f0b8ca149cfcf20b5248799df0feec6f0aa338c3` |
| TD2 | `5d5e0ecc6650e07acf4a4b1695963802cbad3298df41053976d2d30d0636eed3` |
| TD3 | `822aeab68461784d9fa0e410ae18a37bb295486aecb46657e1bce0981c7944e8` |
| TD4 | `fc82a243ba0c09d1a7d1a89203885c78381ccf323a2a3a8c0d93d991b18a0e51` |
| TD5 | `2e2dbc49943a2070b8ad7c155c377a2e30fe8db0fa58e5fd09f70d9c8668b3cf` |
| TD6 | `01e00fff36a012f091097794d1d62b0f9255976fc61a8299366238b131b165d8` |
| TD7 | `b7ff9f64672c0886543a27a5079638f79f8eab4127553d2c1b2b7aaab4489f79` |

## Verdict et relais

**ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE**, pour le nettoyage de présentation des sept TD S1 à ces empreintes. Les 293 cellules et les 45 questions ont été relues ; aucune réduction de cours, exemple, essai, production ou interprétation n'a été relevée. Les notices et minutages retirés correspondent à l'autorisation, la procédure générale est réunie au TD1 et les limites locales restent à leur emplacement utile.

Le périmètre de cet avis ne lève pas le verdict global de l'audit S1, ni les blocages des supports exclus de cette PR. Relais demandé : joindre les avis indépendants pédagogique, technique, de lecture étudiante et de gouvernance ; l'intégration peut alors préparer la PR selon ses propres obligations d'indépendance. Aucune décision de fusion ou de publication en production n'est rendue par ce rapport.
