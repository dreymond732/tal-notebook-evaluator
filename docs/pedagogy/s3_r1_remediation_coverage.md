# S3 — R1 comme remédiation ciblée et autonomie dans les TD

## Cadrage avant conception

Mission du 3 octobre 2026, branche `pedagogy/s3-r1-remediation`. Ce document est produit par TAL-Prof avant la réécriture ; il ne vaut pas revue indépendante du résultat.

**Décision enseignante :** « OK Reprends R1 en ce sens », en réponse à la proposition de conserver R1 comme remédiation ciblée après TD1 selon les difficultés, et non comme une étape obligatoire. Les quatre exercices et leur correcteur restent disponibles. L'enseignant demande aussi de reprendre ses retouches marginales de TD1 et de ne pas faire peser sur lui une relecture systématique des travaux de TD.

**Références effectivement comparées :**

- historique disponible : `2a36752:Notebooks TD/S3/R1_S3_doc_spacy.ipynb`, 11 cellules ; quatre exercices de création de Doc, lecture des annotations et sélection des noms et verbes. Cette référence n'est pas présentée comme le premier état absolu du support ; c'est l'état pédagogique ancien disponible dans cet historique ;
- passage au contrat v2 : même chemin à `c649cfe`, 15 cellules ; précision des quatre traces évaluées, identité, installation et restitution ;
- enrichissement intermédiaire : même chemin à `4fe2e48`, 18 cellules ; repère Q2 et espace d'essais ;
- référence technique au démarrage du lot : même chemin à `2c7dc3c`, 18 cellules, identique pédagogiquement à l'enrichissement précédent ;
- TD1 et TD1B : versions de `2c7dc3c` ; retouches de TD1 apportées par le fichier de l'enseignant `TD1_S3_fondations_spacy(1).ipynb`. La comparaison exacte de ce dernier est à consigner lors de l'intégration ; il ne constitue pas une autorisation de modifier les contrats d'évaluation.

## Place et charge

Titre visible proposé : **R1 S3 — Reprendre le parcours et la sélection des tokens**. Conserver le chemin `R1_S3_doc_spacy.ipynb` et l'identifiant `td-r1-s3` pour garder les liens et le correcteur existants.

R1 se réalise **après TD1, si nécessaire**, avant d'aborder des tâches plus composées. Les critères de recours sont explicites : difficulté à créer ou parcourir un Doc, à distinguer forme/lemme/POS, à construire une liste ou à sélectionner les tokens par leur POS. Les étudiants qui savent déjà réaliser ces opérations poursuivent la progression ; aucun exercice de R1 n'est supprimé pour ceux qui l'utilisent. R1 n'ajoute pas de nouvelle notion TAL au TD1 révisé. R2 garde son rôle distinct de fonctions réutilisables pour filtrer et compter.

La durée indicative de R1 reste **25 minutes**, avec un texte court et une opération principale par question. Elle n'est pas une mesure en classe. Les rappels clarifient les notions déjà vues sans transformer cette remédiation en nouvelle séance obligatoire de deux heures.

## Matrice source → cible

Toutes les activités Q1 à Q4 restent présentes et à réaliser lorsqu'on utilise cette remédiation ; c'est le recours au support complet qui devient conditionnel selon la décision enseignante.

