# Lecture étudiante indépendante — trois pilotes S3

Note de validation destinée au projet, à transmettre aux revues pédagogique et éditoriale. Ce fichier n'est ni une cellule destinée aux étudiants ni un corrigé. Rôle : TAL-Étudiant-Modèle. Branche observée : `pedagogy/s3-r2-spacy-editorial`. Lecture effectuée le 3 octobre 2026, sans exécution des notebooks, sans installation, sans soumission et sans essai dans Colab.

## Périmètre et méthode

Lecture intégrale des sources des cellules des trois sujets : R2, cellules 0 à 25 ; TD1, cellules 0 à 38 ; TD1B, cellules 0 à 30. Les numéros ci-dessous sont des indices commençant à zéro, utilisés uniquement pour tracer cette revue. Les commentaires HTML de cellule 0 ne sont pas du cours visible et ne servent pas de preuve d'introduction d'une notion. Les commentaires des cellules de code et le texte du bloc de restitution ont été relus comme passages visibles.

Lecture de `ressources/exemples.json`, notamment de la référence manuelle effectivement demandée par TD1 Q1. Aucun correcteur, test, corrigé existant, fichier d'infrastructure ou identité réelle n'a été consulté. Aucun besoin d'identité fictive n'est apparu puisqu'aucune copie n'a été résolue ni renseignée. Les noms figurant dans les phrases d'exercice sont uniquement des données du sujet.

Prérequis autorisés consultés : R1, cellules visibles 1 à 17 ; S1 TD3, passages sur liste, tuple, dictionnaire, parcours et accumulation ; S1 TD4, passages sur boucle, condition, appartenance et comptage ; S1 TD5, passages sur définition, appel, paramètre, retour, paramètre par défaut et composition. Il ne s'agit pas d'une revue exhaustive des supports S1. Aucun apport S2 supplémentaire n'a été nécessaire pour comprendre les actions demandées. Les liens externes n'ont pas été ouverts.

La lecture distingue comprendre la consigne, savoir construire une réponse et avoir effectivement vérifié son exécution. Seul le premier point est évalué ici. Les résultats réels de spaCy ne sont jamais devinés.

## R2 — quatre questions

### Q1 — Fonction (cellules 9–10)

- **Action comprise :** construire une fonction réutilisable qui analyse son argument, sélectionne les noms prédits et compte leurs lemmes. Réserver le paramètre facultatif à la suite, sans appliquer encore les deux exclusions.
- **Données :** `texte` fourni en cellule 6 ; le texte reçu par la fonction doit rester sa donnée, même pour un autre appel.
- **Acquis repérés :** S1 TD5 pour `def`, paramètre et `return` ; TD1/R1 pour le parcours du `Doc`, `lemma_` et `pos_` ; cellules 7–8 pour `Counter`, `dict`, `None`, paramètre facultatif et différence entre retour et affichage.
- **Production et emplacement :** définition et appel en cellule 10 ; retour de type `Counter`, affichage converti en dictionnaire avec la ligne proposée. Je n'ai pas à recopier une liste de valeurs attendues.
- **Difficulté restante :** assembler fonction, sélection et comptage demande du travail mais aucune opération n'est laissée implicite. Le nom `stopwords` pourrait faire anticiper le filtre ; la mise en garde de Q1 lève cette hésitation.

### Q2 — Noms et lemmes (cellules 13–14)

- **Action comprise :** reconstruire une trace de tous les tokens et comparer les seuls noms de cette trace au compte précédent.
- **Données :** même `texte`, ponctuation incluse ; aucune substitution par l'exemple des notices.
- **Acquis repérés :** R1 Q2 et TD1 Q1 pour les attributs ; rappel et exemple des cellules 11–12 pour conserver un triple et l'ajouter à une liste.
- **Production et emplacement :** `annotations`, liste ordonnée de triples forme/lemme/POS, affichée en cellule 14 ; vérification et éventuel désaccord linguistique en commentaire dans cette cellule.
- **Difficulté restante :** aucune ambiguïté de sélection : la trace contient aussi les tokens qui n'ont pas été comptés en Q1. L'annotation prédite doit rester intacte.

