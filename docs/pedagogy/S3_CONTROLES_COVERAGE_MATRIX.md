# S3 — Matrice TD → contrôles cumulatifs

## Cadrage avant conception

**Demande enseignante :** un ensemble de contrôles consistants, centré sur le TD précédent et mobilisant les acquis antérieurs, pour apprendre à les transférer à d'autres contextes ; premier contrôle après TD1. Cette série ajoute sept supports ; elle ne remplace ni ne réduit les TD0–TD7 de la progression d'audit.

**Hypothèses de conception :** sept contrôles après TD1 à TD7 ; durée prévisionnelle de 120 minutes chacun, à confirmer par observation en classe ; sept exercices avec plusieurs productions complémentaires ; au moins deux contextes nouveaux par contrôle. Les corpus sont des textes pédagogiques originaux, embarqués dans le notebook. Ils ne constituent pas des observations empiriques sur les institutions évoquées.

**Barème technique proposé :** Q1 = 2 points ; Q2 à Q7 = 3 points chacun, soit 20. Ce score automatique ne constitue pas une note globale : il est accompagné d'une grille humaine distincte. Les conventions et formes de sortie sont données ; aucune valeur résultat, solution, exemple résolu ou démarche de résolution n'est fournie. Les contrôles n'introduisent aucune compétence obligatoire nouvelle.

| Contrôle et placement | Focalisation majoritaire sur le TD précédent | Réactivation cumulative | Contextes de transfert proposés | Productions et autonomie | Statut |
|---|---|---|---|---|---|
| C1 après TD1 | TD1 Q1–Q6 : annotation forme/lemme/POS/tag/position ; phrases ; filtres ; dépendances ; split/tokenisation ; contrôle manuel | TD0 Q1–Q7 : lecture et préservation, listes, vocabulaire, fréquences par fonction, normalisation explicite | Bilans de musée ; annonces de transport ; bulletin météo | Annotation inspectable, offsets vérifiables, comparaison de segmentations, filtres et visualisation syntaxique ; application autonome du même traitement à un second texte | CONSERVÉ et réinvesti |
| C2 après TD2 | TD2 Q1–Q7 : fonctions noms/verbes puis POS paramétrable ; exclusions ; Counter/top3 ; cinq lemmes et expression ; fréquences brutes et unités ; WordCloud | TD0–TD1 : corpus, unités, phrases, filtres et contrôle linguistique | Archives d'atelier ; table annotée du port ; notices d'alimentation | Fonctions réutilisables, tableaux de fréquences brutes avec unité explicite, choix d'exclusions, figure commentée et transfert au second corpus | CONSERVÉ et réinvesti |
| C3 après TD3 | TD3 Q1–Q7 : périmètre/provenance, concordances, formes/lemmes/expressions, citations exactes et normalisées, validation, preuves | TD0–TD2 : unités, positions, fréquences et contrôle d'annotation | Veille patrimoniale ; bulletins radio | Recherche paramétrable avec positions, distinction exact/normalisé/candidat, dossier de preuves ; reprise sur un second texte et une citation nouvelle | CONSERVÉ et réinvesti |
| C4 après TD4 | TD4 Q1–Q7 : présence, marges, paire, union/somme, fenêtre, frontières, normalisation, export | TD0–TD3 : unités, fonctions, recherche et preuves | Signalements de mobilité ; archives sonores | Mesures par phrase et positions séparées ; fonctions testées sur répétition, absence et borne ; preuves et protocole, second contexte de transfert | CONSERVÉ et réinvesti |
| C5 après TD5 | TD5 Q1–Q7 : dénominateurs, association/fréquence, pour mille, condition inverse, table 2×2, zéro/indéfini, sensibilité | TD0–TD4 : annotations, comptages, cooccurrences et preuves | Médiation de musée ; alertes du littoral | Table cohérente, proportions comparables, comparaison de classements, traitement des cas limites et conclusion sur un second contexte | CONSERVÉ et réinvesti |
| C6 après TD6 | TD6 Q1–Q7 : dispersion, segments, carte de chaleur, sensibilité, retour aux passages, figures vérifiables, export | TD0–TD5 : positions, unités, cooccurrences, normalisation et interprétation conditionnelle | Bulletins d'exposition ; retours d'ateliers | Graphiques reliés aux tableaux et passages ; segments mécaniques identifiés ; comparaison d'un second corpus ; analyse des effets du dénominateur | CONSERVÉ et réinvesti |
| C7 après TD7 | TD7 Q1–Q7 : formalisation, moteur paramétrable, citations, comparaison conditionnelle, groupes/expressions, validation indépendante, rapport | TD0–TD6 : chaîne complète de mesure, preuve et représentation | Rapports synthétiques de médiathèque ; jardin partagé | Audit calculé de plusieurs affirmations et citations, protocole original distinct des reconstructions, moteur transféré au second corpus sans nombres fixes, rapport avec limites | CONSERVÉ et réinvesti |

