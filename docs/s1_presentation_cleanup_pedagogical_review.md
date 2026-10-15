# Revue pédagogique indépendante — nettoyage de présentation S1

Mission : vérifier le cadrage préalable puis la conservation pédagogique de la cible des sept TD S1, dans le périmètre des quatre changements de présentation autorisés par l'utilisateur. Rôle : TAL-Pedagogy-Reviewer, distinct du Prof et du Designer. Branche partagée : `pedagogy/s1-nettoyage-presentation` ; source `590b9a6`. Date : 15 octobre 2026.

Aucun support, code, test, document pédagogique ou actif normatif modifié par ce réviseur. Aucun commit, changement de branche ou exécution d'une solution étudiante. Le présent handoff est écrit seulement dans `/tmp` pour archivage par l'intégration.

## Prévalidation avant conception

Sources normatives et rôles lus : `AGENTS.md`, `docs/agents/WORKFLOW.md`, `docs/agents/TAL-Pedagogy-Reviewer.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`, `docs/pedagogy/TUTORING_POLICY.md`. Les matrices antérieures de progression et de reprise éditoriale S1 et la revue indépendante exhaustive du 14 octobre ont déjà été comparées au même commit source.

Lecture intégrale de `docs/pedagogy/s1_presentation_cleanup_coverage.md` avant toute édition de notebook. Première empreinte lue : `fbfcc1238b461d6cabe141f8404def7c32e23177e991d43cb87a9ae004ba72ab`. L'ajustement ultérieur de provenance de l'audit, sans effet sur les opérations autorisées, a également été relu : empreinte `fa9483e94fdd06992d745033e29110ae326e709dad9794b02692bb352c82dca4`. La version comprenant ensuite la provenance révisée et le verdict préalable attribué a également été relue : `f31e39080dd013ab149d3f577ec32ad45e9224e1d5255ca81de73b8910f94b24`. La consignation par le Prof de ce verdict indépendant ne constitue pas son auto-validation.

Au moment du verdict préalable, comparaison indépendante des sept notebooks courants à leur baseline JSON : aucun changement. Inventaire physique : 293 cellules, 45 réponses, 44 exemples, 52 cellules d'essai/vérification/synthèse, deux préparations et sept restitutions. Les sept identifications contiennent les affectations à conserver. Les onze vérifications après réponse de TD5 Q1–6, TD6 Q4–5 et TD7 Q4–6 sont bien livrées après la fonction concernée.

La matrice utilise des indices commençant à 1. Elle désigne précisément les passages de présentation et les 45 questions avec leurs cellules de réponse/exemple/essai. Les suffixes de durée peuvent être supprimés sans toucher les cours. Le commentaire d'identification TD2 peut être retiré sans changer les affectations ou l'AST. La procédure générale et la présentation de Gemini ont pour destination TD1 cellule 5 (base 1). Les prédictions, essais, explications, synthèses spécifiques et critères locaux, dont TD2 Q7 et TD7 Q7, restent obligatoires. Les données d'identité métier TD6 ne sont pas des notices administratives. Les restitutions canoniques et leur commentaire d'injection restent intacts, conformément au périmètre précisé par le relais.

**Verdict préalable : ACCEPT DU CADRAGE**, autorisant l'étape Designer. Ce verdict a été transmis à l'orchestrateur et au Prof avant conception. Il ne valide pas une cible encore non produite.

## Revue de la cible

La cible a été relue après le signal de fin du Designer et comparée indépendamment à la copie JSON source, conservée avant conception. Le handoff du producteur n'a pas remplacé ces vérifications.

Dans la suite, les indices de cellule commencent à **1**, comme dans la matrice du Prof. Les 293 cellules sont présentes, de mêmes types et dans le même ordre, avec mêmes identifiants et métadonnées. Les 45 cellules de réponse, 44 exemples, 52 cellules d'essai/vérification/synthèse, deux préparations et sept restitutions sont conservés dans le même support. Toutes leurs sources de code sont exactement identiques. Toutes les cellules de code ont en outre le même AST : la seule différence de source de code est le retrait du commentaire de notice TD2 cellule 4. Les affectations de l'identification et le commentaire de réponse au rappel TD1 restent présents.

