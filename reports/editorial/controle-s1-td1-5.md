# Revue éditoriale indépendante — Contrôle final S1, TD1 à TD5

## Périmètre et verdict

- Mission : appliquer les quatre substitutions Q5, Q24, Q25 et Q30 acceptées par l'enseignant, corriger les incohérences présentées, aligner le barème.
- Branche : `pedagogy/controle-s1-td1-5`.
- Réviseur : agent indépendant `editorial_review`, rôle TAL-Editorial-Reviewer ; aucun passage du sujet n'a été produit ou modifié par ce réviseur.
- Support relu : `Notebooks contrôles finaux/DevoirS1.ipynb`, contrat `Controletilt-s1` v2, semestre S1, mode contrôle.
- Référence historique et technique : le même sujet au commit `2445c9e18357dc6a99a8e516bf0d7bd7e462fd42`, et sa version courante de travail. Les conclusions ne prétendent pas restaurer une référence antérieure non consultée.
- Matrice préalable : `docs/pedagogy/controle_s1_td1_5_coverage.md`. Les quatre substitutions et les réductions correspondantes relèvent de l'accord enseignant du 19 novembre 2026, conservé dans cette matrice.
- Lecture : les 70 cellules, dans leur ordre, soit les 39 cellules Markdown et les 31 cellules de code, commentaires compris ; aucune sortie n'est fournie dans la nouvelle source.
- Destinataire : étudiant. Le contexte caché est un contrat de tuteur, pas une explication à l'étudiant.

**Verdict éditorial : `ACCEPT`.**  
**Lisibilité : `LISIBILITÉ_ÉTUDIANTE_VALIDÉE`.**

Ce verdict porte sur le sujet et sa compréhension statique. Il ne vaut ni validation du correcteur, ni preuve d'exécution, ni verdict de couverture pédagogique, ni décision de fusion. Les observations rédactionnelles résolues et l’alignement technique de Q2 sont consignés ci-dessous. Sujet relu après corrections finales : SHA-256 `033339bc1e14ced85638919998df45aed92c6c74e14426d66e90902f7aa9d13d`.

## Lecture par question

Les cellules `Qn` et `Qn_code` sont relues pour chacune des lignes. Les données et lignes d'affichage sont fournies ; l'étudiant complète ou corrige le traitement. Les tâches qui demandent la lecture d'un résultat (Q21 et Q23) sont identifiées comme telles.

