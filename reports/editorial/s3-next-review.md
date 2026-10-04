# Revue éditoriale indépendante — TD suivants du S3

## Périmètre et méthode

Mission du 3 octobre 2026, branche `pedagogy/s3-next-review`, par TAL-Editorial-Reviewer (`next_editorial_review`), distinct des Designers et de l'intégration. Référence technique : `cdc52d08cc02c8880003d962d0631658f04392c1`, après fusion de la PR25. La présente revue ne modifie aucun notebook, profil de tutorat ou correcteur.

Lecture exhaustive des **311 cellules** de sept notebooks, code et commentaires compris, **46 questions**, ateliers, bilans et README S3. Les indices ci-dessous commencent à zéro. Tous les chemins de notebooks sont dans `Notebooks TD/S3/`.

| Fichier | Cellules relues | Questions |
|---|---:|---:|
| `TD1B_S3_entites_similarite_regles.ipynb` | 0–35 (36) | 4 |
| `TD2_S3_analyse_corpus.ipynb` | 0–38 (39) | 7 |
| `TD3_S3_concordances_citations.ipynb` | 0–39 (40) | 7 |
| `TD4_S3_cooccurrences.ipynb` | 0–46 (47) | 7 |
| `TD5_S3_associations.ipynb` | 0–45 (46) | 7 |
| `TD6_S3_visualisations.ipynb` | 0–52 (53) | 7 |
| `TD7_S3_audit_llm.ipynb` | 0–49 (50) | 7 |

La matrice `docs/pedagogy/s3_next_review_coverage.md`, validée par le réviseur pédagogique avant conception, a été lue avant les supports. Comparaison des TD2–TD7 avec la référence historique `2a36752` et le parent technique `cdc52d0` ; les repères ajoutés dans les versions intermédiaires sont également présents dans ce parent. Comparaison de TD1B avec `7fdfcd9`, `638b593` et le parent, ainsi qu'avec les activités NER, extraction, similarité et règles de la pièce historique `TD_0_Initiation_spacy.ipynb` (cellules 10–26, références `ea566d77`, `c9f03004`, `84e644b6`, `87830824`, `qZggeSjZ9-pQ`). La matrice historique `s3_r2_spacy_editorial_coverage.md` a également été consultée. Les autres anciens sujets TAL, hors de cette filiation documentée, ne sont pas déclarés restaurés.

La lecture a suivi chaque donnée et chaque production attendue, puis les notions et exemples antérieurs. Les comparaisons de lignes anciennes ont servi à repérer les déplacements du cours et des exemples ; elles ne remplacent pas la lecture des textes réécrits. Les réponses techniques conservées n'ont pas été remplies ni exécutées.

## Lecture par question

Dans les tables, « réponse » désigne la cellule de code immédiatement associée à la consigne. TD2/3 placent prédiction et interprétation en commentaires ou sorties de cette cellule ; les autres TD disposent de cellules Markdown d'observations explicitement désignées. Les cours et exemples fournis restent distincts des calculs demandés.

### TD1B — Cours de bibliothèque puis réemploi

| Question / cellules | Action et données | Production et emplacement | Acquis et explication antérieurs | Autonomie et conclusion de lecture |
|---|---|---|---|---|
| Q1, 9–13, `td1b-q1-consigne` | Prévoir les informations Apple/Allemagne/date/montant, puis observer les entités | Liste complète ordonnée `entites_q1`, réponse 13 ; anticipation et comparaison en 12 | TD1 Doc/Token ; 9 définit Span, ents, labels ; exemple 10 | Manipulation guidée ; catégorie absente distinguée d'une erreur possible. Aucun résultat linguistique à inventer. |
| Q2, 14–18, `td1b-q2-consigne` | Détecter puis filtrer PER/ORG sur texte fixé et texte personnel | Quatre listes, second texte ; réponse 17, observation 18 | Q1 ; 14 distingue détection/extraction/faux positif, exemple LOC 15 | Filtre guidé, texte libre ; ordre et répétitions explicités ; essai personnel non certifié linguistiquement. |
| Q3, 19–23, `td1b-q3-consigne` | Comparer deux couples de mots, deux phrases et une variation choisie | Vecteurs/scores nommés, textes de variation ; réponse 23, prédictions/limites 22 | 19 définit vecteur, score, moyenne ; exemple distinct 20 | Variation autonome conservée ; ni classement sémantique imposé ni score assimilé à une vérité. |
| Q4, 24–31, `td1b-q4-consigne` | Toulon avant/après, trois règles libres supplémentaires, cinq essais avec variante/ambiguïté | Règles, pipeline et traces dans réponse 30 ; tableau attendu/observé et bilan 31 | 24–25 enseignent EntityRuler et place avant ner ; 26–28 montrent conservation des essais, label DATE personnalisé | Construction guidée puis choix autonomes ; chaque règle doit aussi être éprouvée en correspondance exacte. La mise en forme fournie ne réalise aucune analyse à la place de l'étudiant. |

