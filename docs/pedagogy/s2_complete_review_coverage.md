# Révision complète S2 : matrice de couverture avant conception

Base examinée : `b7650e3d035846a67014b94e463a08cd43b67fb5` (PR 21 fusionnée). Mission : consolider les supports S2 existants sans réduire une activité, un jeu de données, une autonomie ou une compétence. Matrice validée par l’orchestrateur avant conception, le 1er octobre 2026, avec les exceptions techniques et le découpage en séances précisés ci-dessous. Aucun code de copie étudiante n’est exécuté.

## Inventaire et déplacements

Les numéros historiques sont conservés : il existe trois TD formatifs, et non six TD successifs. Les fichiers appelés TD2 et TD4 sont des contrôles dans leurs consignes et dans les routes. Aucun TD1 absent n’est inventé. Les sept sources réunissent 140 questions : 65 formatives, 57 dans les trois contrôles actifs et 18 dans le final inactif.

| Séance | Source | Cible | Mode, couverture, maximum |
|---|---|---|---|
| TD3_S2 | `Notebooks TD/TD3_S2.ipynb` | `Notebooks TD/S2/TD3_S2_algorithmique_structures.ipynb` | TD, Q1–Q30, 30 pts |
| TD5_S2 | `Notebooks TD/TD5_S2.ipynb` | `Notebooks TD/S2/TD5_S2_algorithmes_texte.ipynb` | TD, Q1–Q25, 25 pts |
| TD6_S2 | `Notebooks TD/TD6_S2.ipynb` | `Notebooks TD/S2/TD6_S2_fichiers_ressources.ipynb` | TD, Q1–Q10, 20 pts |
| CONTROLE_TD2_S2 | `Notebooks TD/TD2 - S2.ipynb` | `Notebooks contrôles finaux/S2/Controle_TD2_S2_algorithmique.ipynb` | Contrôle, Q1–Q13, 20 pts |
| CONTROLE_TD4_S2 | `Notebooks TD/TD4_S2.ipynb` | `Notebooks contrôles finaux/S2/Controle_TD4_S2_ensembles.ipynb` | Contrôle, Q1–Q14, 40 pts |
| DEVOIR_MAISON_S2 | `Notebooks TD/devoirMaisonS2.ipynb` | `Notebooks contrôles finaux/S2/Devoir_maison_S2_approfondissement.ipynb` | Devoir noté, Q1–Q30, 40 pts |
| CONTROLE_FINAL_S2 | `Notebooks contrôles finaux/ControleFinalS2.ipynb` | `Notebooks contrôles finaux/S2/Controle_final_S2_algorithmique_fichiers.ipynb` | Contrôle final inactif, Q1–Q18, 20 pts annoncés par sections ; pas de barème fiable par question |

Chaque déplacement a un équivalent intégral immédiat au nouveau chemin. Les routes et identifiants publics restent stables. Les corrigés historiques sont conservés inchangés hors distribution. `Notebooks contrôles finaux/DevoirS2.ipynb` est une solution enseignant, mal nommée et tronquée : elle reste une archive exclue, et non un sujet à réparer ou redistribuer.

## Progression et charge

Le parcours relie les fonctions, collections, conditions et fichiers du S1 à la construction d’un pipeline textuel explicite ; il prépare la comparaison avec la tokenisation et les annotations spaCy, les fréquences, fenêtres et audits quantitatifs du S3. Aucune nouvelle bibliothèque n’est introduite : `math` reste réservé à TD3 Q22 ; l’import historique `Counter` est conservé mais n’autorise pas son usage dans les exercices ; TD5 et TD6 restent en Python natif, TD6 sans regex ni Counter.

L’ordre pédagogique doit suivre les acquis plutôt que la numérotation ancienne : TD3 puis contrôle TD2 (boucles imbriquées, anagrammes et Fibonacci doivent avoir leur atelier préparatoire dans TD3) ; TD5 puis contrôle TD4 sur les ensembles et devoir maison ; TD6 puis final seulement après sa remise en conformité. TD3 doit donc aussi préparer les opérations ensemblistes avancées et l’explication des tests aux bornes. TD5 prépare notamment la transposition du DM par un petit exemple distinct de sa matrice évaluée.

