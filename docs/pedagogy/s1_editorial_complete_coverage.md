# S1 — Cadrage préalable de la reprise éditoriale complète

## Mission et références

Mission du 4 octobre 2026 : reprendre les sept TD S1 après les lots S3, sans réduction pédagogique, sans relecture enseignante systématique et sans changer le contrat v2. Auteur du cadrage : TAL-Prof. Cette matrice doit être validée indépendamment **avant conception** ; elle ne vaut ni validation des fichiers futurs ni preuve d'exécution.

Référence technique lue : `670e6c104a6d0228fcad8a91cfc8776117b038bb` (PR26 fusionnée). Référence historique Git lue et comparée : `2a36752`, fichiers `Notebooks TD/S1/TDn_S1_python_texte.ipynb`, n=1..7. Il s'agit du plus ancien état S1 disponible dans cet historique Git, déjà adapté, et non du cours original de l'enseignant. Les révisions intermédiaires `322abf5` et `b1ffd02` sont identifiées par `docs/pedagogy/s1_progression_v2_coverage.md` ; le dernier état contient leurs renforcements, eux aussi obligatoires. Les sources originales ont ensuite été retrouvées et lues intégralement (texte et code, image illustrant les ensembles non interprétée) avant validation du cadrage : le cours de 212 cellules et les six notebooks de l'archive `Revisions-20260917T155854Z-1-001.zip`. Cette seconde comparaison révèle des lacunes héritées, détaillées ci-dessous ; elle interdit d'annoncer une restauration exhaustive du cours historique. Les sources privées ne sont pas copiées dans Git.

### Preuve de lecture des sources originales

| Source | Cellules | SHA-256 |
|---|---:|---|
| Cours — Notebooks Jupyter et bases de la programmation | 212 | `3dffaaabe901e25de0938bda9e20f3841c42cde27080a0db30a642aef73c4aa6` |
| TD1 — Introduction au Python pour le TAL | 26 | `856f67ffeaa4763f97b446f46fcdc6832e0c294305acf81336c5b6997c5d718b` |
| TD2 — Listes, Dictionnaires et Boucles | 29 | `a07cc7e8d691ee1e3a0898d2a7195b9ae8694d123f0886b402ca7e805d61d9ca` |
| TD3 — Fonctions et Modularité | 24 | `76192539022f24f581a68a3181e9fa2268d86704df4fb6c9bbb6336d771cc097` |
| TD4 — Chaînes et Expressions Régulières | 32 | `765e8725c6240a31c7ef425949940d7dbccb66beedf57d19b525d74811163b08` |
| TD_Révisions | 31 | `08b60f3e4919d9b5407d0ab3777d1edf200eeb66073647c20fdc0af0a403c318` |
| DevoirS1 | 69 | `66c48bdeb6fdd08aea91f942db08c0f2c51bdf6dfc93eeb44de8baf6085eb231` |

### Comparaison historique : couverture démontrée et lacunes héritées

