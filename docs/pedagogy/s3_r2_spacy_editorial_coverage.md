# Pilotes S3 — cadrage de la reprise de R2 et de l’introduction à spaCy

## Statut et références

Cadrage TAL-Prof établi **avant conception** le 3 octobre 2026. Pour les activités de l’initiation spaCy historique, il remplace explicitement les annonces antérieures de déplacement vers TD3 ou vers un prolongement non livré dans `S3_COVERAGE_MATRIX.md` ; les autres lacunes historiques restent signalées, sans extension implicite du présent pilote. L’enseignant demande de commencer la reprise par R2 et le TD d’introduction à spaCy, après fusion des règles de révision éditoriale. Cette matrice prescrit la conservation de toutes les activités actuelles ; elle ne vaut ni validation de la rédaction future, ni autorisation de supprimer, déplacer ou rendre facultative une activité historique.

- Référence technique : commit `553f3ada02c8ed93f1e04332a1c42ada5327eaa3`, `Notebooks TD/S3/R2_S3_frequences_reutilisables.ipynb` (20 cellules) et `Notebooks TD/S3/TD1_S3_fondations_spacy.ipynb` (28 cellules). Les indices ci-dessous commencent à zéro et désignent cette référence, avant ajout de cellules.
- Référence historique fournie par l’enseignant : `TD_0_Initiation_spacy.ipynb`, 27 cellules, SHA-256 `e148a687414f1b1bedd7de5195617b4c3fca6219d57c25f87e9422f10416ade4`. Cette pièce jointe n’est pas une source distribuée du dépôt. Ses anciennes sorties ne constituent pas une référence de correction du modèle actuel.
- Cadrages comparés : `docs/pedagogy/S3_COVERAGE_MATRIX.md`, `docs/pedagogy/editorial_revision_inventory.md`, `docs/agents/TAL-Editorial-Reviewer.md` et `docs/agents/WORKFLOW.md`.
- R2 : aucune autre référence historique autonome fournie pour ce pilote. Ne pas prétendre restaurer un document non disponible.
- Décision explicite de l’enseignant, le 3 octobre 2026 après signalement de la surcharge : **deux TD de 2 h**, introduction actuelle conservée et TD compagnon consacré aux entités nommées, à la similarité et à EntityRuler. Insérer **TD1B après TD1 et avant TD2**, sans renuméroter la progression existante.
- Durées à conserver : **30 minutes de consolidation R2**, **120 minutes TD1** et **120 minutes TD1B**, installation et restitution comprises. Il s’agit d’estimations pédagogiques, pas de durées mesurées en classe.

## Règles de conception pour les deux supports

Le destinataire de toute cellule visible est l’étudiant. Les raisons de fabrication, de stabilité technique ou de conformité vont dans cette documentation. Les consignes utiles restent dans le notebook : quoi exécuter, où écrire, quelles données conserver et comment enregistrer son travail.

Avant chaque activité, distinguer une explication de notion, un exemple exécutable sur d’autres données et un énoncé. Une explication ne contient pas de tâche obligatoire cachée. L’énoncé réunit but, données et productions, avec étapes annoncées pour les exercices guidés ; Q6 du TD1 reste un transfert autonome. Donner des espaces distincts pour les essais et la réponse lorsque nécessaire, sans multiplier les manipulations de restitution.

Les exemples fournis montrent un geste sur un texte différent, jamais la réponse de l’exercice. Chaque résultat dépendant de spaCy reste une prédiction à observer : ne pas inventer une sortie déterministe pour un microtexte non vérifié. Une annotation surprenante se commente séparément sans modifier le résultat du modèle.

Préserver les cellules de réponse, leurs identifiants et leurs métadonnées, les identifiants de notebook, la version 2, les variables, clés, types, marqueurs d’affichage et barèmes. Conserver l’installation et les données prescrites. Les modifications structurelles de la restitution des réponses nécessiteraient une revue technique explicite : le présent cadrage n’en demande aucune.