Les 30 exercices du TD3 et les 25 du TD5 sont répartis chacun sur **deux séances accompagnées de 2 h** ; TD6 comporte une séance accompagnée de 2 h. Les trois supports historiques forment ainsi cinq séances formatives, auxquelles s’ajoutent les contrôles et le devoir. **Aucun exercice ne devient optionnel et aucune activité obligatoire n’est externalisée pour tenir artificiellement dans 2 h.** Les estimations ci-dessous sont des repères d’animation, non une durée empirique garantie ; l’enseignant adapte le rythme si nécessaire en conservant toutes les activités.

Chaque séance réserve 5 minutes au lancement, 105 minutes aux activités et 10 minutes à la synthèse. TD3 séance A : Q1–Q5 (25 min), Q6–Q10 (30 min), Q11–Q15 (35 min), essais de transfert (15 min) ; séance B : Q16–Q20 (30 min), Q21–Q25 (35 min), Q26–Q30 (25 min), ateliers préparatoires aux contrôles (15 min). TD5 séance A : Q1–Q5 (30 min), Q6–Q10 (40 min), Q11–Q13 (35 min) ; séance B : Q14–Q18 (35 min), Q19–Q22 (35 min), Q23–Q25 et essai de transposition (35 min). TD6 : Q1–Q3 (25 min), Q4–Q6 (20 min), Q7–Q8 (30 min), Q9–Q10 (30 min). Les exemples et essais sont intégrés à ces plages. Les contrôles conservent leurs durées annoncées ; le final reste à 1 h 30.

## Conservation et structuration communes

- Chaque cellule historique conserve sa source intégrale comme préfixe et son ordre relatif ; les enrichissements sont des cellules nouvelles ou des précisions ajoutées. Les cellules de tuteur et d’identité peuvent être régénérées pour le contrat v2. Une incohérence est corrigée par une précision visible avant l’activité, sans faire disparaître le texte historique ni modifier les données.
- Exceptions bornées validées : corriger le seul titre du contrôle TD4 de « S3 » à « S2 » ; normaliser les seules lignes d’affichage des résultats en `print("Résultat Qn :", valeur)` (TD3 Q1 perd le suffixe euro dans cette trace machine). Les variables, calculs, données et objectifs ne changent pas. Ces exceptions sont explicitement déclarées dans les tests de préservation.
- Métadonnées racine v2 et `cell.id` uniques ; chaque cellule possède un rôle ; une cellule-réponse canonique `Qn` par question. Exemples, essais (`practice`), données fournies, consignes, tuteur, identité et restitution sont exclus des preuves notées.
- Identité nom, prénom, classe et numéro étudiant ; absence de numéro dans TD5 corrigée par insertion de la cellule d’identité.
- Première cellule Markdown et métadonnées portent le même tuteur. Dans un TD S2 : dialogue, questions simplificatrices, théorie et petit exemple distinct ; un fragment de code minimal peut suivre la tentative et l’explication, jamais une solution complète immédiate. Dans un contrôle, devoir maison ou final : aucune assistance, aucun quiz.
- Dernière cellule : restitution HTML canonique avec `__TAL_PUBLIC_URL__`, sans URL de serveur ni sorties enregistrées ; injection au déploiement. Les six supports actifs alimentent dist, le final inactif reste exclu.
- Les apports ciblés commencent par une explication, un exemple sur d’autres données et un essai avec prédiction/observation/interprétation. Aucun exemple ne remplit une réponse évaluée.
- Les valeurs enregistrées et leurs types sont vérifiés dans la bonne question ; booléen distinct de nombre, ensembles non ordonnés. Le code statique doit appuyer la démarche demandée. Commentaires, exemples, code inaccessible et autres questions ne doivent pas créer de preuve. Absence, résultat incorrect et preuve non vérifiable sont distingués ; ce n’est pas une exécution ni une garantie de correction de tout Python possible.

## Matrice question par question

