# Révision des six correcteurs S2 — contrat v2

Branche : `pedagogy/s2-complete-review`. Mission TAL-Code-Architect : fiabiliser les 122 questions des six évaluateurs actifs, sans exécuter les programmes remis, sans changer leurs poids et sans activer le contrôle final historique.

## Fichiers et portée

- `app/s2_reference.py` : références quantitatives, égalité typée, variantes autorisées et constructions syntaxiques par question.
- `app/app_correction_TD2_S2.py`, `app_correction_TD3_S2.py`, `app_correction_TD4_S2.py`, `app_correction_TD5_S2.py`, `app_correction_TD6_S2.py`, `app_correction_devoirMaisonS2.py` : adaptateurs vers le moteur v2 et identifiants exacts du catalogue.
- `tests/test_s2_v2_results.py` : 122 réponses enregistrées indépendantes, sources analysées mais jamais exécutées, appels des six adaptateurs et des six sujets révisés.
- Retouche ciblée de `app/s1_revision.py`, reprise à la demande de l’orchestrateur : un `try` rencontré sur le chemin nominal appartient aux dépendances de sa réponse. Les gestionnaires d’exception ne constituent pas une preuve de lecture ou d’écriture de fichier.

Les maxima restent respectivement **20, 30, 40, 25, 20 et 40**. Les 122 marqueurs principaux restent inchangés. TD6 ajoute Q9b pour le CSV entier et Q10b pour l’en-tête du CSV trié, sans points supplémentaires.

## Rectifications et tolérances

- TD3 Q2 accepte les indices négatifs équivalents ; Q1 accepte 300 entier ou réel, jamais un booléen.
- TD3 Q3 vérifie la structure des deux bornes de l’intervalle `[10, 16[` ; le `or` erroné d’origine est refusé même si le seul exemple affiche `True`. Les variantes équivalentes usuelles sont admises.
- TD3 vérifie les constructions explicitement demandées : insertion et retrait, `enumerate`, paramètre par défaut, gestion d’exception, association avec `zip`, recherche sans `in`, récursivité et compréhension de dictionnaire.
- TD5 Q9 suit la consigne « chaque mot » : TADL, y compris l’initiale de « des ». Les listes d’étudiants par matière admettent tout ordre sans doublon.
- TD6 Q1 compare le contenu multiligne entier par `repr`, Q2 respecte l’absence de saut de ligne final du fichier généré et Q3 conserve les espaces finaux.
- TD6 Q9 vérifie l’en-tête et les 15 paires, sans imposer d’ordre. Q10 vérifie toutes les paires, le tri décroissant et l’en-tête ; les ex æquo sont libres. L’ouverture en écriture doit viser le fichier de cette question : une écriture du CSV précédent ne suffit pas.
- Le devoir maison Q29 accepte liste, tuple ou ensemble de deux entiers distincts, le type n’étant pas prescrit.
- Les ensembles et dictionnaires sont comparés par contenu. Les listes, tuples, booléens et nombres restent distingués, sauf tolérance expressément indiquée.

## Vérifications du producteur

La suite ciblée de **18 tests** passe : 122 cas positifs, altération de chaque sortie, six maxima exacts via les adaptateurs réels, contrats v1 refusés, réponses injectées dans les six sujets révisés, métadonnées d’une autre question, cellules d’exercice libre, marqueurs dupliqués, erreurs enregistrées, types confondus, commentaire servant de leurre, limites des intervalles, équivalences et CSV incomplets.

Commande : `python -m unittest discover -s tests -p test_s2_v2_results.py`.

Les tests ne lancent aucune source étudiante et n’ouvrent aucun chemin cité dans ces sources. Les chemins présents dans les exemples de réponse sont des chaînes inertes.

## Limites et acceptation

Le résultat est un **score technique provisoire**, non une preuve de fraîcheur des sorties, d’auteur ou de correction sur toutes les entrées possibles. La reconnaissance syntaxique couvre les constructions enseignées et les équivalences documentées ; une réalisation inhabituelle peut demander une relecture. Le contrôle final à 18 questions reste inactif, car son ancien module à 11 questions ne correspond pas au sujet.

Acceptation demandée : revue indépendante des références et des méthodes imposées, conservation des poids, refus des contrats incomplets, absence d’exécution, cohérence des sujets distribués et vérification globale des S1/S3. Le producteur ne prononce pas de verdict de conformité.