Conserver le contexte intégral du tuteur en métadonnées Colab et sa copie identique dans le commentaire HTML de la première cellule Markdown, ainsi que le profil structuré. Un encart visible peut expliquer son usage sans remplacer ces copies. Le tuteur ne peut guider qu’avec les notions déjà étudiées ou introduites avant la question concernée. Les imports des cellules techniques ne sont pas des acquis. Conserver la cellule de restitution HTML finale et le seul placeholder `__TAL_PUBLIC_URL__` dans les sources.

## R2 — couverture de chacune des activités actuelles

Bibliothèques de travail : `spacy` et `collections.Counter`. Prérequis : variables, listes, tuples, dictionnaires, boucle, condition, fonction et retour ; token, lemme et POS travaillés au TD1/R1. Le rappel rend visibles ces dépendances sans prétendre dispenser un cours complet de fonctions en 30 minutes.

| Source actuelle | Objectif et activité étudiante conservés | Acquis / apport avant la question | Cible prescrite et statut | Production et contrat conservés |
|---|---|---|---|---|
| Cell. 1–6 : introduction, identité, installation, données | Se repérer avant TD2 ; charger le modèle et le texte fournis ; distinguer prédiction et analyse humaine | Import et chargement fournis ; petit rappel `Doc`/token/lemme/POS | **RENFORCÉ** : introduction orientée vers l’usage d’une fonction réutilisable ; préparation technique limitée aux actions de l’étudiant ; conservation des données | Modèle `fr_core_news_sm` 3.8.0, spaCy 3.8.7 ; variable `texte` inchangée ; identité conservée |
| Cell. 7–9, Q1 `r2-q1-consigne` | Analyser un texte dans une fonction ; sélectionner les noms prédits, compter les lemmes et renvoyer un résultat | Cours bref séparant sélection et comptage ; exemple exécutable de `Counter` sur une liste distincte ; rappel de `return` et argument facultatif | **RENFORCÉ** : expliquer `None` sans y mêler la consigne ; annoncer ensuite que ce paramètre est réservé pour Q3 ; même exercice guidé | `frequences_lemmas(texte, stopwords=None)` renvoie `Counter` ; uniquement POS `NOUN` ; aucun filtre `is_stop` ni exclusion personnelle à ce stade ; affichage `Résultat Q1 :` du dictionnaire |
| Cell. 10–11, Q2 `r2-q2-consigne` | Garder une trace complète et ordonnée des annotations ; vérifier Q1 à partir des noms, lemmes et répétitions ; commenter une surprise | Parcours de tokens et construction de liste ; exemple de triple sur autre donnée si le rappel est nécessaire | **RENFORCÉ** : séparer construction de la trace et vérification linguistique ; faire nommer explicitement le texte utilisé | `annotations` liste de triples forme/lemme/POS, tous tokens y compris ponctuation ; `Résultat Q2 :` ; commentaire d’observation conservé |
| Cell. 12–15, Q3 `r2-q3-consigne` | Distinguer deux exclusions ; prédire leur effet ; réécrire la fonction ; comparer les cas sans/avec exclusion personnelle | Explication autonome de `token.is_stop`, appartenance du **lemme** à une collection, `None` et liste vide ; aucun appel à une suppression de sous-chaîne | **RENFORCÉ** : cours séparé des essais demandés ; espace d’essai conservé ; énoncé guidé en étapes ; vérifier sans forcer une différence liée à `is_stop` | Fonction même signature et retour `Counter` ; filtre `is_stop` actif et exclusion personnelle sur lemmes ; `tests_filtrage` clés `sans_exclusions`, `avec_exclusions`, deuxième appel avec `['texte']` ; `Résultat Q3 :` |
| Cell. 16–18, Q4 `r2-q4-consigne` | Réutiliser la fonction modifiée ; classer, comparer et interpréter l’effet des exclusions personnelles | Exemple distinct de `.most_common()` sans limite ; égalités de fréquence et distinction rang/importance | **RENFORCÉ** : cours sur classement séparé de la tâche ; rappeler la dépendance à Q3 ; conserver le commentaire interprétatif | `classements` clés `avant`, `apres`, listes complètes de couples ; fréquences décroissantes, ex æquo libres ; `is_stop` actif dans les deux appels ; `Résultat Q4 :` |
| Cell. 0 et 19 : tuteur, restitution | Demander un guidage progressif et remettre le travail exécuté | Aucun nouvel acquis évalué | **CONSERVÉ** : double tuteur et restitution finale ; clarifier les actions visibles uniquement | Deux copies identiques du tuteur ; HTML avec placeholder ; aucune URL de serveur exposée |