Toutes les lignes ci-dessous sont obligatoires, données et autonomie historiques conservées. `RENFORCÉ` signifie ajout d’explications/essais dans un TD ; `CONSERVÉ / DÉPLACÉ` signifie contrôle déplacé et contrat clarifié, sans aide nouvelle.

### TD3_S2

| Question | Source et production historique | Cible |
|---|---|---|
| Q1 | Exercice 1 : calculer un coût total avec conversion de types ; cellule 7 ; données et résultat imprimé conservés | RENFORCÉ |
| Q2 | Exercice 2 : extraire une sous-chaîne par indices ; cellule 9 ; données et résultat imprimé conservés | RENFORCÉ |
| Q3 | Exercice 3 : écrire une condition composée ; cellule 11 ; données et résultat imprimé conservés | RENFORCÉ |
| Q4 | Exercice 4 : nettoyer une chaîne de caractères ; cellule 13 ; données et résultat imprimé conservés | RENFORCÉ |
| Q5 | Exercice 5 : choisir la structure adaptée ; cellule 15 ; données et résultat imprimé conservés | RENFORCÉ |
| Q6 | Exercice 6 : modifier une liste avec insert et pop ; cellule 17 ; données et résultat imprimé conservés | RENFORCÉ |
| Q7 | Exercice 7 : compter avec une boucle et enumerate ; cellule 19 ; données et résultat imprimé conservés | RENFORCÉ |
| Q8 | Exercice 8 : utiliser une compréhension de liste ; cellule 21 ; données et résultat imprimé conservés | RENFORCÉ |
| Q9 | Exercice 9 : compter des occurrences avec un dictionnaire ; cellule 23 ; données et résultat imprimé conservés | RENFORCÉ |
| Q10 | Exercice 10 : écrire une boucle while correcte ; cellule 25 ; données et résultat imprimé conservés | RENFORCÉ |
| Q11 | Exercice 11 : définir une fonction simple ; cellule 27 ; données et résultat imprimé conservés | RENFORCÉ |
| Q12 | Exercice 12 : utiliser un paramètre par défaut ; cellule 29 ; données et résultat imprimé conservés | RENFORCÉ |
| Q13 | Exercice 13 : trier une liste avec key ; cellule 31 ; données et résultat imprimé conservés | RENFORCÉ |
| Q14 | Exercice 14 : manipuler des ensembles ; cellule 33 ; données et résultat imprimé conservés | RENFORCÉ |
| Q15 | Exercice 15 : gérer une erreur avec try et except ; cellule 35 ; données et résultat imprimé conservés | RENFORCÉ |
| Q16 | Exercice 16 : implémenter un factoriel itératif ; cellule 37 ; données et résultat imprimé conservés | RENFORCÉ |
| Q17 | Exercice 17 : trouver un maximum et sa position ; cellule 39 ; données et résultat imprimé conservés | RENFORCÉ |
| Q18 | Exercice 18 : produire des bigrammes ; cellule 41 ; données et résultat imprimé conservés | RENFORCÉ |
| Q19 | Exercice 19 : construire un dictionnaire avec zip ; cellule 43 ; données et résultat imprimé conservés | RENFORCÉ |
| Q20 | Exercice 20 : filtrer avec une compréhension ; cellule 45 ; données et résultat imprimé conservés | RENFORCÉ |
| Q21 | Exercice 21 : choisir la bonne complexité ; cellule 47 ; données et résultat imprimé conservés | RENFORCÉ |
| Q22 | Exercice 22 : calculer une moyenne et un écart-type ; cellule 49 ; données et résultat imprimé conservés | RENFORCÉ |
| Q23 | Exercice 23 : renseigner une valeur calculée ; cellule 51 ; données et résultat imprimé conservés | RENFORCÉ |
| Q24 | Exercice 24 : écrire une fonction de recherche linéaire ; cellule 53 ; données et résultat imprimé conservés | RENFORCÉ |
| Q25 | Exercice 25 : écrire une fonction récursive simple ; cellule 55 ; données et résultat imprimé conservés | RENFORCÉ |
| Q26 | Exercice 26 : produire un dictionnaire par compréhension ; cellule 57 ; données et résultat imprimé conservés | RENFORCÉ |
| Q27 | Exercice 27 : sélectionner les deux plus grandes valeurs ; cellule 59 ; données et résultat imprimé conservés | RENFORCÉ |
| Q28 | Exercice 28 : filtrer des stopwords ; cellule 61 ; données et résultat imprimé conservés | RENFORCÉ |
| Q29 | Exercice 29 : produire toutes les paires entre deux listes ; cellule 63 ; données et résultat imprimé conservés | RENFORCÉ |
| Q30 | Exercice 30 : implémenter l'algorithme d'euclide ; cellule 65 ; données et résultat imprimé conservés | RENFORCÉ |
### TD5_S2