Les 45 cellules de présentation modifiées correspondent exactement aux emplacements autorisés par la matrice : TD1 3/5/7/12/17/22/27/32/37 ; TD2 2/3/4/5/6/10/14/18/22/26/30/32 ; TD3 3/5/7/12/17/23/28/33/38 ; TD4 5/7/12/17/22/27/32/37/42 ; TD5 5/43 ; TD6 5/40 ; TD7 5/47. Toutes les phrases retirées, ajoutées ou réorganisées ont été relues, avec leur contexte. Les cours ne perdent que les suffixes chronométrés de leurs titres. Les tableaux de durée et notices administratives sont supprimés, sans activité retirée.

### Vérification des quatre changements autorisés

1. Aucun minutage de séance ne reste dans le Markdown visible. Les activités anciennement listées dans les tableaux sont toujours présentes dans leurs cours, exercices et synthèses ; la disparition des durées n'est pas une diminution du travail demandé.
2. Les notices sur les champs d'identification sont retirées. Les quatre affectations, valeurs de départ et métadonnées restent identiques. La normalisation d'identités métier au TD6 Q4 est intégralement conservée.
3. TD1 cellule 5 regroupe le guide général : copie personnelle, cellules/libellés conservés, exemples distincts, essais obligatoires, prédiction et commentaire, activation des print, exécution ordonnée, sorties enregistrées, dépôt, retour automatique et limites du score pour l'interprétation. Les répétitions générales sont retirées des autres introductions ; les consignes propres aux exercices et à la navigation restent présentes.
4. Cette même cellule présente Gemini une fois. Une occurrence visible dans TD1, aucune dans TD2–7. Il guide par questions et explications en langage naturel dans les notions déjà étudiées ou introduites avant l'exercice, sans code ni réponses. Cette présentation n'ajoute aucun droit au profil caché.

Les indications locales « pour vérifier », la conservation des libellés spécifiques, les affichages fournis, l'ordre des essais après fonction et les conventions propres aux tâches restent à leur place. La synthèse et le dépôt propres à chaque TD ne constituent pas une seconde notice générale du correcteur. Le double contexte caché n'a pas été modifié : première cellule et métadonnées intactes, égalité exacte commentaire HTML/Colab dans les sept supports.

### Preuve par question : source → cible

Chaque ligne signifie conservation des données, productions, formats, marqueurs, critères, prérequis et niveau d'autonomie dans les cellules désignées. Énoncés exactement identiques sauf retrait du suffixe de durée du titre TD2 Q7 ; réponses et activités de code exactement identiques. Ces comparaisons complètent la relecture du contenu, déjà conduite exhaustivement sur la source 590b9a6 et poursuivie sur tous les passages changés. Aucune question n'est seulement réputée couverte par un comptage de cellules.

