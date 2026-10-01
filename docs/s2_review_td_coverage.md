# S2 — bilan de conception des trois TD

Mission TAL-Pedagogy-Designer ; branche `pedagogy/s2-complete-review` ; base `b7650e3d035846a67014b94e463a08cd43b67fb5`. La matrice `docs/pedagogy/s2_complete_review_coverage.md` a été produite par TAL-Prof et validée par l'orchestrateur avant toute modification des notebooks. Ce bilan décrit une production ; il ne vaut pas revue indépendante.

## Couverture conservée et enrichie

| Ancienne source | Nouvelle source dans `Notebooks TD/S2/` | Questions conservées | Apports |
|---|---|---|---|
| TD3_S2.ipynb | TD3_S2_algorithmique_structures.ipynb | Q1–Q30 | Un appui, un exemple distinct et un essai par question ; cinq ateliers préparatoires |
| TD5_S2.ipynb | TD5_S2_algorithmes_texte.ipynb | Q1–Q25 | Un appui, un exemple distinct et un essai par question ; transposition |
| TD6_S2.ipynb | TD6_S2_fichiers_ressources.ipynb | Q1–Q10 | Un appui, un exemple distinct et un essai par question ; vérification intégrale des exports |

Les 65 questions, leurs jeux de données, calculs à corriger et consignes sont conservés dans leur ordre relatif. Aucun corrigé n'a été ajouté aux réponses, aucun exercice n'est devenu optionnel. Les exemples utilisent d'autres données et ne portent aucun marqueur de résultat évalué. Les cellules historiques conservent leur identifiant lorsqu'il existait ; sinon un identifiant stable `tdN-s2-source-III` reprend leur position source. Les métadonnées préexistantes sont préservées, avec ajout du rôle TAL ; les sorties et compteurs d'exécution sont nettoyés.

Les TD3 et TD5 sont explicitement répartis chacun sur deux séances accompagnées de 2 h. TD6 propose une séance de 2 h. Cette charge visible évite de prétendre que 30 ou 25 exercices renforcés seront tous réalisés en deux heures ou d'externaliser silencieusement le travail obligatoire. Les durées restent des repères à ajuster.

TD3 : distinction indice/valeur, compteurs, condition d'arrêt, fonction et défaut, tri/key/lambda, ensembles et opérations complémentaires, exceptions ciblées, fenêtres, complexité moyenne, variance population, récursion, anagrammes, aplatissement, Euclide et Fibonacci. TD5 : multiplicités des anagrammes, Hamming sur longueurs égales, alphabet du décalage, regroupements et fusion additive, transposition, fenêtres, Jaccard/cas vide, TF et dénominateur, produit scalaire, préfixes avec accents et limites de la cooccurrence. TD6 : UTF-8, lignes et sauts de ligne, nettoyage sans supprimer les espaces demandés, portée d'isdigit, ponctuation élargie Q7, pipeline, fréquences, écriture et relecture CSV.

Les contradictions anciennes sont rendues explicites avant la question : TD3 Q6 insère à l'indice 1 ; TD5 Q9 applique la règle de toutes les initiales malgré l'ancien exemple TAL ; TD5 Q24 produit des fréquences marginales, pas encore une matrice de cooccurrences ; TD6 Q1 renseigne reponse_Q1, Q7 élargit le nettoyage sans changer le contrat de Q3. Les résultats de tri acceptent les ex æquo ; les ensembles n'ont pas d'ordre imposé.

## Exceptions de contrat déclarées

Métadonnées racine v2 pour les trois identifiants publics inchangés (`td3-S2`, `td5-S2`, `td6-S2`) ; rôle et identifiant pour chaque cellule ; identité de quatre champs (ajout complet dans TD5) ; tuteur synchronisé depuis le manifeste TAL-Prof ; restitution HTML canonique unique en dernière position. Les nouvelles cellules d'entraînement sont `practice`, les exemples `example` et les données préparées `provided` : elles ne constituent pas des réponses notées. Chaque essai et atelier porte aussi `metadata.tal_review.question` pour transmettre ses prédictions et explications au rapport enseignant, sans ajouter de points ; la synthèse générale est rattachée à la dernière question de chaque TD avec son titre explicite.

L'orchestrateur a autorisé la canonicalisation des seuls affichages TD3 pour que le collecteur associe une valeur typée au marqueur Qn. Aucun calcul ni donnée d'exercice n'est remplacé. L'affichage Q1 ne contient plus le suffixe monétaire ; l'objectif de calcul de coût subsiste. Tableau exhaustif des lignes remplacées :