Les contextes sont des orientations : les Designers peuvent préciser titres et situations en conservant deux corpus différents et les activités recensées. Chaque contrôle mobilise des prérequis utiles à son problème ; il ne réévalue pas artificiellement chaque exercice de tous les TD antérieurs. Les objectifs du TD focal doivent tous demeurer observables, éventuellement regroupés dans une même question.

## Charge et productions minimales

Le budget de référence est : 10 minutes de prise en main et préparation technique ; Q1 10 minutes ; Q2 15 ; Q3 15 ; Q4 15 ; Q5 15 ; Q6 15 ; Q7 20 ; sauvegarde et dépôt 5, soit 120. Les Designers peuvent réallouer les exercices, sans dépasser 120 minutes et sans reléguer une compétence obligatoire dans un prolongement. La préparation fournit corpus et imports autorisés, jamais les fonctions évaluées. La disponibilité des environnements et la vitesse de travail n'ont pas encore été observées en classe.

Chaque exercice comporte au moins deux productions liées (calcul et justification, fonction et transfert, tableau et preuve, figure et interprétation). Les deux derniers exercices permettent le transfert et l'intégration ; ils ne doivent pas répéter simplement les données et paramètres déjà traités. Les blocs de réponse restent vierges ; une reprise des fonctions déjà écrites en TD peut être explicitement autorisée, mais aucune fonction solution n'est embarquée.

## Acquis facultatifs et limites

- Le TD2 illustre le pour-mille dans un exemple sans exercice autonome associé. Le C2 conserve les fréquences brutes et explicite les unités ; le calcul normalisé devient obligatoire au C5 après pratique au TD5.
- Au C5, les taux de sections et le taux global mobilisent les dénominateurs travaillés au TD5. La comparaison avec la moyenne arithmétique des taux segmentaires reste au C6, après TD6 Q7 ; elle ne doit pas être exigée au C5.
- La PMI et la recherche approchée par `difflib`, facultatives dans les TD, ne sont pas nécessaires pour obtenir les 20 points techniques ou achever les activités obligatoires.
- Le modèle spaCy et sa version sont fournis ; sa sortie n'est pas une vérité linguistique. Les offsets et invariants peuvent être vérifiés automatiquement, l'acceptabilité de l'annotation est relue humainement.
- Aucune pandas, NumPy, seaborn, API LLM ou bibliothèque nouvelle n'est imposée. Les seuls modules de préparation non évalués sont clairement signalés.
- Les contours exacts des types et champs JSON sont finalisés avec le Code-Architect et les Designers avant écriture des validateurs. Ce changement du contrat d'évaluation exige les deux revues indépendantes.

## Critères de revue

Le réviseur pédagogique doit vérifier la couverture effective de chaque ligne dans les sept notebooks ; la présence de deux vrais contextes et d'une fonction réutilisée ; l'absence de résultats attendus et de guidage algorithmique ; la charge ; le caractère strictement cumulatif des notions ; la séparation score technique/relecture scientifique ; le refus d'aide du tuteur dans les métadonnées et la toute première cellule Markdown. Le présent document est une spécification de producteur, pas une validation indépendante.

**Revue indépendante préalable :** le TAL-Pedagogy-Reviewer a accepté cette matrice avant conception, avec le verdict `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` limité au cadrage. La conformité des réalisations reste soumise à la revue des notebooks. Vigilances transmises : pas de Counter dans C1, pas de table 2×2/association dans C4, pas de fonction solution fournie et séparation des évaluations technique et humaine.

## Repérage des activités réalisées

Cette table documente les correspondances repérées par le Prof dans les supports ; elle ne remplace pas le verdict de la revue indépendante.

