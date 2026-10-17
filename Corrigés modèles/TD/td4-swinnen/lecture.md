# Lecture et copies de référence — TD4 renforcé

Rôle : TAL-Étudiant-Modèle. Identité fictive stable : Camille Exemple, classe S1, numéro MODELE-TD4-SWINNEN-2026.

Périmètre lu : AGENTS.md, docs/agents/TAL-Étudiant-Modèle.md, TD1 et TD2 S1, TD3-one/bis/ter et les trois nouveaux TD4. Aucun correcteur, test, barème, matrice enseignant, corrigé existant ou fichier d’infrastructure n’a été consulté. Les cellules techniques incluses dans les seuls sujets ont été conservées, sans exécution.

Les attentes suivantes sont consignées avant une éventuelle exécution humaine des réponses. Les résultats indiqués sont des prédictions et calculs manuels ; ils ne sont pas des sorties observées. Les cellules d’essai et de vérification portent des variables distinctes des réponses lorsque leur modification changerait les données demandées.

Les 18 preuves de lecture sont détaillées ci-dessous. Pour chacun des trois TD4, cellules effectivement lues : 0–40 (titre, contexte tuteur fourni, introductions, identification, six cours, six exemples, douze essais/vérifications, six énoncés, six réponses et bilan), ainsi que les annexes et la restitution incluses dans le sujet. Les consignes cachées du tuteur ne sont pas prises comme un apport de cours. L’annexe de licence est conservée intégralement et n’est pas mobilisée comme prérequis de programmation.

Dans les ressources antérieures, cellules mobilisées : TD1 5–35 (variables, types, comparaisons, affichage, len, appartenance), TD2 5–30 (méthodes de chaînes, indices et découpage), TD3-one 3–32 (listes, append, for, indices et copie), TD3-bis 3–32 (tuples, déballage, parcours), TD3-ter 3–32 (dictionnaires, clés, items, affectation, ensembles). Les autres passages de ces ressources antérieures ont été parcourus pour situer leur progression ; aucune notion d’un TD5/TD6 n’est utilisée.

## TD4-one

### Q1 — Lecture préalable et preuve
- Compris : Transformer, sans écraser la source.
- Données : mots = [TAL, corpus, analyse, IA].
- Production attendue : liste majuscules, ordre et quatre occurrences conservés.
- Acquis localisés : TD3-one cellules 8–14 : append et parcours ; cours-Q1/exemple-Q1 : upper et liste résultat.
- Cellules du TD4 lues pour cette question : cours 4, exemple 5, essai 6, énoncé 7, réponse 8, vérification 9 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : [TAL, CORPUS, ANALYSE, IA] ; essai sur trois villes et liste vide ; source réaffichée.

### Q2 — Lecture préalable et preuve
- Compris : Filtrer strictement au-delà de 5.
- Données : mots repris de Q1.
- Production attendue : mots_longs ; test effectif de la longueur 5 hors réponse.
- Acquis localisés : TD1 cours des comparaisons ; cours-Q2/exemple-Q2 : if imbriqué dans for ; TD3-one : len.
- Cellules du TD4 lues pour cette question : cours 10, exemple 11, essai 12, énoncé 13, réponse 14, vérification 15 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : [corpus, analyse] ; abcde est exclu, abcdef retenu ; [] donne [].

### Q3 — Lecture préalable et preuve
- Compris : Tester a sans casse, conserver la graphie.
- Données : mots repris de Q1.
- Production attendue : mots_avec_a avec chaînes initiales dans leur ordre.
- Acquis localisés : TD2 étape 2 : lower ; TD1 appartenance ; cours-Q3/exemple-Q3 : valeur testée distincte de valeur ajoutée.
- Cellules du TD4 lues pour cette question : cours 16, exemple 17, essai 18, énoncé 19, réponse 20, vérification 21 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : [TAL, analyse, IA] ; [A,a,à,vide] ne garde que A et a ; la source est réaffichée.

