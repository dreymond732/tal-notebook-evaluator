# Plan de correction de la restitution étudiante — S1 et S3

Date : 16 octobre 2026. Cadrage TAL-Prof pour la mission `code/rapports-pedagogiques-s1-s3`.
Référence technique inspectée : `c81c38641ecddb66c5ea65c78eafbd2d8d3cbbc5` ; inventaire tiré du catalogue actif, des modules et des sujets de cette révision. Les modifications parallèles de la mission ne sont pas des preuves de validation.

## 1. Décision de périmètre et constats

L'enseignant demande une restitution qui montre ce que le correcteur a effectivement retrouvé dans la copie et, à la demande, un exemple de code répondant à chaque question. S1 et S3 sont prioritaires ; S2 vient ensuite. La présente mission porte sur les rapports, pas sur la refonte des TD : aucun notebook source, exercice, tuteur, acquis préalable, marqueur, barème ou règle de validation ne doit être modifié implicitement. Un changement de ce type ouvre un changement de contrat distinct.

Les deux fichiers HTML transmis constituent des preuves de défaut de présentation, pas des copies de notebook utilisables pour reconstruire le code absent :

| Rapport transmis | Constat directement observable | Correctif demandé |
|---|---|---|
| `NON_RENSEIGNE_Non_renseigne_td1-s1.html` | 6/6 ; « validé » dans chaque réponse ; « Reprendre : … » dans chaque solution, même pour une réponse réussie. Aucun code ni résultat de la copie. | Montrer le code et les sorties réellement enregistrés ; donner un exemple spécifique, y compris en cas de réussite ; ne plus présenter un verdict comme une réponse. |
| `NON_RENSEIGNE_Non_renseigne_td1-s3.html` | 0/6 ; « Un print et une sortie JSON uniques sont attendus… » remplace chaque réponse. La solution décrit une condition du validateur ; elle ne permet pas de reconstruire une réponse. | Garder le diagnostic dans une rubrique séparée ; afficher la cellule retrouvée même sans trace exploitable ; proposer code, affichage attendu et explication du critère. |

L'état du dépôt a évolué depuis ces rapports. `s1_revision.py` montre déjà certaines traces et distingue des états ; `s3_audit.py` fait de même, mais conserve un diagnostic comme réponse de repli et tronque silencieusement certains résultats dans le tableau. `revision_s3.py` place encore le feedback dans `student_answer`. Le gabarit commun présente `correct_answer` comme une solution alors que les moteurs lui donnent généralement un commentaire de validation ; la collecte `review_evidence`, conçue pour la consultation des productions, est affichée en annexe sans assurer une comparaison immédiate par question. La présence de cette annexe ne résout pas la confusion des colonnes.

## 2. Inventaire exhaustif des évaluateurs actifs concernés

La source de vérité est `app/notebook_catalog.json`, recoupée avec `EVALUATORS`, `EVALUATOR_MODES`, les wrappers et les cellules `answer`. Ne pas reprendre les effectifs de documents historiques sans ce recoupement. Le nom visible du TD ne remplace jamais son identifiant technique.

| Priorité | Identifiants techniques | Questions notées | Moteur actif et particularités |
|---|---|---:|---|
| P1 S1 | `td1-s1` à `td7-s1` | 6, 7, 6, 7, 6, 6, 7 : **45** | `s1_revision.py` / `s1_reference.py`, avec spécification TD2 dans son module ; sorties `Résultat Q…`, sous-traces Q…a/Q…b, construction syntaxique et dépendances. |
| P1 S3 | `td0-s3` | 7 | `s3_audit.py`, résultats JSON du texte fixé. |
| P1 S3 | `td-r0-s3`, `td-r1-s3`, `td-r2-s3` | 4 chacun : 12 | `revision_s3.py`, valeurs littérales, calculs et commentaires à relire. R1 reste un bonus facultatif. |
| P1 S3 | `td1-s3` : TD1.a | 6 | `s3_audit.py`, référence spaCy `sm` fixée ; productions personnelles et interprétations partiellement contrôlées. |
| P1 S3 | `td1b-s3` : TD1.c | 4 | **Automatique, version 3**, modèle `md` fixé, wrapper dédié et expression de marqueur spécifique. Les documents anciens qui le décrivent comme un reçu sans note ne décrivent plus le catalogue actuel. |
| P1 S3 | `td2-s3` à `td7-s3` | 7 chacun : 42 | `s3_audit.py`, références linguistiques et microcas déterministes ; traces de transfert au corpus et interprétations conservées. |
| P2 S2 | `td3-S2`, `td5-S2`, `td6-S2` | 30, 25, 10 : 65 | `s2_revision.py` / `s2_reference.py` et moteur partagé `check_saved_notebook` ; présenter ultérieurement des exemples propres au S2. La compatibilité de la présentation partagée doit être vérifiée dès P1. |

