# Revue éditoriale indépendante — rapports simplifiés

## Mission et périmètre

- Rôle : `TAL-Editorial-Reviewer`, indépendant des producteurs du template et du catalogue. Branche : `integration/rapports-simplifies`, reprise de la PR #33.
- Référence Git : `38596070bba39a8535ea8c3cf0c73886d60af27f`, puis fichiers de travail stabilisés le 17 octobre 2026. La comparaison historique porte sur le template à cette révision, avant la simplification.
- Lecture intégrale : `app/templates/corrector_template.html` et les 72 blocs `solution_code`/`solution_explanation` de `app/s1_expansion_feedback.py`, soit les six questions de chacun des douze TD3/4/5/6 one/bis/ter du S1. Les chaînes et éventuels commentaires du code montré aux étudiants sont inclus.
- Lecture complémentaire intégrale du texte rendu des deux exemples `docs/examples/rapport_td1_s1.html` et `docs/examples/rapport_td1_s3.html` : six questions chacun, introduction, portée du score, complément de productions et bilan. Les 116 solutions antérieures ne font pas l'objet d'une nouvelle revue exhaustive dans cette mission.
- Destinataire : étudiant. Le catalogue constitue un exemple de résolution après soumission, distinct des données réellement retrouvées dans la copie ; il ne s'agit ni d'un énoncé ni d'un tutoriel préalable.
- Matrice source → cible examinée : `docs/pedagogy/restitution_simplifiee.md`. Elle porte sur la restitution ; aucun notebook, objectif d'apprentissage ou niveau d'autonomie n'est adapté ici.
- Fichiers écrits par le réviseur : uniquement le présent rapport. Aucune correction du texte audité par son réviseur.

Empreintes SHA-256 des versions relues :

| Fichier | Empreinte |
| --- | --- |
| `app/templates/corrector_template.html` | `c4fbd8dd4498d50783eefaa0ed72020ece3f4337c49bf475018103faa0b66d30` |
| `app/s1_expansion_feedback.py` | `ed6d59571a0bfd63bff2ae4e88c31537898c9e436920d2c4ad83a514d656e02b` |
| `docs/examples/rapport_td1_s1.html` | `f074452110130b78c366d02682cb39a12080378b745796dcc94a4c55c5665d90` |
| `docs/examples/rapport_td1_s3.html` | `337e45b5c9c9e892d06f4d8373a15df4941aaa4b5814ee3380446b2ff3a4c98d` |

## Preuves de lecture par question

Les identifiants ci-dessous repèrent exactement `SOLUTIONS[identifiant][Q - 1]`. Pour chaque ligne, le code fourni apparaît dans « Résultat attendu », et non comme une réponse attribuée à l'étudiant. Les dépendances indiquées sont lisibles dans l'exemple ou annoncées dans l'explication. L'antériorité pédagogique complète des notions dans les notebooks relève de la revue pédagogique distincte ; elle n'est pas déduite de cette lecture éditoriale.