| Source substantielle | Objectif, acquis et données | Activité et production conservées | Cible et statut |
|---|---|---|---|
| Introduction historique puis v2 | Se situer avant les activités suivantes ; durée 25 min | Identifier une difficulté du TD1 et mobiliser ce support si nécessaire | Introduction avec critères de recours après TD1 ; **RENFORCÉ**, changement de positionnement autorisé, sans retrait d'activité |
| Préparation et données fournies | spaCy 3.8.7, modèle français `fr_core_news_sm` 3.8.0 ; texte « Les traducteurs analysent rapidement les nouveaux documents. » | Exécuter les cellules fournies, garder le texte du sujet | Installation et chargement conservés ; **CONSERVÉ**, prose recentrée sur les actions utiles à l'étudiant |
| Q1 historique et `r1-q1-consigne` / `r1-q1-reponse` | Chaîne, variable, `nlp()`, Doc, token, `len`, `print` | Construire `doc`, compter les tokens, ponctuation comprise ; sortie `Résultat Q1 :` | Court rappel distinct de la consigne et vérification ; **RENFORCÉ** |
| Repère Q2 de `4fe2e48`, `s3-review-r1-q2-repere` et `s3-review-r1-q2-essai` | Exemple distinct « La carte change. » ; liste, tuple, boucle et `append` | Observer un triple forme/lemme/POS et pratiquer avant la réponse | Cours, exemple exécutable et espace d'essais identifiables ; **RENFORCÉ**. Ne pas remplacer l'activité par un exemple résolvant le texte du sujet |
| Q2 historique et `r1-q2-consigne` / `r1-q2-reponse` | `token.text`, `token.lemma_`, `token.pos_`, ordre et répétitions | Construire `annotations`, liste complète de triples, ponctuation comprise ; sortie `Résultat Q2 :` ; observation d'une annotation surprenante si nécessaire | Consigne séparée de l'explication et critères de vérification ; **RENFORCÉ**, observation personnelle conservée |
| Q3 historique et `r1-q3-consigne` / `r1-q3-reponse` | Condition `if`, liste, lemme et POS prédit `NOUN` | Construire `noms`, conserver ordre et répétitions ; sortie `Résultat Q3 :` | Rappel du filtre, exemple distinct sur `ADJ`, puis exercice guidé ; **RENFORCÉ**, aucune liste-réponse fournie |
| Q4 historique et `r1-q4-consigne` / `r1-q4-reponse` | Réutilisation de Q3 avec POS `VERB` ; liste vide valide | Construire `verbes`, conserver ordre/répétitions ; sortie `Résultat Q4 :` ; confronter à Q2 en cas de sélection vide | Transfert avec davantage d'autonomie et vérification ; **CONSERVÉ** |
| Interprétation des prédictions | Distinguer annotation calculée et lecture linguistique | Noter un désaccord sans remplacer silencieusement les annotations | Autoévaluation à partir de ses sorties et des critères ; **CONSERVÉ**, pas de promesse de relecture individuelle |
| Identité, version 2, quatre réponses et restitution | Contrat technique actuel, métadonnées, doubles instructions tuteur | Enregistrer sorties et déposer la copie via le HTML distribué | **CONSERVÉ** ; séparateur visuel avant restitution si utile, aucun serveur réel dans Git |

## Périmètre du tuteur et prérequis

Le tuteur reste en mode TD : une demande de résolution déclenche une question ciblée et une attente, pas la fourniture de la réponse. Il conserve le double contexte complet identique, dans la première cellule Markdown et dans les métadonnées Colab.

Bibliothèque autorisée dans les réponses : **`spacy` uniquement**. Les modules d'installation ou d'affichage fournis ne deviennent pas des bibliothèques autorisées pour les solutions. Ni `Counter`, ni expressions régulières, ni nouvelle bibliothèque ne sont nécessaires. Les notions Q1 à Q4 déjà listées dans `tutor_sessions.json` suffisent ; les titres peuvent être harmonisés au support révisé, sans élargissement implicite. Les rappels précèdent leur première réutilisation. Chaque question précise la donnée, l'opération à construire et la production attendue.

## TD1 fourni et absence de relecture systématique

Appliquer les retouches éditoriales demandées par l'enseignant après comparaison du fichier fourni : retirer le commentaire inutile désigné par la différence, présenter Q6 comme **« Exercice non autocorrigé sur le fond linguistique »**, en précisant les vérifications techniques déjà réalisées, conserver intégralement sa réalisation autonome, et séparer visuellement la restitution. Les résultats déjà vérifiables automatiquement gardent le correcteur actuel. Une absence de correction automatique n'est ni une suppression d'exercice ni une promesse de lecture humaine de chaque copie.

Vérifier également les autres phrases du périmètre TD1 qui annoncent un examen avec l'enseignant : garder l'analyse personnelle et les vérifications concrètes, mais ne pas promettre leur relecture systématique. Le score technique ne doit pas être présenté comme un jugement sur la qualité de l'interprétation linguistique.