| Source historique | Destination / constat | Disposition de ce lot |
|---|---|---|
| TD1 historique : types, concaténation/longueur, f-string, split, bilan caractères/mots | TD1 Q1–6, TD2 Q4–5 et TD5 Q6 réinvestissent ces objectifs ; exemples distincts et davantage d'autonomie | Conserver les manipulations et préciser prise en main notebook et présentation du TAL en TD1. La concaténation peut être explicitée dans un essai existant ; aucune nouvelle question notée. |
| TD2 historique : indices, ajout/retrait, majuscules, filtre longueur, lexique/items, fréquence | TD2 Q3–4, TD3 Q1/Q3/Q4, TD4 Q1/Q2/Q6 ; données changées avant ce lot | Équivalence d'objectif et d'activité démontrée ; conserver intégralement. |
| TD3 historique : définir/appeler, carré affiché, addition retournée, traduction mot/phrase | TD5 Q1–6 et exemples encadrer/montrer ; mêmes distinctions paramètres/appels/retour, autres données | Conserver distinction print/return ; expliquer None dès première démonstration. |
| TD4 historique : search/findall/nombres/sub/dates/nettoyage | TD7 Q1/Q2/Q4/Q5 ; conventions accentuation et limites renforcées | Conserver ces objectifs et données actuelles. |
| TD4 historique Q3.2 : extraction de mots exactement deux lettres, frontières `\b` | Extraction de lettres TD7 Q3 ne couvre pas les frontières ni ce critère exact | **Lacune préexistante non restaurée par la simple révision éditoriale** ; ne pas déclarer équivalence complète. |
| TD_Révisions Q1/Q2/Q4 : normalisation, structure, fréquences | TD5 Q2/Q6, TD4 Q6 et TD7 Q6 | Conserver. |
| TD_Révisions Q3/Q5 : extraction de mots commençant par majuscule sur texte brut puis combinaison avec statistiques sur texte normalisé | Pipeline TD7 Q6 couvre composition mais pas séparation brut/normalisé ni critère capitale | **Lacune préexistante d'activité**, pas couverte par un simple exemple minuscule ; à arbitrer dans une éventuelle extension, non présentée comme livrée. |
| Cours cellules 74 : quatre paragraphes par répétition/concaténation | Concaténation TD1 présente, exercice des quatre paragraphes absent | Objectif partiellement couvert ; répétition et sa vérification non restaurées ici. |
| Cours cellules 151–160 : mois → numéro avec compteur et dictionnaire | Construction dictionnaire et boucle séparément enseignées, cette composition non demandée | **Lacune préexistante d'activité** ; non comptée dans les 45 questions conservées. |
| Cours cellules 186–187 : multiples de7 jusqu'à100, variante for en bonus | TD4 Q5 jusqu'à70 puis exercices range et pair Q4 | while, progression, condition et bornes couverts sur nouvelles données ; variante for des mêmes multiples non reprise. |
| Cours cellule195 : filtres mois bre/ier et phrase sur mois retenus | TD4 Q2/Q3/Q7, filtre longueur/appartenance puis transformation, TD1 f-string | Équivalence des opérations, sans reprise littérale du contexte mois. |
| Cours cellules207–209 : normaliser personnes, compter affiliations uniques, CSV | TD6 Q1–6 sur jeu local contrôlé | Pipeline complet conservé ; taille du jeu déjà réduite avant cette mission, aucune réduction nouvelle. |
| Cours : not/or/!=, division entière ; panorama chaînes count/find/index/swapcase/capitalize/tranche négative ; listes insert/remove/sort ; dict valeurs-listes/boucle imbriquée ; ensembles union/différence symétrique/inclusion ; elif/pass ; fichiers mode a | Catalogue d'API et démonstrations dépassant les TD actuels ; non tous enseignés dans les sept TD | Lacunes de couverture historique signalées, sans ajouter en bloc un catalogue qui changerait charge et curriculum. Ni suppression nouvelle ni prétention de restauration. |
| TD4 ancien : `startswith`, `endswith`, `\d`, `\w`, `\s`, `\b` | Opérations de bord et classes abrégées pas toutes exposées dans TD7 actuel ; correction du sens Unicode requise si réintroduites | Lacune héritée de cours, distincte de l’activité deux lettres ci-dessus. |
| DevoirS1 ancien : or/elif Q14, break Q24, strip avec argument Q4/Q25 notamment | Points évalués historiquement mais non pratiqués explicitement dans TD actuels | Dépendances à examiner lors de la reprise des contrôles ; ce lot ne valide pas l'alignement intégral de ce contrôle. |

Les erreurs anciennes ne doivent pas être restaurées : `collection` à installer, dictionnaires prétendument non ordonnés, `{}` assimilé à un ensemble vide, boucle infinie exécutable, `range(100/7)`, et extraction de capitales présentée comme entités linguistiques. Leur présence dans une source ne constitue pas une prescription. La reprise autorisée conserve toutes les activités **actuellement distribuées** ; les lacunes historiques ci-dessus sont un résultat d'audit, pas une permission implicite de supprimer quoi que ce soit. Leur remise en place complète demanderait un cadrage curriculaire supplémentaire et un budget réaliste.