### Q4 — Lecture préalable et preuve
- Compris : Décider trois présences sans compter.
- Données : Revue, ÉTÉ, chaîne vide.
- Production attendue : trois booléens, dans l’ordre revue/été/vide.
- Acquis localisés : TD1 in ; TD2 lower ; cours-Q4/exemple-Q4 : présence, casse, accent et if/else.
- Cellules du TD4 lues pour cette question : cours 22, exemple 23, essai 24, énoncé 25, réponse 26, vérification 27 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : True/False/False ; mère contient un e final, ÉTÉ seulement des é ; eeee donne True sans compter 4.

### Q5 — Lecture préalable et preuve
- Compris : Partitionner exhaustivement au seuil de 6.
- Données : Jean, Maximilien, Brigitte, Sonia, Jean-Pierre, Sandra.
- Production attendue : deux listes courts/longs ; occurrences conservées.
- Acquis localisés : cours-Q5/exemple-Q5 : deux branches et initialisations ; len déjà TD1/TD3-one.
- Cellules du TD4 lues pour cette question : cours 28, exemple 29, essai 30, énoncé 31, réponse 32, vérification 33 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : courts Jean/Sonia ; longs Maximilien/Brigitte/Jean-Pierre/Sandra ; Sonia 5/Sandra 6 ; copie avec deuxième Sonia.

### Q6 — Lecture préalable et preuve
- Compris : Partitionner par parité.
- Données : 32,5,12,8,3,75,2,15.
- Production attendue : pairs et impairs, sans perdre ni réordonner les occurrences.
- Acquis localisés : cours-Q6/exemple-Q6 : reste %, zéro pair ; cours-Q5 : partition.
- Cellules du TD4 lues pour cette question : cours 34, exemple 35, essai 36, énoncé 37, réponse 38, vérification 39 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : pairs 32/12/8/2 ; impairs 5/3/75/15 ; [] et [0,2,2,-1] vérifient vide, zéro, négatif, répétition.

## TD4-bis

### Q1 — Lecture préalable et preuve
- Compris : Produire les pairs 0 à 10 inclus.
- Données : départ 0, dernier 10, pas 2.
- Production attendue : liste positions_paires par range.
- Acquis localisés : cours-Q1/exemple-Q1 : range et borne finale exclue ; TD3-one : listes.
- Cellules du TD4 lues pour cette question : cours 4, exemple 5, essai 6, énoncé 7, réponse 8, vérification 9 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : range(0,11,2) ; six valeurs ; essai borne 8 ; filtre % équivalent sur même intervalle.

### Q2 — Lecture préalable et preuve
- Compris : Descendre puis comparer un sens incompatible.
- Données : départ 10, dernier 0, pas -2 puis +2.
- Production attendue : positions_inversees et positions_vides avec même borne finale.
- Acquis localisés : cours-Q2/exemple-Q2 : pas négatif et suite vide.
- Cellules du TD4 lues pour cette question : cours 10, exemple 11, essai 12, énoncé 13, réponse 14, vérification 15 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : [10,8,6,4,2,0] et [] ; borne -1 ; essai descente 3 à -1 et changement de signe.

### Q3 — Lecture préalable et preuve
- Compris : Conserver les multiples tant que <=70.
- Données : multiple initial 7, progression +7.
- Production attendue : multiples et variable de sortie multiple avec Q3b.
- Acquis localisés : cours-Q3/exemple-Q3 : état, test while, traitement, mise à jour ; essai-Q3 corrige le renvoi.
- Cellules du TD4 lues pour cette question : cours 16, exemple 17, essai 18, énoncé 19, réponse 20, vérification 21 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : début 7, dernière retenue 70, première rejetée 77 ; autre borne 20 donne [7,14] puis 21.