| Question | Objectif / intitulé relu | Énoncé | Réponse | Exemples, essais et vérifications | Couverture |
|---|---|---|---|---|---|
| TD1 Q1 | Exercice 1 — Calculer un coût de traduction | 10 | 11 | 8, 9 | CONSERVÉ |
| TD1 Q2 | Exercice 2 — Identifier un type | 15 | 16 | 13, 14 | CONSERVÉ |
| TD1 Q3 | Exercice 3 — Affectation ou comparaison | 20 | 21 | 18, 19 | CONSERVÉ |
| TD1 Q4 | Exercice 4 — Insérer des valeurs dans une phrase | 25 | 26 | 23, 24 | CONSERVÉ |
| TD1 Q5 | Exercice 5 — Convertir avant de calculer | 30 | 31 | 28, 29 | CONSERVÉ |
| TD1 Q6 | Exercice 6 — Décrire une phrase personnelle | 35 | 36 | 33, 34 | CONSERVÉ |
| TD2 Q1 | Exercice 1 — À vous de travailler | 8 | 9 | 7 | CONSERVÉ |
| TD2 Q2 | Exercice 2 — À vous de travailler | 12 | 13 | 11 | CONSERVÉ |
| TD2 Q3 | Exercice 3 — À vous de travailler | 16 | 17 | 15 | CONSERVÉ |
| TD2 Q4 | Exercice 4 — À vous de travailler | 20 | 21 | 19 | CONSERVÉ |
| TD2 Q5 | Exercice 5 — À vous de travailler | 24 | 25 | 23 | CONSERVÉ |
| TD2 Q6 | Exercice 6 — À vous de travailler | 28 | 29 | 27 | CONSERVÉ |
| TD2 Q7 | Exercice 7 — Observer et interpréter une limite | 30 | 31 | Activité d’observation dans énoncé/réponse | CONSERVÉ |
| TD3 Q1 | Exercice 1 — Ajouter, observer, retirer | 10 | 11 | 8, 9 | CONSERVÉ |
| TD3 Q2 | Exercice 2 — Choisir une référence stable | 15 | 16 | 13, 14 | CONSERVÉ |
| TD3 Q3 | Exercice 3 — Construire un lexique bilingue | 20 | 22 | 18, 19 | CONSERVÉ |
| TD3 Q4 | Exercice 4 — Parcourir le lexique | 26 | 27 | 24, 25 | CONSERVÉ |
| TD3 Q5 | Exercice 5 — Distinguer occurrences et formes | 31 | 32 | 29, 30 | CONSERVÉ |
| TD3 Q6 | Exercice 6 — Comparer deux vocabulaires | 36 | 37 | 34, 35 | CONSERVÉ |
| TD4 Q1 | Exercice 1 — Transformer chaque mot | 10 | 11 | 8, 9 | CONSERVÉ |
| TD4 Q2 | Exercice 2 — Filtrer selon la longueur | 15 | 16 | 13, 14 | CONSERVÉ |
| TD4 Q3 | Exercice 3 — Filtrer selon une lettre | 20 | 21 | 18, 19 | CONSERVÉ |
| TD4 Q4 | Exercice 4 — `range` et positions | 25 | 26 | 23, 24 | CONSERVÉ |
| TD4 Q5 | Exercice 5 — `while` avec condition d’arrêt | 30 | 31 | 28, 29 | CONSERVÉ |
| TD4 Q6 | Exercice 6 — Compter des formes | 35 | 36 | 33, 34 | CONSERVÉ |
| TD4 Q7 | Exercice 7 — Compréhension de liste | 40 | 41 | 38, 39 | CONSERVÉ |
| TD5 Q1 | Exercice 1 — Première fonction | 10 | 11 | 8, 9, 12 | CONSERVÉ |
| TD5 Q2 | Exercice 2 — Normaliser | 16 | 17 | 14, 15, 18 | CONSERVÉ |
| TD5 Q3 | Exercice 3 — Compter les mots | 22 | 23 | 20, 21, 24 | CONSERVÉ |
| TD5 Q4 | Exercice 4 — Traduire un mot | 28 | 29 | 26, 27, 30 | CONSERVÉ |
| TD5 Q5 | Exercice 5 — Traduire une phrase | 34 | 35 | 32, 33, 36 | CONSERVÉ |
| TD5 Q6 | Exercice 6 — Composer un résumé | 40 | 41 | 38, 39, 42 | CONSERVÉ |
| TD6 Q1 | Exercice 1 — Lire sans oublier de fermer | 11 | 12 | 9, 10 | CONSERVÉ |
| TD6 Q2 | Exercice 2 — Lignes utiles | 16 | 17 | 14, 15 | CONSERVÉ |
| TD6 Q3 | Exercice 3 — Lire une ligne structurée | 21 | 22 | 19, 20 | CONSERVÉ |
| TD6 Q4 | Exercice 4 — Normaliser une personne | 26 | 27 | 24, 25, 28 | CONSERVÉ |
| TD6 Q5 | Exercice 5 — Affiliation(s) unique(s) | 32 | 33 | 30, 31, 34 | CONSERVÉ |
| TD6 Q6 | Exercice 6 — Écrire un CSV | 38 | 39 | 36, 37 | CONSERVÉ |
| TD7 Q1 | Exercice 1 — Rechercher | 12 | 13 | 10, 11 | CONSERVÉ |
| TD7 Q2 | Exercice 2 — Extraire plusieurs nombres | 17 | 18 | 15, 16 | CONSERVÉ |
| TD7 Q3 | Exercice 3 — Extraire des suites de lettres | 22 | 23 | 20, 21 | CONSERVÉ |
| TD7 Q4 | Exercice 4 — Remplacer des dates | 27 | 28 | 25, 26, 29 | CONSERVÉ |
| TD7 Q5 | Exercice 5 — Fonction de nettoyage | 33 | 34 | 31, 32, 35 | CONSERVÉ |
| TD7 Q6 | Exercice 6 — Pipeline de synthèse | 39 | 40 | 37, 38, 41 | CONSERVÉ |
| TD7 Q7 | Exercice 7 — Limite méthodologique | 45 | 46 | 43, 44 | CONSERVÉ |

