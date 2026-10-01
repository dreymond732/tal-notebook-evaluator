# S1 — Réalisation de l’étayage TD5 à TD7

Branche `pedagogy/s1-progression-evaluation-v2`, référence source `322abf53` (PR19). Mission TAL-Pedagogy-Designer ; seuls les trois notebooks et ce bilan pédagogique sont produits ici. La matrice `docs/pedagogy/s1_progression_v2_coverage.md` et le contrat associé ont été lus avant conception ; validation de l’orchestrateur reçue avant la première écriture des notebooks.

## Conservation et enrichissement

Les 19 questions principales, leurs données, les consignes originales, leurs identifiants et leur ordre sont conservés. Toutes les sources pédagogiques anciennes restent des préfixes exacts de leur cellule cible. Aucun exercice n’est supprimé, abrégé ou déplacé en option. Les séances prévoient 8 minutes de démarrage, 102 minutes d’activités puis 10 minutes de synthèse et restitution. Les prédictions, essais et exemples entrent dans les temps des questions, et ne s’ajoutent pas aux deux heures annoncées ; cette durée est une hypothèse de préparation à vérifier en classe.

| Source obligatoire | Ajouts avant la question autonome | Production supplémentaire de l’étudiant |
|---|---|---|
| TD5 Q1 : fonction longueur | `def`, indentation, appel, paramètres, distinction affichage/retour, exemple encadrer/montrer | Prédiction, fonction d’annonce sur autres données, appel de longueur sur chaîne vide |
| TD5 Q2 : normaliser | Effets séparés de strip/lower et espaces intérieurs | Deux essais distincts puis cas vide et espaces seuls sur la fonction produite |
| TD5 Q3 : compter en composant | Exemple de composition et de paramètre à valeur par défaut | Fonction saluer avec appels à un/deux arguments ; tests de comptage sur vide/espaces multiples |
| TD5 Q4 : traduire un mot | Casse et appartenance au dictionnaire ; normalisation avant recherche ; paramètre plutôt que variable globale | Vérifier clé connue/inconnue ; essais avec majuscules, espaces et vide |
| TD5 Q5 : traduire une phrase | Séparateur de join et liste vide sur fragments distincts | Deux recompositions ; test inconnu, espaces multiples et phrase vide |
| TD5 Q6 : résumé | Structure dictionnaire, contrat des trois clés et longueur du texte normalisé | Résumé sur nouvelle entrée et vide, commentaire de cohérence |
| TD6 Q1 : lire le fichier fourni | Exemple distinct UTF-8 et fermeture par with ; fins de ligne | Prédire longueur et relire le fichier d’atelier sans modifier le jeu d’affiliations |
| TD6 Q2 : lignes utiles | splitlines, différence entre vide et espaces | Filtrage d’un petit texte distinct avec boucle et condition |
| TD6 Q3 : couples | Séparateur et maxsplit, conservation du second point-virgule | Découpage d’une ligne distincte, commentaire sur maxsplit ; trace Q3b complète |
| TD6 Q4 : normaliser personne | Décomposition strip/split/join/title, limites d’identification | Comparaison de trois graphies distinctes ; trace Q4b et espaces multiples |
| TD6 Q5 : affiliations | Exemple distinct de dictionnaire d’ensembles, absence d’ordre | Ajout répété d’une salle et interprétation ; trace Q5b dictionnaire complet |
| TD6 Q6 : CSV et relecture | Exemple distinct csv.writer, writerow, en-tête, UTF-8, newline et relecture | Création/relecture d’un autre CSV puis exercice original ; contrôle lignes/contenus |
| TD7 Q1 : recherche sans casse | Chaîne brute, search/match, bool/None, IGNORECASE, point échappé | Recherche distincte avec/sans casse, cas absent et prédiction |
| TD7 Q2 : nombres | Classe, +, répétition bornée, chaînes et ordre d’extraction | Autre texte numérique puis texte sans numéro |
| TD7 Q3 : lettres | Classes avec accents et convention de mot, contraste split | Essai avec î/é et apostrophe ; commentaire de la convention |
| TD7 Q4 : dates | Exemple de substitution d’identifiants ; répétitions et limite calendaire | Cas complet/incomplet distinct puis motif de date autonome |
| TD7 Q5 : nettoyage | Contrat explicite de l’ordre, maintien de DATE en majuscules ; ponctuation conservée | Prédiction de l’ordre puis tests vide, espaces multiples, nouvelle date |
| TD7 Q6 : pipeline | Accumulation sur liste distincte, cohérence des trois étapes, interprétation de DATE | Essais vide/transfert, contrôle des effectifs et commentaire méthodologique |
| TD7 Q7 : limite | Exemple de correspondances vides avec * et + ; formes versus information linguistique | Test sur a5b, préparation d’une situation et de l’information manquante |

## Contrat et restitution

Les trois racines TAL passent en v2 ; l’identité conserve ses trois affectations et ajoute `numero_etudiant`. Une notice explique l’ancienne version refusée et la portée technique provisoire du score. Chaque cellule ajoutée possède un identifiant unique et des métadonnées TAL : les exemples et essais sont distincts des `answer`. Les essais `practice` portent également un rattachement `tal_review` pour la relecture. Le bilan final recueille un test utile et une difficulté restante sans point supplémentaire.

Les réponses TD6 Q3, Q4 et Q5 reçoivent uniquement des traces complémentaires en suffixe. TD6 Q6 conserve intégralement son ancien affichage commenté ; le suffixe fourni indique de laisser celui-ci commenté et d’activer son remplacement avec `repr`, pour conserver un CSV multiligne dans une trace lisible. La relecture réelle du CSV reste obligatoire. Les clés du résumé TD5 et les séparateurs CSV TD6 sont précisés dans les nouveaux ateliers, sans fournir les solutions des questions.

Le premier tuteur est synchronisé depuis le manifeste officiel. Les règles S1 ne fournissent pas de code aux demandes étudiantes. La dernière cellule HTML de restitution reste exactement inchangée : seul le substitut `__TAL_PUBLIC_URL__` figure dans les sources. Aucun exemple ni exercice n’est exécuté dans les notebooks livrés et aucune sortie n’est préremplie.

## Vérifications du producteur et limites

- Comparaison avec le commit source : ordre et identifiants de toutes les anciennes cellules conservés ; sources pédagogiques conservées comme préfixes, identité enrichie en suffixe et première cellule tuteur gérée séparément.
- Compilation des cellules de code sans exécution : syntaxe valide ; identifiants uniques, réponses Q1..Qn uniques, quatre champs identité, version2 et dernière cellule restitution inchangée.
- TD5 passe de18 à39 cellules, TD6 de19 à40 et TD7 de21 à45. Ces ajouts segmentent exemples et essais pour la lecture, sans ajouter de questions notées.

Les exercices sont à faire par les étudiants ; les commentaires de travail et traces enregistrées ne prouvent pas une compréhension ou la généralité d’une fonction. Le parcours enrichi demande une revue pédagogique indépendante, les contrats une revue du correcteur, et la durée une observation en séance. Ce bilan décrit la réalisation et ses contrôles de production ; il ne constitue pas une validation indépendante.