### Q4 — Lecture préalable et preuve
- Compris : Arrêter sur vingt tours distincts du terme.
- Données : premier terme 7, compteur initial 0.
- Production attendue : table_sept et nombre_termes.
- Acquis localisés : cours-Q4/exemple-Q4 : deux états distincts ; Q3 : while ; TD3-one : append.
- Cellules du TD4 lues pour cette question : cours 22, exemple 23, essai 24, énoncé 25, réponse 26, vérification 27 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : 20 termes de 7 à 140, pas 7, compteur 20, prochain 147 ; essai 3 puis zéro terme.

### Q5 — Lecture préalable et preuve
- Compris : Filtrer cinquante candidats distincts des résultats.
- Données : rangs 1 à 50, candidat = rang *13, divisibilité par7.
- Production attendue : multiples_retenus avec for.
- Acquis localisés : cours-Q5/exemple-Q5 ; % cours-Q1 ; borne range Q1 ; if TD4-one.
- Cellules du TD4 lues pour cette question : cours 28, exemple 29, essai 30, énoncé 31, réponse 32, vérification 33 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : [91,182,273,364,455,546,637], rangs 7 à49 de7 en7 ; chacun deux restes nuls et <=650.

### Q6 — Lecture préalable et preuve
- Compris : Sommer intersection et union sans double ajout.
- Données : a=1,b=30, bornes incluses, divisibilités 3 et5.
- Production attendue : somme_et puis somme_ou.
- Acquis localisés : cours-Q6/exemple-Q6 : and/or, somme initialisée et mise à jour ; range Q1.
- Cellules du TD4 lues pour cette question : cours 34, exemple 35, essai 36, énoncé 37, réponse 38, vérification 39 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : et 15+30=45 ; ou total225 ; cas a=b=15 produit15/15 ; bornes1/2 produisent0/0.

## TD4-ter

### Q1 — Lecture préalable et preuve
- Compris : Compter e exact en neutralisant la casse seulement.
- Données : Le texte est une donnée.
- Production attendue : nombre_e, source texte conservée.
- Acquis localisés : cours-Q1/exemple-Q1 : compteur par caractère ; TD2 lower ; TD4-one : accent distinct.
- Cellules du TD4 lues pour cette question : cours 4, exemple 5, essai 6, énoncé 7, réponse 8, vérification 9 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : 6 = 1+2+1+1+1 par fragments ; vide/EEE/é è ê donnent0/3/0.

### Q2 — Lecture préalable et preuve
- Compris : Mettre à jour deux meilleurs candidats.
- Données : nombres et negatifs, listes non vides garanties.
- Production attendue : maximum_nombres et maximum_negatifs, sans max ni tri.
- Acquis localisés : cours-Q2/exemple-Q2 : premier élément et comparaison ; TD3-one : indice0.
- Cellules du TD4 lues pour cette question : cours 10, exemple 11, essai 12, énoncé 13, réponse 14, vérification 15 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : 75 et -3 ; essais singleton et maximum répété ; appartient à la liste et >=chaque valeur ; vide exclu.

### Q3 — Lecture préalable et preuve
- Compris : Créer ou augmenter le compteur de chaque animal.
- Données : chat/chien/chat/oiseau/chien/chat.
- Production attendue : frequences_animaux par for et if/else.
- Acquis localisés : TD3-ter cours Q1 : clés/valeurs et affectation ; cours-Q3/exemple-Q3 : appartenance et compteur.
- Cellules du TD4 lues pour cette question : cours 16, exemple 17, essai 18, énoncé 19, réponse 20, vérification 21 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : chat3/chien2/oiseau1, total6 ; [chat,Chat] garde deux clés ; trois chats donnent3.