Préparation 1–8 : bibliothèque, modèle md, chargement et installation distingués ; variables des textes et affichage JSON fournis annoncés. Bilan 32–33 : trois méthodes et trois erreurs possibles conservées ; critères pour les quatre exercices. Restitution 34–35 : séparateur, sauvegarde et dépôt. Le texte annonce exactement quatre points techniques et conserve la critique linguistique sans promettre une relecture individuelle systématique.

### TD2 — Compter, filtrer et représenter

| Question / consigne | Action et données | Production et emplacement | Acquis / cellules antérieures | Autonomie et conclusion |
|---|---|---|---|---|
| Q1, 9, `0910116a4331` | Lire le microcorpus UTF-8, distinguer caractères/tokens/phrases | Trois entiers et dix annotations dans réponse 10 ; commentaire forme/lemme | TD1 annotations ; rappel 7 et exemple exécutable `open` 8 | Unités explicites, fichier distinct de Faguet ; fonction du cours indépendante de la consigne. |
| Q2, 14, `6b03a2dee4a6` | Deux fonctions de fréquences noms/verbes, tests phrase répétée et corpus | Comptes complets dans réponse 15, top cinq pour lecture seulement | 11–12 Counter/return/total ; 13 None/exclusions/argument/VERB-AUX | Étapes annoncées ; tests et distinction des deux exclusions conservés, pas de fonction solution. |
| Q3, 20, `dbb99a0dfe33` | Choisir un nom présent à exclure selon une question d'analyse | Avant/après, liste personnelle, justification ; essai 19 puis réponse 21 | 16–18 expliquent filtre et invariant sur autres comptes | Choix libre conservé ; effet sur femme/homme discuté ; lien vers Q6 et filtre vide explicite. |
| Q4, 23, `97e0baba0c8c` | Distribution POS hors ponctuation/espaces | Dictionnaire complet, top3, limite dans réponse 24 | 22 rappelle distribution, somme et égalités | Ordre libre des ex æquo, entier distinct de booléen ; aucune conclusion thématique automatique. |
| Q5, 27, `e1fafdbee7f2` | Liste de mots pleins et cinq observations réelles ; distinguer objets Gemini | Liste ordonnée répétitions incluses, annotations/jugement, limite ; réponse 28 | TD1 filtres ; cours PhraseMatcher 25, exemple 26 | Choix des occurrences autonome ; lecture du motif sans tâche cachée de programmation de bon sens. |
| Q6, 31, `8bac30105f01` | Nuage et barres du même compte de Q3 | Deux figures, fréquences/hypothèse/vérification dans réponse 32 | 29 explique WordCloud/Matplotlib ; exemple à deux figures 30 | Lien Q3 explicite ; retour au filtre si vide ; hypothèse distincte d'importance graphique. |
| Q7, 33, `2ef5275cac37` | Généraliser POS, égalités et cas vides ; transférer à 5 000 caractères | Cinq comptes/comparaison dans réponse 34 ; transfert séparé | Fonctions Q2, filtres Q3/5 | Problème autonome annoncé ; microcorpus de correction séparé de l'extrait de Faguet. |

