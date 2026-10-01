# S3 v2 — bilan de conception des quinze supports

Mission TAL-Pedagogy-Designer, branche `code/s3-evaluation-complete-v2`, 1er octobre 2026. Référence : commit `02f435dc770834b21e242592804d231e0836a4b7`. La matrice préalable `docs/pedagogy/s3_complete_v2_coverage.md` a été validée par l’orchestrateur avant la première modification. Le contrat appliqué est `docs/pedagogy/s3_complete_v2_spec.md`, dans le périmètre des quatre lots autorisés par l’enseignant.

## Conservation et modifications déclarées

Les 15 notebooks, leurs 104 réponses, leurs 420 cellules, les activités de 2 h et leurs barèmes sont conservés. Aucun exemple, calcul demandé, prédiction, fonction à construire, essai, figure, contrôle manuel, interprétation, transfert, export ou bilan n’est supprimé, déplacé ou rendu optionnel. Aucune solution ni valeur de référence quantitative n’a été ajoutée.

Les seules modifications de source sont des ajouts en fin de cellule : les 15 introductions, les 15 identifications et les 7 consignes détaillées ci-dessous. Les 383 autres sources de cellules sont identiques à la référence. Chaque source modifiée garde intégralement son ancien texte comme préfixe. Le nombre, l’ordre, les identifiants existants, les types, les compteurs d’exécution et les sorties des cellules sont inchangés. Les données et préparations fournies sont inchangées ; aucun code de notebook n’a été exécuté pour cette conception.

Les métadonnées racines `tal.version` passent de 1 à 2. Les autres métadonnées racines, dont les instructions du tuteur, restent identiques. La première cellule Markdown du tuteur est identique dans chaque notebook : guidance en TD, aucune assistance en contrôle. Les 49 cellules rédigées existantes des contrôles reçoivent seulement `metadata.tal_review.question` afin que leurs analyses restent associées à leur question après déplacement ; ce ne sont pas des cellules de preuve quantitative supplémentaires.

Chaque introduction annonce la version 2, le refus « mauvaise version du notebook », la nécessité d’utiliser la copie distribuée à jour et la portée technique provisoire du score. Chaque identité conserve les trois affectations initiales et ajoute `numero_etudiant = ""`, avec un commentaire sur les zéros initiaux. Le format autorisé est indiqué dans l’introduction ; aucune identité réelle n’est fournie.