Toutes les interprétations et vérifications personnelles restent demandées, même lorsque le correcteur ne les note pas automatiquement. Les quatre idées d’exercice ne sont ni remplacées ni fusionnées.

## TD1 — couverture de chacune des activités actuelles

Bibliothèques de travail : spaCy ; displaCy introduit avant Q4 ; `json` limité au format de restitution expliqué et fourni. `pathlib`, `hashlib`, `urllib`, `sys` et `subprocess` servent à la préparation fournie et ne deviennent pas des outils de résolution. Prérequis Python : parcours, conditions, listes, dictionnaires, chaînes et indices ; découpage `split()` travaillé au TD0.

| Source actuelle | Objectif et activité étudiante conservés | Acquis / apport avant la question | Cible prescrite et statut | Production et contrat conservés |
|---|---|---|---|---|
| Cell. 1–6 : préparation et présentation | Installer, charger le pipeline, analyser un texte ; situer l’utilité linguistique et les limites des prédictions | Introduire bibliothèque, modèle/pipeline, appel `nlp(texte)`, objet `Doc`, token et annotation avant leur emploi | **RENFORCÉ** : véritable entrée de bibliothèque ; chargement illustré lisiblement ; longue préparation des ressources identifiée comme fournie ; explications d’architecture déplacées en documentation | Versions et corpus prescrits, texte fixe `texte`, `doc` et `texte_td0` conservés ; identité et droits de correction inchangés |
| Cell. 7–11, Q1 `74ca682aaf0f` | Prédire deux lemmes ; construire annotations et positions ; commenter deux écarts forme/lemme et apport réel de `tag_` ; confronter cinq entrées à une annotation manuelle | Exemple exécutable distinct pour `text`, `lemma_`, `pos_`, `tag_`, `idx` ; différence rang/position ; tranche avec fin exclue ; données manuelles rendues accessibles et leur structure expliquée | **RENFORCÉ** : cours puis exemple, puis exercice guidé ; garder essai, prédictions, comparaison manuelle et désaccord/alignement impossible | `resultat_q1['annotations']`, liste ordonnée non ponctuation, clés `forme`, `lemme`, `pos`, `tag`, `debut`, `fin` ; `tag` chaîne même vide ; marqueur `S3_TD1_Q1:` |
| Cell. 12–14, Q2 `3780d7aaf39b` | Segmenter en phrases ; compter manuellement une phrase ; tester abréviation et citation interrogative ; envisager un cas à vérifier dans Faguet | Exemple exécutable sur `doc.sents`, texte et bornes d’une phrase, `len(phrase)` ; ponctuation comptée comme token | **RENFORCÉ** : expliquer Span/phrase sans jargon non défini ; séparer essai distinct et réponse sur `doc` fixe | `resultat_q2['phrases']`, liste de dictionnaires `texte`, `tokens` ; marqueur `S3_TD1_Q2:` |
| Cell. 15–17, Q3 `e807c249b2b2` | Prédire l’effet de trois filtres ; extraire noms, verbes, mots pleins ; interpréter utilité et perte | Exemple exécutable distinct de sélection POS ; expliquer `is_stop`, `NOUN`, `VERB`, `ADJ`, répétitions et ordre | **RENFORCÉ** : rappeler définition opératoire de mots pleins avant exercice ; conserver prédiction et argumentation thématique | `resultat_q3` clés `noms`, `verbes`, `mots_pleins` ; listes de lemmes ordonnées, répétitions conservées ; dernier filtre POS autorisés ET non `is_stop` ; marqueur Q3 |
| Cell. 18–20, Q4 `2dfebbd9b871` | Visualiser la première phrase ; repérer verbe et dépendant, vérifier annotations ; distinguer lecture et prédiction ; réfléchir à auteur/locuteur cité | Exemple exécutable distinct de `displacy.render`, `dep_`, `head.text`, `idx` ; expliquer relation, tête/dépendant, `nsubj` et `obj` avant emploi | **RENFORCÉ** : lire une figure avant produire ; rattacher le commentaire sur Faguet à un cas concret, sans imposer une conclusion | `resultat_q4` clés `verbe`, `relation`, `interpretation`, `verbe_debut`, `dependant_debut`, `dependant` ; deux tokens distincts de la première phrase ; marqueur Q4 |
| Cell. 21–22, Q5 `95fec9ddcc6b` | Comparer `split()` et deux comptages spaCy sur même texte ; expliquer deux écarts précis ; comparer au TD0 si export disponible | Rappel `split`, `is_punct`, `is_space` ; convention explicite avant mesure, exemple distinct si nécessaire | **RENFORCÉ** : distinguer les trois populations sans changer la convention actuelle | `resultat_q5` clés `split`, `tokens`, `non_ponctuation`, `interpretation` ; tous tokens pour `tokens`, retrait ponctuation ET espaces pour `non_ponctuation` ; marqueur Q5 |
| Cell. 23–24, Q6 `8d36933011cd` | Transfert autonome sur 2–4 phrases ; cinq premiers tokens vérifiés ; noms/verbes ; question de corpus et limite | Uniquement notions Q1–Q5 ; aucune nouvelle méthode imposée ; rappel de la production autorisé | **CONSERVÉ + CLARIFIÉ** : préciser données/productions, laisser le choix de l’extrait et de la méthode ; ne pas transformer en recette | `resultat_q6` clés `texte`, `phrases`, `annotations`, `noms`, `verbes`, `question` ; cinq premiers tokens avec ponctuation, positions relatives à extrait, clés d’annotation sans `tag` ; limite en commentaire ; marqueur Q6 |
| Cell. 25–27 : bilan, export, restitution | Enregistrer les sorties ; conserver l’export pour les séances suivantes ; remettre notebook | Code de sauvegarde fourni ; explication de l’usage du fichier, non de l’architecture du serveur | **CONSERVÉ + CLARIFIÉ** : bilan linguistique visible ; actions de téléchargement regroupées ; tutorat double conservé | `s3_td1_export.json` et résultat Q1–Q6 inchangés ; cellule HTML finale sans URL privée |

