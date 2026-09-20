# Couverture du tutorat : tous les sujets présents et futurs

## Décision et référence avant génération

L'enseignant demande explicitement de généraliser le principe testé : un tuteur dans les métadonnées **et** une cellule Markdown dédiée placée à l'indice 0, pour chaque sujet de TD ou de contrôle, tous niveaux. Le TD guide ; le contrôle refuse toute assistance. Cette matrice est établie sur la branche `pedagogy/td2-markdown-tutor-reminder`, référence `fd77df71`, avant génération des notebooks. Elle doit être relue et validée avant l'intervention du Designer.

La transformation ne porte que sur les instructions du tuteur. Tous les objectifs, notions, activités, exemples, données, productions, obligations/options, durées et degrés d'autonomie des sujets restent conservés. Aucune nouvelle bibliothèque n'est introduite dans le programme. Les profils décrivent les notions explicitement présentes ou prérequises à l'exercice courant, jamais celles d'un exercice ultérieur. Les exemples de l'enseignant restent en place ; l'interdiction de fournir du code en S1 porte sur le tuteur.

## Matrice source → cible

Chaque ligne conserve l'intégralité des cellules de contenu, y compris leurs sources, métadonnées locales, sorties et compteurs d'exécution. Les titres ci-dessous repèrent les activités, sans réduire leur contenu. Les marqueurs, données et productions restent ceux du fichier source. Les consignes de temps, de charge et d'autonomie restent inchangées ; une durée absente n'est pas inventée.