| Question | Source et production historique | Cible |
|---|---|---|
| Q1 | Exercice 1 : Carrés des pairs ; cellule 3 ; données et résultat imprimé conservés | RENFORCÉ |
| Q2 | Exercice 2 : Filtrage de mots ; cellule 4 ; données et résultat imprimé conservés | RENFORCÉ |
| Q3 | Exercice 3 : Dictionnaire de longueurs ; cellule 5 ; données et résultat imprimé conservés | RENFORCÉ |
| Q4 | Exercice 4 : Inversion de phrase ; cellule 6 ; données et résultat imprimé conservés | RENFORCÉ |
| Q5 | Exercice 5 : Association (Zip) ; cellule 7 ; données et résultat imprimé conservés | RENFORCÉ |
| Q6 | Exercice 6 : Palindrome ; cellule 9 ; données et résultat imprimé conservés | RENFORCÉ |
| Q7 | Exercice 7 : Anagrammes ; cellule 10 ; données et résultat imprimé conservés | RENFORCÉ |
| Q8 | Exercice 8 : Distance de Hamming ; cellule 11 ; données et résultat imprimé conservés | RENFORCÉ |
| Q9 | Exercice 9 : Générateur d'acronyme ; cellule 12 ; données et résultat imprimé conservés | RENFORCÉ |
| Q10 | Exercice 10 : Chiffrement de César ; cellule 13 ; données et résultat imprimé conservés | RENFORCÉ |
| Q11 | Exercice 11 : Aplatissement de liste ; cellule 15 ; données et résultat imprimé conservés | RENFORCÉ |
| Q12 | Exercice 12 : Fusion de dictionnaires ; cellule 16 ; données et résultat imprimé conservés | RENFORCÉ |
| Q13 | Exercice 13 : Inversion de dictionnaire ; cellule 17 ; données et résultat imprimé conservés | RENFORCÉ |
| Q14 | Exercice 14 : Tri complexe ; cellule 18 ; données et résultat imprimé conservés | RENFORCÉ |
| Q15 | Exercice 15 : Élément le plus fréquent ; cellule 19 ; données et résultat imprimé conservés | RENFORCÉ |
| Q16 | Exercice 16 : Tokenisation simple ; cellule 21 ; données et résultat imprimé conservés | RENFORCÉ |
| Q17 | Exercice 17 : Suppression des mots vides (Stopwords) ; cellule 22 ; données et résultat imprimé conservés | RENFORCÉ |
| Q18 | Exercice 18 : Bigrammes ; cellule 23 ; données et résultat imprimé conservés | RENFORCÉ |
| Q19 | Exercice 19 : Trigrammes ; cellule 24 ; données et résultat imprimé conservés | RENFORCÉ |
| Q20 | Exercice 20 : Indice de Jaccard ; cellule 25 ; données et résultat imprimé conservés | RENFORCÉ |
| Q21 | Exercice 21 : Calcul de TF (Term Frequency) ; cellule 27 ; données et résultat imprimé conservés | RENFORCÉ |
| Q22 | Exercice 22 : Produit scalaire (Dot product) ; cellule 28 ; données et résultat imprimé conservés | RENFORCÉ |
| Q23 | Exercice 23 : Plus long préfixe commun ; cellule 29 ; données et résultat imprimé conservés | RENFORCÉ |
| Q24 | Exercice 24 : Matrice de co-occurrence (simplifiée) ; cellule 30 ; données et résultat imprimé conservés | RENFORCÉ |
| Q25 | Exercice 25 : Pipeline complet ; cellule 31 ; données et résultat imprimé conservés | RENFORCÉ |
### TD6_S2