Introduction, installation et export 1–6, 35–38 relus : actions utiles à l'étudiant, R2 comme recours, fichiers de session à télécharger, fonctions à conserver. Les anciens exemples sont exécutables, commentés et placés avant usage ; leur contenu n'est pas retiré. Les notes de fabrication ont disparu.

### TD3 — Revenir à la source

| Question / consigne | Action et données | Production et emplacement | Acquis / cellules antérieures | Autonomie et conclusion |
|---|---|---|---|---|
| Q1, 10, `ede8b619b42d` | Lire provenance et conversation, établir le périmètre | Empreinte, six IDs, prompts, paramètres absents, limite ; réponse 11 | 9 explique empreinte/version/convention et donne fichiers et lien README figé `cdc52d0` | Accès aux sources rendu explicite ; absence non remplacée par hypothèse. |
| Q2, 17, `6dfa6e72ddd7` | Fonction concordances non chevauchantes, quatre tests manuels, source_test et Faguet | Liste structurée et absence dans réponse 18 ; table tests et trois contextes séparés | 7–8 find/tranches ; 12–16 contexte, reprise, while, raise/except | Fonction à construire, mécanismes montrés sur autres données ; absence distincte d'erreur et fin exclue expliquées. |
| Q3, 23, `b3861304ce29` | Fragment lit, forme lit, lemme lire ; réemploi sur Faguet et bon sens | Trois listes de formes/positions, explication ; réponse 24 | 19–22 rappellent formes/lemmes, PhraseMatcher et Span.start_char/end_char | Comparaison et adaptation effectives conservées ; positions de tokens et caractères distinguées. |
| Q4, 25, `aa31f6af9aeb` | Trois citations, recherche exacte sans transformation | IDs/textes/débuts/booléens et limite ; réponse 26 | Q2 et rappel find | Réemploi autonome ; -1 explicitement prévu ; absence exacte ne réfute pas l'idée. |
| Q5, 30, `a81cf330c3da` | Normaliser les absences, localiser C1 autour de légalement | Passage exact/position originale, différence et verdict ; réponse 31 | 27–29 fonction fournie sur autre texte, positions déplacées et catégories d'écarts | Argumentation libre et observation des mots maintenues ; copie normalisée ne remplace jamais la source. |
| Q6, 32, `8373304e4726` | Deux passages professions, règle de lecture, tests exact/altéré personnels | Deux cas et règle dans réponse 33 ; passages et comparaison conservés | Q2–5 sans nouvelle bibliothèque | Travail autonome ; attendu écrit avant recherche ; proximité distincte de conformité. |
| Q7, 34, `abcdbeabe3b2` | Choisir G1/G2, trois occurrences distinctes et convention proposée | Preuves avec bornes/passages, convention et limite ; réponse 35 | Q2–3 recherche, cours fenêtre/agrégation dans consigne | Choix de contexte libre ; frontières du mot et trois occurrences, pas trois fenêtres d'un pivot, explicités. |

Préparation, sauvegarde et restitution 1–6, 36–39 relues. Le lien de provenance lu dans la version finale pointe sur le parent qui contient effectivement la notice. L'activité n'est pas remplacée par une fiche déjà remplie. Les explications linguistiques restent demandées, avec critères de reprise personnelle.

### TD4 — Conventions de comptage