| Source | Mode cible | Activités, notions et productions conservées | Statut |
|---|---|---|---|
| `Notebooks TD/S1/TD1_S1_python_texte.ipynb` | TD | Q1–Q6 : expression, type, comparaison, interpolation, conversion, longueur/appartenance | CONSERVÉ intégralement |
| `Notebooks TD/S1/TD2_S1_python_texte.ipynb` | TD | Exercice 1 — Nettoyer sans perdre la source — 14 min; Exercice 2 — Transformer et vérifier — 16 min; Exercice 3 — Indexer puis découper — 17 min; Exercice 4 — Passer d’une chaîne à une liste — 15 min; Exercice 5 — Reconstruire puis comparer — 12 min; Exercice 6 — Trois chaînes, plusieurs vérifications — 18 min; Exercice 7 — Observer et interpréter une limite — 14 min | CONSERVÉ intégralement |
| `Notebooks TD/S1/TD3_S1_python_texte.ipynb` | TD | Q1 : modifier une liste; Exercice 2 — Liste ou tuple ?; Exercice 3 — Lexique bilingue; Exercice 4 — Parcourir un dictionnaire; Exercice 5 — Formes distinctes; Exercice 6 — Comparer deux vocabulaires | CONSERVÉ intégralement |
| `Notebooks TD/S1/TD4_S1_python_texte.ipynb` | TD | Q1 : boucle for et majuscules; Exercice 2 — Filtrer, premier essai; Exercice 3 — Filtrer, second essai; Exercice 4 — `range` et positions; Exercice 5 — `while` avec condition d’arrêt; Exercice 6 — Compter des formes; Exercice 7 — Compréhension de liste | CONSERVÉ intégralement |
| `Notebooks TD/S1/TD5_S1_python_texte.ipynb` | TD | Exercice 1 — Première fonction; Exercice 2 — Normaliser; Exercice 3 — Compter les mots; Exercice 4 — Traduire un mot; Exercice 5 — Traduire une phrase; Exercice 6 — Composer | CONSERVÉ intégralement |
| `Notebooks TD/S1/TD6_S1_python_texte.ipynb` | TD | Exercice 1 — Lire sans oublier de fermer; Exercice 2 — Lignes utiles; Exercice 3 — Lire une ligne structurée; Exercice 4 — Normaliser une personne; Exercice 5 — Affiliation(s) unique(s); Exercice 6 — Écrire un CSV | CONSERVÉ intégralement |
| `Notebooks TD/S1/TD7_S1_python_texte.ipynb` | TD | Exercice 1 — Rechercher; Exercice 2 — Extraire plusieurs nombres; Exercice 3 — Extraire des mots; Exercice 4 — Remplacer des dates; Exercice 5 — Fonction de nettoyage; Exercice 6 — Pipeline de synthèse; Exercice 7 — Limite méthodologique | CONSERVÉ intégralement |
| `Notebooks TD/S3/R0_S3_python_texte.ipynb` | TD | 1. Compter les mots; 2. Normaliser; 3. Fréquences; 4. Regard critique | CONSERVÉ intégralement |
| `Notebooks TD/S3/R1_S3_doc_spacy.ipynb` | TD | 1. Observer le document; 2. Parcourir; 3. Noms; 4. Verbes | CONSERVÉ intégralement |
| `Notebooks TD/S3/R2_S3_frequences_reutilisables.ipynb` | TD | 1. Fonction; 2. Noms et lemmes; 3. Filtrer; 4. Comparer | CONSERVÉ intégralement |
| `Notebooks TD/S3/TD0_S3_diagnostic_texte.ipynb` | TD | Exercice 1 — Lire un fichier; Exercice 2 — Découper et compter; Exercice 3 — Formes distinctes; Exercice 4 — Fréquences brutes; Exercice 5 — Première normalisation; Exercice 6 — Interpréter les limites | CONSERVÉ intégralement |
| `Notebooks TD/S3/TD1_S3_fondations_spacy.ipynb` | TD | Exercice 1 — Tableau d’annotations; Exercice 2 — Segmentation en phrases; Exercice 3 — Filtrer des catégories; Exercice 4 — Visualiser et interpréter; Exercice 5 — Comparer découpage brut et tokenisation; Exercice 6 — Réinvestissement autonome | CONSERVÉ intégralement |
| `Notebooks TD/S3/TD2_S3_analyse_corpus.ipynb` | TD | Exercice 1 — Lire et annoter le corpus; Exercice 2 — Noms, verbes et fréquence; Exercice 3 — Paramètres et exclusions adaptées; Exercice 4 — Fréquences par catégorie grammaticale; Exercice 5 — Liste de lemmes et contrôle qualité; Exercice 6 — Nuage de mots filtré; Exercice 7 — Fonction généralisée | CONSERVÉ intégralement |
| `Notebooks TD/TD2 - S2.ipynb` | CONTRÔLE | Partie 1 : manipulation de chaînes et listes (5 pts); Partie 2 : logique et dictionnaires (6 pts); Partie 3 : algorithmique avancée (9 pts) | CONSERVÉ intégralement |
| `Notebooks TD/TD3_S2.ipynb` | TD | Exercices1–30 : bases, fonctions, algorithmique, statistiques, récursion, ensembles | CONSERVÉ intégralement |
| `Notebooks TD/TD4_S2.ipynb` | CONTRÔLE | Partie 1 : bases et unicité (6 pts); Partie 2 : opérations ensemblistes (14 pts); Partie 3 : Simplification Algorithmique (20 pts) | CONSERVÉ intégralement |
| `Notebooks TD/TD5_S2.ipynb` | TD | Partie 1 : Échauffement et compréhensions; Partie 2 : Manipulation de chaînes et logique; Partie 3 : Structures de données complexes; Partie 4 : Algorithmes pour le TAL; Partie 5 : Avancé / Vectorisation | CONSERVÉ intégralement |
| `Notebooks TD/TD6_S2.ipynb` | TD | Partie 0 : Création des données de test; Partie 1 : Lecture et Nettoyage (Niveau 1); Partie 2 : Traitement algorithmique (Niveau 2); Partie 3 : Construction de ressource (Niveau 3); Partie 4 : Écriture structurée (CSV) | CONSERVÉ intégralement |
| `Notebooks TD/devoirMaisonS2.ipynb` | CONTRÔLE | Partie 0 : identification; Partie 1 : révisions des bases (20 pts); Partie 2 : algorithmique avancée (20 pts) | CONSERVÉ intégralement |
| `Notebooks contrôles finaux/ControleFinalS2.ipynb` | CONTRÔLE | Partie 0 : Génération des Données (Exécuter 1 fois); Partie 1 : Algorithmique et Structures (5 pts); Partie 2 : Lecture et Analyse de Fichiers (5 pts); Partie 3 : Nettoyage et Ressources (6 pts); Partie 4 : Écriture et Sauvegarde (4 pts) | CONSERVÉ intégralement |
| `Notebooks contrôles finaux/DevoirS1.ipynb` | CONTRÔLE | Questions1–30, identification, fichiers, dépôt : toutes les parties existantes | CONSERVÉ intégralement |

