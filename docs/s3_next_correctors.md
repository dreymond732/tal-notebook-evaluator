# Révision des correcteurs S3 après TD1

Base examinée : `cdc52d08cc02c8880003d962d0631658f04392c1` (PR 25 fusionnée).

## Inventaire et portée

| Sujet | État avant cette révision | Contrôles conservés ou créés | Hors score automatique |
|---|---|---|---|
| TD1B | Dépôt sans correction, version 2 | Nouveau correcteur version 3 : 4 vérifications, une par question | Interprétations, qualité linguistique des essais personnels et généralité du code |
| TD2 | 7 vérifications version 2 actives | Q1 annotations et dimensions ; Q2 fréquences ; Q3 exclusions ; Q4 POS ; Q5 annotations inspectées ; Q6 données des figures ; Q7 fonctions spécialisées/générales | Pertinence des exclusions, qualité du commentaire, rendu des deux figures, transfert Faguet |
| TD3 | 7 vérifications version 2 actives | Q1 provenance ; Q2 concordances ; Q3 modes de recherche ; Q4 citations ; Q5 passage de C1 ; Q6 essais contrastés ; Q7 occurrences distinctes | Pertinence de la convention, interprétation de l’altération, exactitude linguistique des lemmes Q3 (provenance contrôlée seulement) |
| TD4 | 7 microcas version 2 actifs | Présences, cooccurrences, union/somme, distances, frontières, formes/lemmes, invariants | Transferts libres à Faguet et interprétations |
| TD5 | 7 microcas version 2 actifs | Dénominateurs, base, normalisation, asymétrie, absence, couverture, synthèse | Transferts libres, choix des protocoles et argumentation |
| TD6 | 7 microcas version 2 actifs | Positions, segments, matrice de taux, sensibilité, contexte, données des barres, agrégation | Rendu et lisibilité des figures, interprétation et transfert |
| TD7 | 7 microcas version 2 actifs | Champs manquants, moteur, citations, intervalles, agrégation, transfert contrôlé, statut du protocole | Application complète aux six lignes Faguet, qualité du rapport et visualisations |

Lecture des 42 consignes et vérifications TD2–TD7 : aucun nouveau barème ni résultat numérique attendu ne doit être inventé. Les contrôles existants sont conservés. En particulier le contrôle des microcas ne devient pas une certification du livrable complet. Les messages des TD indiquent l’autoévaluation et l’absence de relecture individuelle systématique. Les contrôles notés et leur relecture requise ne changent pas.

## Changement de contrat — TD1B version 3

Identifiant et correcteur : `td1b-s3`. Quatre réponses identifiées `Q1` à `Q4` et une identification à quatre champs sont obligatoires. Un notebook version 2 est refusé par `/submit` et `/eval/td1b-s3`, ainsi que par le module, avec **mauvaise version du notebook**, sans enregistrement ni correction. Le catalogue ne contient plus de dépôt manuel actif. Les anciens dépôts `td1b-s3-v2-human-review` restent intacts ; les nouveaux sont enregistrés dans `td1b-s3-v3`.

Chaque réponse émet un `print` explicite au niveau supérieur et une seule sortie stdout JSON `S3_TD1B_Qn:` dans sa propre cellule identifiée. Les affichages Markdown, commentaires, erreurs enregistrées, traces dupliquées, mauvais préfixes, JSON non fini et preuves dans une autre cellule ne valent pas preuve. Le code de sérialisation fourni dans le TD assemble des variables ; il ne calcule aucune solution spaCy à la place de l’étudiant. Aucun code soumis n’est exécuté sur le serveur.

| Question | Champs de la trace | Vérification |
|---|---|---|
| Q1 | `texte`, `entites` | Texte fixé, mentions et labels complets dans leur ordre, référence md |
| Q2 | `texte`, `entites`, `selection`, `essai` (`texte`, `entites`, `selection`) | Référence du texte fixé ; filtre PER/ORG exact sur les deux listes ; provenance/ordre sur le texte personnel distinct |
| Q3 | `vecteurs`, `scores`, `variation` (`original`, `modifie`, `score`) | Trois vecteurs, trois scores fixés, tolérance absolue 0,00001 ; variation distincte et score fini entre −1 et 1 |
| Q4 | `texte`, `avant`, `apres`, `pipeline`, `regles`, `essais` | Texte Toulon, règle ORG, ordre entity_ruler avant ner, autres ORG/LOC/DATE ; au moins cinq textes distincts ; pour chacune des quatre règles requises, au moins un essai dont la sortie contient sa mention exacte et son label ; provenance/ordre des mentions |