| Question | Source et production historique | Cible |
|---|---|---|
| Q1 | Exercice 1 : Lecture simple ; cellule 8 ; données et résultat imprimé conservés | RENFORCÉ |
| Q2 | Exercice 2 : Lecture ligne à ligne (Liste) ; cellule 9 ; données et résultat imprimé conservés | RENFORCÉ |
| Q3 | Exercice 3 : Nettoyage d'une ligne ; cellule 10 ; données et résultat imprimé conservés | RENFORCÉ |
| Q4 | Exercice 4 : Tokenisation ; cellule 13 ; données et résultat imprimé conservés | RENFORCÉ |
| Q5 | Exercice 5 : Filtrage numérique ; cellule 14 ; données et résultat imprimé conservés | RENFORCÉ |
| Q6 | Exercice 6 : Stopwords (Mots vides) ; cellule 15 ; données et résultat imprimé conservés | RENFORCÉ |
| Q7 | Exercice 7 : Pipeline complet ; cellule 18 ; données et résultat imprimé conservés | RENFORCÉ |
| Q8 | Exercice 8 : Comptage (Fréquences) ; cellule 19 ; données et résultat imprimé conservés | RENFORCÉ |
| Q9 | Exercice 9 : Écriture CSV simple ; cellule 22 ; données et résultat imprimé conservés | RENFORCÉ |
| Q10 | Exercice 10 : Formatage avancé ; cellule 23 ; données et résultat imprimé conservés | RENFORCÉ |
### CONTROLE_TD2_S2

| Question | Source et production historique | Cible |
|---|---|---|
| Q1 | print(f"Résultat Q1 : {valeur_Q1}") ; cellule 5 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q2 | print(f"Résultat Q2 : {valeur_Q2}") ; cellule 7 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q3 | print(f"Résultat Q3 : {valeur_Q3}") ; cellule 9 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q4 | print(f"Résultat Q4 : {valeur_Q4}") ; cellule 11 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q5 | print(f"Résultat Q5 : {valeur_Q5}") ; cellule 13 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q6 | print(f"Résultat Q6 : {valeur_Q6}") ; cellule 16 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q7 | print(f"Résultat Q7 : {valeur_Q7}") ; cellule 18 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q8 | print(f"Résultat Q8 : {valeur_Q8}") ; cellule 20 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q9 | print(f"Résultat Q9 : {valeur_Q9}") ; cellule 22 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q10 | print(f"Résultat Q10 : {valeur_Q10}") ; cellule 25 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q11 | print(f"Résultat Q11 : {valeur_Q11}") ; cellule 27 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q12 | print(f"Résultat Q12 : {valeur_Q12}") ; cellule 29 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q13 | print(f"Résultat Q13 : {valeur_Q13}") ; cellule 31 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
### CONTROLE_TD4_S2

| Question | Source et production historique | Cible |
|---|---|---|
| Q1 | print(f"Résultat Q1 : {valeur_Q1}") ; cellule 5 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q2 | print(f"Résultat Q2 : {valeur_Q2}") ; cellule 7 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q3 | print(f"Résultat Q3 : {valeur_Q3}") ; cellule 9 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q4 | print(f"Résultat Q4 : {valeur_Q4}") ; cellule 12 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q5 | print(f"Résultat Q5 : {valeur_Q5}") ; cellule 14 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q6 | print(f"Résultat Q6 : {valeur_Q6}") ; cellule 16 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q7 | print(f"Résultat Q7 : {valeur_Q7}") ; cellule 18 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q8 | print(f"Résultat Q8 : {valeur_Q8}") ; cellule 20 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q9 | print(f"Résultat Q9 : {valeur_Q9}") ; cellule 23 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q10 | print(f"Résultat Q10 : {valeur_Q10}") ; cellule 25 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q11 | print(f"Résultat Q11 : {valeur_Q11}") ; cellule 27 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q12 | print(f"Résultat Q12 : {valeur_Q12}") ; cellule 29 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q13 | print(f"Résultat Q13 : {valeur_Q13}") ; cellule 31 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q14 | print(f"Résultat Q14 : {valeur_Q14}") ; cellule 33 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
### DEVOIR_MAISON_S2