**TD1B** reste techniquement un dépôt reçu sans note automatique (`human_review`) : aucun nouveau correcteur ni changement de route n'est demandé. Les quatre exercices, les observations, les essais de stabilité et le bilan restent entiers. Leur organisation pédagogique doit annoncer un travail **autoévalué à l'aide des critères du TD**, sans promettre que l'enseignant relira chaque copie. Le libellé technique historique du dépôt ne constitue pas une obligation pédagogique de correction individuelle. La documentation actuelle du lot précédent décrit une relecture humaine : elle doit être signalée comme état antérieur, sans effacer la traçabilité de la décision initiale.

## Critères d'acceptation et limites

- Les quatre objectifs et quatre productions de R1 sont conservés ; aucune réponse n'est préremplie.
- Cours, exemple, consigne et vérification ont des fonctions lisibles ; tous les passages visibles s'adressent à l'étudiant.
- R1 est explicitement une remédiation conditionnelle après TD1, sans notion nouvelle obligatoire.
- Les observations linguistiques restent demandées sans imposer une relecture individuelle ; les critères aident l'étudiant à vérifier son travail sans donner les résultats de l'exercice.
- Les retouches TD1 préservent les six exercices et la technique existante ; TD1B conserve ses quatre exercices sans promesse systématique de correction humaine.
- Les quatre réponses R1, leurs identifiants et le contrat v2 demeurent inchangés ; les versions anciennes gardent le refus déjà prévu.
- Double tuteur et restitution HTML restent vérifiés par les contrôles techniques, distincts des verdicts pédagogiques et éditoriaux.
- La durée réelle, l'efficacité sur les difficultés observées en classe et l'obéissance du LLM de Colab restent non mesurées.

## Validation du cadrage et réalisation

Le 3 octobre 2026, `r1_pedagogy_review`, dans le rôle indépendant TAL-Pedagogy-Reviewer, a validé ce cadrage **avant conception**. Après réalisation, le même rôle a rendu **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**, après comparaison historique et examen de l'ensemble du lot. Le TAL-Editorial-Reviewer indépendant a ensuite rendu **ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE** sur les mêmes 98 cellules et 14 questions, ainsi que le README et les textes de réception concernés ; son rapport est `reports/editorial/s3-r1-remediation.md`. La lecture Étudiant-Modèle est également terminée, sans se substituer à ces deux verdicts spécialisés.

Le lot livré comporte **98 cellules et 14 questions** : R1 (26 cellules, 4 questions), TD1 (40 cellules, 6 questions) et TD1B (32 cellules, 4 questions). Les réponses R1, son correcteur et son contrat v2 sont conservés. Les quatre notions historiques restent travaillées ; le passage au recours conditionnel est la décision enseignante citée plus haut.

| Cible | Rappel ou exemple | Activité étudiante et vérification |
|---|---|---|
| R1 Q1 | `r1-rappel-doc`, `r1-exemple-doc` : texte distinct « Un plan apparaît. » | `r1-q1-consigne`, `r1-q1-reponse` ; compter ponctuation comprise |
| R1 Q2 | `s3-review-r1-q2-repere`, `r1-exemple-annotations` : ancien exemple « La carte change. » conservé et exécutable | `r1-observer-exemple`, `s3-review-r1-q2-essai`, `r1-q2-consigne`, `r1-q2-reponse` ; lire les triples puis construire ceux du sujet |
| R1 Q3 | `r1-rappel-selection`, `r1-exemple-selection` : filtre ADJ sur texte distinct | `r1-q3-consigne`, `r1-q3-reponse` ; sélectionner NOUN, garder ordre et répétitions |
| R1 Q4 | Réemploi des opérations de Q3 | `r1-q4-consigne`, `r1-q4-reponse` ; sélectionner VERB et justifier une liste vide par les annotations observées |
| R1 bilan et restitution | `r1-bilan` | Critères de vérification personnelle, `r1-restitution-separateur` et restitution HTML ; aucune relecture individuelle promise |

### Reprise du fichier TD1 de l'enseignant

Le fichier fourni compte 39 cellules. Son empreinte SHA-256 est `a02cce816440e9af7f8d66738cd5b589d20243a8f113dc14f3717120124492a6`. Comparé au parent `2c7dc3c`, les modifications de source concernent uniquement `f1c4b87024c7` et `94811d622eb5`, sans cellule ajoutée. Ses retouches marginales ne sont pas interprétées comme une demande de reprendre d'éventuelles sorties, données de session ou métadonnées d'exécution.