| Question / consigne | Action et données | Production et emplacement | Acquis / cellules antérieures | Autonomie et conclusion |
|---|---|---|---|---|
| Q1, 10, `s3-td4-05` | Présences, marge et N sur microcorpus puis phrases Faguet | Fonction et trois clés ; réponse 11, observation 12 | TD3/TD1 ; cours présence 8, exemple 9 | Prédiction et vide conservés ; représentation de présence distinguée du flux de distance. |
| Q2, 16, `s3-td4-08` | Cooccurrence booléenne, trois paires et deux paires Faguet | Fonction/tests/preuves ; réponse 17, observation 18 | Q1 ; 13–15 assert et symétrie/marges | Assertions expliquées avant usage ; phrase commune distinguée de lien grammatical ou adhésion. |
| Q3, 21, `s3-td4-11` | Union de contextes et somme de paires ; ligne Intelligence | Deux mesures et champs manquants ; réponse 22, observation 23 | 19 tableau distinct, 20 deux agrégations ; fonction Q2 | Double comptage rendu compréhensible, aucune conclusion imposée sur Gemini. |
| Q4, 27, `s3-td4-14` | Fenêtre de positions, k1/k3 et Faguet k5/k10 | Fonction, paires manuelles, indices ; réponse 28, observation 29 | 24–26 token.i/idx, enumerate/abs, TD3 ValueError | Flux non filtré prescrit avant tâche ; preuves de distance conservées. |
| Q5, 31, `s3-td4-17` | Frontières phrase/paragraphe/flux global | Deux traces et trois mesures Faguet ; réponse 32, observation 33 | Q1/2/4 ; exemple frontières 30 | Retours normalisés dans copie seulement ; unités différentes, cas non trouvé accepté explicitement. |
| Q6, 36, `s3-td4-20` | Compter clé forme/lemme, cinq observations et expression | Deux comptes, tableau et essai expression ; réponse 37, observation 38 | 34–35 dictionnaire, TD3 expression ; convention espaces explicite | Famille/lemme séparés ; jugement humain conservé sans écraser modèle. |
| Q7, 41, `s3-td4-23` | Composer mesurer_phrase, bornes/vide, export deux paires | Quatre nombres, fichier td4_mesures, bilan ; réponse 42, observation 43 | Q1–6, rappel JSON 6–7 et export 39–40 | Assemblage autonome ; mesures par phrase/fenêtre séparées, fonctions conservées pour TD5. |

Introduction et préparation 1–7 relues, y compris code fourni et distinction fichiers/fonctions. Bilan 44, séparateur 45 et HTML 46 relus. Le contenu des anciens repères est conservé ; seule la justification « intégré au temps… sans nouvelle question notée » est retirée.

### TD5 — Dénominateurs et limites

| Question / consigne | Action et données | Production et emplacement | Acquis / cellules antérieures | Autonomie et conclusion |
|---|---|---|---|---|
| Q1, 11, `s3-td5-05` | Dessiner huit phrases compatibles et calculer deux proportions | Fonction, deux clés, commentaires dénominateurs ; réponse 12, observation 13 | TD4 ; tableau distinct 8 et cours/exemple 9–10 | Les huit cases ne se confondent plus avec les quatre cases du tableau de contingence. |
| Q2, 15, `s3-td5-08` | Comparer A/B et deux associés Faguet | Conditionnelles/bases, tableau et lecture ; réponse 16, observation 17 | Q1 ; exemple de concentration 14 | Effectif et concentration distingués ; pas de significativité déduite. |
| Q3, 20, `s3-td5-11` | Taux court/long et deux moitiés alphabétiques de Faguet | Fonction/taux/tailles/indices ; réponse 21, observation 22 | 18–19 pour mille ; None annoncé en 8 | Taille nulle explicitement indéfinie ; moitiés jamais renommées chapitres. |
| Q4, 24, `s3-td5-14` | Inverser les conditions, tests et tableau 2×2 | Deux proportions, quatre effectifs/commentaires ; réponse 25, observation 26 | Q1 et cours 23 | Populations explicitées, fonction/test autonome ; tableau descriptif sans test statistique. |
| Q5, 30, `s3-td5-17` | Absences, 1/1 vs20/20, terme rare | None/zéro et inspection ; réponse 31, observation 32 | 27–29 cours et exemple d'arrondi conditionnel | Zéro/indéfini distincts ; PMI reste facultative, hors séance et après prérequis. |
| Q6, 36, `s3-td5-20` | Couverture par position, k1/k3 puis trois fenêtres Faguet | Fonction, ratios, numérateur/dénominateur ; réponse 37, observation 38 | TD4 positions ; 33–35 paires/couverture et exemple | Chaque pivot compté au plus une fois ; absence de protocole LLM non comblée. |
| Q7, 40, `s3-td5-23` | Relier effectif/dénominateur, exporter deux paires et expliquer | Trace Q1 réutilisée, fichier, paragraphe ; réponse 41, observation 42 | Q1–6 ; 39 résultat vérifiable et JSON 6–7 | Deuxième paire à compléter explicitement, observations/explications/limites séparées. |