S1 + S3 : **19 TD ou révisions, 116 questions notées**, sans compter les observations non notées. Les fichiers historiques `formative_s1.py`, `formative_s3.py` et `engine.py` ne définissent pas, à eux seuls, ce périmètre actif : vérifier leurs appels avant toute modification. Aucun moteur historique ou évaluateur inactif n’est réactivé par cette mission. Les PR #31 et #32 ouvertes proposent douze futurs TD `one`/`bis`/`ter` pour TD3, TD4, TD5 et TD6 ; cette mission ne les fusionne pas. Le moteur partagé peut leur fournir code et sorties retrouvés, mais leurs exemples devront être construits depuis leurs sujets stabilisés et relus avant activation. Ne jamais leur attribuer automatiquement les exemples du TD historique de même numéro.

Les contrôles sont un lot de non-régression, pas un lot d'ouverture des réponses : `Controletilt-s1`, `dm-intermediaire-s1`, les sept `controle-td*-s3`, `td2-S2`, `td4-S2`, `ControleDevoirMaisonS2`. Le contrôle final S2 inactif demeure inactif.

## 3. Matrice source → cible : conservation de la couverture

Cette matrice cadre la restitution ; cadrage et implémentation ont été lancés en parallèle. Elle n’autorise aucune réduction des activités des supports.

| Élément substantiel de la source | Objectif / activité / production / autonomie | Cible de restitution | Statut |
|---|---|---|---|
| 45 questions S1, données fixes ou personnelles, sous-traces comprises | Calculer, choisir les structures et fonctions déjà étudiées, enregistrer les résultats et commenter les essais ; conserver le degré de guidage du sujet | Une restitution par question, toutes les sous-traces et la cellule de réponse ; exemple dans le périmètre du TD | CONSERVÉ, restitution RENFORCÉE |
| 71 questions S3, dont révisions et TD1.c v3 | Construire les traitements, conserver leurs preuves, comparer les annotations, contrôler les comptages, transférer au corpus ; autonomie du sujet conservée | Code et sorties repérés ; exemple spécifique ; référence de pipeline précisée ; distinction entre conformité technique et interprétation | CONSERVÉ, restitution RENFORCÉE |
| Prévisions, essais, commentaires, variantes, rédactions et transferts non notés | Faire expliciter l'observation et le raisonnement sans transformer la présence d'un texte en qualité de l'analyse | Conserver les productions rattachées à la question ; signaler « À autoévaluer » ; rappeler les critères du sujet, sans inventer un score | CONSERVÉ |
| Figures / displaCy / sorties riches | Observer puis expliquer une représentation | Signaler précisément les affichages sauvegardés et leur cellule ; conserver la copie pour leur lecture ; aucune exécution HTML/SVG soumis | CONSERVÉ ; rendu riche non promis |
| Notes de validateur, limites répétées et rapports d'audit | Expliquer le fonctionnement aux mainteneurs et rendre les vérifications auditables | Documentation technique / rapports de revue ; dans l'interface étudiante, seulement l'explication utile à la reprise du travail | DÉPLACÉ pour les notes internes ; information utile CONSERVÉE |
| Somme des points, versions, références et tolérances | Autoévaluation technique des preuves enregistrées | Même score et mêmes décisions qu'avant sur les mêmes copies ; libellé explicite de portée | CONSERVÉ |
| Contrôles, devoirs, instructions cachées et refus d'aide | Préserver la confidentialité de la correction et l'autonomie pendant l'épreuve | Reçu public seul ; rapport détaillé conservé dans le circuit enseignant existant | CONSERVÉ |
| 65 questions formatives S2 et archives | Ne pas perdre d'évaluateur lors du changement partagé | Compatibilité et protection immédiates ; complétude des exemples S2 dans le lot P2 | CONSERVÉ ; enrichissement P2 À FAIRE |

