# Retrait des consignes de dépôt des TD S3

## Cadrage préalable — TAL-Prof

Date : 25 septembre 2026. Branche : `pedagogy/td-s3-sans-consigne-depot`.

L'enseignant demande de poursuivre sur les TD S3 le retrait des consignes de dépôt déjà réalisé sur les contrôles. Cet arbitrage autorise le retrait de la logistique de transmission, sans suppression de compétence, d'exercice ou de production attendue. Aucun changement de contrat d'évaluation n'est prévu. La réécriture de l'historique Git relève d'une mission technique distincte.

Cette matrice est établie avant modification des supports à partir de la version issue de la fusion du nettoyage des contrôles. Les indices de cellule sont ceux du JSON, à partir de zéro. Aucune adresse de serveur personnel n'est reproduite dans cette documentation.

## Matrice source → cible

Tous les supports sont dans `Notebooks TD/S3/`. Les activités et productions ci-dessous sont obligatoires ; le choix de suivre une remédiation reste conditionné aux besoins de l'étudiant.

| Support | Objectifs, notions et activités maintenus | Productions, charge et autonomie | Source logistique | Cible |
|---|---|---|---|---|
| `TD0_S3_diagnostic_texte.ipynb` | Python pour le texte, occurrences/formes, normalisation, fréquences et critique du découpage ; Q1–Q7 | Code, sorties et export JSON ; 2 h ; prédire, construire, vérifier et transférer | Cellule 23, invitation à ouvrir le site, choisir le TD et déposer | `SUPPRIMÉ` : seule la phrase de transmission. `CONSERVÉ` : sauvegarde, export, orientation R0, transition TD1 et avertissement sur l'authenticité des traces |
| `TD1_S3_fondations_spacy.ipynb` | Pipeline, Doc, tokens, phrases, lemmes et catégories ; confrontation aux annotations manuelles ; Q1–Q6 | Code, observations et export JSON ; 2 h ; confrontation critique autonome | Cellule 23, même invitation | `SUPPRIMÉ` : seule la phrase de transmission. `CONSERVÉ` : export, R1/R2, reprise TD2 et avertissement sur les traces |
| `TD2_S3_analyse_corpus.ipynb` | Fonctions de fréquences, formes/lemmes, filtres, annotations et nuage de mots ; Q1–Q7 | Fonctions, mesures, figure, interprétations et export ; 2 h | Cellule 26, même invitation | `SUPPRIMÉ` : seule la phrase de transmission. `CONSERVÉ` : sauvegarde des fonctions, export, transition TD3 et avertissement sur les traces |
| `TD3_S3_concordances_citations.ipynb` | Passages probants, positions, fidélité et normalisation des citations ; Q1–Q7 | Fonctions inspectables, concordances, preuves et export ; 2 h | Cellule 25, même invitation | `SUPPRIMÉ` : seule la phrase de transmission. `CONSERVÉ` : export, préparation TD4 et avertissement sur les traces |
| `TD4_S3_cooccurrences.ipynb` | Définitions de cooccurrence, contextes, fenêtres et preuves textuelles ; sept exercices | Fonctions, mesures, JSON et réflexion méthodologique ; 2 h | Cellule 27 : titre « Bilan et dépôt », point 3 de transmission | `SUPPRIMÉ` : instruction de transmission. Titre « Bilan et sauvegarde — 6 min ». `CONSERVÉ` : vérification des sept traces, téléchargements, fonctions, limites du rapport automatique, bilan critique et références |
| `TD5_S3_associations.ipynb` | Associations, tableaux de contingence, taux et interprétation ; sept exercices | Fonctions, calculs, JSON et réflexion méthodologique ; 2 h | Cellule 27 : même titre et point 3 | Même cible que TD4, avec son export propre |
| `TD6_S3_visualisations.ipynb` | Visualisations, dispersion et correspondance entre graphiques, mesures et sources ; sept exercices | Fonctions, figures, tableaux, JSON et réflexion méthodologique ; 2 h | Cellule 28 : même titre et point 3 | Même cible que TD4, avec son export propre et ses références Matplotlib |
| `TD7_S3_audit_llm.ipynb` | Audit quantitatif de résultats LLM, protocoles explicites, preuves et outil réutilisable ; sept exercices | Code réutilisable sur nouveau corpus, tableau d'audit, interprétations et JSON ; 2 h | Cellule 29 : même titre et point 3 | Même cible que TD4, avec son export propre. La cellule 6 expose une limite technique du correcteur : conservation exacte, y compris « serveur de dépôt », qui ne constitue pas une consigne de transmission |

