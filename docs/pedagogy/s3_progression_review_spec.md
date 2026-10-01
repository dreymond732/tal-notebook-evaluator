# S3 — spécification de la revue de progression

Mission TAL-Prof ; branche `pedagogy/s3-progression-review`, source `933b0df6565fbd7d64f02db941eda5e8358eb16e`. La [matrice préalable](s3_progression_review_coverage.md) a été validée par l'orchestrateur avant les modifications de conception. Cette note précise le contrat pédagogique et le relais vers les revues indépendantes.

## Périmètre et conservation

Les onze supports actifs sont concernés : huit TD de deux heures et trois révisions de 25, 25 et 30 minutes. Les 67 questions, corpus, marqueurs, barèmes et contrats évaluateurs v2 restent inchangés. Les renforcements sont des repères courts, placés avant la notion mobilisée : ils expliquent ou préparent les essais déjà demandés, sans fournir les réponses évaluées. Les données d'exemple restent distinctes de celles des exercices. Le code de préparation et les démonstrations sont fournis ; les fonctions, calculs, tests, figures, transferts et conclusions restent à produire par l'étudiant.

Les révisions sont des reprises ciblées, pas des versions réduites destinées à remplacer les TD complets. Les TD0–TD2 conservent leur densité ; les TD3–TD7 renforcent les liens entre les outils et le projet final. Aucun contenu ancien n'est déplacé hors de séance ni rendu facultatif. PMI et difflib gardent leur statut de prolongement optionnel existant.

## Repères et tuteur

Les instructions du tuteur viennent de `tutor_sessions.json`, puis sont générées dans les métadonnées et la première cellule. Aucun profil de contrôle ni profil S1/S2 n'est modifié dans cette revue. Les notions ajoutées au manifeste précisent principalement des opérations déjà requises par les consignes :

| Support | Repères du tuteur à la question concernée |
|---|---|
| R0 | Valeur retournée versus affichée (Q1), compteur et clé absente (Q3) |
| R1 | Triples d'annotation, ordre et répétitions (Q2) |
| R2 | Counter et None (Q1), exclusions par lemme (Q3), ex æquo (Q4) |
| TD0 | Type/unité et dictionnaire de trace (Q1), invariants (Q5) |
| TD1 | Tranche à fin exclue, indice caractère/token et observation structurée (Q1, rappel Q6) |
| TD2 | None/exclusions (Q2), filtre retirant tous les noms (Q3), ex æquo (Q4), reprise Q3 avant figures si nécessaire (Q6) |
| TD3 | Provenance (Q1), départ de recherche, non-chevauchement et exception (Q2), expression contiguë (Q3), positions originales/normalisées (Q5) |
| TD4 | Phrases/formes/filtre alphabétique (Q1), assertion (Q2), tableau des présences (Q3), indices token/caractère (Q4), espaces et expressions (Q6), preuves/export (Q7) |
| TD5 | Dénominateur non nul et tableau 2×2 (Q1), contrôle des marges (Q4), None et arrondi (Q5), couverture unique des pivots (Q6) |
| TD6 | Petits segments/vides et tailles (Q2), taux non défini (Q3), indices token/caractère (Q5), agréger avant division (Q7) |
| TD7 | Champ absent/None (Q1), expression contiguë et indices d'origine (Q2), comparabilité et bornes (Q4), tableau des tests (Q6) |

Les limites par exercice restent fermées. Un repère associé à Q2 ne rend pas ses notions disponibles à Q1. Un exercice de guidage ne donne pas au tuteur le droit de compléter une cellule. Au S3, le fragment minimal après échange reste un exemple distinct ; aucune solution complète, recette de résolution ou valeur attendue n'est fournie. En contrôle, aucune assistance.

Le manifeste a été validé structurellement et rendu en mémoire pour les 34 profils : aucun contexte ne dépasse le budget interne de 4 400 caractères. Pour les onze profils modifiés, les longueurs au moment de la remise Prof sont comprises entre 3 173 et 4 387 caractères. Ce contrôle établit la cohérence des instructions générées ; il ne prouve pas leur respect par Colab. La synchronisation des copies effectives et le contrôle complet du dépôt relèvent de l'intégration.