Les marqueurs Q2–Q6 restent respectivement `S3_TD1_Q2:` à `S3_TD1_Q6:`. Les notions de JSON ne doivent pas occuper la place du tutoriel spaCy : le format de sortie est expliqué comme une action de restitution à exécuter après la construction du résultat, sans divulguer celui-ci.

## Référence historique — écarts à ne pas dissimuler

Le TD historique associait sept exercices et des exemples exécutables, mais ne déclarait pas une répartition temporelle. Ses cellules parfois résolues ne sont pas à recopier comme réponses étudiantes. Conserver l’objectif et la manipulation, en distinguant démonstration et problème.

| Référence historique (indices, identifiants) | Activité et couverture actuelle | Cible / décision du pilote |
|---|---|---|
| 0–3 : présentation, installation, définitions | Présentation de la bibliothèque ; installation ; tokenisation, POS, NER, lemmatisation, syntaxe. L’introduction actuelle était trop abrupte | **RENFORCÉ** pour utilité, installation et objets/annotations mobilisés dans Q1–Q6 ; nommer les autres tâches comme panorama ne les rend pas pratiquées |
| 5–7 : exercice 1, `16bbf47e` | Charger `fr_core_news_md`, analyser une phrase, afficher tokens/lemmes ; autre phrase fournie en démonstration | Geste et activité **CONSERVÉS** dans tutoriel + Q1 avec `fr_core_news_sm` prescrit. Ce changement de modèle antérieur reste explicite ; aucune prétention d’équivalence pour les vecteurs |
| 8–9 : exercice 2, `7fad9720` | Afficher forme, lemme, POS et tag | **CONSERVÉ + RENFORCÉ** Q1 avec positions et comparaison manuelle |
| 10–11 : exercice 3, `ea566d77` | Détecter et afficher entités nommées et labels sur Apple/Allemagne/2024 | **DÉPLACÉ vers TD1B Q1 à livrer** : définition NER, analyse d’un texte et affichage des formes/labels. Aucun Q1–Q6 actuel ne couvre cette manipulation |
| 12–14 : exercice 4, `64c68319` | Visualiser une phrase avec displaCy | **CONSERVÉ + RENFORCÉ** Q4. L’ancien exemple visualisait le `doc` de la cellule NER précédente au lieu de la phrase annoncée : la cible doit créer puis afficher le même exemple, sans reproduire cette erreur |
| 15–18 : exercice 5, `c9f03004` | Comparer chien/chat et chien/voiture, puis phrases, avec similarité et interpretation des scores | **DÉPLACÉ vers TD1B Q3 à livrer** : mots ET phrases, prédictions puis scores, limites et choix du modèle `md`. Les filtres POS, fréquences ou cooccurrences ne sont pas cette tâche |
| 20–21 : exercice 6, `84e644b6` | Extraire les entités PER/ORG d’un texte | **DÉPLACÉ vers TD1B Q2 à livrer**, après introduction NER ; extraction PER/ORG distincte d’afficher toutes les entités |
| 22–26 : exercice 7, `87830824` | Ajouter `EntityRuler`, règle Université de Toulon, tester puis élargir organisations/dates/lieux et observer stabilité | **DÉPLACÉ vers TD1B Q4 à livrer** : règle Toulon, essais et extension organisations/dates/lieux, interprétation de stabilité ; un panorama ne couvre pas ce travail |