Compléments explicitement conservés : TD1 Q6b et phrase personnelle, TD2 Q1b–Q7b et toutes prédictions/observations/justifications, TD3 Q1a/Q2b/Q3b/Q5b, TD6 Q3b/Q4b/Q5b. Les listes et dictionnaires complets, cas limites et tests sur chaînes vides ne sont ni supprimés ni déplacés hors support.

### Synthèses et limites locales

- TD1 cellule 37 : reprise d'un essai, explication des écarts et distinction valeur/type, affectation/comparaison, chaîne/nombre. Seuls le minutage et la seconde notice générale du retour sont retirés.
- TD2 cellules 3–4 : le rappel actif nom/valeur/type/= / == /len et son emplacement de réponse sont présents. Cellule 32 : liste Q1–Q7/Q1b–Q7b, réflexion sur chaîne/liste, borne exclue et limite de split intactes, sans durée.
- TD3 cellule 38 : comparaison des collections, justification d'un choix, intersection/différence et reprise d'un essai inchangées en substance.
- TD4 cellule 42 : bornes, filtres, initialisation et essai où la prédiction différait restent obligatoires.
- TD5 cellules 43–44, TD6 40–41 et TD7 47–48 : choix d'un test utile, explication, difficulté ouverte et enregistrement des sorties conservés. Seule la notice de vérification d'identité est retirée.
- Les onze vérifications après réponse restent après définition : TD5 Q1–6, TD6 Q4–5, TD7 Q4–6. Les avertissements des introductions sur cet ordre restent présents.
- TD1 Q6 cellule 35 rappelle que le retour ne juge pas la qualité de la phrase libre. TD2 Q7 cellule 30 conserve les critères d'interprétation et la limite du fond non autocorrigé ; seule sa durée de titre est retirée. TD7 Q7 cellule 45 conserve exactement son autoévaluation linguistique et l'absence de validation automatique du sens.
- TD6 conserve le cours, les exemples, le format CSV et les ordres libres ; TD7 conserve la convention d'extraction, le marqueur DATE et les conséquences linguistiques du pipeline. Aucune notion ou bibliothèque supplémentaire n'apparaît.

### Empreintes de la cible validée

| Notebook sous Notebooks TD/S1/ | Cellules | SHA-256 |
|---|---:|---|
| `TD1_S1_variables_types.ipynb` | 38 | `94abfa27d9b6a21395f60c91f0b8ca149cfcf20b5248799df0feec6f0aa338c3` |
| `TD2_S1_chaines_sequences.ipynb` | 33 | `5d5e0ecc6650e07acf4a4b1695963802cbad3298df41053976d2d30d0636eed3` |
| `TD3_S1_collections.ipynb` | 39 | `822aeab68461784d9fa0e410ae18a37bb295486aecb46657e1bce0981c7944e8` |
| `TD4_S1_boucles_conditions_comptages.ipynb` | 44 | `fc82a243ba0c09d1a7d1a89203885c78381ccf323a2a3a8c0d93d991b18a0e51` |
| `TD5_S1_fonctions_reutilisation.ipynb` | 46 | `2e2dbc49943a2070b8ad7c155c377a2e30fe8db0fa58e5fd09f70d9c8668b3cf` |
| `TD6_S1_fichiers_csv.ipynb` | 43 | `01e00fff36a012f091097794d1d62b0f9255976fc61a8299366238b131b165d8` |
| `TD7_S1_expressions_regulieres_pipeline.ipynb` | 50 | `b7ff9f64672c0886543a27a5079638f79f8eab4127553d2c1b2b7aaab4489f79` |