Préparation 1–7 et bilan/restitution 43–45 relus. Deux paires de Faguet et leurs trois fenêtres restent dans le livrable ; aucune analyse n'est supprimée pour réduire la charge de l'enseignant.

### TD6 — Valeurs, figures et retour au texte

| Question / consigne | Action et données | Production et emplacement | Acquis / cellules antérieures | Autonomie et conclusion |
|---|---|---|---|---|
| Q1, 13, `s3-td6-06` | Positions relatives, dispersion trois pivots, deux passages | Listes et figure/légende ; réponse 14, observation 15 | TD4 ; atelier 9–10 ; eventplot expliqué 11, exécuté 12 | Une figure montre une distribution sans expliquer un thème ; i/N défini. |
| Q2, 18, `s3-td6-09` | Segmentation microcas puis 11 tokens et dix segments Faguet | Effectifs/tailles/bornes ; réponse 19, observation 20 | 16–17 bornes, vide, somme | Flux complet et dénominateur alphabétique distingués ; segments vides non convertis en taux zéro. |
| Q3, 24, `s3-td6-12` | Taux puis matrice trois pivots/dix segments | Matrice, bruts, carte et case à lire ; réponse 25, observation 26 | 21–23 axes/couleurs, imshow/colorbar et exemple | Même échelle prescrite ; importance thématique non inférée de la couleur. |
| Q4, 29, `s3-td6-15` | Sensibilité des paires aux fenêtres, couverture séparée | Petit cas, table, deux courbes ; réponse 30, observation 31 | TD4/5 ; plot expliqué 27–28 | Deux unités distinguées, classement interprété dans les limites du test. |
| Q5, 35, `s3-td6-18` | Tranche join du petit cas, occurrences de la case choisie, source exacte | Bornes/contexte, trois occurrences ou toutes, tableau preuves ; réponse 36, observation 37 | TD3 ; 32–34 indices/source originale | Join limité au petit cas ; original retrouvé sans reconstruction ; lecture de négation/citation conservée. |
| Q6, 40, `s3-td6-21` | Barres du petit cas, matrice cooccurrences, relecture par un voisin | Figure/table/légende/correction concrète ; réponse 41, observation 42 | Q3 et TD4 ; cours/exemple bar 38–39 | Diagonale nulle conventionnelle expliquée ; activité entre pairs conservée, pas de promesse de relecture enseignante. |
| Q7, 47, `s3-td6-24` | Agréger effectifs avant taux, exporter figures et données | Taux global, fichier, deux paragraphes et préparation TD7 ; réponse 48, observation 49 | 43–46 somme pondérée et savefig avant show | Distante/proche articulées ; figures et trois références conservées. |

Préparation 1–10 et bilan/restitution 50–52 relus. Les fragments Matplotlib sont désormais exécutables et leur vocabulaire expliqué ; les imports fournis ne tiennent pas lieu de tutoriel. Aucun graphique ni réemploi n'a été retranché.

### TD7 — Audit assemblé progressivement