### Q4 — Lecture préalable et preuve
- Compris : Comparer deux constructions et totaliser les effectifs.
- Données : huit fragments de la phrase fournie après lower/split.
- Production attendue : frequences, frequences_autrement, total_effectifs et len.
- Acquis localisés : TD2 split/lower ; cours-Q4/exemple-Q4 : get et if/else ; TD3-ter items et déballage.
- Cellules du TD4 lues pour cette question : cours 22, exemple 23, essai 24, énoncé 25, réponse 26, vérification 27 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : le3, tal/traite/langage/et/texte1 ; total8 ; deux dictionnaires égaux ; essais vide et oui/oui/non.

### Q5 — Lecture préalable et preuve
- Compris : Transformer sans filtrer avec compréhension.
- Données : TAL/corpus/analyse/IA.
- Production attendue : longueurs_tous, une longueur par position.
- Acquis localisés : cours-Q5/exemple-Q5 : forme de compréhension et équivalence boucle ; len TD1.
- Cellules du TD4 lues pour cette question : cours 28, exemple 29, essai 30, énoncé 31, réponse 32, vérification 33 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : [3,6,7,2] ; essai vide/a/a donne [0,1,1] avec deux écritures ; pas de modification source.

### Q6 — Lecture préalable et preuve
- Compris : Filtrer les mots puis conserver des nombres.
- Données : mots de Q5 ; seuil strict >5.
- Production attendue : longueurs_mots_longs et comparaison mots_longs dans essai.
- Acquis localisés : cours-Q6/exemple-Q6 : transformation/parcours/filtre ; cours-Q5 ; TD4-one Q2 ; essai-Q6 explicite compréhension.
- Cellules du TD4 lues pour cette question : cours 34, exemple 35, essai 36, énoncé 37, réponse 38, vérification 39 (indices à partir de 0).
- Ambiguïtés ou passages incompris : aucun blocage identifié pour cette question. Les données imposées et les données d’essai sont distinguées ; aucun résultat ne nécessite une notion implicite absente des ressources autorisées.
- Preuve de construction et vérification prévue : [6,7] ; essai abcde/abcdef/vide/abcdef produit[6,6] ; boucle filtre corpus/analyse puis longueurs.

## État et limites

Les exemples fournis, les énoncés, les cellules de pratique originales, le tuteur caché, les annexes, la restitution et toutes les métadonnées sont conservés. Les ajouts aux cellules de pratique sont nos essais construits ; les lignes de données, exemples et libellés de sortie initialement fournis restent distingués des solutions construites. Les réponses Q1–Q6 et explications sont produites pour cette copie de référence.

Les prédictions ont été écrites avant exécution. Aucune cellule de notebook n’a été exécutée ; aucune soumission au serveur n’a été faite. Toutes les sorties restent vides et tous les execution_count sont nuls. Les vérifications écrites restent à exécuter par une personne habilitée. Ce livrable ne constitue ni validation éditoriale, ni validation pédagogique, ni validation du correcteur.

Reprise finale par TAL-Étudiant-Modèle : les copies sont reconstruites depuis les dernières sources disponibles, puis nos solutions et essais sont réappliqués. Les métadonnées de notebook et de cellule proviennent de ces sources. Les cellules hors réponse/identification/pratique sont strictement celles des sujets.

## Empreintes des sources reprises

- TD4-one_S1_conditions_filtres.ipynb : SHA-256 `1e9b4ef1f8ec4e1740b88bfc18021ac0e75338bd14b050fdccb6d2274c3a20e4` ; copie `TD4-one_S1_conditions_filtres_corrige_non_execute.ipynb`.
- TD4-bis_S1_bornes_repetitions.ipynb : SHA-256 `de787ab06945e2e8c6934b4199c00cf738d94a27951ca3b2cc3446344caa46c1` ; copie `TD4-bis_S1_bornes_repetitions_corrige_non_execute.ipynb`.
- TD4-ter_S1_comptages_comprehensions.ipynb : SHA-256 `0eb734bbc132d8b83f04081f0bc617d2709aa65718c362d8059490dea19dcefd` ; copie `TD4-ter_S1_comptages_comprehensions_corrige_non_execute.ipynb`.