| Élément transversal source | Cible | Justification |
|---|---|---|
| Métadonnées du tuteur et limites par exercice des pilotes | RENFORCÉ | Même politique harmonisée, étendue à chaque sujet et reproduite en Markdown |
| Rappel HTML du TD2 attaché à la cellule d'introduction | DÉPLACÉ avec équivalent immédiat | Retrait du seul bloc reconnu ; texte pédagogique introductif identique, instruction complète dans nouvelle cellule0 |
| Cellules pédagogiques et exécutables de chaque sujet | CONSERVÉ | Insertion d'une cellule0 ; ancien contenu dans le même ordre, sans réécriture ni exécution |
| R0 prescrit conditionnellement dans le bilan du TD0 S3 | CONSERVÉ | Aucun changement du caractère conditionnel de cette prescription |
| R0, R1 et R2 autonomes | CONSERVÉ | Titres, durées, activités et prescriptions propres inchangés ; classés TD de remédiation |
| Barèmes, correcteurs et sorties enregistrées | CONSERVÉ | Aucun changement demandé au contrat d'évaluation |

## Périmètre et exclusions explicites

Le manifeste `tutor_sessions.json` contient 21 sujets : 16 TD et 5 contrôles. Son inventaire doit couvrir tout fichier `.ipynb` des deux répertoires de supports et de `Corrigés modèles/`, soit par une séance, soit par une exclusion motivée. Tout nouveau sujet non manifesté doit faire échouer le contrôle structurel ; il ne reçoit aucune classification implicite tirée du seul chemin.

Les huit corrigés enseignants et le corrigé modèle sont exclus du rendu du tuteur : ils ne sont pas des sujets distribués pour produire une réponse. Leur contenu reste strictement intact. `Notebooks contrôles finaux/DevoirS2.ipynb` porte, malgré son chemin, le titre explicite « TD6 ... (CORRIGÉ) » et « Version Enseignant / Solution » ; il est tronqué et invalide JSON, comme `Notebooks TD/TD6_S2-corrigé.ipynb`. Les deux anomalies préexistent ; aucune fin de fichier n'est reconstruite ni aucune cellule corrigée dans ce lot.

## Réserves pédagogiques héritées

- `TD2 - S2.ipynb` est titré contrôle ; `TD4_S2.ipynb` est titré « Contrôle S3 » malgré son chemin S2. Le registre et les routes existants les classent contrôles ; ce mode strict est maintenu. Le semestre2 du registre est conservé pour TD4, sans trancher son intitulé contradictoire.
- `devoirMaisonS2.ipynb` est classé contrôle selon le contrat de route existant. Le travail à domicile n'autorise pas un tutorat implicite.
- TD3 S1 Q4 demande déjà un parcours de dictionnaire avant la séance dédiée aux boucles. Le profil autorise seulement les notions nécessaires à cette activité explicitement demandée, sans déclarer la progression validée ni la réécrire.
- Les TD3/TD5 S2 couvrent de nombreuses notions et certains exercices paraissent isolés ; les fiches décrivent leur sujet présent. Ce lot n'est pas la refonte progressive de ces séances.

## Preuves d'acceptation attendues

1. Inventaire exhaustif, classification explicite, exclusions motivées et profils sans réponses attendues.
2. Égalité exacte du contexte canonique dans le profil Colab et le corps du commentaire HTML de la cellule0 ; les métadonnées structurées restent cohérentes avec ce texte.
3. Soustraction de la cellule0 et du seul ancien rappel TD2 reconnu : restitution intégrale des anciennes cellules ; aucune modification des corrigés exclus.
4. Bibliothèques et notions bornées par exercice ; refus total en contrôle ; aucune résolution/édition/exécution par le tuteur.
5. Revue indépendante pédagogique et technique puis gouvernance. Cette matrice spécifie la conservation : elle ne s'auto-valide pas.

L'enseignant rapporte que le pilote TD2 « marche parfaitement ». C'est une observation favorable rapportée pour le pilote, sans transcription détaillée ni validation générale. Le rendu généralisé et les autres niveaux restent à essayer dans Colab ; conformité structurelle et observation du comportement sont des preuves distinctes.