### Décision enseignante et conservation réalisée dans deux séances

La matrice générale S3 du 20 septembre annonçait NER, EntityRuler et similarité dans un prolongement non livré. L’enseignant a maintenant explicitement retenu **deux TD de deux heures**, en conservant l’introduction actuelle et en lui ajoutant un compagnon. La réalisation prescrite ci-dessous comble cette lacune sans comprimer TD1 ni rendre facultatives ses activités. Une simple annonce du compagnon ne permet toujours pas de prononcer la conservation historique : sa livraison et sa relecture sont requises.

Le compagnon est un TD du parcours, **après TD1 et avant TD2**. R2 garde sa fonction de consolidation préparatoire avant TD2. Le placement des contrôles existants n’est pas modifié ; cette livraison n’ajoute pas de compétences nouvelles à leurs barèmes.

## TD1B — spécification du compagnon autorisé

**Fichier :** `Notebooks TD/S3/TD1B_S3_entites_similarite_regles.ipynb`. **Identifiant :** `td1b-s3`. **Version :** 2. **Session tuteur :** `TD1B_S3`. Quatre questions, réception et relecture humaine explicites, sans score automatique inventé. L’identification, la restitution HTML et le classement S3 nécessitent l’intégration technique associée ; cette partie constitue une nouvelle association de support et reçoit sa revue technique propre.

**Acquis d’entrée :** TD1 pour pipeline, `Doc`, tokens, formes, lemmes, POS, syntaxe et distinction prédiction/observation ; Python S1/S2 pour parcours, conditions, listes, dictionnaires et fonctions simples. Les entités, labels NER, vecteurs, similarité et règles de pipeline sont **introduits ici**, jamais supposés déjà acquis.

**Préparation :** spaCy 3.8.7 et `fr_core_news_md` 3.8.0. Expliquer que ce modèle français contient des vecteurs utilisés dans cette séance et peut produire d’autres prédictions que le petit modèle du TD1. Ne pas remplacer le pipeline `nlp` de TD1 ; le compagnon est autonome et utilise un nom explicite, par exemple `nlp_entites`. L’installation est fournie, avec consigne de reprise après redémarrage. Les exemples n’imposent pas une sortie linguistique présumée : regarder puis discuter la prédiction réelle.