Toutes les activités restent dans leur notebook actuel et au moment actuel de la progression. Aucun déplacement d'exercice, suppression de question, remplacement par un exemple ou nouvelle compétence n'est proposé. L'annexe donne la correspondance question → présentation à vérifier ; les productions non notées ne sont pas réputées absentes parce qu'elles ne figurent pas dans le total 116.

## 4. Contrat de présentation étudiante

Chaque question affiche quatre informations distinctes, quelle que soit la réussite :

1. **Question et critère** : numéro et titre du sujet, critère en français courant et points de cette question.
2. **Dans votre notebook** : source exacte de la cellule `answer`, sorties textuelles sauvegardées et éventuelle erreur, avec numéro de cellule suivant l'ordre de la copie et identifiant lorsqu'il existe. Conserver les accents, types et marqueurs. Les sous-traces ne doivent pas disparaître. Ne pas remplacer ces éléments par « validé », un diagnostic ou une paraphrase générée.
3. **Résultat de la vérification** : libellé textuel, raison localisée et action à mener si nécessaire. « Sortie manquante : exécutez puis enregistrez cette cellule » n'est pas « votre calcul est faux ». Un succès ne porte aucune injonction générique à reprendre.
4. **Exemple de réponse**, ouvert à la demande : code propre à cette question, résultat attendu ou exemple de sortie, explication courte reliant méthode et critère, prérequis explicitement nommés. L'exemple ne devient pas un texte attendu à recopier mot pour mot.

Le contrôle d'affichage s'intitule « Afficher les exemples de réponse ». Les exemples sont dissimulés visuellement par défaut ; dans un TD, ils restent présents dans le HTML livré : ce masquage est une aide pédagogique, pas une confidentialité. Ne jamais employer ce mécanisme pour un contrôle.

Pour des cellules longues, un extrait est possible sous réserve d'annoncer explicitement la troncature, son repère et la présence du reste dans le notebook. Ne pas laisser croire à une reproduction complète. Afficher « Aucune sortie enregistrée » lorsque la cellule est présente mais n'a pas de sorties ; « Aucune cellule de réponse retrouvée » lorsque l'association est réellement impossible. Ne pas attribuer arbitrairement une cellule voisine ou une consigne à la réponse étudiante.

L'extraction repose sur les métadonnées et liens déjà utilisés par le contrat (`tal.question`, rôle `answer`, rattachements explicites de relecture), sans élargir ce qui donne des points. Les cellules non attribuées, si utiles au lecteur, restent dans un bloc distinct explicitement non associé à une question. La source affichée peut contenir des commentaires préremplis : la légende décrit une « cellule retrouvée », sans garantir que chaque ligne a été écrite par l'étudiant.

### États à préserver et à rendre lisibles

| État technique | Formulation étudiante | Ce qui ne doit pas être conclu |
|---|---|---|
| `conforme` | Critère technique vérifié | Compréhension, auteur, fraîcheur de l'exécution ou vérité linguistique certifiés |
| `incorrect` | Résultat enregistré différent de la référence ; préciser le critère contrôlé | Que toute la démarche est fausse ou que la sortie a été recalculée sur le serveur |
| `construction_absente` | Résultat enregistré conforme ; méthode demandée non repérée | Que la valeur est fausse ; que toute solution alternative est invalide |
| `preuve_absente` | Résultat manquant ou inexploitable ; expliquer absence, ambiguïté, JSON illisible ou erreur sauvegardée | Une erreur indépendante de calcul |
| `non_verifiable` | Vérification bloquée par une étape préalable ; préciser Q… | Une faute nouvelle de cette question |
| Observation sans point | À autoévaluer avec les critères du TD | Une note nulle, une correction linguistique ou une relecture individuelle promise |

Conserver les décisions numériques existantes : une explication de non-vérifiabilité ne remodèle pas le barème. Si une incohérence du validateur est découverte, la documenter et traiter séparément le changement de contrat. Les icônes ne doivent jamais être l'unique information de statut.

### Exemple pilote S1

Pour Q1 de TD1, un exemple est :