| Repère | Chemin actuel sous `Notebooks TD/S1/` | Questions |
|---|---|---:|
| TD1 | `TD1_S1_variables_types.ipynb` | 6 |
| TD2 | `TD2_S1_chaines_sequences.ipynb` | 7 |
| TD3 | `TD3_S1_collections.ipynb` | 6 |
| TD4 | `TD4_S1_boucles_conditions_comptages.ipynb` | 7 |
| TD5 | `TD5_S1_fonctions_reutilisation.ipynb` | 6 |
| TD6 | `TD6_S1_fichiers_csv.ipynb` | 6 |
| TD7 | `TD7_S1_expressions_regulieres_pipeline.ipynb` | 7 |

Les 45 questions principales, traces complémentaires, données fournies, prédictions, essais personnels, justifications et synthèses sont obligatoires. Aucun déplacement hors support ni passage en option. Chaque ligne suivante signifie `CONSERVÉ` pour objectif, activité, données et autonomie ; `RENFORCÉ` pour lisibilité. Les exemples restent distincts des données évaluées. Durées par question conservées comme hypothèses, non comme mesures en classe.

## Matrice par question : source, acquis, production et cible

Pour chaque Q, la référence historique est le même numéro dans le fichier ancien indiqué ci-dessus ; la référence technique est ce numéro dans le fichier actuel. Les éléments ajoutés depuis l'historique (traces a/b, essais et exemples) sont inclus dans la conservation. Aucun code solution des questions n'est fourni par cette révision.