| Cible | Cours / exemple fourni avant exercice | Activité étudiante et données | Production et interprétation | Charge indicative |
|---|---|---|---|---|
| Entrée / préparation | Utilité d’une entité pour l’extraction d’information ; rappel bibliothèque/modèle ; chargement du modèle prescrit | Installer, charger, vérifier le nom/version du modèle ; prévoir les objets manipulés | Pipeline fonctionnel et repérage des quatre étapes ; aucun exercice résolu | 15 min |
| Q1 — Entités nommées | Définir entité, segment de texte, label prédit ; `doc.ents`, `ent.text`, `ent.label_` sur un exemple exécutable distinct | Analyser le texte Apple/Allemagne/2024 historique ; relever toutes les entités et leurs labels ; confronter au repérage humain préalable | Liste ordonnée des entités ; observation des absences/erreurs sans forcer les catégories attendues ; expliquer que dates/montants ne sont pas garantis par chaque modèle/langue | 20 min |
| Q2 — Extraction PER/ORG | Montrer sur un autre type de sélection la distinction détecter/classer puis filtrer ; rappeler que `PER` et `ORG` sont des labels du modèle français, distincts de `NOUN` | Sur le texte historique Macron/Musk/Paris/Google/Tesla, extraire toutes les personnes et organisations détectées, puis essayer un texte personnel | Résultat filtré distinct de la liste entière de Q1 ; explication d’un faux positif, d’une absence ou d’une limite constatée ; ne pas confondre nom propre et entité garantie | 20 min |
| Q3 — Similarités | Notion de représentation vectorielle puis proximité numérique ; appel `.similarity()` dans un exemple distinct ; avertissement score ≠ vérité, entaillement ou identité de sens | Comparer `chien`/`chat` et `chien`/`voiture`, puis deux phrases ; prédire un ordre, calculer, comparer ; essai de variation ou contre-exemple motivé | Scores associés clairement aux deux objets comparés ; interprétation de l’ordre observé et limite, y compris une éventuelle absence de vecteur utile ; aucune conclusion numérique prédéterminée | 25 min |
| Q4 — Ajouter des règles et éprouver leur stabilité | Présenter règle exacte et prédiction, place du composant ; `add_pipe('entity_ruler', before='ner')`, `add_patterns`, dictionnaire de règle ; exemple distinct de Toulon | Dans un pipeline dédié aux règles, reconnaître « Université de Toulon » ; comparer avant/après sur même texte ; ajouter des règles pour d’autres organisations, des dates et des lieux ; tester plusieurs textes, variantes et cas où la règle ne convient pas | Règles construites, entités avant/après, tableau ou liste d’essais avec attendu/observé ; commentaire sur couverture, exactitude et limites de correspondance ; ne pas prétendre entraîner le modèle | 30 min |
| Bilan / restitution | Consignes de sauvegarde et dépôt ; expliquer relecture humaine | Enregistrer notebook avec sorties et commentaires ; bilan reliant données, prédictions et règles | Notebook complet remis par la cellule HTML ; aucune note automatique fictive | 10 min |

**Total : 120 minutes.** Cette estimation suppose les acquis Python annoncés et reste à mesurer en classe. Les quatre exercices historiques supplémentaires sont des activités du TD livré, pas des prolongements simplement promis. Les démonstrations et les jeux d’essai peuvent être courts, mais ni les exercices ni les interprétations ne sont supprimés pour tenir cette estimation.

### Périmètre du tuteur TD1B à inscrire après finalisation du support

Le Designer et l’Architecte transcrivent ces limites dans le manifeste, sans élargir rétroactivement les permissions des questions précédentes. Le TAL-Prof n’édite pas le manifeste technique.

