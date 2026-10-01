# Contrat des productions enregistrées S2 v2

Spécification TAL-Prof complémentaire à la matrice préalable. Les littéraux ci-dessous sont des références enseignantes, jamais à insérer dans un tuteur ni un notebook sujet. Ils dérivent des données des sujets examinés, avec rectifications indiquées. Ils ne constituent pas à eux seuls une preuve d’algorithme : l’évaluateur doit examiner la cellule-réponse et les dépendances réellement liées à son affichage, sans exécuter le code étudiant. Les sorties requises sont `Résultat Qn : ...`, typées par leur trace v2 ; seules les lignes print sont normalisées, sans modification des calculs ni des activités. Les marqueurs auxiliaires ne créent pas de nouvelles questions ni de points.

Les barèmes historiques actifs sont conservés. Résultat absent, incorrect et non vérifiable sont distingués. Les données ordonnées restent ordonnées ; ensembles et dictionnaires se comparent par contenu. Les booléens ne se comparent pas à 0 ou 1. Les réels tolèrent les seuls écarts d’arrondi appropriés. Une valeur ne prouve pas automatiquement la méthode demandée.

## TD3_S2

| Q | Référence sur les données du sujet | Critère complémentaire / tolérance |
|---|---|---|
| Q1 | `300.0` | Nombre 300 entier ou réel ; pas booléen. Le suffixe historique € est retiré de la seule ligne de trace, qui porte la valeur numérique. |
| Q2 | `{'deb': 13, 'fin': 19}` | Les indices deb/fin doivent réellement extraire python. Les indices négatifs Python équivalents sont acceptables si leur découpe est identique. |
| Q3 | `True` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q4 | `'python tal'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q5 | `2` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q6 | `['tal', 'spacy', 'nlp']` | Insertion indice 1, puis retrait du dernier élément explicités dans le sujet. |
| Q7 | `3` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q8 | `[0, 4, 16, 36, 64]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q9 | `{'tal': 2, 'est': 1, 'cool': 1, 'python': 1}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q10 | `[3, 2, 1]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q11 | `'tal'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q12 | `17` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q13 | `[('annotation', 10), ('python', 6), ('tal', 3), ('nlp', 3)]` | Longueur décroissante ; tous les ordres entre tal et nlp sont acceptés. |
| Q14 | `{'intersection': {3}, 'union': {1, 2, 3, 4}}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q15 | `None` | None est une valeur attendue, distincte de l’absence de trace. Le code doit traiter la division impossible. |
| Q16 | `120` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q17 | `{'max': 10, 'index': 1}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q18 | `[('tal', 'est'), ('est', 'cool')]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q19 | `{'a': 1, 'b': 2, 'c': 3}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q20 | `[1, 2, 4, 5, 7, 8]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q21 | `1` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q22 | `{'moyenne': 5.0, 'ecart_type': 2.0}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q23 | `4` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q24 | `True` | Recherche itérative sans opérateur d’appartenance ; le seul True fourni ne prouve pas tous les cas. |
| Q25 | `15` | Récursivité et cas de base ; pas une constante 15. |
| Q26 | `{'tal': 3, 'python': 6, 'spacy': 5}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q27 | `[9, 7]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q28 | `['tal', 'et', 'python']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q29 | `[('analyser', 'corpus'), ('analyser', 'termes'), ('analyser', 'tokens'), ('extraire', 'corpus'), ('extraire', 'termes'), ('extraire', 'tokens')]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q30 | `6` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |

## TD5_S2

| Q | Référence sur les données du sujet | Critère complémentaire / tolérance |
|---|---|---|
| Q1 | `[0, 4, 16, 36, 64, 100, 144, 196, 256, 324, 400]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q2 | `['arbre', 'ecole', 'igloo', 'orange']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q3 | `{'le': 2, 'traitement': 10, 'automatique': 11, 'du': 2, 'langage': 7, 'est': 3, 'passionnant': 11}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q4 | `'passionnant est langage du automatique traitement le'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q5 | `{'nom': 'Dupont', 'prenom': 'Jean', 'age': 25}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q6 | `True` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q7 | `True` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q8 | `2` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q9 | `'TADL'` | RECTIFICATION : initiale de chaque mot => TADL, sans suppression de des. |
| Q10 | `'bcd'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q11 | `[1, 2, 3, 4, 5, 6]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q12 | `{'a': 10, 'b': 25, 'c': 40, 'd': 40}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q13 | `{'Maths': ['Alice', 'Bob'], 'Physique': ['Charlie']}` | Les noms de chaque groupe peuvent être présentés dans tout ordre, sans doublon ni oubli. |
| Q14 | `[('Bob', 15), ('Alice', 12), ('Charlie', 10)]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q15 | `2` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q16 | `['bonjour', 'comment', 'ça', 'va']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q17 | `['chat', 'noir', 'chien', 'dort']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q18 | `[('je', 'suis'), ('suis', 'content')]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q19 | `[('un', 'deux', 'trois'), ('deux', 'trois', 'quatre')]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q20 | `0.5` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q21 | `0.5` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q22 | `32` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q23 | `'progr'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q24 | `{'chat': 1, 'chien': 1}` | Décompte marginal dans un contexte unique, pas une matrice de cooccurrences. |
| Q25 | `['python', 'est', 'super']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |

## TD6_S2

| Q | Référence sur les données du sujet | Critère complémentaire / tolérance |
|---|---|---|
| Q1 | `"Le chat, mange la souris.\nLe chien; aboie fort!!\nL'oiseau vole... dans le ciel.\nLa souris (petite) court vite.\nCHAT et chien sont des amis?\n123 souris mangent 456 graines."` | Chaîne entière exacte ; conserver apostrophe, casse, ponctuation et sauts de ligne. |
| Q2 | `['Le chat, mange la souris.\n', 'Le chien; aboie fort!!\n', "L'oiseau vole... dans le ciel.\n", 'La souris (petite) court vite.\n', 'CHAT et chien sont des amis?\n', '123 souris mangent 456 graines.']` | RECTIFICATION : pas de saut de ligne dans la dernière entrée, car le générateur écrit texte_brut.strip(). |
| Q3 | `'le chien  aboie fort  '` | Deux espaces à la place de ; + espace voisin, deux espaces finaux issus de !! ; ne pas strip la valeur lors du parsing. |
| Q4 | `['le', 'chien', 'aboie', 'fort']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q5 | `['souris', 'mangent', 'graines']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q6 | `['chat', 'souris']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q7 | `['chat', 'mange', 'souris', 'chien', 'aboie', 'fort', 'oiseau', 'vole', 'ciel', 'souris', 'petite', 'court', 'vite', 'chat', 'chien', 'amis', 'souris', 'mangent', 'graines']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q8 | `{'chat': 2, 'mange': 1, 'souris': 3, 'chien': 2, 'aboie': 1, 'fort': 1, 'oiseau': 1, 'vole': 1, 'ciel': 1, 'petite': 1, 'court': 1, 'vite': 1, 'amis': 1, 'mangent': 1, 'graines': 1}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q9 | `['Mot;Frequence', 'chat;2', 'mange;1']` | La trace historique ne porte que les trois premières lignes. Q9b requis : CSV entier, en-tête exact Mot;Frequence, toutes les paires Q8 une seule fois ; ordre quelconque des données. |
| Q10 | `[('souris', 3), ('chat', 2), ('chien', 2), ('mange', 1), ('aboie', 1), ('fort', 1), ('oiseau', 1), ('vole', 1), ('ciel', 1), ('petite', 1), ('court', 1), ('vite', 1), ('amis', 1), ('mangent', 1), ('graines', 1)]` | Tous les mots/fréquences exacts, fréquences décroissantes, ex æquo libres. Q10b requis : en-tête exact Mot;Frequence. L’écriture/relecture sont visibles statiquement. |

## CONTROLE_TD2_S2

| Q | Référence sur les données du sujet | Critère complémentaire / tolérance |
|---|---|---|
| Q1 | `'nohtyP'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q2 | `'chat-chien-souris'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q3 | `'3.14'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q4 | `[1, 4, 9, 16]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q5 | `4` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q6 | `{'Français': 'FR', 'Anglais': 'EN'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q7 | `50` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q8 | `['Alice', 'Charlie']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q9 | `{'b': 2, 'a': 2}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q10 | `[1, 2, 3, 4, 5, 6]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q11 | `[0, 1, 1, 2, 3, 5, 8]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q12 | `True` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q13 | `[12, 20]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |

## CONTROLE_TD4_S2

| Q | Référence sur les données du sujet | Critère complémentaire / tolérance |
|---|---|---|
| Q1 | `{'chat', 'oiseau', 'chien'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q2 | `{'souris', 'chat', 'chien'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q3 | `True` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q4 | `{'data', 'code'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q5 | `{'data', 'code', 'algo', 'python'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q6 | `{'pomme', 'poire'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q7 | `{'linux', 'windows'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q8 | `True` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q9 | `True` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q10 | `{'tag3', 'tag2', 'tag1'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q11 | `{'le', 'est'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q12 | `{'Paul', 'Jean'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q13 | `0.5` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q14 | `True` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |

## DEVOIR_MAISON_S2

| Q | Référence sur les données du sujet | Critère complémentaire / tolérance |
|---|---|---|
| Q1 | `'bon'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q2 | `[1, 2, 3, 4]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q3 | `3` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q4 | `20` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q5 | `{'nom': 'A', 'age': 20, 'ville': 'Paris'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q6 | `6` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q7 | `'TEST'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q8 | `'mon chien'` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q9 | `5` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q10 | `{1, 2}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q11 | `True` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q12 | `['a', 'b', 'c']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q13 | `[1, 2]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q14 | `5` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q15 | `9` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q16 | `42` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q17 | `3.14` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q18 | `True` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q19 | `['a']` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q20 | `[1]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q21 | `[1, 4, 9, 16, 25]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q22 | `{1: 1, 2: 4, 3: 9}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q23 | `[2, 4]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q24 | `[1, 2, 3, 4]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q25 | `{'a': 2, 'b': 1, 'c': 1}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q26 | `{'a': 1, 'b': 2}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q27 | `{1: 'a', 2: 'b'}` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q28 | `[[1, 3], [2, 4]]` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |
| Q29 | `[2, 3]` | Type/ordre non prescrits : liste, tuple ou ensemble des communs sans doublon sont recevables. |
| Q30 | `120` | Type et structure demandés, démarche liée au résultat ; ne pas valider sur un commentaire ou une autre question. |

## Final S2 inactif

Le final conserve ses 18 activités et la durée de 1 h 30. Il reste hors distribution active ; aucune référence du module historique à 11 Q n’est utilisable. L’activation nécessite un correcteur 18 Q et un barème détaillé validé, avec vérification de la sauvegarde et des CSV entiers.

Points d’attention de la référence future : le corpus contient 600 lignes dont 480 non vides ; ses lignes incluent apostrophes et accents, que la fonction clean demandée ne supprime pas. Pour Q8, rechercher PARFUMS sans distinction de casse ; Q9 prend les 50 premiers caractères exacts ; Q10 remplace uniquement ,;:.?! par des espaces. Q11–Q14 doivent donc calculer leurs attendus depuis ces conventions, sans importer la tokenisation plus large du TD6. Q14 peut avoir des ex æquo : accepter tous les maxima légitimes. Q15 exige l’intégralité du CSV trié, pas seulement son en-tête. Q16 respecte la casse L initiale du texte brut. Q17 vérifie toutes les longueurs/fréquences. Q18 exige l’égalité du contenu de la copie, pas seulement son existence.