La similarité du texte personnel n’est pas recalculée. Les entités du texte personnel ne sont pas comparées à une référence statistique. Un filtre vide cohérent peut être correct lorsque le modèle n’a retenu aucune mention ; il ne certifie pas la bonne rédaction du texte. Pour Q4, les sorties sans règles n’admettent que les quatre labels du modèle français ; DATE est attendu dans un essai après règles, pas dans les prédictions statistiques. Les règles supplémentaires ne sont pas pénalisées si elles ne sont pas attestées ; le contrôle demande seulement Toulon/ORG, une autre ORG, une LOC et une DATE attestées. Les essais de variantes et d’ambiguïté peuvent produire des absences : le contrôle n’impose pas leur interprétation. Aucun score ne prouve l’authenticité d’une trace enregistrée ni l’exécution effective du programme.

## Référence reproductible

Référence produite localement avec spaCy **3.8.7**, modèle **fr_core_news_md 3.8.0**. Aucun code d’étudiant n’a été exécuté. Les entrées sont les textes fixes de l’énoncé.

- Q1 : Apple/ORG, Allemagne/LOC.
- Q2 : Emmanuel Macron/PER, Elon Musk/PER, Paris/LOC, Google/ORG, Tesla/PER. **Tesla/PER est la prédiction réellement observée**, pas une vérité linguistique à imposer au commentaire.
- Q3 : chien/chat = 0,6840823292732239 ; chien/voiture = 0,3173190653324127 ; phrases = 0,9808356761932373. Une tolérance de 0,00001 couvre l’affichage arrondi à cinq décimales.
- Q4 avant et après la première règle : Université de Toulon/ORG. Cette absence de différence ne prouve pas à elle seule l’application d’une règle ; les essais incluant DATE apportent une vérification supplémentaire.

## Conservation et validation

`tests/fixtures/s3_next_editorial_source_baseline.json` capture le texte exact des sept notebooks au commit parent, sans reconstruire une référence après réécriture. Les TD2–TD7 conservent identifiants, métadonnées, ordre des anciennes cellules et arbres syntaxiques de tout code préexistant. Les preuves des révisions antérieures restent archivées et vérifiées ; aucune exception générale n’est ajoutée aux autres supports.

Le catalogue comporte désormais 34 correcteurs automatiques et 34 distributions actives. Les tests TD1B couvrent résultats exacts/erronés, refus v2, absence de preuve, isolation Q1/TD1B, filtrage, scores non finis/booléens, règles sans application, métadonnées hostiles, non-exécution, échappement HTML, routes et persistance versionnée. Le déploiement doit précéder la distribution du nouveau TD1B.

### Échec de sauvegarde

Le rapport intermédiaire est rendu sans consommer les messages Flask. La réponse publique du TD est rendue après réussite de la sauvegarde ; si le CSV, le notebook ou le rapport ne peuvent être écrits, la première réponse affiche immédiatement l’erreur, sans score ni confirmation de dépôt. Un test utilise une session neuve pour chaque étape et les deux routes. La persistance historique reste non transactionnelle : un échec tardif peut laisser des fichiers ou une ligne CSV partiels, sans confirmation de succès.

## Vérification d’intégration du lot

Le 3 octobre 2026, la suite complète a exécuté **293 tests avec succès**. Les 35 profils du tuteur sont synchronisés ; les 34 sources distribuables passent la génération et la vérification avec une adresse neutre. Les sept notebooks passent la validation nbformat et l’analyse syntaxique de leurs cellules de code.

Les **39 exemples fournis** ont été exécutés localement, sans exécuter les cellules de réponse : TD1B 5, TD2 5, TD3 7, TD4 5, TD5 5, TD6 7, TD7 5. L’environnement de vérification utilisait spaCy 3.8.7, modèles français sm/md 3.8.0, Matplotlib 3.11.2 et WordCloud 1.9.6 ; le rendu Matplotlib utilisait le backend non interactif Agg. Les fichiers de démonstration ont été produits dans un répertoire temporaire, sans sortie enregistrée dans les sujets distribués. Les versions constatées des bibliothèques graphiques ne sont pas de nouvelles contraintes de version dans les notebooks.

L’audit technique indépendant a réussi 136 tests ciblés et éprouvé 228 mutations de types/structures des traces TD1B. Il a recalculé les références fixes du correcteur avec le modèle md installé. Ces preuves ne remplacent ni une exécution complète dans Colab par un étudiant, ni la mesure de la durée en classe. Les interprétations linguistiques restent hors score automatique.