### Q3 — Filtrer (cellules 15–20)

- **Action comprise :** prédire trois cas, puis réécrire la fonction avec les exclusions spaCy et personnelles ; comparer deux appels nommés et revenir aux prédictions.
- **Données :** même texte, annotations Q2 ; `None`, liste vide et `['texte']` pour la prédiction. Les deux résultats à conserver sont sans collection personnelle et avec `['texte']`.
- **Acquis repérés :** S1 TD4 pour conditions et appartenance ; cellules 15–16 pour distinguer forme, lemme, `is_stop`, exclusions personnelles et absence de collection. La différence `None`/liste vide est expliquée avant la demande.
- **Production et emplacement :** prédictions, essais et confrontation en cellule 18 ; nouvelle définition, `tests_filtrage` et affichage en cellule 20. Les valeurs de ce dictionnaire sont elles-mêmes des dictionnaires.
- **Difficulté restante :** je comprends que la liste vide mérite un essai, même si elle ne constitue pas une troisième clé imposée de `tests_filtrage`. Il faut trouver moi-même une façon de traiter `None` avant une recherche d'appartenance : la notion et le cas à traiter sont enseignés, le code reste à construire. Aucun écart dû à `is_stop` ne doit être inventé.

### Q4 — Comparer (cellules 21–24)

- **Action comprise :** utiliser la nouvelle fonction pour deux classements complets puis discuter l'effet des exclusions et les limites d'une lecture par fréquence.
- **Données :** même texte, fonction de Q3, sans exclusion personnelle puis avec `['texte']`. `is_stop` reste actif dans les deux cas.
- **Acquis repérés :** rappel et exemple des cellules 21–22 pour `.most_common()` sans argument et les ex æquo ; dictionnaires déjà étudiés au S1.
- **Production et emplacement :** dictionnaire `classements`, clés `avant` et `apres`, contenant des listes de couples ; affichage et commentaire en cellule 24.
- **Difficulté restante :** aucune ambiguïté sur « avant » : il ne faut pas reprendre la fonction Q1. Le texte distingue classement numérique et importance argumentative sans imposer une conclusion linguistique.

## TD1 — six questions

### Q1 — Lire puis contrôler les annotations (cellules 16–17)

- **Action comprise :** prédire deux lemmes ; relever tous les tokens non ponctués de `doc`, vérifier leurs tranches, commenter deux différences forme/lemme et la valeur du tag ; analyser séparément le texte de référence et comparer cinq entrées.
- **Données :** `texte` et `doc` de cellule 8 pour `resultat_q1`. Pour la comparaison manuelle seulement, `exemples['annotation_manuelle']['texte']` et ses `tokens` ; le JSON lu contient effectivement forme, lemme et POS ainsi qu'une note disant qu'il ne s'agit pas d'une sortie garantie du modèle.
- **Acquis repérés :** S1 TD3–4 pour accumulation et dictionnaires ; cellules 9–15 pour attributs, positions, tranche à fin exclue et affichage JSON fourni.
- **Production et emplacement :** cellule 17 : prédictions et commentaires, comparaison manuelle et `resultat_q1` avec liste `annotations` à six champs par token, puis affichage proposé.
- **Difficulté restante :** « un accord, un désaccord » ne précise pas si je dois conclure pour l'entrée entière ou séparément pour lemme et POS. Je peux décrire les deux champs mais il s'agit d'une interprétation à annoncer. Deux points identiques apparaissent dans la référence ; si j'en choisis un, je dois conserver son occurrence dans l'ordre du texte, pas seulement sa forme. Cela demande attention, sans empêcher de choisir cinq autres entrées. Je ne connais pas les valeurs prédites avant exécution.

### Q2 — Segmenter et vérifier (cellules 18–21)