| Question / minutes | Objectif, données et production conservés | Acquis antérieurs ; apport avant l'exercice | Lacune rédactionnelle / cible vérifiable |
|---|---|---|---|
| TD1 Q1 / 15 | Prix 0.12, 125 mots ; calcul de `cout_total` | Débutant ; affectation, multiplication, affichage | Consigne seulement en commentaire : créer un véritable énoncé, conserver exemple cahiers et essai de recalcul. |
| TD1 Q2 / 12 | `note=14.5` ; afficher son type | Q1 ; int/float/str/bool, `type` | Énoncé explicite hors code ; conserver prédiction 6/6.0/"6" et choix du type d'un titre. |
| TD1 Q3 / 18 | `meme_nombre`, `commande_importante` sur données Q1 | Q1–2 ; comparaisons, `and` | Nommer données réutilisées ; séparer cours de prédiction ; garder essais places=18 et inscrits=18/19. |
| TD1 Q4 / 17 | Français→anglais, phrase exacte par f-string | Chaînes ; interpolation | Distinguer phrase attendue et syntaxe à construire ; annonce atelier/salle et variation conservées. |
| TD1 Q5 / 18 | Convertir "80", ajouter 20, `volume_corrige` et type | Calcul/type ; `int` | Séparer explication chaîne/nombre, exemple et consigne ; garder essai "42" +3. |
| TD1 Q6 / 22 | Phrase personnelle ; longueur, présence de TAL, Q6b source | Chaînes ; `len`, `in`, casse, `repr` | Expliquer le rôle pratique de l'affichage sans jargon du correcteur ; conserver comparaison TAL/tal. |
| TD2 Q1 / 14 | `texte_brut` inchangé, `texte_propre`, Q1b longueurs, explication | TD1 ; immuabilité, `strip` | Scinder cours/exemple/prédiction/énoncé ; rendre l'exemple Atelier exécutable et garder toutes observations. |
| TD2 Q2 / 16 | Minuscules puis textes→corpus ; Q2b booléens, contrôle source et justification ordre | Q1, `in` TD1 ; `lower`, `replace` | Isoler cours et consigne ; exemple LIVRE exécuté ; ne pas supprimer nuance ordre non indispensable sur données précises. |
| TD2 Q3 / 17 | `tokenisation`, premier/dernier/debut/milieu ; Q3b longueur et source | Chaînes ; indices négatifs, tranches | Exemple archive exécutable ; conserver indices sur brouillon et explication borne exclue. |
| TD2 Q4 / 15 | Phrase donnée, `tokens`, troisième/dernier, Q4b longueur, types et interprétation | Indices ; liste minimale, `split` | Définir clairement caractère/élément ; garder espaces multiples et comparaisons type/longueur. |
| TD2 Q5 / 12 | `phrase_avec_barres`, `tokens_reconstruits`, égalité Q5b | Q4 ; `join`, séparateur exact | Exemple palette exécutable ; garder prédiction nombre séparateurs et explication espaces autour barre. |
| TD2 Q6 / 18 | Trois chaînes données traitées par indices, nouvelle liste, Q6b original | Q1–5 ; liste littérale | Exercice autonome sans boucle ; préserver comparaison accents/espaces/source. |
| TD2 Q7 / 14 | "L’analyse, c’est utile !", tokens Q7b et commentaire Q7 | `split` et observations Q4 | Distinguer tâche d'analyse et vérification ; critères personnels ponctuation/apostrophe, sans promesse de relecture. |
| TD3 Q1 / 16 | Outils, append tokeniseur, état Q1a puis pop et Q1 final | Listes TD2 ; mutation append/pop | Énoncé hors code ; clarifier chronologie affichages ; conserver essai trois villes. |
| TD3 Q2 / 15 | Tuple français/italien/espagnol, type, justification et Q2b | Listes ; tuple stable | Distinguer définition de l'argumentation ; conserver tuple codes et choix liste/tuple. |
| TD3 Q3 / 18 | Lexique book/language/data puis corpus, traduction et Q3b lexique | Chaînes ; clés/valeurs, ajout | Rassembler les traductions prescrites et consigne ; garder exemple couleurs, essai animaux et réaffectation clé. |
| TD3 Q4 / 25 | `lexique.items()` → liste `anglais -> français` | Q1 et Q3 ; premier for, indentation, déballage | Explication complète avant parcours ; ne pas supposer TD4 déjà fait ; garder exemple couleurs et essai animaux. |
| TD3 Q5 / 14 | Six formes répétées → ensemble, deux comptes et Q5b | Listes ; set, occurrences/formes | Séparer cours et travail ; garder essai poésie, casse Roman/roman et interprétation fréquences perdues. |
| TD3 Q6 / 14 | Deux corpus donnés → communs/seulement_a | Q5 ; intersection/différence | Clarifier sens de la différence ; garder deux différences dans essai langues et interprétation. |
| TD4 Q1 / 13 | Liste TAL/corpus/analyse/IA → `majuscules` par for | TD3 boucle/liste, TD2 upper | Consigne hors commentaire ; conserver états intermédiaires et essai villes, initialisation hors boucle. |
| TD4 Q2 / 14 | `mots_longs`, longueur strictement >5 | Q1 ; if et indentation imbriquée | Préciser liste source ; garder filtre distinct <=3 et cas limite 5. |
| TD4 Q3 / 12 | `mots_avec_a`, casse ignorée mais formes originales | Q2 ; appartenance après lower | Séparer normalisation du test et valeur conservée ; garder différence e/é et essai o. |
| TD4 Q4 / 15 | `positions_paires` de 0 à 10 inclus avec range | Listes/boucles ; bornes, pas, modulo | Garder cours modulo, pas négatif, essais 8..2 et 5..1, parité 8/9/10 ; aucune notion implicite. |
| TD4 Q5 / 20 | Multiples de7 ≤70 par while, départ7 | Conditions ; while, mise à jour/arrêt | Séparer règles et consigne ; conserver première valeur rejetée et essai 2/4/6/8 sans exécuter boucle infinie. |
| TD4 Q6 / 17 | Texte fourni lower/split → fréquences | Dictionnaires, parcours ; get ou if/else | Garder deux exemples alternatifs et suivi oui/non ; énoncé distinct des explications d'accumulation. |
| TD4 Q7 / 11 | Compréhension des longueurs des mots >5 | Q2/Q6 ; compréhension | Expliciter sortie longueur, pas mot ; conserver essai carrés et comparaison boucle/compréhension. |
| TD5 Q1 / 16 | `longueur_texte`, tests TAL/corpus et vide | TD1 len ; def, paramètre, appel, return vs print | Expliciter None de l'exemple montrer ; placer test vide après définition, conserver essai annoncer. |
| TD5 Q2 / 14 | `normaliser` strip/lower, espaces de bord | TD2 chaînes ; fonction Q1 | Distinguer exemple séparé et composition demandée ; test vide/espaces après définition. |
| TD5 Q3 / 16 | `nombre_mots` réutilise normaliser puis split | Q1–2 ; composition, paramètre par défaut | Retirer note destinée au concepteur sur préparation contrôle ; conserver enseignement défaut et essai saluer. |
| TD5 Q4 / 18 | Traduire un mot via lexique paramètre, inconnu normalisé | Dictionnaires/tests ; normalisation de clé | Déplacer règles Q4 vers énoncé ; tests BOOK/Mystery/vide après définition ; aucune variable globale requise. |
| TD5 Q5 / 20 | `traduire_phrase`, phrase Language data, appel traduction puis join | TD4 boucle, TD2 join, Q4 | Distinguer explication et exigence réemploi ; conserver tests inconnu/espaces/vide après définition. |
| TD5 Q6 / 18 | `resume_texte` : texte_normalise, nb_caracteres, nb_mots | Q1–5 ; dictionnaire de résultats | Noms et sens des champs dans énoncé ; caractères normalisés ; tests ARCHIVE ORALE/vide après définition. |
| TD6 Q1 / 15 | affiliations_s1.txt fourni → texte et longueur | Chaînes ; with/open/read/UTF-8 | Chemin explicite ; préparation Path fournie, pas acquis implicite ; garder lecture distincte atelier. |
| TD6 Q2 / 13 | Lignes utiles du texte, ordre conservé, nombre | TD4 filtre ; splitlines | Clarifier vides/espaces ; garder essai avec ligne blanche et espaces. |
| TD6 Q3 / 17 | Couples identité/affiliation par split(';',1), premier et Q3b complet | Listes/boucles ; maxsplit | Clarifier liste ordonnée de couples de deux chaînes, chaque couple pouvant être liste ou tuple ; exemple avec plusieurs points-virgules et retrait des bords conservés. |
| TD6 Q4 / 17 | `normaliser_personne`, graphies Durand Alice et Q4b | TD5 fonction, split/join ; title | Énoncé précise espaces intérieurs et bords ; garder limite identité/graphie et essai Lamy Zoé. |
| TD6 Q5 / 18 | Dictionnaire personne normalisée→set affiliations ; Q5b complet | TD3 sets/dict, Q4 ; add | Critères ordre indifférent et contenu complet ; préserver essai Studio doublé et vérification chaque personne. |
| TD6 Q6 / 22 | CSV UTF-8, 3 colonnes, une ligne/personne, affiliations jointes, relecture repr | Q1–5 ; csv.writer/writerow/newline/en-tête | Présenter module csv avant exemple ; consigne autonome complète ; afficher clairement unique ligne Q6 à activer, enlever jargon v2. |
| TD7 Q1 / 12 | TAL insensible casse → booléen | Chaînes ; module re, raw string, search, None, bool, flags | Véritable introduction bibliothèque avant manipulations ; garder match/search, point littéral et essai archive/absence. |
| TD7 Q2 / 13 | Séquences chiffres de texte_nombres → liste | Q1 ; classes, +, findall | Clarifier chaînes non nombres ; garder essai Lot7/36 et absence. |
| TD7 Q3 / 18 | Lettres accentuées dans texte_mots et comparaison split | Q2 ; classe étendue | Consignes distinctes du cours ; garder casse/ordre, essai île/apostrophe et convention non universelle. |
| TD7 Q4 / 14 | Journal : JJ/MM/AAAA → [DATE] | Q2 ; sub, quantités exactes | Garder distinction forme/calendrier et exemples identifiants ; test complet/incomplet après construction motif. |
| TD7 Q5 / 20 | Fonction nettoyage : lower, dates, chiffres, espaces ; résultat | TD5 fonction ; composition transformations | Retirer langage contrat du cours ; mettre étapes/casse DATE/ponctuation dans énoncé ; tests vide/espaces/date après définition. |
| TD7 Q6 / 16 | Fonction analyse → texte_nettoye, mots, frequences | TD4 comptes et Q5 ; composition | Séparer rappel compte et production attendue ; garder somme effectifs, test vide/transfert et conséquence DATE. |
| TD7 Q7 / 9 | `limite_regex` : situation française + information linguistique manquante | Q1–6 ; distinction forme/sens et * vs + | Garder exemple occurrences vides et essai a5b ; critères d'autoévaluation explicites, pas validation sémantique annoncée. |

