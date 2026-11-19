# Contrôle final S1 — Périmètre TD1 à TD5

## Mandat et décision enseignante

Le 19 novembre 2026, l'enseignant indique ne pas pouvoir dépasser le TD6 et demande un contrôle fondé sur les TD1 à TD5 et le DM. Après présentation de quatre substitutions et des incohérences sujet–correcteur, il demande : « OK Applique ces corrections ». Cette décision autorise les substitutions Q5, Q24, Q25 et Q30, ainsi que l'alignement des consignes et du correcteur. Aucune question à explication rédigée ni correction humaine supplémentaire n'est ajoutée.

La présente matrice est établie avant l'adaptation. La décision vise les objectifs de remplacement présentés dans la conversation ; elle ne prétend pas maintenir les notions écartées du nouveau contrôle. Les objectifs supprimés sont explicitement listés ci-dessous. L'enseignant conserve la décision de fusion et de mise en production.

## Sources et statuts

- Référence historique disponible : `Notebooks contrôles finaux/DevoirS1.ipynb` et `DevoirS1_TILT_corrigé.ipynb`, révision Git `2445c9e18357dc6a99a8e516bf0d7bd7e462fd42`.
- Version technique actuelle : même sujet, contrat `Controletilt-s1`, version 1 ; `app/app_correction_controle_S1.py` et entrée du registre `app/routes.py` à la même révision.
- Ressources autorisées pour cette adaptation : cahiers actuels `Notebooks TD/S1/S1_TD1*` à `S1_TD5*`, dont variantes A/B/C, et `Notebooks contrôles finaux/S1/DM_intermediaire_S1.ipynb`. Le DM guidé reprend les mêmes questions et données ; il n'est pas un second contrôle final.
- Cible de la révision pédagogique initiale : même chemin de sujet et même identifiant d'évaluateur, contrat version 2. Depuis le rangement approuvé le 19 novembre 2026, le sujet courant se trouve dans `Notebooks contrôles finaux/S1/Controle_final_S1_python.ipynb` ; ce reclassement conserve toutes les cellules et le contrat v2. Les identifiants de cellules et les marqueurs `Résultat Qn :` restent stables. Les sorties, les variables de Q5 et les attendus ci-dessous changent explicitement.

Les poids effectivement appliqués auparavant sont conservés : Q1–Q25, 1 point chacune ; Q26–Q30, 2 points chacune ; identification, 1 point. Le total cohérent est donc **36 points**, dont 35 de questions. La valeur 35 annoncée auparavant comme maximum global était incohérente avec ces poids ; aucun point de question n'est retiré.

## Matrice source → cible

Toutes les activités sont obligatoires. Il s'agit d'un contrôle autonome sans aide du tuteur, sans cours nouveau ni bibliothèque à découvrir. Les données sont fournies dans chaque cellule. L'autonomie du contrôle est conservée : les noms de production et appels imposés ne fournissent pas l'algorithme.