- **Action comprise :** compter les tokens de chaque phrase de `doc`, refaire un compte à la main, essayer abréviation et citation interrogative sur des données distinctes et proposer une situation où vérifier les frontières de Faguet.
- **Données :** `doc` pour la liste évaluée ; deux textes d'essai que je choisis, sans remplacer `doc`.
- **Acquis repérés :** cellules 18–19 pour `Span`, `.sents`, `len`, bornes et abréviation ; bases Python antérieures.
- **Production et emplacement :** cellule 21 : `resultat_q2['phrases']`, liste de dictionnaires texte/tokens, plus textes d'essai et commentaires ; affichage fourni.
- **Difficulté restante :** le sujet ne dit pas de lire un passage déterminé de Faguet. Je comprends la demande comme une situation de vigilance à formuler, pas comme une preuve sur un passage absent. Les tokens incluent explicitement la ponctuation.

### Q3 — Comparer trois filtres (cellules 22–25)

- **Action comprise :** prédire ce que trois sélections retiennent, construire les listes de lemmes puis justifier un choix exploratoire et une perte possible.
- **Données :** uniquement `doc` ; trois conventions du tableau.
- **Acquis repérés :** exemple des adjectifs en cellule 23, boucle et `append` déjà étudiés ; cellule 22 définit les mots pleins et relativise le statut de mot-outil.
- **Production et emplacement :** cellule 25 : `resultat_q3` avec `noms`, `verbes`, `mots_pleins`, ordre et répétitions conservés ; prédictions, interprétation et affichage.
- **Difficulté restante :** aucune ambiguïté sur les catégories ou les répétitions. Le choix du filtre est une justification à construire, sans « bonne liste thématique » annoncée.

### Q4 — Visualiser puis expliquer (cellules 26–29)

- **Action comprise :** afficher la première phrase, confronter une relation grammaticale lue à une relation prédite, puis expliquer le risque d'attribuer une citation à l'auteur.
- **Données :** première phrase de `doc` ; une courte citation inventée est autorisée si elle est identifiée comme telle.
- **Acquis repérés :** cours et exemple des cellules 26–27 pour tête, dépendance, `nsubj`, `obj`, `ROOT` et displaCy ; positions en caractères enseignées avant Q1 ; accès à la première phrase indiqué dans Q4.
- **Production et emplacement :** figure et `resultat_q4` en cellule 29, deux mots distincts, positions, relation et interprétation ; affichage conservé.
- **Difficulté restante :** je comprends `relation` comme l'étiquette observée via `dep_`, mais le tableau dit seulement « sous forme de chaîne ». Reprendre explicitement l'attribut dans le tableau rendrait ce point plus sûr pour une première rencontre. La qualité de la figure et de la lecture ne peut pas être constatée ici.

### Q5 — Comparer deux découpages (cellules 30–33)

- **Action comprise :** comparer trois comptages du même `texte_td0`, puis expliquer deux écarts avec les formes concernées.
- **Données :** texte fourni en cellule 8 ; nouveau `Doc` distinct de `doc`. L'ancien export TD0 est facultatif.
- **Acquis repérés :** cellules 30–31 pour `split`, `is_punct`, `is_space` et conventions de comptage ; parcours et compte étudiés au S1.
- **Production et emplacement :** cellule 33 : `resultat_q5` avec trois entiers `split`, `tokens`, `non_ponctuation`, et `interpretation` ; affichage fourni.
- **Blocage initial levé après relecture ciblée :** la cellule 31 contient désormais la séquence échappée `\n` à l'intérieur de la chaîne, à la place d'un saut de ligne réel coupant celle-ci. L'obstacle visible dans l'exemple fourni est corrigé. Aucune réparation ni exécution par ce rôle.
- **Autre hésitation levée par le texte :** le nom `non_ponctuation` seul pourrait laisser penser que les espaces restent comptés ; le tableau dit explicitement de les exclure aussi.

### Q6 — Réinvestissement autonome (cellules 34–35)

