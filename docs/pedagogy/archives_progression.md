# Archives de progression — classement des versions remplacées

## Mandat et références

Le 19 novembre 2026, l'enseignant demande de conserver seulement les versions actuelles dans les dossiers de semestre et de ranger les versions remplacées dans `historique/`. Cette matrice est établie **avant les déplacements**. La référence technique immédiate est la révision `501413c3e5c216138595e68bee714d7902e9a393` sur la branche `code/archives-progression`, dans la suite de la PR de distribution des contrôles ; elle n'est pas remplacée par un nouvel état de `main`.

Le travail porte sur un rangement, pas sur une réécriture pédagogique. Tous les octets des douze notebooks déplacés restent conservés. Aucun exercice, exemple, donnée, sortie, identifiant, barème, rôle ou contexte de tuteur n'est modifié dans ces fichiers. Les anciens profils gardent leur chemin source interne comme provenance ; l'emplacement physique d'archive est déclaré séparément dans le manifeste.

## Classification avant rangement

| Famille | Décision | Motif et couverture |
|---|---|---|
| Quatre synthèses S1 TD3/4/5/6 | DÉPLACÉES vers historique | Le parcours courant comporte déjà leurs douze cahiers A/B/C. Les synthèses restent intégrales comme références et pour les copies commencées ; leur déplacement ne démontre pas une nouvelle équivalence pédagogique. |
| Douze cahiers A/B/C S1, TD1, TD2 et TD7 | CONSERVÉS dans S1 | Quinze cahiers courants ; les profils, données et contrats sont inchangés. |
| Huit corrigés historiques déjà exclus | DÉPLACÉS vers historique | Ils n'étaient pas distribués. Les modèles courants dans `Corrigés modèles/` restent inchangés. |
| S3 R0 et R2 | CONSERVÉS dans S3 | Remédiations distinctes, respectivement Python/texte et fréquences réutilisables ; leur nom R ne signifie pas une ancienne version du TD. |
| S3 TD1.b | CONSERVÉ dans S3 | Activité distincte de lecture du Doc spaCy, bonus facultatif ; ni doublon ancien de TD1.a ni version remplacée de TD1.c. |
| Contrôle final S2 à 18 questions | CONSERVÉ dans les contrôles S2 | Sujet distinct, inactif pour la correction automatique, exporté dans `dist/` avec sauvegarde locale depuis la mission précédente ; l'absence de correcteur n'en fait pas une ancienne version remplacée. |

## Matrice source → archive et correspondances courantes

Tous les contenus des sources archivées ont le statut **DÉPLACÉ, octets conservés**. Il n'y a pas de réduction d'activité ni de transfert vers un support futur à produire. Le changement de visibilité du parcours courant est explicitement demandé par l'enseignant.