| Question | Ligne source | Ligne v2 |
|---|---|---|
| Q1 | `print(f"Résultat Q1 : {cout_total} €")` | `print("Résultat Q1 :", cout_total)` |
| Q3 | `print(f"Résultat Q3 : {valeur_Q3}")` | `print("Résultat Q3 :", valeur_Q3)` |
| Q4 | `print(f"Résultat Q4 : {valeur_Q4}")` | `print("Résultat Q4 :", valeur_Q4)` |
| Q5 | `print(f"Résultat Q5 : {reponse_Q5}")` | `print("Résultat Q5 :", reponse_Q5)` |
| Q6 | `print(f"Résultat Q6 : {outils}")` | `print("Résultat Q6 :", outils)` |
| Q7 | `print(f"Résultat Q7 : {compteur}")` | `print("Résultat Q7 :", compteur)` |
| Q8 | `print(f"Résultat Q8 : {resultat_Q8}")` | `print("Résultat Q8 :", resultat_Q8)` |
| Q9 | `print(f"Résultat Q9 : {resultat_Q9}")` | `print("Résultat Q9 :", resultat_Q9)` |
| Q10 | `print(f"Résultat Q10 : {resultat_Q10}")` | `print("Résultat Q10 :", resultat_Q10)` |
| Q11 | `print(f"Résultat Q11 : {valeur_Q11}")` | `print("Résultat Q11 :", valeur_Q11)` |
| Q12 | `print(f"Résultat Q12 : {valeur_Q12}")` | `print("Résultat Q12 :", valeur_Q12)` |
| Q13 | `print(f"Résultat Q13 : {paires_triees}")` | `print("Résultat Q13 :", paires_triees)` |
| Q14 | `print(f"Résultat Q14 : {resultat_Q14}")` | `print("Résultat Q14 :", resultat_Q14)` |
| Q15 | `print(f"Résultat Q15 : {valeur_Q15}")` | `print("Résultat Q15 :", valeur_Q15)` |
| Q16 | `print(f"Résultat Q16 : {fact}")` | `print("Résultat Q16 :", fact)` |
| Q17 | `print(f"Résultat Q17 : {resultat_Q17}")` | `print("Résultat Q17 :", resultat_Q17)` |
| Q18 | `print(f"Résultat Q18 : {bigrams}")` | `print("Résultat Q18 :", bigrams)` |
| Q19 | `print(f"Résultat Q19 : {resultat_Q19}")` | `print("Résultat Q19 :", resultat_Q19)` |
| Q20 | `print(f"Résultat Q20 :", resultat_Q20)` | `print("Résultat Q20 :", resultat_Q20)` |
| Q21 | `print(f"Résultat Q21 :", reponse_Q21)` | `print("Résultat Q21 :", reponse_Q21)` |
| Q22 | `print(f"Résultat Q22 :", resultat_Q22)` | `print("Résultat Q22 :", resultat_Q22)` |
| Q23 | `print(f"Résultat Q23 :", reponse_Q23)` | `print("Résultat Q23 :", reponse_Q23)` |
| Q24 | `print(f"Résultat Q24 :", valeur_Q24)` | `print("Résultat Q24 :", valeur_Q24)` |
| Q25 | `print(f"Résultat Q25 :", valeur_Q25)` | `print("Résultat Q25 :", valeur_Q25)` |
| Q26 | `print(f"Résultat Q26 :" , resultat_Q26)` | `print("Résultat Q26 :", resultat_Q26)` |
| Q27 | `print(f"Résultat Q27 :", resultat_Q27)` | `print("Résultat Q27 :", resultat_Q27)` |
| Q28 | `print(f"Résultat Q28 :", tokens_filtres)` | `print("Résultat Q28 :", tokens_filtres)` |
| Q29 | `print(f"Résultat Q29 :", paires)` | `print("Résultat Q29 :", paires)` |
| Q30 | `print(f"Résultat Q30 :", valeur_Q30)` | `print("Résultat Q30 :", valeur_Q30)` |

TD3 Q2 était déjà canonique et reste inchangée. TD6 Q1 conserve son `repr(reponse_Q1)` historique pour représenter sans ambiguïté une chaîne contenant des sauts de ligne. TD6 Q9 conserve intégralement sa source puis ajoute Q9b, qui affiche toutes les lignes relues depuis le fichier et non les seules trois premières. TD6 Q10 conserve sa source puis ajoute la relecture et la trace Q10b de l'en-tête `Mot;Frequence`. Ces preuves complémentaires ne changent pas le barème ; les architectes les prennent en compte dans les critères. Aucun autre corps historique n'est changé ; les cellules d'identité et de tuteur sont les exceptions de maintenance prévues.

## Vérifications du producteur et relais

Vérification statique des identifiants uniques, rôles sur toutes les cellules, 30/25/10 réponses, absence de sorties enregistrées et syntaxe Python des nouveaux exemples/essais/préparations. Aucun notebook étudiant ni algorithme de réponse n'a été exécuté. Les contrôles de conservation, de contrats, de distribution et de correction sont réalisés indépendamment par l'intégration et les réviseurs.

Fichiers possédés : les trois TD déplacés, `Notebooks TD/S2/README.md`, le présent bilan. Aucun correcteur, test, corrigé historique ou manifeste pédagogique n'est modifié par le Designer. Risques à examiner : charge de deux séances, correspondance des scopes de tuteur et des ateliers, distinction résultat technique/qualité du raisonnement, prise en compte des traces CSV complètes. Verdict demandé : `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` après revue indépendante.