- **Action comprise :** choisir un extrait, réutiliser annotation, segmentation et sélections, vérifier cinq tokens et formuler une question de corpus avec une limite.
- **Données :** extrait personnel ou passage exact de Faguet, de deux à quatre phrases et au moins cinq tokens ; nouveau `Doc`.
- **Acquis repérés :** réemploi de Q1, Q2 et Q3. La consigne redonne la différence entre positions dans l'extrait et positions dans un corpus complet.
- **Production et emplacement :** cellule 35 : `resultat_q6` avec texte, nombre de phrases, cinq annotations, listes noms/verbes, question ; vérification manuelle et limite en commentaire, puis affichage.
- **Difficulté restante :** « question de corpus » n'a pas de définition ni de modèle explicite avant cet exercice. Je comprends qu'elle doit pouvoir être éclairée par les annotations, mais déterminer sa portée reste moins guidé que les opérations Python. C'est compatible avec l'autonomie annoncée ; je signalerais une hésitation à l'enseignant au lieu d'inventer une norme. Si mon découpage humain et spaCy divergent, le nombre demandé est explicitement celui de spaCy ; le choix de départ reste de deux à quatre phrases selon ma lecture.

## TD1B — quatre questions

### Q1 — Entités détectées (cellules 7–11)

- **Action comprise :** relever humainement des expressions et leurs catégories, analyser le texte, afficher toutes les entités prédites puis confronter les deux relevés.
- **Données :** phrase sur Apple reproduite exactement depuis l'énoncé ; pipeline `nlp_entites` préparé avec le modèle `md`.
- **Acquis repérés :** TD1 pour `Doc`, `Span` et parcours ; cellules 7–8 pour `ents`, `text`, `label_`, labels disponibles et absence de catégories DATE/MONEY ; S1 TD3 pour couples et listes.
- **Production et emplacement :** observations avant/après en cellule Markdown 10 ; code, liste `entites_q1` et affichage en cellule 11. La liste garde toutes les prédictions dans l'ordre.
- **Hésitation initiale levée après relecture ciblée :** Q1 demande désormais une « liste d'informations tirées de ce texte », avant la distinction détection/extraction enseignée en cellule 12. Je comprends l'action sans devoir déjà connaître ce terme. Je ne dois pas ajouter une date à la sortie pour remplir mon relevé humain.

### Q2 — Personnes et organisations (cellules 12–16)

- **Action comprise :** afficher toutes les entités du texte donné, filtrer PER/ORG, réutiliser la sélection sur un texte personnel, puis commenter une décision et une limite.
- **Données :** phrase sur Emmanuel Macron, Elon Musk, Paris, Google et Tesla, puis texte personnel contenant personne, organisation et lieu.
- **Acquis repérés :** cellule 12 distingue détection, extraction et POS ; cellule 13 montre une sélection LOC ; TD1 Q3 et S1 TD4 introduisent l'appartenance.
- **Production et emplacement :** cellule 15 : affichage complet initial, `personnes_organisations_q2` et résultats du second essai ; cellule 16 : observations argumentées. L'ordre et les répétitions sont explicites.
- **Difficulté initiale levée après relecture ciblée :** « faux positif » est désormais défini en cellule 12, avant sa demande en Q2. Je peux distinguer une détection ou une catégorie injustifiée d'une absence. Le texte autorise une limite même lorsque les deux essais paraissent corrects : inutile de fabriquer une erreur.

### Q3 — Similarité (cellules 17–21)

- **Action comprise :** prédire un ordre pour deux comparaisons de mots, calculer et lire les scores, comparer deux phrases puis une phrase et sa modification choisie.
- **Données :** chien/chat, chien/voiture, deux phrases fournies, puis modification personnelle ; pipeline séparé `nlp_sim`.
- **Acquis repérés :** cellules 17–18 pour représentation vectorielle, moyenne, `.similarity`, `.has_vector`, avertissements et limites d'interprétation.
- **Production et emplacement :** prédiction, effet sémantique de la modification et interprétation en cellule 20 ; code et affichages avec textes/couples identifiables en cellule 21.
- **Difficulté restante :** aucune sortie chiffrée n'est imposée ni déduite ici. La présence des vecteurs est explicitement demandée pour les mots ; la consigne générale impose aussi de conserver les avertissements. Un score élevé ne fournit pas une réponse linguistique prête à recopier.

### Q4 — Règles exactes (cellules 22–27)