| Question | Source et production historique | Cible |
|---|---|---|
| Q1 | Q1: Slicing: extrayez 'bon' de 'bonjour'. ; cellule 4 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q2 | Q2: Ajoutez 4 à la liste [1, 2, 3]. ; cellule 5 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q3 | Q3: Récupérez le dernier élément de [1, 2, 3]. ; cellule 6 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q4 | Q4: Récupérez la valeur de 'age'. ; cellule 7 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q5 | Q5: Ajoutez 'ville': 'Paris' au dictionnaire. ; cellule 8 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q6 | Q6: Calculez la somme de [1, 2, 3]. ; cellule 9 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q7 | Q7: Mettez 'test' en majuscules. ; cellule 10 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q8 | Q8: Remplacez 'chat' par 'chien' dans 'mon chat'. ; cellule 11 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q9 | Q9: Trouvez la longueur de la liste. ; cellule 12 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q10 | Q10: Créez un set des éléments uniques. ; cellule 13 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q11 | Q11: Vérifiez si 10 est strictement supérieur à 5. ; cellule 14 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q12 | Q12: Séparez 'a-b-c' en liste avec le délimiteur '-'. ; cellule 15 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q13 | Q13: Concaténez [1] et [2]. ; cellule 16 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q14 | Q14: Valeur absolue de -5. ; cellule 17 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q15 | Q15: Maximum de [1, 9, 3]. ; cellule 18 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q16 | Q16: Convertissez la chaîne '42' en entier. ; cellule 19 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q17 | Q17: Arrondissez 3.14159 à 2 décimales. ; cellule 20 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q18 | Q18: Vérifiez (booléen) si 2 est dans [1, 2, 3]. ; cellule 21 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q19 | Q19: Récupérez la liste (list) des clés du dictionnaire. ; cellule 22 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q20 | Q20: Récupérez la liste (list) des valeurs du dictionnaire. ; cellule 23 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q21 | Q21: Compréhension: liste des carrés de 1 à 5 inclus. ; cellule 25 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q22 | Q22: Compréhension: dictionnaire associant x à x**2 pour x dans [1, 2, 3]. ; cellule 26 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q23 | Q23: Filtrez les nombres pairs de la liste avec une compréhension. ; cellule 27 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q24 | Q24: Aplatissez [[1, 2], [3, 4]] avec des boucles imbriquées. ; cellule 28 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q25 | Q25: Comptez les fréquences des lettres dans 'abac'. ; cellule 29 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q26 | Q26: Zippez ['a', 'b'] et [1, 2] pour former un dictionnaire. ; cellule 30 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q27 | Q27: Inversez clés/valeurs du dictionnaire. ; cellule 31 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q28 | Q28: Transposez la matrice (les lignes deviennent des colonnes). ; cellule 32 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q29 | Q29: Trouvez les éléments communs aux deux listes. ; cellule 33 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q30 | Q30: Calculez la factorielle 5*4*3*2*1 de 5 avec une boucle. ; cellule 34 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
### CONTROLE_FINAL_S2