## Prescriptions transversales de conception

- Les introductions, exemples, essais, synthèses et commentaires visibles parlent à l'étudiant. Retirer notamment « cellules contenant les preuves du correcteur », justifications de version et références à la conservation des exercices. Remplacer les promesses de relecture par des critères pour comparer son propre travail et signaler une difficulté.
- Les cours exposent une notion ; les exemples fournis sont exécutables et leur résultat est interprétable ; les essais et énoncés annoncent action/données/production. Ne pas dissimuler une consigne de Q dans un paragraphe théorique. Les prédictions doivent être formulées avant exécution. Les tests demandant une fonction encore inexistante vont après la réponse correspondante ou dans une cellule clairement différée, sans casser l'exécution du notebook complété.
- Préserver intégralement les essais renforcés, y compris modulo TD4, paramètre par défaut TD5, chaînes vides, variantes de casse et espaces. Les rendre facultatifs pour gagner du temps serait une réduction interdite.
- Double tuteur identique dans commentaire HTML initial et `metadata.colab.aiContexts`, configuration `metadata.tal_tutor` conservée et synchronisée. S1 : guidage sans code solution. Chaque permission doit correspondre à une explication déjà rencontrée. Bibliothèques : aucune TD1–5 ; TD6 Path fourni, csv introduit Q6 ; re introduit TD7. IPython/html de restitution restent infrastructure, pas notions à employer dans les réponses.
- Métadonnées de toutes cellules, identifiants answer Q, versions v2, données et affichages évalués restent inchangés. Les cellules exemples ne deviennent pas des réponses et n'affichent pas les marqueurs notés. Pas de nouveau correcteur sans défaut constaté : les sept correcteurs actifs existent déjà.
- Restitution HTML finale conservée avec séparateur visuel et adresse injectée au déploiement. La notice étudiant décrit exécuter/enregistrer/déposer et le rôle du retour automatique. Elle ne promet aucune relecture individuelle.
- Pour les explications libres (TD2 Q7, TD3 Q2, TD7 Q3/Q7 notamment), distinguer contrôle automatique de présence/structure et appréciation du sens. Donner des critères vérifiables par l'étudiant ; ne pas transformer longueur ou mots-clés en validation linguistique.