| Question / consigne | Action et données | Production et emplacement | Acquis / cellules antérieures | Autonomie et conclusion |
|---|---|---|---|---|
| Q1, 13, `s3-td7-07` | Champs manquants et six annonces originales | Booléen/liste, tableau original/choix ; réponse 14, observation 15 | Atelier 8–9 ; champs/get/None 10–11 ; protocole 12 | Ambiguïtés et original conservés ; mesurable n'est pas vrai. |
| Q2, 19, `s3-td7-10` | Assembler expressions contiguës et moteur union ; une ligne Faguet | N/cooc/marges, indices preuves et tests ; réponse 20, observation 21 | TD3–5 ; 16–18 tranche, expressions alternatives, marge | Architecture décomposée sans moteur fourni ; espaces ignorés pour expressions seulement. |
| Q3, 24, `s3-td7-13` | Citations exactes/candidats/non localisées | Trace microcas, trois citations et différences ; réponse 25, observation 26 | TD3, rappel/find 22–23 | Option difflib hors séance ; aucune certification par proximité. |
| Q4, 30, `s3-td7-16` | Comparabilité puis intervalle et bornes | Deux libellés, garde et ligne réelle ; réponse 31, observation 32 | 27–29 statuts et intervalle inclusif | Absence de protocole bloque verdict de réfutation ; recomptage séparé. |
| Q5, 34, `s3-td7-19` | Somme de paires, six regroupements explicites et visualisation | Deux recomptages, marges/preuves, figure ; réponse 35, observation 36 | Q2, TD6 ; 33 deux agrégations et import pour reprise | Variantes choisies ouvertement, aucune méthode choisie pour rejoindre Gemini. |
| Q6, 39, `s3-td7-22` | Référence manuelle livre/plume, autre cas voisin, limites et cinq annotations | Résultats/tests/écarts pour export ; réponse 40, observation 41 | 37–38 tableau attendu avant exécution et généralité | Données indépendantes de spaCy, correction motivée par écart ; aucune garantie universelle. |
| Q7, 44, `s3-td7-25` | Fonction auditer et recomptage séparé, assembler le dossier | Deux statuts, six lignes/3 citations/lot manuel, tableau, synthèse de 200–300 mots / figure / 3 passages ; réponse 45, observation 46 | Q1–6, 42–43 assemblage et cohérence | Synthèse construite depuis les travaux précédents ; critères d'autoévaluation remplacent la promesse de relecture sans réduire le dossier. |

Introduction, préparation et atelier 1–12, bilan/restitution 47–49 relus. La densité demeure importante : les deux heures supposent des fonctions antérieures disponibles et des notes assemblées en continu. Ce n'est pas une durée mesurée en classe. Cette limite est annoncée ; aucun exercice obligatoire n'est rendu facultatif.

## Constats et conservation

Aucun blocage éditorial n'a été découvert dans les textes visibles finaux. Les notes sur la fixation des versions, la fabrication des repères et la substitution d'une ancienne variante graphique ont quitté le cours ; leurs activités utiles sont toujours présentes. Les titres, cours, exemples, consignes, espaces de réponse, commentaires de code et vérifications ont l'étudiant pour destinataire. Le commentaire canonique de restitution « URL injectée lors du déploiement » reste l'exception de format explicitement demandée par l'enseignant, sans devenir un cours d'infrastructure.

Les consignes TD2/3 remplacent les paragraphes compacts par buts, productions et vérifications lisibles. TD4–7 séparent les conventions théoriques et exemples de la tâche à programmer. Les fonctions, tests manuels, transferts à Faguet, figures, commentaires et synthèses des sources comparées restent exigés. Aucun déplacement vers un support à venir ne sert de preuve de conservation.

La réduction de charge enseignante vient de critères d'autoévaluation et de la délimitation du score. Aucun texte ne promet la correction automatique de la qualité linguistique ni la lecture systématique des interprétations par l'enseignant. La relecture par un voisin de TD6/7 reste une activité étudiante effective.

| ID | Gravité / état | Constat | Critère de résolution |
|---|---|---|---|
| TAL-EDIT-S3NEXT-001 | Résolu | Des permissions anciennes du tuteur (`any`, `scatter`, `axvline`, `savefig` avant introduction) ont été signalées avant synchronisation. | Relecture finale : `any` retiré de TD4 Q3 et TD5 Q6 ; `scatter`/`axvline` retirés des périmètres non enseignés ; `savefig` limité à Q7 du TD6. Copies complètes identiques. |

## Vérifications finales et limites