| Source | Archive | Raison | Parcours ou référence actuelle |
|---|---|---|---|
| `Notebooks TD/S1/S1_TD3_collections.ipynb` | `historique/Notebooks TD/S1/S1_TD3_collections.ipynb` | Les trois cahiers TD3-A/B/C : listes, tuples, dictionnaires et ensembles. | S1_TD3_A_listes.ipynb ; S1_TD3_B_tuples.ipynb ; S1_TD3_C_dictionnaires_ensembles.ipynb |
| `Notebooks TD/S1/S1_TD4_boucles_conditions_comptages.ipynb` | `historique/Notebooks TD/S1/S1_TD4_boucles_conditions_comptages.ipynb` | Les trois cahiers TD4-A/B/C : conditions, répétitions et comptages. | S1_TD4_A_conditions_filtres.ipynb ; S1_TD4_B_bornes_repetitions.ipynb ; S1_TD4_C_comptages_comprehensions.ipynb |
| `Notebooks TD/S1/S1_TD5_fonctions_reutilisation.ipynb` | `historique/Notebooks TD/S1/S1_TD5_fonctions_reutilisation.ipynb` | Les trois cahiers TD5-A/B/C : fonctions, paramètres et composition. | S1_TD5_A_fonctions.ipynb ; S1_TD5_B_parametres_portee.ipynb ; S1_TD5_C_composition_texte.ipynb |
| `Notebooks TD/S1/S1_TD6_fichiers_csv.ipynb` | `historique/Notebooks TD/S1/S1_TD6_fichiers_csv.ipynb` | Les trois cahiers TD6-A/B/C : fichiers texte, données délimitées et CSV. | S1_TD6_A_fichiers_texte.ipynb ; S1_TD6_B_donnees_delimitees.ipynb ; S1_TD6_C_csv.ipynb |
| `Notebooks TD/TD2 - S2 - Corrigé.ipynb` | `historique/Notebooks TD/TD2 - S2 - Corrigé.ipynb` | Corrigé historique déjà exclu des sujets distribués. | Sujet courant : Notebooks contrôles finaux/S2/Controle_TD2_S2_algorithmique.ipynb ; ce sujet n’est pas un corrigé de remplacement. |
| `Notebooks TD/TD3 - S2 - Corrigé.ipynb` | `historique/Notebooks TD/TD3 - S2 - Corrigé.ipynb` | Corrigé historique déjà exclu des sujets distribués. | Sujet courant : Notebooks TD/S2/TD3_S2_algorithmique_structures.ipynb ; correspondance pédagogique non revalidée ici. |
| `Notebooks TD/TD4_S2-corrigé.ipynb` | `historique/Notebooks TD/TD4_S2-corrigé.ipynb` | Corrigé historique déjà exclu des sujets distribués. | Sujet courant : Notebooks contrôles finaux/S2/Controle_TD4_S2_ensembles.ipynb ; ce sujet n’est pas un corrigé de remplacement. |
| `Notebooks TD/TD5_S2-corrigé.ipynb` | `historique/Notebooks TD/TD5_S2-corrigé.ipynb` | Corrigé historique déjà exclu des sujets distribués. | Sujet courant : Notebooks TD/S2/TD5_S2_algorithmes_texte.ipynb ; correspondance pédagogique non revalidée ici. |
| `Notebooks TD/TD6_S2-corrigé.ipynb` | `historique/Notebooks TD/TD6_S2-corrigé.ipynb` | Corrigé historique déjà exclu ; JSON invalide conservé sans réparation. | Sujet courant : Notebooks TD/S2/TD6_S2_fichiers_ressources.ipynb ; aucune complétion de l’archive tronquée. |
| `Notebooks TD/devoirMaisonS2-corrigé.ipynb` | `historique/Notebooks TD/devoirMaisonS2-corrigé.ipynb` | Corrigé historique déjà exclu des sujets distribués. | Sujet courant : Notebooks contrôles finaux/S2/Devoir_maison_S2_approfondissement.ipynb ; ce sujet n’est pas un corrigé de remplacement. |
| `Notebooks contrôles finaux/DevoirS1_TILT_corrigé.ipynb` | `historique/Notebooks contrôles finaux/DevoirS1_TILT_corrigé.ipynb` | Corrigé historique du contrôle S1 v1, déjà exclu ; le contrôle v2 possède un autre modèle. | Corrigé v2 : Corrigés modèles/Contrôles finaux/controle-s1-v2/Controle_S1_v2_corrige_non_execute.ipynb. |
| `Notebooks contrôles finaux/DevoirS2.ipynb` | `historique/Notebooks contrôles finaux/DevoirS2.ipynb` | Archive de solution mal nommée, JSON invalide, déjà exclue ; aucun sujet étudiant courant. | Aucun remplacement de corrigé déclaré ; le contrôle final S2 à 18 questions est un sujet distinct conservé. |

Pour les quatre lignes S1, les noms A/B/C désignent les fichiers existants de `Notebooks TD/S1/`. Les autres correspondances n'affirment pas qu'un ancien corrigé résout le sujet courant ; elles repèrent les supports à utiliser désormais. Deux archives sont invalides en JSON avant déplacement : `TD6_S2-corrigé.ipynb` et `DevoirS2.ipynb`. Elles sont conservées telles quelles, sans inventer ni réparer de cellules.

## Empreintes de référence avant déplacement