## Charge, périmètre et acceptation

Chaque support conserve sa cible de deux heures. Les temps existants couvrent exemples, essais et exercices : TD1 et TD3–7 8+102+10 minutes ; TD2 8+106+6. La capacité réelle à terminer n'a pas été mesurée : aucune certitude de faisabilité ne sera déduite d'une somme de durées. Les exemples rendus exécutables remplacent leurs blocs Markdown correspondants et n'ajoutent pas de travail redondant.

Ce lot couvre les **sept TD S1** demandés. Les contrôles et DM associés restent recensés dans l'inventaire global ; ils ne sont pas déclarés révisés dans ce lot. Leurs notions ne doivent pas régresser par modification des TD. Aucun changement de barème, de route ou de contrat n'est prévu. Toute incompatibilité découverte doit être signalée et suivre le flux mixte.

Critères d'acceptation : vérification exhaustive des 45 lignes et essais ; lecture éditoriale de toutes cellules visibles ; lecture Étudiant-Modèle limitée aux sujets ; double tuteur/séquençage validés ; exemples exécutés ; compatibilité avec correcteurs et distribution ; revues pédagogique et éditoriale indépendantes. Les résultats de réalisation seront consignés séparément, avec limites non vérifiées.

## Validation préalable

Statut : **ACCEPT_SUR_PÉRIMÈTRE_COURANT**, avis indépendant TAL-Pedagogy-Reviewer du 4 octobre 2026, avant conception. Les 45 questions et tous les essais/acquis actuels restent obligatoires. La couverture de l’intégralité des originaux demeure **NON_DÉMONTRÉE**, avec les écarts ci-dessus explicitement signalés. Cette acceptation autorise la conception sur le périmètre actuel ; elle ne valide pas encore les supports réalisés. Aucun notebook modifié par TAL-Prof.