## Cas pédagogiques à préserver dans les correcteurs

### TD2 Q3 et Q6 : filtre vide puis reprise

Q3 autorise l'observation d'un filtrage qui retire tous les noms : le résultat peut être un dictionnaire vide et cette observation ne doit pas être faussement rejetée. Q6 exige ensuite les deux figures sur les mêmes fréquences. La consigne source dit explicitement de réadapter le filtre si tout a été retiré, de l'expliquer et de réexécuter Q3 puis Q6. On ne doit donc pas accorder à une trace Q6 vide le statut de réalisation de cette activité. Le retour doit indiquer la reprise nécessaire, sans exécuter le code ni inventer une note de qualité de figure.

### R2 Q2 : observation indépendante

La constitution d'une liste d'annotations par parcours d'un nouveau `nlp(texte)` peut réussir même si la fonction de Q1 est incomplète. Le correcteur doit vérifier la production propre de Q2 ; l'échec Q1 n'est pas une raison de rejeter une observation autonome conforme. La conformité aux prédictions du modèle reste distincte d'un accord grammatical avec ces prédictions.

### R2 Q3 : conditions équivalentes

Le filtre demandé conserve les NOUN non stopwords dont le lemme n'appartient pas aux exclusions. Des expressions conditionnelles équivalentes ne doivent pas provoquer un faux négatif. Tolérer un code valide qui exprime la même condition ne nécessite pas d'enseigner toutes ses variantes : le tuteur demeure limité aux notions du sujet. Aucun choix de style n'est un critère pédagogique supplémentaire.

### Rédactions et figures

Une rédaction ou une figure manquante doit rester visible comme manque à relire. La présence d'un texte ou d'une image n'établit pas sa qualité scientifique. Les interprétations, annotations manuelles, passages, nouveaux cas de test, exports et fonctions réutilisables restent à examiner ; les points techniques ne sont pas une validation automatique du projet final.

## Métadonnées et restitution

La version racine reste 2 ; les identifiants d'évaluateur et les questions restent stables. Une identité comprend toujours nom, prénom, classe et numéro étudiant littéraux. Toutes les cellules reçoivent un identifiant unique et un rôle adapté. Les cellules d'interprétation personnelle doivent être rattachées à leur question pour la relecture humaine, sans devenir des cellules de réponse technique concurrentes. Les repères d'entraînement ne peuvent fournir de preuve de calcul au correcteur.

Chaque source comporte une cellule finale de restitution canonique au marqueur `__TAL_PUBLIC_URL__`, sans adresse de serveur. Le déploiement produit la copie distribuée configurée et vérifie son état. Cette cellule et ses imports sont de l'infrastructure ; ils ne constituent ni un acquis supplémentaire ni une réponse aux exercices.

## Limites et preuves attendues

Le maintien du minutage est un choix de conception : les appuis sont brefs et intégrés aux activités existantes, mais aucune observation en classe ne démontre encore la durée réelle. TD7 suppose les fonctions et notes des séances précédentes disponibles ; reconstruire tout le parcours pendant ses deux heures n'est pas l'objectif. L'installation et l'annotation nécessitent la préparation annoncée ; une connexion lente peut déborder le temps prévu.

Les correcteurs inspectent des traces stockées et, selon les questions, le code statiquement ; ils ne certifient ni l'exécution passée, ni l'authenticité des sorties, ni la généralité d'une fonction. Les cas Faguet et les tests personnels sont conservés précisément pour permettre une discussion des hypothèses et limites. Le critère de réussite final est un audit traçable, nuancé et réutilisable, pas le nombre d'erreurs attribuées au LLM.

À contrôler avant publication : conservation contre la source, cohérence des scopes et des cellules, tutorat double emplacement, rejet des anciennes versions, essais positifs et négatifs des correcteurs, collecte qualitative, génération et vérification des onze copies, absence d'adresse privée, puis revues code et pédagogie indépendantes, gouvernance et intégration. Le Prof documente cette spécification ; il ne valide pas seul sa propre production.