- Base : acquis Python déjà enseignés et notions du TD1 ; bibliothèque `spacy` seulement pour les réponses. Préparation et restitution fournies ne rendent pas leurs imports utilisables dans les exercices.
- Q1 : entités et labels, `Doc.ents`, `Span.text`, `Span.label_`, parcours ; pas encore similarité ni EntityRuler.
- Q2 : acquis Q1 et filtrage des labels PER/ORG ; pas de nouvelle bibliothèque, pas de similarité ni règles anticipées.
- Q3 : acquis Q1/Q2 plus introduction des vecteurs du modèle, `Doc.has_vector` et `.similarity()` ; pas de bibliothèque numérique additionnelle ni nouveau modèle non fourni.
- Q4 : acquis précédents plus pipeline distinct, `pipe_names`, `add_pipe`, `add_patterns`, dictionnaires de règles exactes, label personnalisé pour une date si nécessaire, comparaison avant/après et essais. `EntityRuler` est fourni par spaCy ; un import direct `spacy.pipeline.EntityRuler` n’est nécessaire que si le cours l’emploie réellement.
- Demande de résolution : une question ciblée puis attente ; mini-cours ou exemple différent en cas de blocage ; au S3, fragment minimal seulement après échange, jamais solution entière ni écriture/exécution dans le notebook.

## Preuves attendues après conception

1. Relire toutes les cellules visibles, y compris commentaires, des trois notebooks ; consigner une preuve pour chacune des quatorze questions et le parcours initial de la bibliothèque.
2. Vérifier chaque ligne des matrices actuelles : activité, réflexion, données, autonomie, contrats conservés ; reporter les identifiants des nouveaux exemples. Distinguer conservation de la version active et couverture de la référence historique.
3. Vérifier techniquement métadonnées, doubles contextes identiques, sortie de restitution à placeholder, identification du correcteur, nombre et identifiants de questions. Ne pas présenter ces vérifications comme une preuve de compréhension.
4. Faire une lecture indépendante Étudiant-Modèle : « que dois-je faire, sur quelles données, avec quels acquis, où produire la réponse ? ». Ce rôle n’a pas à exécuter du code étudiant sur le serveur.
5. Demander deux verdicts séparés, pédagogique et éditorial ; consigner explicitement les limites : durée non mesurée en classe, comportement Colab du tuteur non garanti par ses métadonnées, réalisation effective des quatre activités historiques dans TD1B, avec ses limites d’annotations.

Le cadrage est prêt à transmettre au Designer pour les deux reprises et le compagnon expressément autorisé. La validation finale des nouveaux textes reste distincte de cette spécification. Aucune suppression ou réduction de couverture n’est proposée.

### Validation préalable indépendante

Le 3 octobre 2026, le TAL-Pedagogy-Reviewer indépendant (`pilot_pedagogy_review`) a validé le cadrage avant conception, d’abord pour les dix questions R2/TD1, puis pour les quatre questions TD1B et leur couverture historique. Cette validation permet la conception ; elle ne constitue pas le verdict sur les supports effectivement produits. Les contraintes de durée et d’acquis restent des hypothèses à éprouver auprès d’étudiants.

## Cibles effectivement écrites — relevé après conception, avant verdict final

Les trois supports sont présents dans la branche de ce lot : R2 comporte 26 cellules, TD1 39 et TD1B 31 dans cet état de livraison. Les indices historiques précédents restent ceux des références initiales ; les identifiants ci-dessous permettent de retrouver les nouvelles cibles sans ambiguïté. Ce relevé ne constitue pas une auto-validation pédagogique.

| Support / question | Exemple ou cours livré avant la question | Cellule de réponse conservée ou créée |
|---|---|---|
| R2 Q1 | `s3-review-r2-q1-repere`, `r2-exemple-q1-counter-parametre` | `r2-q1-reponse` |
| R2 Q2 | `r2-rappel-q2-triples`, `r2-exemple-q2-triple` | `r2-q2-reponse` |
| R2 Q3 | `s3-review-r2-q3-repere`, `r2-exemple-q3-exclusions`, `r2-q3-prediction-consigne` ; essai `s3-review-r2-q3-essai` | `r2-q3-reponse` |
| R2 Q4 | `s3-review-r2-q4-repere`, `r2-exemple-q4-classement` | `r2-q4-reponse` |
| TD1 entrée et Q1 | `td1-cours-bibliotheque`, `5516945566d9`, `td1-exemple-annotations`, `td1-exemple-positions`, `td1-exemple-dictionnaire` | `f0868b90c1ec` |
| TD1 Q2 | `3fd4db7ab180`, `td1-exemple-phrases` | `6f8e948b3277` |
| TD1 Q3 | `2319f64ee6f1`, `td1-exemple-filtre` | `0d6d764a0ba2` |
| TD1 Q4 | `fd2acde816dc`, `td1-exemple-dependances` | `6026f523bc1f` |
| TD1 Q5 | `td1-cours-decoupage`, `td1-exemple-decoupage` | `951832c4e554` |
| TD1 Q6 | Réinvestissement autonome de Q1–Q5 ; consigne `8d36933011cd` | `4b47b9af0c87` |
| TD1B Q1 | `td1b-q1-cours`, `td1b-q1-exemple` | `td1b-q1-reponse`, observations `td1b-q1-observations` |
| TD1B Q2 | `td1b-q2-cours`, `td1b-q2-exemple` | `td1b-q2-reponse`, observations `td1b-q2-observations` |
| TD1B Q3 | `td1b-q3-cours`, `td1b-q3-exemple` | `td1b-q3-reponse`, observations `td1b-q3-observations` |
| TD1B Q4 | `td1b-q4-cours`, `td1b-q4-exemple`, `td1b-q4-observation-exemple` | `td1b-q4-reponse`, observations `td1b-q4-observations` |