| Question | Action et données lisibles dans l'exemple | Dépendance, précision ou décision de lecture |
| --- | --- | --- |
| td3-one-s1 Q1 | Extraire premier, dernier et tranche de la liste de mots | Borne finale exclue et conservation de la source expliquées. |
| td3-one-s1 Q2 | Ajouter puis retirer le dernier outil | Les deux moments d'affichage et la valeur retournée sont distingués. |
| td3-one-s1 Q3 | Produire une fiche avec longueur pour chaque prénom | Initialisation et trait d'union compté explicités. |
| td3-one-s1 Q4 | Afficher les mois puis construire une ligne | Le rôle de `strip` sur la nouvelle chaîne est précisé. |
| td3-one-s1 Q5 | Alterner mois et nombres de jours | Association par indice et sources inchangées explicites. |
| td3-one-s1 Q6 | Copier une liste puis modifier la copie | La différence entre copie et simple affectation est formulée. |
| td3-bis-s1 Q1 | Créer une référence de langues sous forme de tuple | La stabilité des positions est distinguée de l'exactitude des valeurs. |
| td3-bis-s1 Q2 | Créer un tuple à un élément et extraire une tranche | « Contenant une seule chaîne » lève l'ambiguïté signalée. |
| td3-bis-s1 Q3 | Parcourir les prénoms sans modifier le tuple | Les longueurs et la construction d'une autre liste sont explicites. |
| td3-bis-s1 Q4 | Déballer prénom, âge et taille | Ordre et unités sont indiqués. |
| td3-bis-s1 Q5 | Déballer les couples code/langue pendant le parcours | Association et ordre conservés, sans promesse supplémentaire. |
| td3-bis-s1 Q6 | Construire deux nouvelles références | Le tuple initial reste inchangé ; les nouvelles valeurs sont visibles. |
| td3-ter-s1 Q1 | Ajouter et parcourir les entrées du lexique | La variante langue/langage est acceptée sous condition de cohérence explicite. |
| td3-ter-s1 Q2 | Accéder à une fiche et à la taille de Zoé | Les deux niveaux d'accès et positions sont distingués. |
| td3-ter-s1 Q3 | Inverser un dictionnaire de codes de langues | Le risque de valeurs identiques devenant une même clé est expliqué. |
| td3-ter-s1 Q4 | Comparer occurrences et formes distinctes | Six occurrences, quatre formes et ordre libre de l'ensemble explicités. |
| td3-ter-s1 Q5 | Accumuler les langues observées et tester l'appartenance | Doublons et valeurs booléennes attendues sont distingués. |
| td3-ter-s1 Q6 | Calculer intersection et différences de vocabulaires | Chaque opération est associée à ses formes ; perte des fréquences rappelée. |
| td4-one-s1 Q1 | Transformer les mots en majuscules | Conservation des positions et de la source expliquée. |
| td4-one-s1 Q2 | Filtrer les mots de plus de cinq caractères | Reprise de Q1 et seuil strict annoncés. |
| td4-one-s1 Q3 | Filtrer sans tenir compte de la casse | Reprise de Q1 ; distinction entre test normalisé et mot conservé. |
| td4-one-s1 Q4 | Rechercher e dans Revue, ÉTÉ et une chaîne vide | Résultats True/False/False et conservation des accents explicites. |
| td4-one-s1 Q5 | Répartir les prénoms selon leur longueur | Cas Sonia/Sandra et branche unique rendent la borne claire. |
| td4-one-s1 Q6 | Répartir nombres pairs et impairs | Rôle du modulo et ordre relatif conservé expliqués. |
| td4-bis-s1 Q1 | Construire les positions paires de 0 à 10 | Borne 11 exclue, pas 2 et borne finale obtenue explicites. |
| td4-bis-s1 Q2 | Comparer deux parcours de 10 vers -1 | Le signe du pas explique la liste vide. |
| td4-bis-s1 Q3 | Accumuler les multiples de 7 jusqu'à 70 | Le passage à 77 explique l'arrêt de la boucle. |
| td4-bis-s1 Q4 | Produire vingt multiples avec un compteur | Premier et dernier termes distinguent nombre de termes et valeur du terme. |
| td4-bis-s1 Q5 | Filtrer les cinquante premiers multiples de 13 | Les rangs parcourus et les sept résultats sont explicités. |
| td4-bis-s1 Q6 | Comparer les sommes obtenues avec and et or | Bornes incluses et absence de double compte dans or précisées. |
| td4-ter-s1 Q1 | Compter e dans une phrase mise en minuscules | Le résultat 6 et la différence e/é sont explicites. |
| td4-ter-s1 Q2 | Chercher deux maxima par parcours | Initialisation dans chaque liste ; cas négatif et absence de tri explicites. |
| td4-ter-s1 Q3 | Compter les occurrences d'animaux | Création d'une clé et incrémentation sont distinguées. |
| td4-ter-s1 Q4 | Comparer get et if/else pour les fréquences | Égalité des fréquences et total 8 expliqués. |
| td4-ter-s1 Q5 | Transformer tous les mots en longueurs | La compréhension est présentée sans filtrage. |
| td4-ter-s1 Q6 | Filtrer puis transformer en longueurs | Reprise de Q5 et distinction des deux opérations explicites. |
| td5-one-s1 Q1 | Retourner la longueur d'une chaîne | Type entier et deux résultats 3/6 annoncés. |
| td5-one-s1 Q2 | Répéter un caractère puis réutiliser la valeur retournée | Construction des crochets séparée de la fonction. |
| td5-one-s1 Q3 | Calculer le volume d'une boîte | Résultats 24/0 et possibilité de dimensions décimales lisibles. |
| td5-one-s1 Q4 | Retourner le maximum de trois nombres | Égalités et nombres négatifs explicitement couverts dans le commentaire. |
| td5-one-s1 Q5 | Normaliser les bords et la casse | Espaces intérieurs conservés, portée de chaque méthode claire. |
| td5-one-s1 Q6 | Construire une annonce avec le thème normalisé | Réemploi de Q5 annoncé ; préfixe conservé même avec thème vide. |
| td5-bis-s1 Q1 | Composer une étiquette à deux paramètres | L'inversion des arguments rend l'ordre observable. |
| td5-bis-s1 Q2 | Normaliser localement le paramètre texte | Valeur retournée et variable extérieure sont distinguées. |
| td5-bis-s1 Q3 | Appeler une fonction avec valeurs par défaut | Quatre nombres d'arguments et quatre résultats explicités. |
| td5-bis-s1 Q4 | Saluer avec une formule par défaut ou fournie | Conservation et remplacement de Bonjour clairement distingués. |
| td5-bis-s1 Q5 | Traduire depuis le dictionnaire reçu | Normalisation et comportement du mot inconnu explicites. |
| td5-bis-s1 Q6 | Choisir une valeur pour une traduction absente | La chaîne « absent » et le troisième argument remplacent le terme ambigu signalé. |
| td5-ter-s1 Q1 | Compter les caractères exacts | e et é distingués ; absence de normalisation annoncée. |
| td5-ter-s1 Q2 | Normaliser puis compter les fragments | Fonction fournie annoncée ; résultat 5 et chaîne vide précisés. |
| td5-ter-s1 Q3 | Traduire puis réunir les fragments | Fonction et lexique fournis signalés ; espace de jointure précisé. |
| td5-ter-s1 Q4 | Produire un résumé du texte normalisé | Fonction fournie et Q2 distinguées ; 13 caractères et 3 fragments annoncés. |
| td5-ter-s1 Q5 | Comparer nombres de fragments source et cible | Q2/Q3 cités ; expression traduite à plusieurs mots montrée. |
| td5-ter-s1 Q6 | Résumer successivement les textes d'un corpus | Réemploi de Q4, conservation de l'ordre et des doublons explicites. |
| td6-one-s1 Q1 | Lire un fichier et compter ses caractères | Préparation annoncée ; fins de ligne comprises et fermeture expliquée. |
| td6-one-s1 Q2 | Retenir les lignes non blanches | Réemploi de Q1 ; test strip distinct du texte conservé. |
| td6-one-s1 Q3 | Écrire puis relire deux lignes UTF-8 | Le rôle de repr pour voir les fins de ligne est explicite. |
| td6-one-s1 Q4 | Écarter les lignes blanches puis réécrire | Préparation annoncée ; espaces de bord conservés malgré le test strip. |
| td6-one-s1 Q5 | Chercher la plus longue ligne | Préparation et exclusion des fins de ligne précisées ; fichier vide traité. |
| td6-one-s1 Q6 | Tripler chaque espace et relire | Préparation annoncée ; autres caractères conservés, sans ambiguïté sur « chaque ». |
| td6-bis-s1 Q1 | Lire des couples identité/affiliation | Préparation et découpage au premier point-virgule explicites. |
| td6-bis-s1 Q2 | Écrire trois champs séparés par des points-virgules | Le code postal avec zéro initial reste une chaîne. |
| td6-bis-s1 Q3 | Filtrer les personnes du code 83000 | Fichier de Q2 annoncé ; deux noms et ordre précisés. |
| td6-bis-s1 Q4 | Normaliser quatre variantes d'identité | La normalisation de graphie ne prouve pas l'identité réelle. |
| td6-bis-s1 Q5 | Regrouper les affiliations distinctes | Enregistrements Q1 et fonction Q4 annoncés séparément. |
| td6-bis-s1 Q6 | Regrouper un nouvel atelier avec doublons | Q4 annoncée ; point-virgule interne, lignes blanches et doublons distingués. |
| td6-ter-s1 Q1 | Écrire puis relire un CSV de documents | Préparation/import signalés ; pages relues comme chaînes. |
| td6-ter-s1 Q2 | Lire un CSV avec une virgule dans un champ | Import signalé ; deux colonnes malgré la virgule interne. |
| td6-ter-s1 Q3 | Filtrer les personnes depuis un CSV | Préparation/import signalés ; en-tête exclu et code postal comparé comme chaîne. |
| td6-ter-s1 Q4 | Regrouper les affiliations distinctes | Préparation et fonction fournie annoncées ; dédoublonnage expliqué. |
| td6-ter-s1 Q5 | Exporter puis relire les groupes de Q4 | Dépendance et import annoncés ; sens des trois colonnes précisé. |
| td6-ter-s1 Q6 | Exporter de nouveaux groupes puis relire | Tri explicité ; virgule interne protégée par writer, trois colonnes à la relecture. |