| Question / cellules | Action et données comprises | Production et emplacement | Acquis antérieurs vérifiés | Fourni / construction autonome / ambiguïté |
|---|---|---|---|---|
| Q1 / Q1_code | Convertir `"3000"` et calculer un coût au tarif 0.05 | Montant dans `valeur_Q1`, affichage conservé | TD1, `td1-s1-prompt-q5`, conversion ; `s1-editorial-td1-enonce-q1`, coût | Calcul à corriger ; résultat demandé annoncé, pas de nouvelle solution ajoutée |
| Q2 / Q2_code | Extraire exactement `extraction` d'une chaîne fournie en fixant deux bornes | `valeur_Q2_deb`, `valeur_Q2_fin`, `mot_extrait` dans la cellule | TD2, `s1-editorial-td2-enonce-q3`, indices et tranches | L'extraction fournie reste inchangée ; le nom de la production est désormais cohérent. Les indices positifs ne sont pas imposés : signalement technique ci-dessous |
| Q3 / Q3_code | Corriger l'erreur syntaxique du `if` pour note12/seuil10 | Booléen `valeur_Q3` | TD1 `td1-s1-prompt-q3` ; TD4-A `td4-one-s1-09` | Comparaison fournie désormais compatible avec le résultat demandé ; le défaut syntaxique intentionnel demeure |
| Q4 / Q4_code | Retirer espaces de bord et point final sans perdre la majuscule de `Terminologie` | Chaîne `valeur_Q4` | TD2, `s1-editorial-td2-enonce-q1` et `q2` | La casse est explicitée ; aucune exigence de `strip(chars)` n'est imposée |
| Q5 / Q5_code | Tester langue appartenant au tuple et places strictement positives | Booléen calculé `inscription_possible`, relayé par `valeur_Q5` | DM `dm-s1-enonce-q3`, TD1 `td1-s1-prompt-q3`, TD3-B tuple | Données immuables, expression à construire ; le résultat n'est pas recopié dans le nouveau sujet |
| Q6 / Q6_code | Retirer `morphosyntaxe`, ajouter `segmentation` dans la liste fournie | Liste dans `valeur_Q6` | TD3-A `td3-one-s1-10` | Deux méthodes erronées fournies ; commentaires existants déjà explicatifs conservés |
| Q7 / Q7_code | Compter les mots de longueur strictement supérieure à six | Entier `valeur_Q7` | TD4-A `td4-one-s1-12` ; TD4-C compteurs | Seule la condition est à corriger ; le seuil est sans ambiguïté |
| Q8 / Q8_code | Transformer les éléments de la liste source en majuscules | Liste `valeur_Q8`, ordre conservé | TD4-A `td4-one-s1-06` | Le défaut porte effectivement sur la chaîne littérale ajoutée et non sur un indice ; explication désormais fidèle au code |
| Q9 / Q9_code | Parcourir les trois notes à rebours via `range` | Liste `valeur_Q9` | TD4-B `td4-bis-s1-12` | Paramètres de parcours à corriger ; résultat demandé inchangé |
| Q10 / Q10_code | Initialiser et faire progresser un compte à rebours en conservant sa condition | Liste `valeur_Q10` de cinq valeurs | TD4-B `td4-bis-s1-18` | Faux diagnostic d'IndexError retiré ; tâche désormais déterminée. Commentaire corrigé après signalement |
| Q11 / Q11_code | Consulter la clé absente `cible` avec la valeur de repli `inconnu` | Chaîne `valeur_Q11` | TD5-B `td5-6e3b4d453f33` et son cours | Valeur de repli explicite ; méthode non imposée |
| Q12 / Q12_code | Parcourir les paires du dictionnaire de fréquences | Dictionnaire reconstitué `valeur_Q12` | TD3-C `td3-ter-s1-05` | Ligne de parcours à corriger ; clé et valeur distinguées |
| Q13 / Q13_code | Compter les occurrences de la liste `phrase` | Dictionnaire `valeur_Q13` | TD4-C `td4-ter-s1-18` ; DM `dm-s1-enonce-q13` | Faux diagnostic de KeyError retiré ; la logique du comptage reste à corriger |
| Q14 / Q14_code | Choisir des valeurs de a,b,c déclenchant la branche `Vrai` | Chaîne `valeur_Q14` | TD4-B `td4-bis-s1-36` et conditions TD4-A | Plusieurs réponses numériques sont légitimes ; l'énoncé autorise ce choix et protège les conditions |
| Q15 / Q15_code | Filtrer les clés strictement plus longues que trois caractères | Dictionnaire `longs_mots` puis `valeur_Q15` | TD4-A `td4-one-s1-12` ; TD3-C dictionnaires | Seuil et exclusion de l'égalité explicites ; pas de confusion avec au moins trois |
| Q16 / Q16_code | Retourner la salutation au lieu de seulement l'afficher | Valeur reçue dans `valeur_Q16` | TD5-A `td5-504eaa47e846` | Erreur print/return volontaire ; consigne et test compatibles |
| Q17 / Q17_code | Retourner le carré du paramètre plutôt que son double | Valeur reçue dans `valeur_Q17` | TD5-A `td5-504eaa47e846` | L'expression du carré est déjà fournie dans l'affichage : elle n'est pas à découvrir. La tournure a été simplifiée après signalement |
| Q18 / Q18_code | Construire deux retours selon la longueur du paramètre | `analyse` si longueur au moins6, sinon `court` | TD5-A `td5-ddfe392db1a0` ; TD4-A seuils | Seuil corrigé, cas de `corpus` explicitement cohérent ; fonction à construire |
| Q19 / Q19_code | Compléter deux transformations et conserver l'appel composé | Chaîne `valeur_Q19` | TD2 transformations ; TD5-A `td5-671e1350b9b8`, composition | Retirer les points est une action définie ; pas de généralisation implicite à toute ponctuation |
| Q20 / Q20_code | Calculer longueur et minuscules du paramètre `mot` | Dictionnaire `valeur_Q20` | TD5-C `td5-71a685a37716` | Valeurs attendues annoncées historiquement ; instruction générale impose bien d'utiliser les paramètres, pas de constantes finales |
| Q21 / Q21_code | Prédire un appel avec argument par défaut | Numéro du choix dans `reponse_Q21` | TD5-B `td5-27f065258d53` | Lecture de code et réponse numérique clairement distinguées |
| Q22 / Q22_code | Rendre le second argument facultatif pour l'appel `addition(5)` | Résultat `valeur_Q22` | TD5-B `td5-60707c75c07a` | L'appel, la cible15 et la valeur par défaut à déterminer concordent désormais |
| Q23 / Q23_code | Suivre l'appel `calculer(y)` avec y5 | Valeur de `resultat` dans `reponse_Q23` | TD5-A `td5-504eaa47e846` | Le titre ne prétend plus enseigner une portée absente de l'activité ; production numérique précise |
| Q24 / Q24_code | Construire quatre effectifs à partir de4 et du doublement | Liste `effectifs`, relayée par `valeur_Q24` | DM `dm-s1-enonce-q12`, TD4-B `td4-bis-s1-18` | Quatre tours, donnée initiale, mode de progression et arrêt explicites ; ni série finale ni algorithme complet fourni |
| Q25 / Q25_code | Normaliser les bords et la casse en conservant ponctuation et espaces internes | Liste de trois résultats dans `valeur_Q25` | TD5-A `td5-865f32abb332` ; DM `dm-s1-enonce-q15` | Cas vide et espaces multiples annoncés ; appels et ordre fixes, fonction autonome |
| Q26 / Q26_code | Répartir selon la présence d'au moins une majuscule | Dictionnaire de deux listes `valeur_Q26` | TD4-A `td4-one-s1-30` pour partition ; TD2 `lower()` | `.isupper()` est dans la ligne erronée fournie. La tâche peut être résolue par comparaison avec `lower()` déjà appris ; pas de nouvelle méthode exigée |
| Q27 / Q27_code | Associer chaque mot à sa longueur | Dictionnaire `valeur_Q27` | TD3-A `td3-one-s1-15` ; TD4-C compréhensions | Boucle ou compréhension explicitement acceptées ; pas de méthode arbitrairement imposée |
| Q28 / Q28_code | Traduire si connu, retourner l'inconnu en minuscules | Liste `valeur_Q28` pour dog et CAT | TD5-B `td5-6e3b4d453f33` ; DM `dm-s1-enonce-q17` | Deux cas fournis ; résultat de repli défini et ressource en paramètre |
| Q29 / Q29_code | Conserver le nettoyage fourni, mesurer la phrase originale | Dictionnaire `valeur_Q29` | TD5-C `td5-71a685a37716` ; DM `dm-s1-enonce-q18` | La fonction fournie est maintenant cohérente avec sa description ; faute à corriger limitée à la mesure. Ni tuple passé à strip ni suppression injustifiée d'un blanc après split |
| Q30 / Q30_code | Chercher la chaîne la plus longue, première en cas d'égalité, traiter le vide | Liste de trois résultats dans `valeur_Q30` | TD4-C `td4-ter-s1-09`, TD5-A fonctions et cas vide | Trois situations annoncées, entrée à préserver, calcul par appel ; aucune réponse finale dans la nouvelle cellule |

