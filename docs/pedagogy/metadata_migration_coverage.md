# Couverture pédagogique de la migration des métadonnées TAL

Référence : commit `2a367529963f66a186dff1658b5951d0dbc27642`, branche `integration/tal-metadata-submit`.

## Mission et décision préalable

Rôle : TAL-Prof. Ce document fixe la matrice source → cible avant ajout des métadonnées techniques. Le périmètre comporte les 32 sujets associés à un évaluateur actif et un support explicitement inactif parmi les 33 profils du tuteur. La migration conserve intégralement le contenu pédagogique ; elle ne conçoit aucun nouvel exercice et ne modifie aucune compétence attendue.

**Décision de conception : couverture conservée par identité des contenus.** Tous les éléments substantiels ci-dessous ont le statut cible `CONSERVÉ`. Aucune suppression, réduction, substitution, réorganisation ni extension de bibliothèque n’est autorisée. Cette décision de cadrage ne constitue pas la validation de réalisation : le Pedagogy-Reviewer vérifiera indépendamment les différences et rendra son verdict.

## Matrice transversale obligatoire

| Élément source | Objectif / activité / production | Obligation et autonomie | Cible | Preuve attendue |
|---|---|---|---|---|
| Consignes, exemples, rappels, questions et sous-questions | Lire, prévoir, programmer, observer, justifier et interpréter selon le support | Statut obligatoire ou optionnel et niveau d’autonomie inchangés | CONSERVÉ | Sources Markdown et code strictement identiques |
| Données, ressources figées, bibliothèques et versions | Reproduire les traitements prévus sur les mêmes données | Aucune ressource nouvelle ni dépendance enseignée ajoutée | CONSERVÉ | Sources et métadonnées existantes identiques |
| Réponses, figures, commentaires, exports et sorties | Produire les mêmes preuves et interprétations | Ne pas réduire une activité à sa seule sortie automatique | CONSERVÉ | Sources, sorties, pièces jointes et compteurs identiques |
| Ordre et interdépendance des cellules | Construire les compétences cumulativement et réutiliser les acquis | Charge, séquence et temps annoncés inchangés | CONSERVÉ | Ordre, nombre, types et IDs de cellules identiques |
| Barème technique et appréciation humaine | Évaluer les mêmes acquis sans réduire l’analyse linguistique | Aucun point ni critère modifié | CONSERVÉ | Consignes et correcteurs comparés avant/après ; revue mixte |
| Tuteur TD | Guider, questionner et expliquer dans les limites du semestre | S1 sans code ; S2/S3 exemples distincts dans les notions autorisées | CONSERVÉ | Politique de `tal_tutor`, contexte Colab et première cellule strictement inchangés |
| Tuteur contrôle | Préserver le travail autonome | Aucun guidage, quiz, correction ni aide théorique | CONSERVÉ | Mode serveur contrôle et instructions conservés même pour noms ambigus |
| Identification et dépôt | Relier une copie à son étudiant et à l’activité | Aucun exercice ajouté ; identité existante conservée | CONSERVÉ | Cellule identité inchangée ; dépôt injecté uniquement dans des copies distribuables, hors cette migration |

## Matrice par support

Le chemin cible est le chemin source. Les identifiants ci-dessous reprennent les routes existantes, y compris leur casse ; ils ne doivent pas être inférés du nom du fichier. La liste détaillée des activités suit cette table.