| Question / cellule | Objectif, activité et données sources | Statut et cible | Acquis et production cible |
|---|---|---|---|
| Q1 / Q1_code | Convertir un volume saisi et calculer le coût de 3 000 mots | CONSERVÉ | TD1 conversion et multiplication ; montant 150.0 |
| Q2 / Q2_code | Choisir les indices du mot extraction | CONSERVÉ, nom de variable clarifié | TD2 indices et tranches ; bornes et chaîne extraite |
| Q3 / Q3_code | Réparer la syntaxe d'un if | CONSERVÉ, comparaison fournie alignée | TD1/TD4 comparaison et condition ; booléen True |
| Q4 / Q4_code | Nettoyer Terminologie sans changer sa casse | CONSERVÉ, casse de référence alignée | TD2 strip/replace ; chaîne Terminologie |
| Q5 / Q5_code | Interpréter la conversion bool de None | SUPPRIMÉ pour cet objectif ; remplacement validé | TD1/TD3/DM Q3 : appartenance à un tuple et places strictement positives ; booléen calculé False |
| Q6 / Q6_code | Supprimer et ajouter dans une liste d'outils | CONSERVÉ | TD3-A méthodes de liste ; liste obtenue |
| Q7 / Q7_code | Compter les mots de plus de six caractères | CONSERVÉ | TD4-A/C parcours, condition et compteur ; entier 3 |
| Q8 / Q8_code | Transformer chaque élément en majuscules | CONSERVÉ, description du défaut clarifiée | TD4-A Q1 for/upper/append ; liste de trois chaînes |
| Q9 / Q9_code | Parcourir les notes en sens inverse avec range | CONSERVÉ | TD4-B parcours inverse ; liste [15, 12, 9] |
| Q10 / Q10_code | Corriger un compte à rebours | CONSERVÉ, faux diagnostic IndexError retiré | TD4-B initialisation et progression de while ; liste [5, 4, 3, 2, 1] |
| Q11 / Q11_code | Accéder à une clé absente avec repli | CONSERVÉ | TD3-C et TD5-B Q5 ; chaîne inconnu |
| Q12 / Q12_code | Parcourir les paires d'un dictionnaire | CONSERVÉ | TD3-C items ; dictionnaire reconstruisant les effectifs |
| Q13 / Q13_code | Corriger un comptage d'occurrences | CONSERVÉ, faux diagnostic KeyError retiré | TD4-C / DM Q13 comptage par dictionnaire ; trois effectifs |
| Q14 / Q14_code | Choisir des valeurs déclenchant une branche | CONSERVÉ, résultat chaîne explicite | TD4 conditions et opérateurs logiques ; chaîne Vrai |
| Q15 / Q15_code | Filtrer les clés de longueur strictement supérieure à 3 | CONSERVÉ, référence de correction alignée | TD4-A filtre ; dictionnaire {'code': 'nom'} |
| Q16 / Q16_code | Remplacer un simple affichage par un retour | CONSERVÉ | TD5-A print/return ; salutation |
| Q17 / Q17_code | Distinguer une valeur affichée et retournée | CONSERVÉ | TD5-A print/return et multiplication ; carré 16 |
| Q18 / Q18_code | Retour conditionnel selon la longueur | CONSERVÉ, seuil rendu cohérent (au moins 6) | TD4/TD5-A ; analyse pour corpus, court sous le seuil |
| Q19 / Q19_code | Composer deux transformations de chaîne | CONSERVÉ, rôle des fonctions précisé | TD2 lower/replace et TD5-C composition ; nltk |
| Q20 / Q20_code | Retourner un dictionnaire décrivant le paramètre | CONSERVÉ, appel répété retiré | TD5-C résumé ; longueur 7 et minuscules termino |
| Q21 / Q21_code | Interpréter un paramètre par défaut | CONSERVÉ | TD5-B ; choix numéro 3 |
| Q22 / Q22_code | Ajouter une valeur par défaut | CONSERVÉ, appel aligné sur l'énoncé | TD5-B ; addition(5) produit 15 |
| Q23 / Q23_code | Suivre la transmission d'un argument | CONSERVÉ, titre précisé | TD5-A/B ; résultat numérique 10 |
| Q24 / Q24_code | Interrompre une boucle avec break | SUPPRIMÉ pour cet objectif ; remplacement validé | TD4-B / DM Q12 : produire quatre effectifs par while ; liste [4, 8, 16, 32] |
| Q25 / Q25_code | Retirer une ponctuation aux extrémités via strip(chars) | SUPPRIMÉ pour cet objectif ; remplacement validé | TD5-A Q5 / DM Q15 : normaliser_etiquette(texte), strip/lower ; trois résultats incluant chaîne vide et espaces intérieurs conservés |
| Q26 / Q26_code | Répartir les mots selon la présence de majuscules | CONSERVÉ | TD2 lower et TD4-A partition ; comparaison à la forme en minuscules possible sans méthode nouvelle |
| Q27 / Q27_code | Associer chaque mot à sa longueur | CONSERVÉ | TD3/TD4 dictionnaire et boucle ; dictionnaire des trois longueurs |
| Q28 / Q28_code | Traduire avec un lexique et un repli | CONSERVÉ | TD5-B / DM Q17 ; deux traductions avec cas inconnu |
| Q29 / Q29_code | Composer nettoyage et synthèse ; distinguer caractères et fragments | CONSERVÉ, nettoyage fourni corrigé | TD2/TD4/TD5-C ; boucle de replace fournie, faute à corriger sur la mesure ; liste nettoyée et 16 caractères de l'original |
| Q30 / Q30_code | Compter les lignes et mots d'une chaîne multiligne | SUPPRIMÉ pour cet objectif ; remplacement validé | TD4-C Q2 et TD5 : mot_le_plus_long(mots), sans max ; trois cas dont égalité et liste vide |
| Identification | Nom, prénom, classe | CONSERVÉ | Même cellule et même point |
| Sauvegarde | Télécharger le notebook avec ses sorties | CONSERVÉ | Exécuter dans l'ordre, conserver les sorties ; aucun dépôt ni envoi ajouté |