| Question | Source et production historique | Cible |
|---|---|---|
| Q1 | Q1 : Liste des nombres de 0 à 50 divisibles par 3 mais PAS par 9. ; cellule 6 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q2 | Q2 : Filtrage de mots longs ; cellule 7 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q3 | Q3 : Fusion de dictionnaires (Somme des valeurs) ; cellule 8 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q4 | Q4 : Extraction de clés ; cellule 9 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q5 | Q5 : Similarité de Jaccard (Intersection / Union) ; cellule 10 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q6 | Q6 : Nombre total de lignes du fichier 'corpus_litterature.txt' ; cellule 12 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q7 | Q7 : Nombre de lignes NON vides (contenant du texte) ; cellule 13 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q8 | Q8 : Extraction ; cellule 14 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q9 | Q9 : Lecture partielle ; cellule 15 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q10 | Q10 : Fonction de nettoyage ; cellule 17 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q11 | Q11 : Tokenisation complète ; cellule 18 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q12 | Q12 : Suppression des Stopwords ; cellule 19 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q13 | Q13 : Fréquences ; cellule 20 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q14 | Q14 : Le mot le plus fréquent ; cellule 21 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q15 | Q15 : Export CSV trié ; cellule 23 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q16 | Q16 : Sous-corpus filtré ; cellule 24 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q17 | Q17 : Statistiques de longueur ; cellule 25 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |
| Q18 | Q18 : Copie de sauvegarde ; cellule 26 ; données et résultat imprimé conservés | CONSERVÉ / DÉPLACÉ |

## Renforcements ciblés et ambiguïtés à lever

### TD3

Avant Q6 préciser insertion de `spacy` à l’indice 1 puis suppression du dernier élément ; Q7 distinguer indice et valeur avec enumerate ; Q8 expliciter borne exclusive et modulo ; Q9 montrer un accumulateur à deux branches et la variante get ; Q11 distinguer espaces de bord et ponctuation finale. Avant Q13 introduire key/reverse avec fonction de clé puis lambda, et accepter tous les ordres entre longueurs égales. Q15 : division impossible, exception ciblée, valeur None. Q16 : produit initial et intervalle inclusif. Q18 : n−1 positions de bigrammes. Q19 : ordre des listes dans zip et limite de longueur. Q21 : O(1) en moyenne, pas « instantané » garanti. Q22 : variance de population, division par n, racine, données distinctes en exemple. Q24 : recherche et sortie anticipée, tentative présente ET absente. Q25 : cas d’arrêt et diminution garantissant la terminaison, arbre d’appels sur autre valeur. Q26 : compréhension de dictionnaire. Q28 : absence de suppression automatique des mots hors stoplist. Q29 : produit cartésien distinct de bigrammes. Q30 : invariant et diminution du reste, modulo avec diviseur non nul.

Un atelier de transfert prépare les thèmes que les contrôles/DM demandent mais qui ne sont pas couverts : Fibonacci avec seuil sur valeur, anagrammes avec multiplicité, formatage numérique à deux décimales, boucles imbriquées et aplatissement ; opérations set (différence symétrique, inclusion, sur-ensemble) avant leur contrôle. Toutes ces notions restent des essais non notés sur données distinctes.

### TD5

Avant Q6–Q10 cadrer palindrome, anagrammes, longueur égale pour Hamming, alphabet restreint du décalage. Q9 : la règle explicite « première lettre de chaque mot » produit quatre lettres ; la mention TAL historique est un exemple contradictoire à signaler et le correcteur doit suivre la règle, sans filtrer `des`. Q11–Q15 : exemples de listes imbriquées, fusion additive, regroupement à plusieurs valeurs, clé de tri et égalités, mode. Ajouter essai de transposition sur matrice distincte pour préparer le DM. Q18–Q19 : fenêtres et bornes. Q20 : Jaccard sur ensembles, cas vide discuté hors question sans imposer convention silencieuse. Q21 : dénominateur de TF explicite, différent d’un décompte brut. Q22 : deux vecteurs de même longueur, produit puis somme. Q23 : accents conservés et arrêt dès divergence. Q24 est un décompte de vocabulaire dans un seul contexte : **ce n’est pas encore une matrice de cooccurrences** ; garder le travail et ajouter ce cadrage pour le S3. Q25 : justifier l’ordre du pipeline.

### TD6