Le README d'`historique/` reprend le tableau source → archive et les empreintes effectivement vérifiées après déplacement. L'identité des octets porte aussi sur les deux JSON invalides.

| Source | Taille en octets | SHA-256 avant déplacement | Lecture JSON |
|---|---:|---|---|
| `Notebooks TD/S1/S1_TD3_collections.ipynb` | 38134 | `8407ad74986617b6990cd512b3d9b5d7e01557276dbfeb7531db372641483642` | JSON lisible |
| `Notebooks TD/S1/S1_TD4_boucles_conditions_comptages.ipynb` | 39273 | `b620f2b1331a42eee0f69ebebb9f73c9efce01c150ec6d9ca924ce3321be9460` | JSON lisible |
| `Notebooks TD/S1/S1_TD5_fonctions_reutilisation.ipynb` | 40284 | `38deb1f0ab17ee767e171c5cd9a81be98318f78075c1948cea7172f55cefd907` | JSON lisible |
| `Notebooks TD/S1/S1_TD6_fichiers_csv.ipynb` | 40847 | `887f9901410def59fa8e404c185ca4b8c17254a1a06064b9e7673a23fa293c43` | JSON lisible |
| `Notebooks TD/TD2 - S2 - Corrigé.ipynb` | 7964 | `f24b5ef65a72aff0627920bbeeede3381416689b0552ef77fbc43dd764dbb848` | JSON lisible |
| `Notebooks TD/TD3 - S2 - Corrigé.ipynb` | 15519 | `f1770e04a81f6bff5825cefe1e1e84048e2afddf85fdbebdf8658f067a591b91` | JSON lisible |
| `Notebooks TD/TD4_S2-corrigé.ipynb` | 9155 | `02a4b802902ae2f5d56518e17dd0a9b7f221de48d1001dd2c3173c0076324377` | JSON lisible |
| `Notebooks TD/TD5_S2-corrigé.ipynb` | 15447 | `d56c498cab4b570208a678ca37e073a0e7ebb15cfd6b9f2124546087f662c48a` | JSON lisible |
| `Notebooks TD/TD6_S2-corrigé.ipynb` | 9505 | `b570c2bbe013147920d937cb939899305346f925fa16f1160df924dad9e89260` | JSON invalide |
| `Notebooks TD/devoirMaisonS2-corrigé.ipynb` | 7361 | `7b2f68ba8cc8e83ac9184cbbed9b1399f8057cce4fc219165f6de4fb65efdd5c` | JSON lisible |
| `Notebooks contrôles finaux/DevoirS1_TILT_corrigé.ipynb` | 41324 | `5181bba76ded28bd461e5f8bd1f67afbeb8988fb52de6832a1e9ef13ab7f19a7` | JSON lisible |
| `Notebooks contrôles finaux/DevoirS2.ipynb` | 9507 | `89f66a15da739680ca808015de90ffa550e9a43e877b55d57c8cef8de4a0292d` | JSON invalide |

## Manifeste, copies déjà commencées et limites

Les sessions `TD3_S1`, `TD4_S1`, `TD5_S1` et `TD6_S1` quittent les sessions courantes du manifeste et deviennent des exclusions explicitement archivées. Les douze profils A/B/C et les autres sessions restent identiques. Les huit exclusions de corrigés pointent vers leur nouvelle adresse sous `historique/`.

Le rangement ne retire ni ne change les correcteurs de compatibilité des quatre anciennes synthèses. Les copies déjà commencées gardent leurs métadonnées et leur contrat ; les archives ne sont pas redistribuées comme nouvelles versions. Aucune soumission ancienne n'est réévaluée, aucun fichier de copie remis n'est déplacé et aucun barème n'est activé ou désactivé.

Le recensement technique doit inclure `historique/` sans intégrer ces fichiers au catalogue courant ni au générateur de distribution. Les contrôles du générateur et les tests de non-régression restent une étape indépendante. Cette matrice documente le classement et les références ; elle ne vaut pas nouvelle revue de fond des contenus ou validation d'un correcteur pour le contrôle final S2.