- **Action comprise :** comparer le même texte avant/après une règle ORG, compléter avec trois règles choisies, les éprouver sur cinq textes au moins et comparer chaque texte au pipeline sans règle.
- **Données :** phrase sur l'Université de Toulon, autres expressions organisation/lieu/date choisies, variantes et contre-exemple de sens. Nouveau pipeline `nlp_regles` rechargé au début de la cellule.
- **Acquis repérés :** cellules 22–24 expliquent dictionnaires de règle, liste de patterns, placement avant `ner`, stabilité de l'expression, absence de réentraînement et label personnalisé DATE ; exemple complet distinct de l'exercice.
- **Production et emplacement :** code et sorties identifiables en cellule 26 ; tableau de cinq essais au moins et bilan de trois ou quatre phrases en cellule 27. Toutes les quatre expressions doivent apparaître au moins une fois dans l'ensemble.
- **Difficulté restante :** trouver un emploi d'une même expression dans un autre sens est une vraie difficulté de conception des essais ; le sujet me laisse choisir les expressions, donc je peux préparer ce cas avant de fixer mes règles. Je ne suppose pas que les sorties avant/après seront nécessairement différentes. Le tableau permet de distinguer attente humaine, référence sans règle et prédiction avec règle.

## Passages visibles hors questions

| Support et cellules | Preuve de lecture et constat |
|---|---|
| R2 1–6 | Durée, place avant TD2, quatre points techniques, cellules de réponse, installation et modèle sont distingués. Les attributs sont réexpliqués. Le texte fixe clairement la donnée et demande de conserver les sorties. |
| R2 7–8, 11–12 | Cours bref et exemples séparés des exercices : comptage de documents, titre facultatif, notice d'archive. Ces données ne se confondent pas avec celles du sujet. |
| R2 15–18, 21–22 | Explications sur les deux exclusions, prédiction avant modification et classement complet. La cellule 18 indique qu'elle ne remplace pas la trace évaluée ; c'est compréhensible pour organiser le travail. |
| R2 25 | Les étapes de restitution parlent à l'étudiant. Le commentaire « URL injectée lors du déploiement » signale la préparation technique du bloc ; le responsable précise qu'il appartient au format canonique explicitement fourni par l'utilisateur. Ce bloc est conservé dans cette PR et ne constitue pas un paragraphe de cours adressé à l'auteur. Le lien effectif n'est pas vérifié. |
| TD1 1–8 | Objectifs, étapes et durées sont annoncés ; distinction bibliothèque/modèle/pipeline/Doc/Token. Préparation fournie explicitement hors travail à réécrire. L'erreur de chargement a un recours identifié : l'enseignant. Contexte historique de Faguet expliqué. |
| TD1 9–15 | Cours sur forme/lemme/POS/tag, exemple distinct, position caractère versus rang et essai personnel c13. La ligne JSON fournie n'est pas présentée comme un nouvel algorithme à maîtriser. |
| TD1 18–19, 22–23, 26–27 | Phrases, filtres et dépendances sont introduits avant leur exercice, avec vocabulaire défini et exemples à données distinctes. Les annotations sont explicitement discutables. |
| TD1 30–31 | Conventions de découpage expliquées ; le blocage initial de chaîne multiligne est levé par la séquence échappée relue en cellule 31. |
| TD1 36–38 | Bilan, export optionnel pour la suite, conservation du notebook avec figure et sorties, score technique provisoire et rôle enseignant sont explicites. Je sais où retrouver l'export dans Colab sans avoir testé cette indication. Même bloc canonique de restitution que R2, conservé. |
| TD1B 1–6 | Parcours après TD1, quatre activités, absence de note automatique, pas de JSON à produire ; installation de md et contrôle des versions expliqués. |
| TD1B 7–8, 12–13 | Différence entre limites d'une catégorie et erreur du modèle, puis entre détection et filtre. Les exemples montrent ce qu'on observe sans imposer leurs prédictions comme réponses. |
| TD1B 17–18 | Cours accessible sur les vecteurs, le score et ses limites, exemple de deux mots distincts des exercices. |
| TD1B 22–24 | Exemple de règle avec pipeline propre ; explication d'une absence possible de différence et du label DATE choisi manuellement. |
| TD1B 28–30 | Un bilan supplémentaire est demandé en cellule Markdown 29 pour les trois méthodes. Conserver les essais décevants est une action explicite. Relecture enseignante sans note automatique rappelée. Même bloc canonique de restitution que R2, conservé. |