| Profil tuteur | Sujet source = cible | Évaluateur cible | Mode / semestre | Objectifs et activités conservés | Statut |
|---|---|---|---|---|---|
| `CONTROLE_S1` | `Notebooks contrôles finaux/DevoirS1.ipynb` | `Controletilt-s1` | controle / S1 | Contrôle S1 : fondamentaux Python et TAL | CONSERVÉ |
| `TD1_S1` | `Notebooks TD/S1/TD1_S1_python_texte.ipynb` | `td1-s1` | td / S1 | Variables, types et premières expressions | CONSERVÉ |
| `TD2_S1` | `Notebooks TD/S1/TD2_S1_python_texte.ipynb` | `td2-s1` | td / S1 | Chaînes et séquences | CONSERVÉ |
| `TD3_S1` | `Notebooks TD/S1/TD3_S1_python_texte.ipynb` | `td3-s1` | td / S1 | Collections : listes, dictionnaires et ensembles | CONSERVÉ |
| `TD4_S1` | `Notebooks TD/S1/TD4_S1_python_texte.ipynb` | `td4-s1` | td / S1 | Boucles, conditions et comptages | CONSERVÉ |
| `TD5_S1` | `Notebooks TD/S1/TD5_S1_python_texte.ipynb` | `td5-s1` | td / S1 | Fonctions et réutilisation du code | CONSERVÉ |
| `TD6_S1` | `Notebooks TD/S1/TD6_S1_python_texte.ipynb` | `td6-s1` | td / S1 | Lire, transformer et écrire des fichiers | CONSERVÉ |
| `TD7_S1` | `Notebooks TD/S1/TD7_S1_python_texte.ipynb` | `td7-s1` | td / S1 | Motifs, expressions régulières et pipeline | CONSERVÉ |
| `CONTROLE_FINAL_S2` | `Notebooks contrôles finaux/ControleFinalS2.ipynb` | Aucun — inactif | controle / S2 | Contrôle final S2 : algorithmique et fichiers | CONSERVÉ |
| `CONTROLE_TD2_S2` | `Notebooks TD/TD2 - S2.ipynb` | `td2-S2` | controle / S2 | Contrôle S2 : renforcement et algorithmique | CONSERVÉ |
| `CONTROLE_TD4_S2` | `Notebooks TD/TD4_S2.ipynb` | `td4-S2` | controle / S2 | Contrôle : manipulation des ensembles | CONSERVÉ |
| `DEVOIR_MAISON_S2` | `Notebooks TD/devoirMaisonS2.ipynb` | `ControleDevoirMaisonS2` | controle / S2 | Devoir maison intermédiaire d’approfondissement | CONSERVÉ |
| `TD3_S2` | `Notebooks TD/TD3_S2.ipynb` | `td3-S2` | td / S2 | Renforcement Python et algorithmique | CONSERVÉ |
| `TD5_S2` | `Notebooks TD/TD5_S2.ipynb` | `td5-S2` | td / S2 | Approfondissement et algorithmique avancée | CONSERVÉ |
| `TD6_S2` | `Notebooks TD/TD6_S2.ipynb` | `td6-S2` | td / S2 | Fichiers et ressources linguistiques — sans Regex | CONSERVÉ |
| `CONTROLE_TD1_S3` | `Notebooks contrôles finaux/S3/Controle_TD1_S3.ipynb` | `controle-td1-s3` | controle / S3 | Contrôle TD1 S3 — Annotations linguistiques et décisions de lecture | CONSERVÉ |
| `CONTROLE_TD2_S3` | `Notebooks contrôles finaux/S3/Controle_TD2_S3.ipynb` | `controle-td2-s3` | controle / S3 | Contrôle TD2 S3 — Fréquences et choix de représentation | CONSERVÉ |
| `CONTROLE_TD3_S3` | `Notebooks contrôles finaux/S3/Controle_TD3_S3.ipynb` | `controle-td3-s3` | controle / S3 | Contrôle TD3 S3 — Concordances et fidélité documentaire | CONSERVÉ |
| `CONTROLE_TD4_S3` | `Notebooks contrôles finaux/S3/Controle_TD4_S3.ipynb` | `controle-td4-s3` | controle / S3 | Contrôle TD4 S3 — Cooccurrences entre fiches et documents | CONSERVÉ |
| `CONTROLE_TD5_S3` | `Notebooks contrôles finaux/S3/Controle_TD5_S3.ipynb` | `controle-td5-s3` | controle / S3 | Contrôle TD5 S3 — Dénominateurs et portée des associations | CONSERVÉ |
| `CONTROLE_TD6_S3` | `Notebooks contrôles finaux/S3/Controle_TD6_S3.ipynb` | `controle-td6-s3` | controle / S3 | Contrôle TD6 S3 — Figures vérifiables et retour aux passages | CONSERVÉ |
| `CONTROLE_TD7_S3` | `Notebooks contrôles finaux/S3/Controle_TD7_S3.ipynb` | `controle-td7-s3` | controle / S3 | Contrôle TD7 S3 — Audit quantitatif d’un rapport synthétique | CONSERVÉ |
| `R0_S3` | `Notebooks TD/S3/R0_S3_python_texte.ipynb` | `td-r0-s3` | td / S3 | Python pour le texte | CONSERVÉ |
| `R1_S3` | `Notebooks TD/S3/R1_S3_doc_spacy.ipynb` | `td-r1-s3` | td / S3 | Parcourir un Doc spaCy | CONSERVÉ |
| `R2_S3` | `Notebooks TD/S3/R2_S3_frequences_reutilisables.ipynb` | `td-r2-s3` | td / S3 | Fréquences réutilisables | CONSERVÉ |
| `TD0_S3` | `Notebooks TD/S3/TD0_S3_diagnostic_texte.ipynb` | `td0-s3` | td / S3 | Du texte à une mesure vérifiable | CONSERVÉ |
| `TD1_S3` | `Notebooks TD/S3/TD1_S3_fondations_spacy.ipynb` | `td1-s3` | td / S3 | Du texte aux annotations spaCy | CONSERVÉ |
| `TD2_S3` | `Notebooks TD/S3/TD2_S3_analyse_corpus.ipynb` | `td2-s3` | td / S3 | Fréquences, filtres et objets de recherche | CONSERVÉ |
| `TD3_S3` | `Notebooks TD/S3/TD3_S3_concordances_citations.ipynb` | `td3-s3` | td / S3 | Concordances et fidélité des citations | CONSERVÉ |
| `TD4_S3` | `Notebooks TD/S3/TD4_S3_cooccurrences.ipynb` | `td4-s3` | td / S3 | Définir et vérifier les cooccurrences | CONSERVÉ |
| `TD5_S3` | `Notebooks TD/S3/TD5_S3_associations.ipynb` | `td5-s3` | td / S3 | Comparer fréquences et associations | CONSERVÉ |
| `TD6_S3` | `Notebooks TD/S3/TD6_S3_visualisations.ipynb` | `td6-s3` | td / S3 | Lire à distance et revenir au texte | CONSERVÉ |
| `TD7_S3` | `Notebooks TD/S3/TD7_S3_audit_llm.ipynb` | `td7-s3` | td / S3 | Auditer une analyse textométrique produite par un LLM | CONSERVÉ |