| Cellule | Différence parent → fichier fourni | Intégration dans la cible |
|---|---|---|
| `f1c4b87024c7` | Suppression de « de 2 h » dans l'annonce du TD1B | Retouche conservée ; phrase R1 précisée pour annoncer son recours selon les difficultés. La durée prévue du TD1B n'est pas réduite |
| `94811d622eb5` | Suppression de la promesse que l'enseignant examinera essais, interprétations, figure et Q6 ; suppression du paragraphe sur la mauvaise version ; phrase de signalement des autres versions conservée | Suppressions conservées ; ajout des limites du score technique et de l'absence de relecture systématique ; correction de « aussi l'enseignant » en « aussi à l'enseignant » |
| Q6 et restitution | Mention et séparateur demandés dans le message mais absents du différentiel de source joint | Mention précise ajoutée à Q6 ; nouvelle cellule séparatrice avant le display. Aucun exercice ni code de réponse supprimé |

Le rejet technique des anciennes versions reste actif malgré le retrait de son explication dans le bilan. Il ne faut pas confondre la suppression d'un paragraphe visible avec la suppression d'une règle du correcteur.


Q6 porte désormais la précision : **« Exercice non autocorrigé sur le fond linguistique. Le correcteur contrôle la structure et certains repères textuels de votre résultat ; il ne juge pas la justesse des lemmes et catégories ni la pertinence de votre question ou de votre interprétation. »** Le point technique déjà attribuable dans le total de six points demeure ; aucun barème n'est supprimé. Les six exercices sont conservés. Les passages de Q4 et du bilan ne promettent plus une relecture systématique par l'enseignant. La restitution bénéficie d'un séparateur visible.

TD1B conserve ses quatre exercices, ses interprétations et son bilan. Le dépôt n'attribue toujours aucune note automatique ; les instructions visibles privilégient l'autoévaluation avec les critères du TD, sans engagement de correction individuelle de chaque copie.

### État exact des supports examinés

| Support | SHA-256 |
|---|---|
| `R1_S3_doc_spacy.ipynb` | `f7d2a865ece47f3c679476cbb164fa6dcc0329871c125480cc137785c374fcbd` |
| `TD1_S3_fondations_spacy.ipynb` | `9de9c90179b5ff99e477a7e8dc8abd99c6089cfd614a5f92aba4788bb46deed1` |
| `TD1B_S3_entites_similarite_regles.ipynb` | `abb86418ddcfcab29b1be7b18ac063a228196d0a74d01af5c690a867fee24069` |

### Vérifications techniques transmises par l'intégration

- 292 tests réussis ; contrats d'évaluation inchangés.
- Trois exemples fournis de R1 exécutés avec spaCy 3.8.7 et `fr_core_news_sm` 3.8.0 : succès. Aucune réponse étudiante exécutée.
- Validation nbformat et analyse AST des trois notebooks : succès.
- Génération et vérification des 34 supports distribués : succès, avec URL de test neutre.
- Audit technique indépendant : **ACCEPT**, 49 tests ciblés réussis, 35 profils tuteur vérifiés et référence de conservation R1 comparée exactement au parent.

Ces vérifications ne remplacent ni la lecture indépendante du français, ni l'essai en classe. À ce stade, **R1 est REVU, avec avis pédagogique et éditorial indépendants favorables** ; les ajustements actuels de TD1 et TD1B ont reçu les mêmes verdicts. Les autres supports ne sont pas déclarés révisés par ce lot. Le statut REVU n'est ni une validation en classe ni une décision de fusion ou de déploiement.

### Orientation pour les reprises suivantes

La décision enseignante fixe l'objectif pratique suivant pour les prochains lots : **pas de relecture individuelle systématique des TD**. Les résultats mécaniquement vérifiables peuvent bénéficier du retour technique déjà prévu ; les exercices ouverts restent à réaliser et s'accompagnent de critères d'autoévaluation, avec des échanges ciblés en cas de difficulté. Il ne faut ni supprimer l'interprétation linguistique, ni inventer une note automatique sur sa qualité, ni transformer chaque dépôt en promesse de correction individuelle. Cette orientation pédagogique documente la demande du mainteneur ; elle ne modifie pas les règles normatives des agents ou les contrats des correcteurs.