| Compétences sources | Activités du contrôle |
|---|---|
| TD0 Q1–Q6 : lire, préserver, découper, dénombrer, fréquences et minuscules ; TD0 Q7 : limites | C1 Q1 : source du musée, fonction de fréquences et discussion des unités ; reprise C1 Q6–Q7 sur transport et météo |
| TD1 Q1 : forme/lemme/POS/tag/position, contrôle manuel | C1 Q2 : tableau complet et cinq annotations relues ; C1 Q7 : contrôle météo |
| TD1 Q2 : phrases et longueurs | C1 Q3 : phrases, positions, tokens et cas personnel d'abréviation |
| TD1 Q3 : filtres noms/verbes/contenu | C1 Q4 : trois listes et justification des objets retenus |
| TD1 Q4 : dépendances et lecture displaCy | C1 Q5 : figure, tête/dépendant et interprétation de la relation |
| TD1 Q5 : split/tokenisation ; Q6 : texte nouveau et preuves | C1 Q6 : annonce de transport ; Q7 : fonction de diagnostic sur trois corpus et chaîne vide |
| TD2 Q1 : corpus et annotations ; Q5 : cinq lemmes contrôlés | C2 Q1 : lecture et annotation du journal d'atelier, cinq contrôles manuels |
| TD2 Q2 : fonctions spécialisées ; Q3 : exclusions | C2 Q2–Q3 : noms/verbes puis exclusion motivée, invariants de comptage |
| TD2 Q4 : fréquences grammaticales et top3 | C2 Q4 : bilan grammatical et classement |
| TD2 Q5 : objet expression ; Q7 : généralisation | C2 Q5 : entrée annotée indépendante (port) ; Q7 : fonction paramétrable appliquée à l'alimentation, distinction expression/lemmes, essai vide |
| TD2 Q6 : WordCloud et lecture critique | C2 Q6 : nuage et barres fondés sur les mêmes valeurs, hypothèse et vérification à proposer |
| TD3 Q1 : périmètre et provenance | C3 Q1 : fiche de corpus et conventions de vérification |
| TD3 Q2 : concordances exactes ; Q3 : objets recherchés | C3 Q2–Q3 : indices/contextes ; fragment, forme, lemme et expression contiguë |
| TD3 Q4 : exactitude des citations ; Q5 : altération | C3 Q4–Q5 : citations P1–P4 exactes puis normalisées, candidats dans le texte original |
| TD3 Q6 : validation manuelle et proximité/conformité | C3 Q6 : quatre cas indépendants, prédictions et comparaison, entrée invalide |
| TD3 Q7 : dossier de preuves et transfert | C3 Q7 : bulletin radio, nouvelles citations, passages et rapport documentaire |
| TD4 Q1 : présences/marges ; Q2 : cooccurrence par contexte ; Q3 : union/somme | C4 Q1–Q3 : fiches de mobilité, fréquences et présences distinguées, indices preuves, deux agrégations |
| TD4 Q4 : fenêtres ; Q5 : frontières | C4 Q4–Q5 : flux complet avec borne incluse, distinction paires/fiches ; regroupement en dossiers et segmentation spaCy |
| TD4 Q6 : formes/lemmes/expressions ; Q7 : preuves/export | C4 Q6 : relevé manuel et expression contiguë ; Q7 : transfert aux archives sonores, preuve textuelle et export |
| TD5 Q1 : dénominateurs ; Q4 : condition inverse et table 2×2 | C5 Q1–Q2 : corpus complet de médiation, deux marges, deux proportions, tableau et preuves |
| TD5 Q2 : fréquence/association ; Q3 : tailles et pour mille | C5 Q3–Q4 : deux associés comparés à leur base ; tailles des sections et taux explicites |
| TD5 Q5 : zéros/indéfinis/faibles effectifs ; Q6 : sensibilité | C5 Q5–Q6 : pivot absent, absence conjointe, petit dénominateur ; couverture des pivots par fenêtre et distinction du nombre de paires |
| TD5 Q7 : conclusion et export ; réinvestissement TD1/TD3 | C5 Q7 : application aux bulletins du littoral, table/proportions, annotation, passage de réserve et export |
| TD6 Q1 : dispersion ; Q2 : segments | C6 Q1–Q2 : exposition, positions relatives, figure, bornes et couverture sans chevauchement |
| TD6 Q3 : carte de chaleur ; Q4 : sensibilité | C6 Q3–Q4 : effectifs/dénominateurs/taux par segment ; deux courbes de fenêtres et distinction d'une couverture |
| TD6 Q5 : retour au texte ; Q6 : figure vérifiable | C6 Q5–Q6 : annotations relues et concordances originales ; matrice de présences par fiche avec preuves, unité et diagonale déclarée |
| TD6 Q7 : interprétation/export/moyenne pondérée | C6 Q7 : transfert aux retours d'ateliers, trois segments, taux global et moyenne des taux, figures, textes et export |
| TD7 Q1 : formaliser ; Q2 : moteur commun | C7 Q1–Q2 : quatre annonces simulées de médiathèque, paramètres manquants, moteur paramétrable et preuves |
| TD7 Q3 : citations ; Q4 : comparer sous protocole | C7 Q3–Q4 : trois citations exactes/normalisées ; comparaison conditionnelle des intervalles et statut original séparé du recomptage |
| TD7 Q5 : groupes/expressions et visualisation | C7 Q5 : union/somme, expression contiguë/mots dispersés, singulier/groupe déclaré, matrice et phrase preuve |
| TD7 Q6 : cas indépendant | C7 Q6 : jardin partagé, référence manuelle, réemploi sans changement interne, vide et pivot absent |
| TD7 Q7 : dossier argumenté et export | C7 Q7 : audit de trois nouvelles annonces du jardin, citation, export des sept annonces originales et rapport intégré |