## État de validation, hypothèses et critères de levée

**Verdict après relecture ciblée : favorable à la compréhension des quatorze tâches, sans blocage de lecture restant.** Le blocage de l'exemple TD1 cellule 31 et les deux difficultés lexicales de TD1B sont levés. Les petites hésitations non bloquantes de TD1 Q1, Q4 et Q6 restent explicitement signalées : elles ne sont pas comblées par des connaissances de spécialiste. Cette note ne vaut ni verdict technique, ni validation éditoriale, ni validation pédagogique complète.

Hypothèse de travail : l'étudiant a suivi S1 et réalise TD1 avant TD1B et R2 ; cela permet de retrouver les acquis, sans prouver leur maîtrise. R1 est une révision autorisée. Les exemples fournis sont des ressources à lire et exécuter lors de la séance humaine, pas des résultats déjà observés dans cette revue.

Seconde lecture ciblée : TD1 cellules 1, 31 et 38 ; TD1B cellules 9, 12 et 14 ; R2 cellules 15 et 19. Outre les corrections ci-dessus, la restriction de caractères de TD1 est désormais explicitement limitée au numéro étudiant ; elle ne peut plus se lire comme une interdiction des accents dans les noms. R2 emploie « mot vide », expliqué comme appartenance à une liste, et précise que la réponse doit être écrite dans la cellule ci-dessous. La distinction avec les exclusions personnelles reste claire. Le mécanisme canonique de restitution est conservé conformément à la précision du responsable ; la remarque initiale sur son commentaire n'est pas une demande de modification dans cette PR.

Le responsable rapporte séparément la réussite de quinze exemples enseignants exécutés après correction. Ce résultat n'a pas été reproduit par ce rôle et ne se transforme pas en essai Colab ou en résolution étudiante. La durée réelle de travail pour un novice n'a pas été mesurée ; les durées imprimées restent des repères à éprouver en séance. Les hésitations non bloquantes sur la portée des commentaires de TD1 restent à apprécier par les revues pédagogique et éditoriale.

Dernier contrôle ciblé : relecture de la seule cellule d'installation TD1, indice 5, identifiant `c4eb9544f889`. Elle ajoute `IPython==8.37.0` aux dépendances fournies. Cet ajout reste dans la préparation à exécuter sans réécriture et ne crée aucune notion ni action nouvelle à apprendre dans les quatorze questions. Le responsable indique qu'il vise le fonctionnement de displaCy ; ce rôle n'a pas exécuté l'installation ni vérifié le rendu. Les quatorze tâches inchangées n'ont pas été relues à cette étape. Le verdict de compréhension reste favorable et l'empreinte TD1 ci-dessous a été recalculée.

Non vérifié : exécution Python, versions réellement installées, téléchargements, annotations et scores du modèle, rendu displaCy, restitution effective, affichage dans Colab, export et réception du serveur. **Aucun test Colab n'a été réalisé.** Aucun accès aux tests ou au correcteur ne sert de preuve de compréhension.

Repères de la version après corrections et relecture ciblée (SHA-256) :

- R2 : `a74becd52bbfbc09a7643d4fd3cd5060daa69f9983308641c7d391e9f84b7e34`.
- TD1 : `d8b38f08f425ef46fa1ae420fc15a32e96ac71dd07d2d9a2486dba5ef973e2bb`.
- TD1B : `023abc0989f0a3fb35de7a16780681d63d2b0804f5ca7aea07bbc2d42497bf2b`.
- `exemples.json` : `e2a30148bf43f703129a7ab103e1f3173982f8e9902c87be4bd781e7a8b497af`.

Fichier écrit par ce rôle : cette note uniquement. Aucune solution complète n'a été produite. Verdicts demandés à d'autres rôles : revue pédagogique et revue éditoriale indépendantes, puis vérification technique humaine pour ce qui relève de l'exécution.