## Template et exemples rendus

- Les intitulés « Votre réponse retrouvée », « Résultat attendu » et « Bilan » distinguent ce qui a été soumis, l'exemple de solution et l'appréciation. Les repères de cellules et les sorties enregistrées restent du côté de la copie.
- Le résultat attendu est visible dès l'ouverture, avec une commande explicite pour le masquer. « Un exemple de code » présente une possibilité de résolution, sans disqualifier une autre solution correcte.
- Pour une réponse validée sans champ obligatoire manquant, le bilan ne contient que ✓. Son libellé accessible signifie que les critères vérifiés sont satisfaits ; il ne prétend pas valider toute interprétation.
- Les états « À reprendre », « Non vérifiable », « Résultat manquant ou inexploitable », « À compléter » et « À autoévaluer » restent distincts. Les textes de reprise s'affichent seulement hors réussite complète.
- L'introduction explique une seule fois la lecture des sorties enregistrées et la nécessité d'exécuter/enregistrer dans l'ordre. La portée détaillée du score et les autres productions sont repliables ; elles ne sont pas répétées après chaque réussite.
- Dans le rendu S1, les six bilans sont ✓ seuls ; code et résultat attendu restent visibles. Dans le rendu S3, le `NameError` de la copie est lisible et les réponses manquantes donnent un état de reprise explicite. Les solutions linguistiques ne prétendent pas fixer arbitrairement les prédictions du modèle ; les transferts ouverts invitent à conserver un choix personnel.