```python
prix_par_mot = 0.12
nb_mots = 125
cout_total = prix_par_mot * nb_mots
print("Résultat Q1 :", cout_total)
```

Sortie : `Résultat Q1 : 15.0`. Explication : multiplier le nombre de mots par le prix d'un mot ; afficher seulement `15.0` saisi comme constante ne montre pas ce calcul. Ne pas imposer cet exemple comme seule écriture correcte.

Pour Q6, utiliser une phrase explicitement illustrative, par exemple `phrase = "Le TAL avance."`, puis `len(phrase)`, `"TAL" in phrase` et `repr(phrase)` avec Q6/Q6b. Annoncer que longueur et booléen varient avec le texte choisi ; ne pas opposer la phrase personnelle de l'étudiant à une phrase unique de correction.

### Exemple pilote S3

Q1 de TD1.a doit montrer une boucle sur `doc`, le filtre demandé, la construction des dictionnaires d'annotations et l'affichage JSON **avec les noms de clés exacts du sujet**. La sortie peut être présentée par un extrait annoncé, suivi de l'indication du nombre total d'annotations. Q5 doit montrer les trois calculs distincts sur `texte_td0` et la sortie de référence `split=47`, `tokens=56`, `non_ponctuation=41` du pipeline fixé. Q4 et Q6 doivent montrer une possibilité commentée ; une interprétation linguistique n'est pas une vérité imposée par l'autocorrection.

## 5. Exemples : couverture par question et destinataires

Créer un catalogue d'exemples applicatif indexé par **identifiant technique + numéro de question**, y compris Q…a/Q…b dans la question mère. Ce catalogue appartient au projet : aucune donnée d'un notebook soumis ne peut choisir un module, une fonction de validation ou du code à exécuter. Aucun exemple n'est construit à partir d'une simple liste de mots-clés du validateur.

Chaque entrée doit comporter : code complet du traitement demandé, données ou prérequis nécessaires, affichage attendu lorsque déterministe, critère expliqué, limite lorsque la réponse est libre. Si une question exige plusieurs essais, une fonction réutilisable, un cas vide, une convention de comptage ou un transfert, l'exemple conserve cette exigence. Un résultat JSON préfabriqué peut illustrer un format ; il ne suffit pas comme exemple de programme lorsque l'objectif est de calculer ce résultat.

| Famille | Construction de l'exemple à vérifier |
|---|---|
| S1 TD1–TD4 | Chaque question et chaque sous-trace ; affectations, types, chaînes, collections, parcours, conditions et comptages demandés ; aucune nouvelle bibliothèque. |
| S1 TD5–TD7 | Fonctions et cas d'essai, lecture/écriture et encodage, structures CSV, expressions régulières et pipeline ; dépendances des questions précédentes explicites ; pas de raccourci supprimant la méthode à apprendre. |
| S3 R0–R2 | Quatre exemples par révision ; calcul et réemploi des fonctions, essais et observations du sujet ; pas de mélange entre valeur attendue et commentaire. |
| S3 TD0 | Sept exemples produisant les mesures sur le texte fixé, avec conventions et exemple des limites de `split`. |
| S3 TD1.a–TD2 | Annotations et positions, phrases, filtres, fréquence, figures et réemploi ; versions de modèle adéquates ; variantes libres signalées. |
| S3 TD1.c | Quatre exemples `md` : entités, filtre et essai personnel, similarités et variation, règles avant `ner` et cinq essais ; aucune assimilation au modèle `sm`. |
| S3 TD3 | Recherche et citations avec données d'origine, positions, provenance et CRLF ; aucun résultat inventé pour remplacer le corpus. |
| S3 TD4–TD7 | Sept exemples par TD ; calculs des microcas, unités et dénominateurs ; préserver séparément la demande de transfert, les figures et l'interprétation du corpus. |

**Étudiant** : question, cellule retrouvée, sorties, diagnostic compréhensible, piste de reprise, exemple, limites utiles. **Enseignant** : éléments de preuve et productions non notées, points à réexaminer, références et limites de la correction, rapport archivé existant. **Agents/mainteneurs** : AST, collecteurs, contrat, règles, stratégie de test et verdicts dans les docs et rapports de revue. Des identifiants de cellules sont des repères pour retrouver sa réponse ; ils ne doivent pas devenir une explication technique du fonctionnement interne du système.

