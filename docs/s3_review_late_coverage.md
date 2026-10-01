# S3 — bilan de couverture des TD3 à TD7

Mission TAL-Pedagogy-Designer sur `pedagogy/s3-progression-review`, référence `933b0df6565fbd7d64f02db941eda5e8358eb16e`. La matrice préalable `docs/pedagogy/s3_progression_review_coverage.md` a été validée par l'orchestrateur avant conception. Le principe enseignant est appliqué : aucun retrait ou réduction ; les appuis préparent les activités existantes, sur des données distinctes.

| Support | Conservation | Renforcement intégré aux temps existants |
|---|---|---|
| TD3 — concordances et citations | 27 cellules originales, Q1–Q7, données, traces, tests manuels, transferts et export | Q1 provenance ; Q2 reprise de `find` et exception typée ; Q3 expression contiguë ; Q5 indices originaux et normalisés |
| TD4 — cooccurrences | 28 cellules originales, Q1–Q7, marges, union/somme, frontières, lemmes, export | Q2 lecture d'une assertion ; Q3 tableau de présences ; Q4 token/caractère et distance non filtrée ; Q7 réemploi des preuves |
| TD5 — associations | 28 cellules originales, Q1–Q7, dénominateurs, taux, inversion, absence, sensibilité et export | Q1 tableau 2 × 2 avant les quotients ; Q5 `None` et arrondi ; Q6 couverture d'un pivot versus paires |
| TD6 — visualisations | 29 cellules originales, Q1–Q7, dispersion, segments, chaleur, sensibilité, passages, matrice et export | Q2 segments vides ; Q3 axes et table source ; Q5 caractères originaux ; Q7 agrégation des effectifs et sauvegarde de figure |
| TD7 — audit LLM | 30 cellules originales, Q1–Q7, six affirmations, trois citations, moteur, lot manuel, export et synthèse | Q1 reprise des fonctions et champs absents/`None`/renseignés ; Q2 tranche contiguë ; Q4 portée des trois verdicts ; Q6 table de tests ; Q7 cohérence des livrables |

Les vingt repères nouveaux sont des cellules Markdown de rôle `practice`, avec identifiant propre `s3-tdN-review-qM` et rattachement `tal_review.question = QM`. Ils ne contiennent ni nouveaux marqueurs de correction ni résultats des cas évalués. Ils préparent les essais déjà prévus ; aucun exercice source ne devient optionnel. Le minutage de deux heures et le niveau d'autonomie source restent inchangés. La faisabilité temporelle doit être confrontée à une séance réelle, notamment pour l'assemblage final du TD7.

## Métadonnées, tutorat et restitution

- Tous les anciens identifiants et l'ordre relatif des anciennes cellules sont conservés. Les sources originales restent intégralement inchangées, à l'exception de la première cellule de tuteur régénérée depuis le manifeste validé.
- Le contrat notebook reste en version 2 ; les identités, les 35 réponses et leurs métadonnées sont inchangées. Toutes les cellules ont désormais un rôle explicite : consigne, exemple, préparation fournie, pratique, identité, réponse, tuteur ou restitution.
- Les 28 anciennes cellules d'interprétation des TD4–TD7 reçoivent `tal_review.question` ; la reprise de fonctions `s3-td7-06` est rattachée à Q1. Ce rattachement maintient leur visibilité au rapport enseignant malgré la classification complète des cellules. Il ne leur attribue aucun point automatique.
- Le tuteur en première cellule et les métadonnées sont synchronisés à partir du manifeste du Prof, sans changer les règles de guidance ni ouvrir une bibliothèque supplémentaire.
- Chaque notebook se termine par la cellule canonique de `app.prepare_student_notebooks.submission_cell()` : HTML de restitution, marqueur `__TAL_PUBLIC_URL__`, sorties vides. L'injection relève du déploiement ; aucune adresse privée n'est introduite.

## Vérification du producteur et relais

Vérification directe contre le commit source : les 142 anciennes cellules conservent leurs identifiants et leur ordre, et les 137 sources hors tuteur restent identiques (les cinq cellules de tuteur sont régénérées) ; 20 repères et 5 cellules de restitution sont ajoutés, soit 167 cellules au total. Le contrôle de métadonnées `validate_cell_metadata` accepte chacun des cinq notebooks et confirme l'unicité des identifications de rôle/question. Les cellules de restitution sont identiques à la fabrique canonique. Aucun code étudiant n'a été exécuté.

Les effectifs finaux sont TD3 32, TD4 33, TD5 32, TD6 34 et TD7 36 cellules. Ces comptages attestent une conservation structurelle ; le jugement de couverture revient à la revue pédagogique indépendante, pas au producteur. Les contrôles d'intégration doivent confirmer la préservation des réponses, la visibilité des interprétations, la synchronisation du tuteur et la distribution sans doublon.

Fichiers concernés : les cinq notebooks TD3–TD7 et ce bilan. Les correcteurs associés restent `td3-s3` à `td7-s3` ; aucun changement de marqueur, résultat attendu, type, barème ou bibliothèque n'est introduit. Les interprétations, modèles linguistiques et résultats sur Faguet restent soumis à relecture humaine.

Verdict demandé : `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`, après revue indépendante.