## Constats et résolution

| ID | Gravité | Emplacement et extrait initial | Difficulté et ordre de reprise | Résolution constatée |
| --- | --- | --- | --- | --- |
| TAL-EDIT-RAP-001 | Mineure | td3-bis Q2 : « tuple d'une chaîne entière » | Formulation peu naturelle, pouvant confondre contenance et type ; préciser une seule chaîne. | Producteur : « tuple contenant une seule chaîne ». Relu dans la version stabilisée. |
| TAL-EDIT-RAP-002 | Mineure | td5-bis Q6 : « repli absent » | Terme de programmation inutilement abstrait et valeur littérale peu repérable ; nommer la valeur et l'argument. | Producteur : « la valeur \"absent\" donnée au troisième argument ». Relu dans la version stabilisée. |

Aucun blocage rédactionnel restant dans le périmètre exhaustif déclaré. Les deux reformulations ont été proposées au producteur puis réalisées par lui, sans modification du support par le réviseur.

## Vérifications distinctes et limites

- Lecture des deux fichiers sources complets, comparaison du diff du template, lecture de la matrice et extraction du texte des deux HTML avec BeautifulSoup. La commande d'extraction a été relancée avec l'environnement Python du projet après absence de BeautifulSoup dans le Python système ; extraction finale réussie.
- Contrôle final des nettoyages d'espaces : rendu des deux HTML reconstruit en mémoire sans écriture, anciennes empreintes retrouvées, puis égalité exacte des fichiers finaux avec ce rendu après `rstrip` de chaque ligne et terminaison finale. Pour le catalogue, ancienne empreinte et deux lignes blanches espacées reconstituées ; les 72 couples code/explication après `dedent(...).strip()` sont strictement identiques. Les empreintes ci-dessus correspondent aux fichiers nettoyés. Aucun texte étudiant modifié par ces nettoyages.
- Ce rapport ne remplace pas les tests du rendu, l'audit du code, la vérification exécutable des 72 solutions ni la revue pédagogique. Il ne certifie pas les 116 exemples antérieurs au-delà des douze questions effectivement relues dans les rendus joints.
- Aucun notebook modifié ou soumis ; aucune expérience en classe, navigation visuelle, mesure de durée, exécution humaine Colab ou observation du comportement du tuteur. Les règles de double contexte/tuteur et la progression complète ne sont pas réauditées pour ce changement de restitution.
- L'absence de réduction pédagogique est examinée ici à l'échelle de la restitution : solution, copie, points, états d'incomplétude et rappel d'autoévaluation sont conservés. Le verdict `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` reste de la compétence du réviseur pédagogique indépendant.

## Verdict et relais

- Verdict éditorial : **ACCEPT**.
- Lisibilité : **LISIBILITÉ_ÉTUDIANTE_VALIDÉE**, pour le template simplifié et les 72 nouveaux exemples S1 aux empreintes ci-dessus.
- Blocages éditoriaux restant ouverts : aucun.
- Relais : audit pédagogique et audit de gouvernance indépendants, puis proposition d'intégration au mainteneur. Aucune décision de fusion dans ce verdict.