La portée du score apparaît une fois hors du tableau des réponses : « Vérifications sur le code et les sorties enregistrées. Le serveur ne relance pas votre programme. Les commentaires et interprétations restent à autoévaluer. » Compléter seulement selon le TD : conformité à un pipeline fixé, observations linguistiques, figures non certifiées. Le libellé du total évite de faire d'un score technique une validation finale de toutes les compétences. Le rapport ne promet pas un retour individuel systématique de l'enseignant.

## 6. Exécution et partage du travail

| Lot | Responsable producteur | Livrable / vérification |
|---|---|---|
| 0 — cadrage | TAL-Prof | Ce plan, inventaire et matrice ; pas de modification des supports. |
| 1 — S1 | TAL-Code-Architect S1 | Source et sorties par question, exemples des 45 questions et sous-traces ; mêmes notes et références. |
| 2 — S3 | TAL-Code-Architect S3 | Même traitement pour les 71 questions des 12 évaluateurs ; inclure R0–R2, TD1.c v3 et productions non notées. |
| 3 — présentation commune | TAL-Code-Architect interface | Présentation distincte réponse / diagnostic / exemple, accès à la demande, repères et troncatures, séparation des destinataires ; rétrocompatibilité S2 et protection des contrôles. |
| 4 — vérification indépendante | TAL-Code-Auditor, TAL-Pedagogy-Reviewer, TAL-Editorial-Reviewer | Comparaison des décisions avant/après, fidélité des extractions, justesse et niveau des exemples par question, lecture comme étudiant, rendu et sécurité. Aucun producteur ne valide sa propre production. |
| 5 — intégration | TAL-Governance-Auditor puis TAL-Integration-Master indépendant | Couverture prouvée, verdicts distincts, risques et tests consignés ; décision du mainteneur sur fusion et production. Si l’intégrateur a lui-même produit la PR, le statut est `MAINTAINER_REVIEW`, jamais `READY_TO_MERGE` indépendant. |
| 6 — S2 | Nouvelle phase après P1 | Enrichir les 65 questions formatives, après audit des exemples et données propres au S2 ; garder les évaluateurs de mode `controle` protégés. |

Une CI verte, un effectif de questions ou ce plan ne vaut pas revue pédagogique/éditoriale acquise. Les supports restent hors modification ; les textes visibles des rapports et les exemples ajoutés requièrent néanmoins les revues spécialisées du changement mixte.

## 7. Critères d'acceptation et preuves

- Reproduire explicitement les défauts des deux rapports fournis sur des copies synthétiques compatibles avec les contrats actuels. Les HTML seuls ne prouvent pas quel code était dans les copies d'origine.
- Pour chacun des 19 évaluateurs P1, associer toutes les questions à une restitution et à un exemple propre au sujet ; vérifier la correspondance des 116 numéros, des sous-traces et des observations hors score. Aucune question active omise silencieusement.
- Vérifier plusieurs cas utiles : réponse réussie ; résultat faux avec code présent ; code sans sortie ; erreur sauvegardée ; trace illisible ou multiple ; prérequis absent ; réponse libre ; plusieurs sous-traces ; sortie volumineuse ; figure/HTML ; donnée non attribuable. La copie affichée doit rester reconnaissable dans tous ces cas.
- Vérifier qu'un succès ne produit ni « Reprendre » générique ni diagnostic dans la colonne réponse. Une absence de trace laisse visible la cellule retrouvée ; le diagnostic explique pourquoi cette sortie n'a pas été utilisable.
- Vérifier les exemples par comparaison aux sujets et aux références, pas seulement par recherche d'une ligne `print`. Exécuter les exemples de confiance dans un environnement de validation isolé si nécessaire, jamais via le serveur qui reçoit les notebooks. Les exemples dépendant de spaCy utilisent la version et le modèle du sujet ; noter les vérifications non exécutées.
- Comparer avant/après les scores, maximums, décisions et versions sur les fixtures de référence et les cas de non-conformité pertinents. Aucun changement de barème ou tolérance dans ce lot de présentation.
- Vérifier affichage des guillemets, caractères `<`, `>`, esperluettes, accents, code multiligne, source ou sortie contenant `<script>` et SVG. Les contenus soumis restent du texte échappé ; aucun `safe`, JavaScript ou HTML étudiant exécuté.
- Tester le parcours GET/POST de TD sous préfixe proxy, le contrôle d'affichage des exemples, l'ouverture des blocs par question, l'absence de débordement horizontal gênant et l'enregistrement du même contenu utile dans le rapport HTML persistant.
- Tester la non-divulgation des contrôles : aucune réponse, correction, score ou exemple dans le HTML public, y compris dans les éléments cachés, les scripts et les données sérialisées. Vérifier la réussite et l'erreur de persistance.
- Vérifier S2 dès l'évolution du moteur/template partagé : les trois TD formatifs restent consultables et les trois contrôles/devoirs restent des reçus publics ; l'absence d'exemples S2 complets est une limite annoncée, pas une validation P2.
- Vérifier par diff que les notebooks source et leur couverture sont inchangés ; produire des verdicts indépendants explicitant les fichiers relus et les limites de la revue.