Les profils `TD1_S3`, `R2_S3` et `TD1B_S3` de `tutor_sessions.json` sont ajustés aux notions explicitement présentes dans ces cours. TD1B n’autorise que `spacy` dans les réponses ; les règles ne sont autorisées qu’en Q4, la similarité qu’en Q3. TD1 n’anticipe pas NER, similarité ou EntityRuler du compagnon. Les bibliothèques d’installation et de restitution restent fournies seulement. La génération du double contexte et sa vérification technique sont à effectuer après cette mise à jour du manifeste.

## Bilan final des revues indépendantes

Le 3 octobre 2026, après les corrections de lisibilité demandées et la lecture du produit livré, les deux rôles indépendants ont communiqué leurs verdicts sur **R2, TD1 et TD1B : quatorze questions, quatre-vingt-seize cellules** (26 + 39 + 31).

- **TAL-Pedagogy-Reviewer** : `ACCEPT` et `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`. Ce verdict porte sur les quatre questions R2 et les six questions TD1 conservées, ainsi que sur le rétablissement effectif dans TD1B des activités historiques NER, extraction PER/ORG, similarité de mots et de phrases, EntityRuler et essais de stabilité. Il ne certifie pas la restauration des autres enseignements avancés explicitement hors de ce pilote.
- **TAL-Editorial-Reviewer** : `ACCEPT` et `LISIBILITÉ_ÉTUDIANTE_VALIDÉE`. La [revue détaillée](../../reports/editorial/s3-r2-spacy.md) recense toutes les cellules, les preuves par question, les corrections demandées et les limites de la lecture.
- **TAL-Étudiant-Modèle** : lecture favorable à la compréhension des quatorze tâches après corrections ciblées, sans blocage restant. La [note de lecture](../../Corrigés%20modèles/TD/s3-spacy-editorial/lecture_etudiante.md) conserve les hésitations non bloquantes et distingue reformulation des tâches, relecture des exemples et exécution réelle. Elle n'est ni une copie résolue ni un verdict technique.

Ces verdicts remplacent l'attente de revue inscrite dans le relevé de livraison précédent, sans réécrire rétrospectivement le cadrage préalable. L'inventaire passe les trois supports à **REVU**. Les profils du tuteur sont gelés pour la génération et la vérification des deux copies ; cette documentation ne modifie plus le manifeste.

Le rapport de gouvernance `reports/governance/s3-r2-spacy-editorial.md`, préparé séparément avant publication, consignera les avis indépendants, les contrôles techniques et les limites d'intégration. Son existence et son verdict doivent être vérifiés par l'Integration-Master ; le présent bilan ne les anticipe pas.

**Limites conservées :** aucune durée réelle n'a été mesurée en classe ; aucun essai Colab du comportement du tuteur ne peut être déduit des métadonnées ; une lecture favorable ne garantit pas les performances de chaque étudiant. Le nouveau TD1B reçoit une relecture humaine et aucun score automatique. Les autres supports de la progression restent à reprendre suivant l'inventaire intégral.