| Support et correcteur associé | Réponses | Précisions pédagogiques au-delà de l’introduction et de l’identité |
|---|---:|---|
| `TD0_S3_diagnostic_texte.ipynb` → `app_correction_TD0_S3.py` | 7 | Aucune ; la synthèse non vide était déjà demandée en Q7. |
| `TD1_S3_fondations_spacy.ipynb` → `app_correction_TD1_S3.py` | 6 | Introduction : conformité au pipeline, distincte de la justesse linguistique. Q1 : ordre, type de tag et bornes. Q4 : lecture grammaticale et annotation du modèle distinguées, repères distincts dans la première phrase, relation relue humainement. Q5 : espaces inclus dans tous les tokens et exclus avec la ponctuation du compte filtré. Q6 : cinq premiers tokens, ponctuation comprise, limites du contrôle de l’extrait libre. |
| `TD2_S3_analyse_corpus.ipynb` → `app_correction_TD2_S3.py` | 7 | Introduction : références sur microcorpus et pipeline, critique conservée. Q4 : ordre libre des ex æquo et effectifs entiers. Q5 : lemmes complets ordonnés hors mots vides, choix libre de cinq occurrences réellement présentes et distinction entre annotation observée et jugement. |
| `TD3_S3_concordances_citations.ipynb` → `app_correction_TD3_S3.py` | 7 | Q7 : trois occurrences distinctes du pivot, fenêtres de contexte libres, bornes exactes et préservation des sauts de ligne. |
| `TD4_S3_cooccurrences.ipynb` → `app_correction_TD4_S3.py` | 7 | Aucune. |
| `TD5_S3_associations.ipynb` → `app_correction_TD5_S3.py` | 7 | Aucune. |
| `TD6_S3_visualisations.ipynb` → `app_correction_TD6_S3.py` | 7 | Aucune. |
| `TD7_S3_audit_llm.ipynb` → `app_correction_TD7_S3.py` | 7 | Aucune. |
| `Controle_TD1_S3.ipynb` → `app_correction_Controle_TD1_S3.py` | 7 | Métadonnées de relecture des 7 cellules « Votre analyse ». |
| `Controle_TD2_S3.ipynb` → `app_correction_Controle_TD2_S3.py` | 7 | Métadonnées de relecture des 7 cellules « Votre analyse ». |
| `Controle_TD3_S3.ipynb` → `app_correction_Controle_TD3_S3.py` | 7 | Métadonnées de relecture des 7 cellules « Votre analyse ». |
| `Controle_TD4_S3.ipynb` → `app_correction_Controle_TD4_S3.py` | 7 | Métadonnées de relecture des 7 cellules « Réponse rédigée / preuves ». |
| `Controle_TD5_S3.ipynb` → `app_correction_Controle_TD5_S3.py` | 7 | Métadonnées de relecture des 7 cellules « Réponse rédigée / preuves ». |
| `Controle_TD6_S3.ipynb` → `app_correction_Controle_TD6_S3.py` | 7 | Métadonnées de relecture des 7 cellules « Réponse rédigée / preuves ». |
| `Controle_TD7_S3.ipynb` → `app_correction_Controle_TD7_S3.py` | 7 | Métadonnées de relecture des 7 cellules « Réponse rédigée / preuves ». |

Les TD sont dans `Notebooks TD/S3/` et les contrôles dans `Notebooks contrôles finaux/S3/`. Les modules de correction indiqués sont dans `app/` et relèvent du travail distinct de l’architecte. Les ressources R0/R1/R2 déjà v2 n’ont pas été modifiées par le designer.

## Preuve de conservation et relais

Une comparaison JSON avec `origin/main` au commit de référence a vérifié, sur les quinze fichiers, l’égalité de toutes les cellules après retrait des seuls suffixes autorisés et des 49 annotations de relecture, ainsi que l’égalité des métadonnées racines après mise à jour du seul entier de version. Résultat : 15 notebooks, 104 cellules de réponse, 49 cellules de relecture, 37 sources enrichies par suffixe, 383 sources inchangées. L’Integration-Master reprend cette preuve dans une vérification reproductible indépendante de la conception.

Vérifications locales de préparation : `python app/tutor_metadata.py --check` réussit pour les 34 profils ; `python app/prepare_student_notebooks.py check` réussit pour les 33 sources distribuables. Ces contrôles ne remplacent ni la revue indépendante ni la vérification du rendu `dist/` par l’intégration.

Hypothèses : les corpus et installations figés restent accessibles ; les contraintes v2 de l’architecte correspondent aux précisions des sujets. Risques résiduels : la conformité à un modèle n’est pas une vérité linguistique, les traces enregistrées ne prouvent ni l’exécution effective ni l’autonomie, et le contrôle statique d’un extrait libre ne certifie pas sa tokenisation. Ces limites sont explicites dans les sujets et dans la spécification.

Critères d’acceptation demandés : conservation substantielle des 104 activités, correspondance avec les validateurs v2, tuteurs inchangés, contrats d’identité complets, anciens notebooks refusés, sources sans dépôt privé et distribution générée avec cellule HTML finale. Le designer ne valide pas son propre travail : verdict demandé au Pedagogy-Reviewer, puis au Code-Auditor pour la cohérence de contrat, à la gouvernance et à l’intégration. Fusion et déploiement restent à la décision du mainteneur. Les quinze supports doivent être régénérés et redistribués après fusion ; les anciennes copies ne doivent pas être renommées v2.