## Bilan de réalisation et preuves finales — 4 octobre 2026

Le lot réalisé conserve les **45 questions principales et tous les essais** des sept TD actuellement distribués. Le verdict pédagogique indépendant est **ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE** sur ce périmètre. La lecture éditoriale indépendante de toutes les cellules visibles conclut **ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE** : voir `reports/editorial/s1-editorial-complete.md`. La lecture Étudiant-Modèle, question par question, est favorable dans `Corrigés modèles/TD/s1-editorial-complete/lecture_etudiante.md` ; cette lecture n'est pas une copie résolue ni une exécution des réponses.

| Élément réalisé | Preuve concrète |
|---|---|
| TD1 — entrée dans le travail | Présentation du TAL et prise en main du notebook ; Q1/Q2 disposent désormais d'un énoncé distinct ; Q4 nomme `phrase_presentation`. Six questions et six groupes d'exemples/essais conservés. |
| TD2 — cours et manipulations | Six cellules exécutables `s1-editorial-td2-exemple-q1` à `q6` remplacent les exemples Markdown ; les observations, prédictions, explications et traces complémentaires restent demandées. Q7 reste autonome. |
| TD3 — choix des collections et parcours | Q1 sépare ajout, affichage intermédiaire et retrait ; Q3 explicite les traductions admises ; Q4 enseigne `for`, l'indentation et le déballage avant le parcours. Six groupes d'entraînement conservés. |
| TD4 — boucle, condition et accumulation | Q1 possède un énoncé ; Q2/Q3 identifient `mots` ; Q7 distingue critère >5 et longueur retournée. Modulo, parcours inverses, arrêt while, deux méthodes de comptage et compréhension sont conservés. |
| TD5 — fonctions | `None` est expliqué avant le premier exemple et autorisé dans le double tuteur de Q1. Paramètre par défaut, composition, cas vides et inconnus conservés. Les vérifications Q1–Q6 suivent maintenant les définitions étudiantes. |
| TD6 — fichiers et CSV | Structure des couples explicitée (liste ou tuple), `set`/`add` expliqués avant regroupement, `join` sur affiliations expliqué avant CSV ; un seul affichage Q6 à activer. Vérifications Q4/Q5 après réponses. |
| TD7 — bibliothèque re et pipeline | Introduction du module avant emploi ; convention des suites de lettres explicite ; ordre du nettoyage, marqueur DATE et critères d'interprétation clarifiés. Vérifications Q4/Q5/Q6 après réponses. |
| Ordre d'exécution corrigé | Onze cellules `tdN-s1-verification-qK` placées après leur réponse : TD5 Q1–Q6, TD6 Q4–Q5, TD7 Q4–Q6. Aucun essai dépendant d'une fonction future ne doit être exécuté avant sa définition. |
| Destinataire et charge enseignante | Notes de fabrication retirées, consignes et connaissances distinguées ; autoévaluation explicite sans promesse de relecture individuelle. Les explications restent obligatoires, leur sens n'est pas certifié par le score technique. |
| Métadonnées et restitution | Tuteurs synchronisés dans les deux emplacements, version v2 et identifiants de questions conservés ; restitution HTML avec séparateur et adresse injectée. |