Q1 : l’instruction mentionne contenu_Q1 alors que la sortie utilise reponse_Q1 : préciser que reponse_Q1 doit contenir le texte lu. Q2 : le fichier fourni n’a pas de saut de ligne final (strip), donc la dernière ligne de readlines n’en contient pas ; corriger l’attendu et expliquer la représentation. Q3 : ponctuation remplacée caractère par caractère, espaces multiples conservés ; les espaces de sortie ne doivent pas être supprimés par le parseur. Q7 : ponctuation élargie fournie, apostrophe et parenthèses comprises ; la fonction Q3 seule n’est pas suffisante. Q8 : comptage par Python natif sans Counter. Q9 : vérifier le fichier entier par une trace complémentaire Q9b, en-tête exact puis paires mot/fréquence sans ordre imposé. Q10 : contenu entier, fréquence décroissante, ex æquo acceptés dans tout ordre ; trace Q10b de l’en-tête du CSV pour prouver son format. Exemples de fichiers UTF-8, modes et relecture, conservation du texte brut, limites des nombres isdigit et de la stoplist préparant l’audit S3.

### Contrôles et devoir

Contrôle TD2 conserve toutes ses consignes et 20 points ; TD4 est bien S2, le titre historique S3 doit être explicitement rectifié. L’affirmation « instantanée O(1) » est à nuancer en complexité moyenne, sans nouvelle aide au raisonnement. Pour DM Q29, le sujet ne prescrit pas le type de collection ni l’ordre : accepter liste/ensemble/tuple des éléments communs, sans doublons. Les autres types prescrits restent exigés. Les commentaires d’aide déjà présents sont historiques : ne pas ajouter de guidage, de cours ni de corrigé dans les contrôles.

## Contrôle final : blocage d’activation documenté

Le sujet a 18 questions, mais `app_correction_controle_Final_S2.py` définit 11 réponses d’un autre sujet, avec identifiant `controle-s2`, numérotation et quantités divergentes. Le sujet annonce des totaux par partie (5, 5, 6, 4) sans pondération détaillée des 18 questions. Ne pas activer ce module sous prétexte qu’il existe. La révision inclut classement, métadonnées, identité, refus tutoriel et restitution ; la source demeure inactive et n’est pas distribuée. Un correcteur indépendant conforme aux 18 Q et un barème validé seront nécessaires à son activation. Les Q15–Q18 doivent vérifier les fichiers relus intégralement (et non seulement existence, première ligne ou nombre de lignes).

## Critères d’acceptation et changement de contrat

`CHANGEMENT_DE_CONTRAT` : six évaluateurs actifs passent en v2, refus explicite des copies anciennes par « mauvaise version du notebook », répertoire de résultats v2 et numéro étudiant. Les six barèmes actifs restent inchangés. Les sept supports conservent leurs 140 questions. La validation exige conservation de toutes les cellules sources (hors tuteur/identité régénérables), correspondance des 65 exercices des profils TD, métadonnées sans doublon, restitution unique finale, traces typées et attachées à Qn, jeux positifs/négatifs de correction, routes et distribution cohérentes. Les ateliers et commentaires personnels peuvent être transmis à l’enseignant mais ne valent pas réponse automatique.

Verdict demandé après mise en œuvre : `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`, puis revue technique indépendante et gouvernance. Le présent document est une spécification de TAL-Prof, pas une auto-validation.

### Alignement final des ateliers et des périmètres de tuteur

Sur mandat explicite de l'orchestrateur, une correction ciblée du manifeste rattache l'atelier anagrammes à TD3 Q27 (tri, ensembles, multiplicité et fonction), à l'endroit où il est effectivement placé. Q30 garde Euclide et Fibonacci. La transposition est préparée uniquement dans TD5 Q11 ; elle est retirée du périmètre TD3 Q29, qui conserve paires et aplatissement. Le synonyme redondant « accumulateur » est retiré de TD3 Q9, où « accumulation » reste présent : aucune notion n'est supprimée. Cette mise en cohérence respecte le plafond de contexte, sans modifier les règles de tuteur. Le producteur cumule ici une mission TAL-Prof limitée au manifeste et sa mission Designer ; la revue et la validation demeurent indépendantes.

Le périmètre TD6 Q1 inclut également l’écriture et `repr` mobilisés par son exemple distinct ; celui de Q10 comprend explicitement la relecture CSV (`open`, `readline`, `readlines`, `int`, `split`). L’appui TD3 Q18 distingue les n−1 bigrammes pour n≥2 et l’absence de fenêtre pour zéro ou un token.
