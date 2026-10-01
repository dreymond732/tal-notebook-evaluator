# S3 — couverture des révisions et des trois premiers TD

Mission TAL-Pedagogy-Designer, branche `pedagogy/s3-progression-review`. Référence : `933b0df6565fbd7d64f02db941eda5e8358eb16e`. Conception réalisée après validation par l'orchestrateur de la matrice du Prof, `docs/pedagogy/s3_progression_review_coverage.md`.

## Conservation et besoins traités

Les six noms de fichier étaient déjà thématiques ; ils sont conservés. Les six racines d'identification et les contrats de correction restent en version 2. Les 32 questions, leurs cellules de réponse, les quatre champs d'identification, leurs marqueurs, leurs données et leurs barèmes sont inchangés.

Les 121 anciennes cellules restent dans le même ordre relatif avec les mêmes identifiants. Le texte de toutes les anciennes cellules pédagogiques est identique au texte source ; seule la cellule gérée du tuteur est synchronisée avec son manifeste. Les nouvelles métadonnées classent les cellules auparavant non renseignées suivant leur fonction : consigne, exemple, préparation fournie ou infrastructure. Aucun énoncé n'est remplacé par son corrigé.

| Support | Renforcement avant la question concernée | Cellules avant → après |
|---|---|---:|
| R0 Python pour le texte | Q1 : résultat retourné, appel et dictionnaire de tests sur des longueurs de notices ; Q3 : mise à jour `.get()` sur atlas/plan | 13 → 17 |
| R1 Parcourir un Doc spaCy | Q2 : triple forme/lemme/POS, ordre et répétitions sur un texte distinct | 15 → 18 |
| R2 Fréquences réutilisables | Q1 : `Counter` et paramètre réservé ; Q3 : `None`, exclusions personnelles et filtre spaCy ; Q4 : classements complets et ex æquo | 15 → 20 |
| TD0 Diagnostic du texte | Q1 : tableau variable/type/unité et trace JSON distincte ; Q5 : total des effectifs et diversité | 25 → 29 |
| TD1 Fondations spaCy | Q1 : tranche avec fin exclue, position en caractères et observations concernant le même token | 25 → 28 |
| TD2 Analyse de corpus | Q2 : paramètre facultatif et portée de l'argument ; Q3 : invariants du filtrage ; Q4 : ordre décroissant et ex æquo | 28 → 33 |

Chaque support reçoit un espace d'essai non noté, associé par `tal_review.question` à l'activité déjà demandée, et la cellule finale canonique de restitution. Les identifiants `practice-Qn` distinguent ces espaces des réponses notées. Le serveur ne peut pas utiliser leur sortie comme réponse à une question. Les essais et commentaires de ces nouvelles cellules restent accessibles au rapport enseignant.

Les repères sont placés devant la question qui mobilise la notion. Cette séparation préserve les périmètres du tuteur : `.get()` n'est pas introduit dans l'appui de R0 Q1 et le classement n'est pas anticipé dans l'appui de R2 Q1. Les exemples utilisent des données distinctes de celles des exercices et ne produisent pas leurs résultats attendus.

## Charge et autonomie

R0, R1 et R2 restent des reprises de 25, 25 et 30 minutes. TD0, TD1 et TD2 conservent intégralement leurs parcours de 120 minutes. Les repères servent à conduire les prédictions, essais et contrôles déjà demandés ; ils ne créent aucune question notée ni liste obligatoire supplémentaire. Ce minutage est un choix de conception à éprouver en séance, pas une durée mesurée.

Les choix de l'étudiant, les essais personnels, les comparaisons, les interprétations et les transferts à Faguet restent tous présents. En particulier, TD2 Q6 demande toujours un nuage et des barres sur des effectifs non vides ; si toutes les formes ont été exclues, le retour au choix de filtre et la réexécution cohérente de Q3 sont conservés. Aucun travail existant n'est devenu facultatif.

## Restitution, vérifications et relais

Les six dernières cellules sont exactement celles produites par `app/prepare_student_notebooks.py:submission_cell()`, avec `__TAL_PUBLIC_URL__`, aucune exécution et aucune sortie. L'injection effective relève du déploiement ; aucune adresse de dépôt n'est ajoutée aux sources. La première cellule reste le tuteur, classée comme infrastructure, et ses instructions sont synchronisées dans les métadonnées.

Vérifications du producteur : comparaison des 121 cellules anciennes au commit source, sources pédagogiques identiques et ordre/identifiants conservés ; résolution des six contrats v2 ; métadonnées TAL présentes sur toutes les cellules ; contrôle des sources sans adresse de dépôt ; unicité et égalité exacte de la dernière cellule canonique. Aucun notebook étudiant n'a été exécuté.

Fichiers de production : les six notebooks ci-dessus et le présent bilan. Contrat affecté : classification des cellules et représentation des essais à relire ; aucune modification des réponses ou du barème. Risques : minutage réel et interprétations linguistiques nécessitent l'observation de l'enseignant ; les métadonnées de tutorat ne constituent pas une garantie d'obéissance d'un service externe. Verdict demandé : revue pédagogique indépendante de conservation et de cohérence avec le manifeste ; revue technique de non-évaluation des cellules d'essai et de restitution.