Relecture après synchronisation : les sept contextes complets présents dans les métadonnées Colab sont contenus à l'identique dans le commentaire HTML de la première cellule Markdown. Les sept empreintes `tal_tutor.context_sha256` correspondent à ces contextes. Les profils structurés et leurs identifiants de séance sont présents. Les règles communes imposent une question ciblée puis attente si une résolution est demandée, un exemple distinct en cas de blocage, aucun travail à la place de l'étudiant et les seuls acquis permis pour la question. Les phases entités, similarité et règles de TD1B restent séparées. PhraseMatcher est autorisé après son explication ; les méthodes graphiques suivent leur introduction. PMI et difflib restent des prolongements explicitement conditionnés. Les imports de préparation ne deviennent pas des permissions de réponse.

Les sept restitutions finales contiennent le placeholder `__TAL_PUBLIC_URL__`, après un séparateur ; aucune sortie n'est enregistrée dans les sept sources. La présence du contexte machine est une vérification structurelle, pas une preuve que Colab respecte les règles.

Les cellules TD6 `s3-td6-18`, `s3-td6-21` et `s3-td6-23` ont été relues après les derniers ajustements : changer de case en l'annonçant permet de chercher effectivement négation/citation/opinion ; si le voisin ne demande pas de modification graphique, le nombre et le passage retrouvés restent une preuve de relecture. Ni l'analyse de contexte ni l'échange entre pairs ne disparaissent.

La note `Corrigés modèles/TD/s3-next-review/lecture_etudiante.md` apporte une seconde lecture des 46 questions, sans exécution ni accès aux correcteurs. Sa réserve initiale TD6 Q5 a motivé la clarification ci-dessus. Les réserves de durée et de travail en présence d'un voisin demeurent des conditions d'organisation à annoncer, pas des acquis manquants dissimulés. L'inventaire de lecture de cette note concorde avec 311 cellules.

Contrôles exécutés personnellement : lecture JSON de chaque cellule, comparaison des sources par `git show`, calcul SHA-256, égalité des deux contextes, vérification des SHA de profils et des sorties vides. L'intégration annonce séparément 293 tests et 39 exemples fournis exécutés avec succès, plus le contrôle de 35 tuteurs et la préparation de 34 notebooks distribués. Ces annonces techniques ne fondent pas le verdict de lisibilité.

### Empreintes des supports relus

| Support | SHA-256 |
|---|---|
| TD1B | `7f740064aecb0d877d1e407429c4e26ded1ac6a7b89637049a8fd4a9594c6daa` |
| TD2 | `ff5fd1d037eb8c4e7c5b5495e0903d4ba2a8844678ececad28462e7c1c17f6f9` |
| TD3 | `1ec40c816a269a79c925eaab48b2d4db16c5b6a64c48640f44367a2d6ca77e95` |
| TD4 | `dc8d1b7240f1be8ec6a57f314bdf5cb50742487849e622d3e14f8d2f8e9aa2f7` |
| TD5 | `b9beee85f8e11b4c676c7507d649644f0d61a17b8ed1b7d33978e11f1412e74c` |
| TD6 | `828aabddf5410bda7dfea9c0bc7f7e0ee8e365e47c1a9bb17687a96a494d0f73` |
| TD7 | `bf1a04b5193d52bd1dcf9ecad40d512b816d31b1259906eddd8c13443ada384f` |

L'essai réel en classe, le comportement effectif du LLM dans Colab et la durée humaine ne sont pas testés par cette revue. L'exécution des exemples fournis, la validité technique des correcteurs, leurs protections et la génération distribuée relèvent de preuves techniques séparées. Le correcteur TD1B v3 ne peut noter que des sorties et leur cohérence, pas garantir la pertinence de l'interprétation d'un texte personnel.


## Verdict et relais

**ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE**, pour les sept supports aux empreintes ci-dessus et le README S3 relu. Aucun blocage éditorial restant. Les 46 questions, cours, exemples, essais, transferts et bilans ont été lus, sans échantillonnage.

Ce verdict reste distinct de la conservation pédagogique examinée par TAL-Pedagogy-Reviewer, de l'audit du contrat TD1B v3 et des correcteurs v2, de la gouvernance, puis de la décision du mainteneur. Le relais attendu est l'examen de ces preuves séparées par Governance-Auditor et Integration-Master ; aucune fusion ni mise en production n'est autorisée par cette seule revue.