## 8. Livraison et limites

Livrer la PR avec un titre et une description informatifs : problème visible, comportement obtenu, 19 évaluateurs et 116 questions visés, fichiers, compatibilité des contrats, preuves, revues et limites. Joindre deux aperçus de rapport reconstruits sans données personnelles réelles : un succès S1 et un échec ou une preuve absente S3. Ne pas présenter les anciennes restitutions anonymisées comme des copies reconstituées de l'étudiant.

Après validation et fusion par le mainteneur, déployer l'application selon sa procédure existante. Les notebooks ne changeant pas, aucune redistribution n'est nécessaire pour ce seul changement de présentation. Les rapports déjà archivés ne se corrigent pas rétroactivement : une nouvelle soumission, ou une régénération explicitement demandée à partir du notebook original encore disponible, est nécessaire. Ne pas déduire des sources manquantes à partir des anciens HTML.

Limites maintenues : analyse statique et sorties sauvegardées ; absence de preuve d'authenticité ou de fraîcheur ; variantes valides éventuellement non reconnues ; qualité des raisonnements, figures et interprétations non certifiée ; écrasement ou changement de politique de stockage hors périmètre. Une limite découverte doit être indiquée à son emplacement utile sans transformer le rapport en documentation d'agents.

Statut de ce document : **plan et inventaire établis**. Implémentation, tests de cette implémentation, revues indépendantes, conformité, fusion et déploiement ne sont pas déclarés acquis.

## Annexe — Inventaire question → cible à vérifier

Pour chaque ligne ci-dessous, la cible conserve le sujet et son autonomie. La restitution doit contenir la cellule retrouvée, les sorties, le diagnostic séparé et un exemple spécifique. Cette liste est extraite des sujets actuels ; elle n'est pas un verdict de qualité sur les exemples à produire.


### S1