Les paragraphes qui distinguent vérifications techniques et interprétation linguistique sont substantiels : ils ne doivent pas disparaître avec la phrase de dépôt. Pour TD4–TD7, le commentaire sur les limites du rapport reste présent hors de l'instruction supprimée ; renuméroter le bilan sans changer sa durée.

## Documentation d'accompagnement

Le fichier `Notebooks TD/S3/README.md`, section « Démarrer dans Colab », point 5, contient également une consigne de dépôt avec une adresse de destination. **`SUPPRIMÉ`** : uniquement la première phrase demandant la transmission et le choix de séance. **`CONSERVÉ`** : la phrase qui distingue contrôles des traces enregistrées et relecture des interprétations et choix méthodologiques par l'enseignant. Le titre et la numérotation peuvent être adaptés pour maintenir une présentation cohérente ; aucune activité étudiante ni objectif n'est supprimé. Les liens vers Colab, les huit TD, les ressources et les remédiations restent identiques.

## Éléments communs obligatoires

| Élément source | Statut cible | Preuve attendue |
|---|---|---|
| Objectifs, notions, corpus, exemples, questions, grilles et consignes de réflexion | `CONSERVÉ` | Diff limité aux cellules logistiques désignées ; TD7 cellule 6 reste identique |
| Toutes les cellules de code, sorties et compteurs d'exécution | `CONSERVÉ` | Égalité structurelle avant/après ; aucune exécution du code étudiant |
| Métadonnées et première cellule d'instructions du tuteur | `CONSERVÉ` | Égalité structurelle avant/après ; aucune modification des périmètres du tuteur |
| Installations et téléchargements des modèles/corpus, liens documentaires | `CONSERVÉ` | Liens de ressources et préparation inchangés ; ne pas supprimer tous les liens indistinctement |
| Sauvegarde avec sorties, export JSON et réemploi des fonctions | `CONSERVÉ` | Vérification des paragraphes de bilan et des fichiers attendus |
| Durées, autonomie, progression entre séances et remédiations | `CONSERVÉ` | Aucune modification des parcours ni des exercices |
| Adresse personnelle et consigne de transmission de la copie | `SUPPRIMÉ` | Aucune invitation de dépôt ni adresse de destination dans les huit TD |

## Audit des remédiations R0, R1 et R2

Les trois notebooks ne contiennent ni adresse de serveur ni invitation à transmettre une copie. Leur cellule 1 signale seulement la disponibilité du correcteur sous l'intitulé de la remédiation. Cette information pédagogique de repérage n'est pas une consigne de dépôt : **conservation intégrale** des trois fichiers.

- R0 : 25 min, avant TD1 ; comptage, normalisation, fréquences, limite argumentée et marqueurs d'exécution.
- R1 : 25 min, avant TD2 ; Doc, tokens, lemmes/POS, sélection de noms et verbes.
- R2 : 30 min, avant TD2 ; fonction réutilisable, noms/lemmes, filtrage et comparaison de fréquences.

Le terme « dépôt » désigne aussi le dépôt de code dans les instructions de récupération des ressources : ce sens doit rester intact. La mention qu'un serveur ne lance pas le code expose une limite de l'évaluation et ne demande aucune transmission ; elle est conservée.

## Critères d'acceptation

1. Huit TD principaux et leur README nettoyés, trois remédiations auditées et inchangées.
2. Aucune réduction des activités, de leur autonomie ou des productions attendues.
3. Code, sorties, métadonnées, ressources et politique du tuteur identiques.
4. Conservation explicite du bilan méthodologique et des limites de l'évaluation automatique.
5. Revue indépendante demandée : `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` ; la présente matrice est un cadrage préalable, pas une auto-validation de la réalisation.

Risque principal : supprimer le paragraphe entier contenant le lien ferait perdre une mise en garde méthodologique. Le retrait doit viser la seule instruction logistique. Aucun nouveau prérequis, bibliothèque ou mode d'évaluation n'est introduit.