## Passages hors question

- Première cellule : titre visible puis contexte caché complet ; pas de cellule exclusivement cachée.
- Introduction : périmètre TD1–TD5, production, utilisation des paramètres, ordre d'exécution et conservation des sorties explicites. Aucun résultat enregistré n'est présenté comme une preuve de compréhension.
- Identification : une cellule à compléter, pas de règle nouvelle sur le numéro étudiant.
- Transitions : cinq parties ; la dernière annonce désormais une synthèse sur les textes et les séquences, sans annoncer des fichiers absents des tâches.
- Barème : 5+5+5+10+10 = 35 points de questions, plus1 d'identification ; total36 clairement distingué. Les nouvelles questions gardent leur poids approuvé.
- Sauvegarde : télécharger le `.ipynb` avec ses sorties ; aucune nouvelle consigne de dépôt serveur n'a été inventée.
- Pas de note de conception, de couverture ou d'architecture dans les passages visibles. La version2 est dans les métadonnées, pas dans un discours au mainteneur intégré au sujet.

## Constats et relais

| ID | Gravité / périmètre | Preuve | Effet / reprise demandée | Statut |
|---|---|---|---|---|
| TAL-EDIT-S1-001 | Mineur, rédaction | Q10_code : `CORRECTION REQUISES (LIGNES SUIVANTESS)` | Corriger en `CORRECTIONS REQUISES (LIGNES SUIVANTES)` ; aucune incidence sur l'action à réaliser | Résolu : commentaire relu dans le sujet final |
| TAL-EDIT-S1-002 | Mineur, rédaction héritée | Q17 : « Corrigez de sorte à ce que » | Préférer « Corrigez la fonction pour que… » ; l'objet à corriger reste compréhensible avec la cellule suivante | Résolu : énoncé final relu, « Corrigez la fonction pour que… » |
| TAL-EDIT-S1-003 | Alignement technique à contrôler, hors verdict de lisibilité | Q2 ne contraint pas le signe des indices ; TD2 enseigne les indices négatifs | Les variantes négatives donnant la même tranche doivent être acceptées par le correcteur. Ne pas ajouter rétrospectivement une restriction absente de la consigne | Alignement statique observé : bornes et extrait lus dans la trace, puis tranche de référence ; tests à vérifier par la revue technique |