| Évaluateur | Question | Activité du sujet conservée |
|---|---|---|
| `td1-s1` | Q1 | Exercice 1 — Calculer un coût de traduction |
| `td1-s1` | Q2 | Exercice 2 — Identifier un type |
| `td1-s1` | Q3 | Exercice 3 — Affectation ou comparaison |
| `td1-s1` | Q4 | Exercice 4 — Insérer des valeurs dans une phrase |
| `td1-s1` | Q5 | Exercice 5 — Convertir avant de calculer |
| `td1-s1` | Q6 | Exercice 6 — Décrire une phrase personnelle |
| `td2-s1` | Q1 | Exercice 1 — À vous de travailler |
| `td2-s1` | Q2 | Exercice 2 — À vous de travailler |
| `td2-s1` | Q3 | Exercice 3 — À vous de travailler |
| `td2-s1` | Q4 | Exercice 4 — À vous de travailler |
| `td2-s1` | Q5 | Exercice 5 — À vous de travailler |
| `td2-s1` | Q6 | Exercice 6 — À vous de travailler |
| `td2-s1` | Q7 | Exercice 7 — Observer et interpréter une limite — 14 min |
| `td3-s1` | Q1 | Exercice 1 — Ajouter, observer, retirer |
| `td3-s1` | Q2 | Exercice 2 — Choisir une référence stable |
| `td3-s1` | Q3 | Données du lexique |
| `td3-s1` | Q4 | Exercice 4 — Parcourir le lexique |
| `td3-s1` | Q5 | Exercice 5 — Distinguer occurrences et formes |
| `td3-s1` | Q6 | Exercice 6 — Comparer deux vocabulaires |
| `td4-s1` | Q1 | Exercice 1 — Transformer chaque mot |
| `td4-s1` | Q2 | Exercice 2 — Filtrer selon la longueur |
| `td4-s1` | Q3 | Exercice 3 — Filtrer selon une lettre |
| `td4-s1` | Q4 | Exercice 4 — `range` et positions |
| `td4-s1` | Q5 | Exercice 5 — `while` avec condition d’arrêt |
| `td4-s1` | Q6 | Exercice 6 — Compter des formes |
| `td4-s1` | Q7 | Exercice 7 — Compréhension de liste |
| `td5-s1` | Q1 | Exercice 1 — Première fonction |
| `td5-s1` | Q2 | Exercice 2 — Normaliser |
| `td5-s1` | Q3 | Exercice 3 — Compter les mots |
| `td5-s1` | Q4 | Exercice 4 — Traduire un mot |
| `td5-s1` | Q5 | Exercice 5 — Traduire une phrase |
| `td5-s1` | Q6 | Exercice 6 — Composer un résumé |
| `td6-s1` | Q1 | Exercice 1 — Lire sans oublier de fermer |
| `td6-s1` | Q2 | Exercice 2 — Lignes utiles |
| `td6-s1` | Q3 | Exercice 3 — Lire une ligne structurée |
| `td6-s1` | Q4 | Exercice 4 — Normaliser une personne |
| `td6-s1` | Q5 | Exercice 5 — Affiliation(s) unique(s) |
| `td6-s1` | Q6 | Exercice 6 — Écrire un CSV |
| `td7-s1` | Q1 | Exercice 1 — Rechercher |
| `td7-s1` | Q2 | Exercice 2 — Extraire plusieurs nombres |
| `td7-s1` | Q3 | Exercice 3 — Extraire des suites de lettres |
| `td7-s1` | Q4 | Exercice 4 — Remplacer des dates |
| `td7-s1` | Q5 | Exercice 5 — Fonction de nettoyage |
| `td7-s1` | Q6 | Exercice 6 — Pipeline de synthèse |
| `td7-s1` | Q7 | Exercice 7 — Limite méthodologique |

### S3