Les quatre remplacements ne déplacent pas leurs anciens objectifs vers un support futur : ils les écartent de cette évaluation conformément au périmètre validé. Les TD6 et TD7 existants restent disponibles mais ne sont pas requis pour le contrôle.

## Contrat de restitution cible

- Q2 : le correcteur lit la trace canonique déjà enregistrée et vérifie les bornes rapportées sur la chaîne de référence. Des bornes positives, négatives ou calculées équivalentes sont acceptées si elles extraient exactement `extraction`. Il ne se limite plus à extraire deux affectations littérales. Le code étudiant n’est pas exécuté.
- Q5 affiche `valeur_Q5`, booléen calculé à partir d'`inscription_possible`, sans l'ancien préfixe `Choix`.
- Q24 affiche `valeur_Q24`, liste des quatre effectifs.
- Q25 affiche `valeur_Q25`, liste des trois appels de `normaliser_etiquette`, dans l'ordre imposé.
- Q30 affiche `valeur_Q30`, liste des trois appels de `mot_le_plus_long`, dans l'ordre imposé.
- Q4, Q15 et Q22 changent d'attendu : respectivement `Terminologie`, `{'code': 'nom'}` et `15`.
- Tous les autres marqueurs, formes et poids restent inchangés. Le correcteur est à adapter dans le même lot ; une nouvelle valeur attendue ne peut être appliquée tacitement aux copies historiques version 1.
- Le tuteur de contrôle reste identique en première cellule et dans les métadonnées Colab. Ses instructions interdisent toute assistance ; ce contrôle structurel ne démontre pas le comportement de Colab.
- La source étudiante est vierge : pas de sorties ni de métadonnées d'exécution sauvegardées.

## Vérification et limites

La matrice repose sur la lecture statique des sources actuelles. Le retrait de la correction humaine n'est pas un objectif nouveau : le contrôle de référence ne demandait pas d'explications rédigées. Le correcteur lit les résultats enregistrés ; il ne prouve ni l'authenticité de ces sorties, ni la compréhension, ni la généralité des fonctions. Les trois appels de Q25 et Q30 rendent plusieurs cas vérifiables sans constituer une preuve générale.

Aucune durée n'est inventée : l'enseignant n'a pas fixé de nouvelle durée d'épreuve. La construction autonome des nouvelles fonctions peut demander davantage de temps qu'une correction d'une seule ligne ; la charge reste à apprécier en classe. Les revues pédagogique, éditoriale et technique indépendantes, l'essai Étudiant-Modèle et l'intégration sont à réaliser après adaptation ; cette spécification n'en tient pas lieu.