**TAL-PED-S1-01 — résolu.** Des consignes « après Q » restaient physiquement avant la définition de la fonction et pouvaient provoquer une `NameError` lors d’une réexécution depuis une session vide, une fois les cellules remplies. Le déplacement des seuls essais concernés dans les onze nouvelles cellules `practice` après réponse, avec renvois depuis les anciennes cellules conservées, résout cette incohérence. La revue pédagogique indépendante a contrôlé leur position réelle et clôturé le constat.

### Empreintes des supports relus

Les empreintes suivantes concordent avec le rapport éditorial final et ancrent les verdicts à ces fichiers. Les 293 cellules finales sont relues, et pas seulement les 45 cellules de réponse.

| Notebook sous `Notebooks TD/S1/` | Cellules | SHA-256 |
|---|---:|---|
| `TD1_S1_variables_types.ipynb` | 38 | `d842f8962bfbc754296345ccc4ba191db97b27253d033f725e754a53259f7acf` |
| `TD2_S1_chaines_sequences.ipynb` | 33 | `17e0ba28fc732b26270d62018b4e48d4a04e005d042329819534549ac09c78bd` |
| `TD3_S1_collections.ipynb` | 39 | `e01e6ed9ae0c7db5158e3397ef9c4091964b4ad1c0072e7f91c9e700d83ce1a7` |
| `TD4_S1_boucles_conditions_comptages.ipynb` | 44 | `71298b908b755cd2db81c2585fca4f9ecdcd1b7366161a80c845b3abc20a1f6d` |
| `TD5_S1_fonctions_reutilisation.ipynb` | 46 | `38aa2dfd789abe9e7aef7280d71f9bba716430105e3b5043742122fcdd14cf89` |
| `TD6_S1_fichiers_csv.ipynb` | 43 | `85fbce645000e443ff378b94fdd9e3653bc7f98feaacca1b8c06bcb30773c50d` |
| `TD7_S1_expressions_regulieres_pipeline.ipynb` | 50 | `04fe8873b656a41e1b87468ea252d576309314443bc260fa869cd98cdef4024f` |

### Vérifications rapportées par l'intégration

L'intégration a exécuté les 44 exemples et les deux préparations fournies ; validation nbformat et syntaxe Python des sept notebooks ; contrôle des 35 profils de tutorat ; génération et vérification des 34 supports distribuables. Ces résultats concernent les exemples fournis et la cohérence technique : ils ne prouvent ni que les réponses des étudiants sont correctes, ni que tous terminent en deux heures, ni que Colab applique effectivement le tuteur. La revue technique des correcteurs est distincte dans `docs/s1_editorial_correctors.md`.

### Limites et statut du suivi

Les sept TD S1 passent à **REVU**, pas les contrôles, DM, corrigés ou archives. La conservation démontrée porte sur les TD actuels et leurs essais ; la couverture exhaustive des sources originales 2025 demeure **NON_DÉMONTRÉE**. Les écarts détaillés en début de matrice ne sont ni supprimés tacitement du programme historique ni présentés comme restaurés. Toute remise en place de leurs activités substantielles nécessite un cadrage de progression et de charge distinct. Le temps réel des séances, notamment TD3 Q4, TD6 Q5–Q6 et TD7 Q5–Q6, reste à observer en classe.