| Évaluateur | Question | Activité du sujet conservée |
|---|---|---|
| `td0-s3` | Q1 | Exercice 1 — Lire et préserver le texte |
| `td0-s3` | Q2 | Exercice 2 — Voir les unités réellement comptées |
| `td0-s3` | Q3 | Exercice 3 — Occurrences et vérification |
| `td0-s3` | Q4 | Exercice 4 — Construire le vocabulaire observé |
| `td0-s3` | Q5 | Exercice 5 — Fréquences brutes et fonction réutilisable |
| `td0-s3` | Q6 | Exercice 6 — Normaliser sans tout confondre |
| `td0-s3` | Q7 | Exercice 7 — Passer du comptage à l’audit |
| `td-r0-s3` | Q1 | 1. Compter les mots |
| `td-r0-s3` | Q2 | 2. Normaliser |
| `td-r0-s3` | Q3 | 3. Fréquences |
| `td-r0-s3` | Q4 | 4. Regard critique |
| `td1-s3` | Q1 | Exercice 1 — Lire puis contrôler les annotations |
| `td1-s3` | Q2 | Exercice 2 — Segmenter et vérifier |
| `td1-s3` | Q3 | Exercice 3 — Comparer trois filtres |
| `td1-s3` | Q4 | Exercice 4 — Visualiser puis expliquer |
| `td1-s3` | Q5 | Exercice 5 — Comparer deux découpages sur une même donnée |
| `td1-s3` | Q6 | Exercice 6 — Réinvestissement autonome et export de preuves |
| `td-r1-s3` | Q1 | 1. Construire et compter les tokens |
| `td-r1-s3` | Q2 | 2. Décrire les tokens dans leur ordre |
| `td-r1-s3` | Q3 | 3. Sélectionner les noms |
| `td-r1-s3` | Q4 | 4. Réutiliser la sélection pour les verbes |
| `td-r2-s3` | Q1 | 1. Fonction |
| `td-r2-s3` | Q2 | 2. Noms et lemmes |
| `td-r2-s3` | Q3 | 3. Filtrer |
| `td-r2-s3` | Q4 | 4. Comparer |
| `td2-s3` | Q1 | Exercice 1 — Lire le corpus et rendre l’annotation inspectable |
| `td2-s3` | Q2 | Exercice 2 — Deux fonctions de fréquences |
| `td2-s3` | Q3 | Exercice 3 — Mesurer l’effet des exclusions |
| `td2-s3` | Q4 | Exercice 4 — Fréquences grammaticales |
| `td2-s3` | Q5 | Exercice 5 — Contrôle qualité et objets recherchés |
| `td2-s3` | Q6 | Exercice 6 — Visualiser sans surinterpréter |
| `td2-s3` | Q7 | Exercice 7 — Généraliser et transférer |
| `td3-s3` | Q1 | Exercice 1 — Fixer le périmètre de la preuve |
| `td3-s3` | Q2 | Exercice 2 — Construire une concordance exacte |
| `td3-s3` | Q3 | Exercice 3 — Comparer des recherches explicites |
| `td3-s3` | Q4 | Exercice 4 — Auditer une citation exacte |
| `td3-s3` | Q5 | Exercice 5 — Qualifier une altération |
| `td3-s3` | Q6 | Exercice 6 — Un rapprochement n’est pas une preuve automatique |
| `td3-s3` | Q7 | Exercice 7 — Assembler un dossier de preuves |
| `td4-s3` | Q1 | Exercice 1 — Présence et marges |
| `td4-s3` | Q2 | Exercice 2 — Compter une paire par phrase |
| `td4-s3` | Q3 | Exercice 3 — Réunion et somme des paires |
| `td4-s3` | Q4 | Exercice 4 — Mesurer une distance entre positions |
| `td4-s3` | Q5 | Exercice 5 — Choisir les frontières |
| `td4-s3` | Q6 | Exercice 6 — Contrôler la normalisation |
| `td4-s3` | Q7 | Exercice 7 — Exporter une mesure contrôlable |
| `td5-s3` | Q1 | Exercice 1 — Donner un dénominateur |
| `td5-s3` | Q2 | Exercice 2 — Fréquent ou associé ? |
| `td5-s3` | Q3 | Exercice 3 — Comparer des tailles de texte |
| `td5-s3` | Q4 | Exercice 4 — Inverser la condition |
| `td5-s3` | Q5 | Exercice 5 — Traiter les absences et les petits nombres |
| `td5-s3` | Q6 | Exercice 6 — Tester la sensibilité du résultat |
| `td5-s3` | Q7 | Exercice 7 — Rédiger une conclusion mesurée |
| `td6-s3` | Q1 | Exercice 1 — Situer les occurrences |
| `td6-s3` | Q2 | Exercice 2 — Découper en segments |
| `td6-s3` | Q3 | Exercice 3 — Comparer une carte de chaleur |
| `td6-s3` | Q4 | Exercice 4 — Visualiser la sensibilité |
| `td6-s3` | Q5 | Exercice 5 — Revenir aux passages |
| `td6-s3` | Q6 | Exercice 6 — Rendre un graphique vérifiable |
| `td6-s3` | Q7 | Exercice 7 — Interpréter et exporter |
| `td7-s3` | Q1 | Exercice 1 — Formaliser une affirmation |
| `td7-s3` | Q2 | Exercice 2 — Construire le moteur commun |
| `td7-s3` | Q3 | Exercice 3 — Vérifier les citations |
| `td7-s3` | Q4 | Exercice 4 — Comparer un nombre défini |
| `td7-s3` | Q5 | Exercice 5 — Traiter groupes et expressions |
| `td7-s3` | Q6 | Exercice 6 — Éprouver sur un cas nouveau |
| `td7-s3` | Q7 | Exercice 7 — Livrer un audit argumenté |
| `td1b-s3` | Q1 | Exercice Q1 — Confronter le repérage humain aux entités détectées |
| `td1b-s3` | Q2 | Exercice Q2 — Extraire les personnes et les organisations |
| `td1b-s3` | Q3 | Exercice Q3 — Des mots aux phrases : que mesure le score ? |
| `td1b-s3` | Q4 | Exercice Q4 — Reconnaître « Université de Toulon », puis éprouver vos règles |