## Vérifications réellement réalisées

Lecture intégrale du sujet, comparaison avec le sujet de référence par JSON et examen des ressources antérieures désignées dans la table. Contrôles statiques par script Python, sans exécution de cellule :

- séquence des 70 identifiants strictement identique à la référence ;
- première cellule, `metadata.colab.aiContexts` et `metadata.tal_tutor` strictement identiques à la référence ;
- toutes les cellules de code : `outputs=[]`, `execution_count=null` ;
- valeurs de barème relues dans les cinq parties et dans l'introduction ;
- nouvelles substitutions sans résultat final ajouté dans les cellules de réponse.

La duplication du tuteur de contrôle et son refus complet sont conservés structurellement. Aucun essai comportemental Colab, aucune mesure de durée en classe, aucune exécution du notebook ni transmission de copie n'a été effectué dans cette revue. L'injection d'une URL de dépôt et le correcteur relèvent des contrôles techniques du lot ; le présent contrôle ne contient pas de cellule de dépôt source.

## Rapprochement avec la lecture indépendante de l’Étudiant-Modèle

Deux livrables lus après la première revue : `Corrigés modèles/Contrôles finaux/controle-s1-v2/lecture_etudiante.md` et `Controle_S1_v2_corrige_non_execute.ipynb`. La lecture préalable couvre les 30 questions ; la copie emploie une identité fictive et ne contient ni sorties ni compteurs d’exécution. Son état non exécuté est clairement annoncé. Ce contrôle hors épreuve ne constitue pas un essai étudiant réel.

- Q2 : la lecture indépendante confirme que des bornes négatives équivalentes sont légitimes. Une évolution statique du correcteur observée après signalement utilise la tranche de la chaîne de référence et accepte ces bornes ; son test reste une preuve de la revue technique.
- Q28 : la consigne ne demande pas explicitement de normaliser avant la consultation du lexique, alors que TD5-B et DM Q17 le font. La lecture littérale retenue dans la copie (recherche de la clé brute, repli en minuscules) satisfait les données `dog` et `CAT`. Une recherche sur la forme minuscule satisfait aussi les deux appels fournis. La revue n’ajoute aucun test caché sur `DOG`, ni normalisation obligatoire rétrospective : il s’agit d’une limite de généralisation, sans indécidabilité des cas évalués. Ce point n’est pas bloquant.
- Q26 : la méthode erronée `isupper()` n’est pas un acquis démontré par les ressources consultées, mais la comparaison à la forme minuscule résout la tâche avec un acquis antérieur. La copie indépendante confirme cette voie sans introduire `any` ni nouvelle bibliothèque.
- Q7/Q10/Q13/Q17 : plusieurs écritures figurent dans l’ossature fournie sans appui retrouvé (`+=`, `**`, etc.). Elles sont distinguées des traitements à construire ; une affectation ordinaire ou l’expression du carré déjà fournie permet de répondre. La présence dans le sujet n’est pas présentée comme une preuve d’enseignement.
- Q1/Q9/Q12 : les formulations locales résument parfois le résultat, tandis que les lignes d’affichage fournies précisent son emballage. Les instructions générales exigent de conserver ces lignes ; aucune nouvelle contrainte de format n’est découverte seulement par le correcteur.
- Q21/Q23 : il s’agit explicitement de lecture de code avec réponse numérique, et non de questions de calcul dont la réponse finale serait recopiée sans traitement.
- Q27 : la boucle autorisée fournit une voie apprise ; la compréhension de dictionnaire n’est pas imposée.
- Q24 : le classement dans la partie « fonctions et modularité » reste approximatif pour une boucle autonome. L’intitulé local précise néanmoins la tâche et son périmètre ; aucune compétence supplémentaire n’en est déduite.

Les observations du modèle ne révèlent donc pas de blocage supplémentaire de lisibilité. Le verdict éditorial reste `ACCEPT` / `LISIBILITÉ_ÉTUDIANTE_VALIDÉE`, limité aux tâches et cas annoncés.

## Conditions de clôture du lot

Le verdict pédagogique et les tests techniques restent distincts du verdict ci-dessus. Les observations de l’Étudiant-Modèle sont rapprochées ci-dessus ; les deux corrections rédactionnelles ont été constatées dans le sujet final. Relais au Governance-Auditor après réception des revues technique et pédagogique, incluant les tests de Q2. La décision de fusion et de mise en production appartient à l'enseignant.