### Verdict final de cette revue

Aucun constat pédagogique nouveau ne bloque ce nettoyage. Le constat de présentation TAL-PED-006 de l'audit précédent est traité pour ces sept TD, dans les quatre points effectivement autorisés. Les données, cours, exemples, essais, productions, interprétations et autonomie restent couverts. Le résultat est **COUVERTURE_PÉDAGOGIQUE_CONSERVÉE — ACCEPT**, séparément pour TD1, TD2, TD3, TD4, TD5, TD6 et TD7, dans ce seul périmètre de présentation.

Ce verdict ne tient pas lieu de revue éditoriale, de revue technique ou de gouvernance. Les contrôles indépendants JSON/AST et contextes cachés sont des preuves de conservation, pas une preuve d'apprentissage ni de comportement effectif de Gemini. Aucun test de classe, temps réel ou conversation Colab n'a été réalisé par ce réviseur. Aucun changement de contrat d'évaluation n'a été observé et aucun ordre technique de modification du correcteur n'est nécessaire pour ce nettoyage.

### Handoff final

Mission et branche indiquées en tête ; fichiers modifiés par le réviseur : aucun. Les sept notebooks produits par le Designer sont les cibles examinées. Hypothèse explicitée : la procédure générale appartient au premier TD du parcours, les critères locaux et synthèses restent dans chaque TD. Comparaisons indépendantes : toutes les cellules et leur ordre, 45 questions, 44 exemples, 52 essais/vérifications/synthèses, deux préparations, sept restitutions, métadonnées et code ; égalité des doubles contextes. Risque examiné : réduction involontaire d'une activité par retrait d'une notice ; aucune réduction constatée. Critères d'acceptation de la matrice satisfaits pour cette spécialité. Verdict demandé au relais : poursuivre les revues éditoriale, technique, étudiante et de gouvernance, puis intégrer dans la PR de nettoyage. La fusion reste décision du mainteneur.


## Limites du périmètre

Les rapports de l'audit S1 préexistaient à ce nettoyage et ne sont pas des supports modifiés par cette mission. Les constats du DM, du contrôle final et de leurs corrigés restent ouverts. La couverture historique exhaustive des sources privées 2025 n'est pas démontrée par cette opération. L’ACCEPT final porte seulement sur la conservation de l’état courant et les quatre changements autorisés ; il ne valide pas toute la conformité S1.

## Clôture après lecture étudiante indépendante

Le rapport `Corrigés modèles/TD/s1-presentation-cleanup/lecture_etudiante.md` a été lu intégralement après sa remise. Il couvre les mêmes sept empreintes de cible, 293 cellules et 45 questions, avec indices base 0 explicitement annoncés. Le lecteur n'a consulté ni corrigés, ni correcteurs, ni matrice : son contrôle de compréhension complète la comparaison source→cible sans la remplacer. Il ne relève aucun blocage précis nouveau et confirme que les productions, prérequis présentés, essais et critères restent identifiables.

Le commentaire « URL injectée lors du déploiement » des sept restitutions canoniques est consigné par l'étudiant sans être qualifié de régression. Sa conservation est explicitement prévue par le périmètre autorisé et la matrice préalable ; il ne justifie donc pas une demande de changement dans ce lot. La phrase générique du TD4 sur les essais après fonction, déjà présente dans la source et sans fonction à écrire dans ce TD, ne crée aucune dépendance nouvelle.

**ACCEPT et COUVERTURE_PÉDAGOGIQUE_CONSERVÉE maintenus** pour les sept TD dans le périmètre du nettoyage. Aucun autre fichier ou recherche n'a été nécessaire à cette clôture. Les limites et constats hors lot restent inchangés.