## Activités et productions à préserver

Pour chaque entrée, les données, notions, exemples, manipulations, productions, interprétations, charge et autonomie sont exactement celles des cellules du sujet référencé. Toutes les sous-questions, y compris les suffixes `b`, demeurent couvertes. Le caractère obligatoire/optionnel est celui des consignes sources ; la présente migration ne le réinterprète pas. Les listes ci-dessous identifient les activités, mais ne remplacent pas l’exigence d’identité intégrale du contenu.

### CONTROLE_S1 — Contrôle S1 : fondamentaux Python et TAL

- Partie 1 : Variables, types et chaînes (5 Q - 5.0 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 1 : correction de type (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 2 : indexation et slicing (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 3 : rigueur syntaxique (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 4 : nettoyage de chaîne (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 5 : évaluation booléenne (choix multiple) (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 2 : listes et itération (5 Q - 5.0 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 6 : modification de liste (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 7 : parcours avec condition (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 8 : itération d'index erronée (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 9 : parcours inversé (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 10 : `IndexError` (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 3 : dictionnaires et conditions (5 Q - 5.0 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 11 : accès sécurisé (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 12 : Itération de Dictionnaire (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 13 : décompte de fréquence (Correction logique) (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 14 : logique conditionnelle (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 15 : filtrage de dictionnaire (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 4 : fonctions et modularité (10 Q - 10.0 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 16 : fonction simple (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 17 : distinguer `print` et `return` (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 18 : portée du `return` (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 19 : modularité (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 20 : retour de dictionnaire (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 21 : arguments par défaut (Choix multiple) (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 22 : argument manquant (Correction) (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 23 : portée des variables (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 24 : Boucle `while` (Correction logique) (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 25 : modularité (Correction + Renseignement) (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 5 : Synthèse, Algorithmique Avancée et Fichiers (5 Q - 9.0 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 26 : séparer par Casse (Correction Logique) (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 27 : Création de Dictionnaire (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 28 : traducteur Mot à Mot (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 29 : synthèse de traitement (Correction logique) (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 30 : (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.

### TD1_S1 — Variables, types et premières expressions

- `Q1` — Q1 — Expression numérique et affectation (commentaire de cellule) → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Q2 — Observation du type d'une valeur (commentaire de cellule) → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Comparaison et condition composée → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Chaîne et interpolation → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Conversion explicite d'une valeur → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Longueur et appartenance dans une chaîne → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD2_S1 — Chaînes et séquences

- `Q1` — Exercice 1, Q1b → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2, Q2b → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3, Q3b → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4, Q4b → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5, Q5b → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6, Q6b → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7, Q7b → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD3_S1 — Collections : listes, dictionnaires et ensembles

- `Q1` — Q1 — Modifier une liste → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Liste ou tuple ? → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Lexique bilingue → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Parcourir un dictionnaire → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Formes distinctes → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Comparer deux vocabulaires → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD4_S1 — Boucles, conditions et comptages

- `Q1` — Q1 — Boucle et majuscules → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Filtrer, premier essai → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Filtrer, second essai → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — range et positions → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — while avec condition d’arrêt → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Compter des formes → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Compréhension de liste → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD5_S1 — Fonctions et réutilisation du code

- `Q1` — Exercice 1 — Première fonction → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Normaliser → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Compter les mots → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Traduire un mot → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Traduire une phrase → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Composer → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD6_S1 — Lire, transformer et écrire des fichiers

- `Q1` — Exercice 1 — Lire sans oublier de fermer → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Lignes utiles → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Lire une ligne structurée → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Normaliser une personne → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Affiliations uniques → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Écrire un CSV → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD7_S1 — Motifs, expressions régulières et pipeline

- `Q1` — Exercice 1 — Rechercher → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Extraire plusieurs nombres → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Extraire des mots → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Remplacer des dates → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Fonction de nettoyage → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Pipeline de synthèse → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Limite méthodologique → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### CONTROLE_FINAL_S2 — Contrôle final S2 : algorithmique et fichiers

- Partie 0 : Génération des Données (Exécuter 1 fois) → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 1 : Algorithmique et Structures (5 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 2 : Lecture et Analyse de Fichiers (5 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 3 : Nettoyage et Ressources (6 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 4 : Écriture et Sauvegarde (4 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.

### CONTROLE_TD2_S2 — Contrôle S2 : renforcement et algorithmique

- Partie 1 : manipulation de chaînes et listes (5 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 1 : inversion de chaîne (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 2 : assemblage de liste (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 3 : formatage numérique (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 4 : compréhension de liste simple (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 5 : unicité avec set (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 2 : logique et dictionnaires (6 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 6 : construction de dictionnaire (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 7 : somme de valeurs (1.0 pt)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 8 : filtrage conditionnel (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 9 : comptage de fréquence (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 3 : algorithmique avancée (9 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 10 : boucles imbriquées (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 11 : suite de Fibonacci (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 12 : détection d'anagrammes (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 13 : compréhension conditionnelle (3.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.

### CONTROLE_TD4_S2 — Contrôle : manipulation des ensembles

- Partie 1 : bases et unicité (6 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 1 : dédoublonnage (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 2 : modification d'ensemble (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 3 : test d'appartenance rapide (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 2 : opérations ensemblistes (14 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 4 : intersection (3.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 5 : union (3.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 6 : différence (3.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 7 : différence symétrique (3.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 8 : sous-ensemble (2.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 3 : Simplification Algorithmique (20 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 9 : optimisation de recherche (3.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 10 : algorithme de nettoyage (3.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 11 : mots communs sans boucles (3.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 12 : gestion des absents (Différence) (3.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 13 : Index de Jaccard (NLP) (4.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.
- **Question 14 : Pangramme (Superset) (4.0 pts)** → CONSERVÉ : travail autonome, productions et critères inchangés.

### DEVOIR_MAISON_S2 — Devoir maison intermédiaire d’approfondissement

- Partie 0 : identification → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 1 : révisions des bases (20 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.
- Partie 2 : algorithmique avancée (20 pts) → CONSERVÉ : travail autonome, productions et critères inchangés.

### TD3_S2 — Renforcement Python et algorithmique

- `Q1` — Exercice 1 — Coût et types → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Sous-chaîne → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Condition composée → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Nettoyage → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Structure adaptée → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Modification de liste → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Comptage → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q8` — Exercice 8 — Compréhension → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q9` — Exercice 9 — Occurrences → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q10` — Exercice 10 — Boucle conditionnelle → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q11` — Exercice 11 — Fonction → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q12` — Exercice 12 — Paramètre par défaut → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q13` — Exercice 13 — Tri avec clé → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q14` — Exercice 14 — Ensembles → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q15` — Exercice 15 — Gestion d’erreur → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q16` — Exercice 16 — Factorielle itérative → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q17` — Exercice 17 — Maximum et position → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q18` — Exercice 18 — Bigrammes → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q19` — Exercice 19 — Association → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q20` — Exercice 20 — Filtrage → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q21` — Exercice 21 — Complexité → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q22` — Exercice 22 — Moyenne et écart-type → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q23` — Exercice 23 — Formes distinctes → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q24` — Exercice 24 — Recherche sans in → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q25` — Exercice 25 — Récursivité → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q26` — Exercice 26 — Dictionnaire par compréhension → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q27` — Exercice 27 — Deux plus grandes valeurs → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q28` — Exercice 28 — Mots vides → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q29` — Exercice 29 — Toutes les paires → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q30` — Exercice 30 — Euclide → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD5_S2 — Approfondissement et algorithmique avancée

- `Q1` — Exercice 1 — Carrés des pairs → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Filtrage de mots → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Dictionnaire de longueurs → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Inversion des mots → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Association → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Palindrome → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Anagrammes → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q8` — Exercice 8 — Distance de Hamming → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q9` — Exercice 9 — Acronyme → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q10` — Exercice 10 — Chiffrement de César → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q11` — Exercice 11 — Aplatissement → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q12` — Exercice 12 — Fusion de dictionnaires → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q13` — Exercice 13 — Inversion de dictionnaire → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q14` — Exercice 14 — Tri complexe → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q15` — Exercice 15 — Mode → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q16` — Exercice 16 — Tokenisation → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q17` — Exercice 17 — Stopwords → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q18` — Exercice 18 — Bigrammes → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q19` — Exercice 19 — Trigrammes → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q20` — Exercice 20 — Jaccard → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q21` — Exercice 21 — Fréquence normalisée → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q22` — Exercice 22 — Produit scalaire → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q23` — Exercice 23 — Préfixe commun → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q24` — Exercice 24 — Cooccurrence simplifiée → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q25` — Exercice 25 — Pipeline → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD6_S2 — Fichiers et ressources linguistiques — sans Regex

- `Q1` — Exercice 1 — Lecture simple → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Lecture ligne à ligne → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Nettoyer une ligne → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Tokenisation → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Filtrage numérique → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Stopwords → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Pipeline complet → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q8` — Exercice 8 — Fréquences sans Counter → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q9` — Exercice 9 — Écriture CSV sans bibliothèque → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q10` — Exercice 10 — CSV trié → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### CONTROLE_TD1_S3 — Contrôle TD1 S3 — Annotations linguistiques et décisions de lecture

- Exercice 1 — Préserver une source et définir un comptage → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 2 — Rendre l’annotation vérifiable → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 3 — Segmenter un compte rendu → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 4 — Choisir les informations à conserver → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 5 — Lire une relation plutôt qu’un sac de mots → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 6 — Transfert 1 — Une annonce de transport → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 7 — Transfert 2 — Réutiliser un diagnostic → CONSERVÉ : travail autonome, productions et critères inchangés.

### CONTROLE_TD2_S3 — Contrôle TD2 S3 — Fréquences et choix de représentation

- Exercice 1 — Constituer une base contrôlable → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 2 — Produire deux fonctions spécialisées → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 3 — Mesurer le coût d’une exclusion → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 4 — Distinguer structure grammaticale et contenu → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 5 — Transfert 1 — Exploiter une annotation reçue → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 6 — Représenter exactement les mêmes valeurs → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 7 — Transfert 2 — Généraliser à l’alimentation → CONSERVÉ : travail autonome, productions et critères inchangés.

### CONTROLE_TD3_S3 — Contrôle TD3 S3 — Concordances et fidélité documentaire

- Exercice 1 — Définir l’objet de la vérification → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 2 — Construire un dispositif de concordances → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 3 — Comparer plusieurs objets de recherche → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 4 — Vérifier les citations sans les réécrire → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 5 — Normaliser et qualifier les écarts → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 6 — Mettre les fonctions à l’épreuve → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 7 — Transfert — Auditer un bulletin radio → CONSERVÉ : travail autonome, productions et critères inchangés.

### CONTROLE_TD4_S3 — Contrôle TD4 S3 — Cooccurrences entre fiches et documents

- Exercice 1 — Définir les unités du relevé · 10 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 2 — Produire des cooccurrences avec preuves · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 3 — Évaluer une annonce de groupe · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 4 — Définir une fenêtre sur le flux · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 5 — Changer le contexte documentaire · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 6 — Contrôler formes, lemmes et expressions · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 7 — Transférer aux archives sonores · 20 min → CONSERVÉ : travail autonome, productions et critères inchangés.

### CONTROLE_TD5_S3 — Contrôle TD5 S3 — Dénominateurs et portée des associations

- Exercice 1 — Reconstruire les effectifs de base · 10 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 2 — Construire les deux populations de référence · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 3 — Distinguer fréquence et concentration · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 4 — Comparer deux tailles de texte · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 5 — Distinguer zéro, absence de base et rareté · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 6 — Mesurer une couverture de positions · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 7 — Transférer aux bulletins du littoral · 20 min → CONSERVÉ : travail autonome, productions et critères inchangés.

### CONTROLE_TD6_S3 — Contrôle TD6 S3 — Figures vérifiables et retour aux passages

- Exercice 1 — Situer les occurrences sans changer le flux · 10 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 2 — Segmenter et conserver les frontières · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 3 — Relier la carte de chaleur aux dénominateurs · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 4 — Visualiser la sensibilité aux fenêtres · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 5 — Revenir du graphique au texte original · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 6 — Rendre une matrice de cooccurrences lisible · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 7 — Transférer aux retours d’ateliers · 20 min → CONSERVÉ : travail autonome, productions et critères inchangés.

### CONTROLE_TD7_S3 — Contrôle TD7 S3 — Audit quantitatif d’un rapport synthétique

- Exercice 1 — Qualifier les annonces du rapport · 10 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 2 — Construire un moteur paramétrable de mesure · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 3 — Vérifier la fidélité des citations · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 4 — Comparer des nombres dans leur protocole · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 5 — Éprouver groupes, expressions et représentations · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 6 — Valider sur un autre domaine · 15 min → CONSERVÉ : travail autonome, productions et critères inchangés.
- Exercice 7 — Livrer un dossier complet de vérification · 20 min → CONSERVÉ : travail autonome, productions et critères inchangés.

### R0_S3 — Python pour le texte

- `Q1` — 1. Compter les mots → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — 2. Normaliser → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — 3. Fréquences → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — 4. Regard critique → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### R1_S3 — Parcourir un Doc spaCy

- `Q1` — 1. Observer le document → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — 2. Parcourir → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — 3. Noms → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — 4. Verbes → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### R2_S3 — Fréquences réutilisables

- `Q1` — 1. Fonction → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — 2. Noms et lemmes → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — 3. Filtrer → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — 4. Comparer → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD0_S3 — Du texte à une mesure vérifiable

- `Q1` — Exercice 1 — Lire et préserver le texte → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Voir les unités réellement comptées → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Occurrences et vérification → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Construire le vocabulaire observé → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Fréquences brutes et fonction réutilisable → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Normaliser sans tout confondre → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Passer du comptage à l’audit → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD1_S3 — Du texte aux annotations spaCy

- `Q1` — Exercice 1 — Lire puis contrôler les annotations → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Segmenter et vérifier → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Comparer trois filtres → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Visualiser puis expliquer → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Comparer deux découpages sur une même donnée → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Réinvestissement autonome et export de preuves → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD2_S3 — Fréquences, filtres et objets de recherche

- `Q1` — Exercice 1 — Lire le corpus et rendre l’annotation inspectable → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Deux fonctions de fréquences → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Mesurer l’effet des exclusions → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Fréquences grammaticales → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Contrôle qualité et objets recherchés → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Visualiser sans surinterpréter → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Généraliser et transférer → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD3_S3 — Concordances et fidélité des citations

- `Q1` — Exercice 1 — Fixer le périmètre de la preuve → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Construire une concordance exacte → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Comparer des recherches explicites → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Auditer une citation exacte → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Qualifier une altération → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Un rapprochement n’est pas une preuve automatique → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Assembler un dossier de preuves → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD4_S3 — Définir et vérifier les cooccurrences

- `Q1` — Exercice 1 — Présence et marges → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Compter une paire par phrase → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Réunion et somme des paires → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Mesurer une distance entre positions → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Choisir les frontières → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Contrôler la normalisation → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Exporter une mesure contrôlable → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD5_S3 — Comparer fréquences et associations

- `Q1` — Exercice 1 — Donner un dénominateur → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Fréquent ou associé ? → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Comparer des tailles de texte → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Inverser la condition → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Traiter les absences et les petits nombres → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Tester la sensibilité du résultat → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Rédiger une conclusion mesurée → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD6_S3 — Lire à distance et revenir au texte

- `Q1` — Exercice 1 — Situer les occurrences → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Découper en segments → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Comparer une carte de chaleur → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Visualiser la sensibilité → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Revenir aux passages → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Rendre un graphique vérifiable → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Interpréter et exporter → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

### TD7_S3 — Auditer une analyse textométrique produite par un LLM

- `Q1` — Exercice 1 — Formaliser une affirmation → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q2` — Exercice 2 — Construire le moteur commun → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q3` — Exercice 3 — Vérifier les citations → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q4` — Exercice 4 — Comparer un nombre défini → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q5` — Exercice 5 — Traiter groupes et expressions → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q6` — Exercice 6 — Éprouver sur un cas nouveau → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.
- `Q7` — Exercice 7 — Livrer un audit argumenté → CONSERVÉ : mêmes consigne, notion, activité, données et production attendue.

## Rôles des cellules et exceptions de résolution

- Les nouvelles métadonnées techniques sont isolées dans `metadata.tal`, au niveau notebook et, lorsque nécessaire, au niveau cellule. Ne remplacer aucune métadonnée existante. Le vocabulaire final des rôles relève du contrat technique, pas des consignes pédagogiques.
- Distinguer cellule de réponse/code, consigne, interprétation écrite, préparation fournie, identité, export et contexte du tuteur. Une préparation fournie n’est pas une réponse d’étudiant. L’interprétation linguistique ne disparaît pas parce qu’elle n’est pas notée automatiquement.
- Identifier les réponses à partir des marqueurs effectivement présents et du correcteur : `Résultat Q…`, sorties JSON `S3_TD…_Q…` ou `S3_C…_Q…`. Les marqueurs, variables et sorties restent littéralement inchangés.
- Une cellule peut porter plusieurs sorties ou sous-questions. Le contrat doit représenter toutes les questions associées sans découper la cellule, supprimer un suffixe ou attribuer deux cellules à la même question/rôle sans règle explicite.
- Les TD S3 permettent de réutiliser des fonctions des activités antérieures. Leur reconnaissance ne doit pas exclure ces cellules auxiliaires du contrôle de code lorsque le correcteur les prenait déjà en compte.
- Les contrôles S3 cumulent production technique et interprétation humaine ; le score technique provisoire conserve ce statut. Le rapport détaillé reste destiné à l’enseignant.
- `td2-S2` et `td4-S2` restent des contrôles. Le mode ne se déduit pas des préfixes `TD` ou `td` ni d’une valeur libre fournie par la copie.
- `CONTROLE_FINAL_S2` conserve son tuteur mais aucun correcteur actif ne lui est associé dans le registre actuel. Fichier inchangé dans cette migration ; aucune activation ou cellule de dépôt implicite.
- Dans le manifeste du tuteur, `exercises: []` des contrôles exprime l’interdiction d’assistance. Cela ne signifie ni absence de questions ni absence de couverture à vérifier.

## Exclusions conservées

| Fichier | Motif source ; décision cible |
|---|---|
| `Corrigés modèles/TD/td2-s1/TD2_S1_EtudiantModele_non_execute.ipynb` | Corrigé modèle séparé, non destiné au travail étudiant ; conserver sans tuteur ni modification. |
| `Notebooks TD/TD2 - S2 - Corrigé.ipynb` | Corrigé enseignant, hors sujets étudiants ; conservé sans modification. |
| `Notebooks TD/TD3 - S2 - Corrigé.ipynb` | Corrigé enseignant, hors sujets étudiants ; conservé sans modification. |
| `Notebooks TD/TD4_S2-corrigé.ipynb` | Corrigé enseignant, hors sujets étudiants ; conservé sans modification. |
| `Notebooks TD/TD5_S2-corrigé.ipynb` | Corrigé enseignant, hors sujets étudiants ; conservé sans modification. |
| `Notebooks TD/TD6_S2-corrigé.ipynb` | Corrigé enseignant, hors sujets étudiants ; conservé sans modification. |
| `Notebooks TD/devoirMaisonS2-corrigé.ipynb` | Corrigé enseignant, hors sujets étudiants ; conservé sans modification. |
| `Notebooks contrôles finaux/DevoirS1_TILT_corrigé.ipynb` | Corrigé enseignant, hors sujets étudiants ; conservé sans modification. |
| `Notebooks contrôles finaux/DevoirS2.ipynb` | Corrigé enseignant mal nommé : titre TD6 (CORRIGÉ), Version Enseignant / Solution ; JSON tronqué préexistant, hors sujets et inchangé. |

Le JSON préexistant de `Notebooks contrôles finaux/DevoirS2.ipynb` est tronqué. Il ne doit être ni réparé, ni réinterprété comme sujet, ni activé à l’occasion de cette mission. Les corrigés enseignants et modèles restent hors distribution des sujets.

## Hypothèses, risques, vérification et handoff

- Hypothèse : le registre actif et le manifeste tuteur de la référence sont les sources d’autorité de l’inventaire. Tout écart est signalé, sans rapprochement automatique fondé uniquement sur les noms.
- Risques : assignation incorrecte d’une cellule, perte d’une sous-question, confusion TD/contrôle, inclusion d’un corrigé, réduction de l’analyse à une trace JSON, effacement d’une métadonnée Colab. Les preuves d’intégrité et les cas multi-questions doivent les couvrir.
- Critère d’acceptation pédagogique : après suppression des seules nouvelles clés `metadata.tal`, égalité profonde du JSON avant/après pour chaque sujet ; aucune autre clé/cellule ajoutée ou retirée. Les fichiers exclus et le contrôle inactif doivent rester identiques. Le simple décompte des cellules est insuffisant.
- Critère d’évaluabilité : mêmes correcteurs et barèmes pour les anciennes copies ; essais comparatifs sur des copies identiques avant/après migration ; contrôler les ambiguïtés et les sous-sorties. Le nouveau routage reste un changement de contrat technique soumis à double revue.
- Injection HTML ultérieure : exclusivement dans des copies générées de distribution, hors Git. Elle ne doit pas introduire de compétence à acquérir, solution ou guidage en contrôle, ni remplacer la cellule initiale du tuteur.
- Tests de cadrage effectués : lecture statique du registre, des 33 profils et des sujets JSON valides ; inspection des familles de cellules S1, S2, TD S3 et contrôles S3. Aucun code étudiant exécuté. Aucune réalisation n’est déclarée validée par le présent document.
- Handoff : Designer applique les ajouts techniques ; Architecte préserve l’évaluabilité ; Pedagogy-Reviewer vérifie la couverture et Code-Auditor le contrat. Gouvernance puis intégration suivent. Verdict demandé à la revue : `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` si et seulement si les invariants sont démontrés.
