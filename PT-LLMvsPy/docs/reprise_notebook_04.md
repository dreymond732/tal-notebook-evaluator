# Vérifier une affirmation par le calcul et la lecture — préparer le TD

Cette fiche compare la [version distribuée avant la reprise](https://github.com/dreymond732/tal-notebook-evaluator/blob/fcf8bdf152db52c26ec17f1ffc81618a3d9458a0/PT-LLMvsPy/notebooks/04_audit_llm.ipynb) au cahier [Vérifier une affirmation par le calcul et la lecture](../notebooks/04_verifier_une_affirmation_par_le_calcul_et_la_lecture.ipynb). Les tableaux rapprochent les valeurs publiées par Gemini des calculs sur deux TXT du 01, la référence et sa variante après retrait des `_`. Les mesures des cahiers 02 et 03 ont été vérifiées avec spaCy 3.8.18 et `fr_core_news_sm` 3.8.0. Le cahier étudiant est distribué avec les sorties vides.

## Évolution du découpage et des tâches

| Dans la version précédente | Dans le cahier révisé | Travail observable en classe |
|---|---|---|
| Ouverture, puis §1 sur les trois sources | Reprendre le corpus nettoyé et les JSON des fréquences et des cooccurrences et identifier séparément le rapport chiffré transmis le 10 novembre 2026, la proposition M4 et la transcription citée | Montrer à son binôme où figure une annonce chiffrée, une mesure laissée à réaliser et une formulation attribuée à Faguet. |
| §2, deux phrases personnelles, un entier annoncé et une convention manquante | Vérifier aussi un intervalle décimal construit sur un cas personnel, puis auditer le TTR et la longueur moyenne du § 1 du rapport | Nommer le numérateur et le dénominateur, distinguer ratio et pourcentage, confronter les valeurs aux conventions des deux sources. |
| §2, volume et « 208 phrases », puis mesure M4 du cahier sur les cooccurrences | Relier la preuve numérique aux passages retenus dans le JSON des cooccurrences. Conserver les deux enquêtes communes et leurs conventions | Expliquer la portée de « toujours » en relisant les mots et le locuteur. Pour M4, préciser l’origine du résultat numérique. Reprendre aussi, si elle existe, la mesure du couple choisi au 03 et retrouver ses propres témoins. |
| §3, citation personnelle, choix entre trois citations de la transcription et recherche d’une expression distinctive | Tester le rôle de la casse et des frontières de mots, puis localiser une citation, l’ancre éventuelle et son cotexte | Prévoir quelles chaînes seront retenues. Sur le livre, préciser la provenance de la citation et choisir une ancre pour chercher un passage candidat. Distinguer les mots retrouvés, leur fidélité et leur attribution. Documenter aussi une recherche infructueuse. |
| §4, une enquête au choix et deux passages, puis confrontation des lectures | Conserver les trois voies. Modifier une cible et choisir la recherche adaptée à sa longueur, mot entier ou suite de mots | Relever un indice dans chacun des deux extraits, identifier la voix, confronter une lecture au binôme et limiter la conclusion à ce que ces passages étayent. |
| Conclusion et lecture du binôme saisies dans la cellule d’export | Séparer la réponse individuelle de l’écriture du fichier, puis vérifier un commentaire en rouvrant le JSON téléchargé | Après une correction, vérifier la nouvelle version du commentaire dans la copie personnelle et dans la copie de remise. |

## Deux règles à modifier pendant le TD

Au § 1, faire prédire ce que donnera `dans_mon_intervalle` pour une valeur égale à la borne basse. Remplacer le premier `<=` par `<` et relancer la définition puis le calcul. Avec les mêmes bornes, cette valeur passe de `True` à `False`. L’essai enregistre aussi le résultat pour le TTR des phrases et celui du livre.

Au § 3, exécuter `normaliser_citation` puis l’essai sur « En droit donc ». Activer la ligne `texte = texte.replace("_", "")` et relancer les deux cellules. Dans la phrase d’essai et le TXT où figure `_En droit_ donc`, le nombre de correspondances passe de 0 à 1. Sur le TXT déjà nettoyé des `_`, la correspondance est présente dès le premier essai. Cette recherche compte les chaînes de caractères transformées. Pour relire la citation de la pièce C ou une formulation personnelle, la cellule de lecture affiche une fenêtre du TXT du 01. Après normalisation, elle estime le décalage à partir de l’écart de longueur et de la part du livre déjà parcourue. La largeur de lecture est réglable.

Les deux règles et les valeurs qu’elles produisent figurent dans `essais_personnels`, sous `regle_intervalle` et `normalisation_citation`.

## Deux questions distinctes sur les ratios

Le rapport annonce 8 633 unités distinctes, 79 540 tokens et 3 829 phrases. Pour refaire le calcul sur Faguet, le 04 reprend trois valeurs du 02. N est le nombre de tokens alphabétiques, V le nombre de leurs formes distinctes en minuscules et S le nombre de phrases qui en contiennent au moins un. [Tableau du rapport chiffré, § 1](../../app/static/PT_LLMvsPy_Analyse_Gemini_source_originale.md) · [Conventions et mesures du cahier sur les fréquences](reprise_notebook_02.md)

| Mesure | Rapport publié | Quotient des effectifs du rapport | TXT de référence avec les `_` | Même TXT après retrait des `_` |
|---|---:|---:|---:|---:|
| TTR (V/N) | 0,1085 (10,85 %) | 8 633 / 79 540 ≈ 0,108537 | 8 380 / 74 090 ≈ 0,113106 | 8 397 / 74 192 ≈ 0,113179 |
| Longueur moyenne (N/S) | 20,77 mots par phrase | 79 540 / 3 829 ≈ 20,773048 | 74 090 / 3 416 ≈ 21,689110 | 74 192 / 3 494 ≈ 21,234116 |

Les deux quotients du rapport reproduisent ses valeurs affichées à leur précision publiée. Le filtre de tokens, la normalisation et la segmentation du rapport restent insuffisamment documentés pour imputer l’écart à une erreur de calcul. L’intervalle décimal utilisé dans le cas personnel appartient au protocole de cet exercice. Il ne constitue pas un seuil de tolérance annoncé dans le rapport.

Au § 4, le rapport annonce 208 phrases rapprochant les graphies *femme(s)* et *homme(s)*. Le décompte en union donne 199 sur chacun des deux TXT. Pour les lemmes *femme* et *droit*, la conversation Gemini décrit un protocole et laisse la valeur à calculer. Le cahier 03 a trouvé 48 phrases sur la référence et 47 après retrait des `_`. Le passage qui explique l’écart figure dans la [fiche du 03](reprise_notebook_03.md).

## De la chaîne de caractères à son interprétation

| Mot recherché | Sous-chaîne, casse exacte (deux TXT) | Sous-chaîne, casse ignorée (deux TXT) | Mot entier, casse ignorée, avec les `_` | Mot entier, casse ignorée, après retrait des `_` |
|---|---:|---:|---:|---:|
| `droit` | 139 | 140 | 77 | 86 |
| `état` | 19 | 55 | 42 | 43 |

*Droits* et *endroit* contiennent la chaîne *droit*. Pour isoler l’effet des frontières de mot, comparer les colonnes qui ignorent la casse. Dans `_En droit_ donc`, Python considère le soulignement comme un caractère de mot. Il empêche de reconnaître une frontière immédiatement après *droit*. Les neuf occurrences qui apparaissent dans la dernière colonne lorsque les tirets bas sont retirés permettent d’expliquer l’écart entre 77 et 86.

| Formulation de la pièce C | Résultat dans les deux TXT | Point à discuter |
|---|---|---|
| Formule se terminant par *naturally* | `NON_RETROUVEE` | Avec l’ancre française « peut être naturellement », la recherche propose deux passages. |
| « Les professions n'ont pas de sexe. » | `NORMALISEE` | Le passage commence par une minuscule. |
| « même capacité intellectuelle » | `EXACTE` | La chaîne est présente. Le cotexte reste à lire pour identifier la voix. |

Pour la première citation, choisir la première piste de l’ancre « peut être naturellement » dans l’un ou l’autre TXT. La mention « de l’avis de M. Turgeon » introduit les mots cités. Faguet les rapporte et les commente. Choisir ce passage comme candidat permet d’expliquer le rapprochement et de discuter l’attribution de la transcription. [Transcription, réponses 1 et 2](../../Notebooks%20TD/S3/ressources/gemini_transcription.txt)

## Bibliothèque et références mobilisées

| Référence | Ce qui évolue dans le cahier d’audit |
|---|---|
| [Fonctions de textométrie](../src/tal_toolkit/textometry.py) | `concordances_exactes` recherche un motif littéral sensible à la casse. `concordances_mot(source, mot, largeur=45)` ajoute une recherche de graphie entière insensible à la casse. Elle conserve le pivot tel qu’il est écrit et ses positions en caractères dans le texte fourni. |
| [Fonctions d’audit](../src/tal_toolkit/audit_llm.py) | `evaluer_affirmation` et `comparer_intervalle` acceptent les entiers et les décimaux, avec bornes inclusives. `champs_manquants`, `concordances_expression` et `verifier_citation` servent toujours à documenter le protocole, une locution et la fidélité d’une citation. |
| Pièces déjà étudiées | Le [rapport chiffré](../../app/static/PT_LLMvsPy_Analyse_Gemini_source_originale.md), la [conversation partagée, ligne M4](https://share.gemini.google/43HURKzcfoet) et la [transcription de septembre](../../Notebooks%20TD/S3/ressources/gemini_transcription.txt) sont les trois sources des affirmations. |
| Bird, Klein et Loper (2009), *Natural Language Processing with Python* | L’ouvrage est déjà référencé dans le projet. Le cahier d’audit renvoie désormais au chapitre 1, §1.3, pour apprendre à lire une concordance. Le TD utilise les fonctions du projet. [Chapitre en ligne](https://www.nltk.org/book/ch01.html) |
| Bender et Koller (2020), « Climbing towards NLU » | Lecture ajoutée pour situer la distinction entre la forme observée et le sens attribué à un énoncé. [Article publié à l’ACL](https://aclanthology.org/2020.acl-main.463/) |
| Documentation Python | Le passage sur la frontière de mot précise le traitement des lettres accentuées, des chiffres et du soulignement. [Définition de la frontière de mot](https://docs.python.org/fr/3/library/re.html#regular-expression-syntax) |

## Sauvegarde et remise

Dans le JSON, `ratios_A` regroupe le contrôle arithmétique des valeurs publiées, leur comparaison au calcul commun et la lecture de l’étudiant. Les trois effectifs du calcul commun (N, V, S) proviennent de la ligne `mesures.alphabetiques` du 02. La rubrique `concordance_mot` conserve la graphie, les trois effectifs, les témoins localisés et leur interprétation. Les essais sur l’intervalle et sur le mot entier figurent aussi dans `essais_personnels`.

La rubrique `lectures_personnelles` rassemble l’essai sur les fréquences (`frequences_02`), le couple de lemmes choisi dans le 03 (`cooccurrences_03`) et le commentaire de l’étudiant (`lecture`). Par exemple, dans une variante du 02 qui sélectionne seulement les formes *femme* et *femmes* sur le TXT sans tirets bas, le filtre garde 958 positions. Si on applique cette même condition au couple *femme* / *droit* dans le 03, le filtre écarte toutes les occurrences de *droit* et le résultat personnel vaut zéro. Sur ce même TXT, la mesure commune de la pièce B reste de 47 phrases. L’enquête personnelle du 03 est facultative.

L’étudiant télécharge `resultats_04_<numero>.json` depuis la session temporaire. Il ouvre le fichier, vérifie son numéro, sa propre conclusion et la lecture du binôme, puis importe la version vérifiée dans **Mon Drive → S3-PythonVsLLM**. En cas de correction, la nouvelle réponse doit être visible après réouverture du fichier téléchargé. À la revue finale, l’étudiant copie les trois JSON des fréquences, des cooccurrences et de l’audit dans le dossier partagé. Il y retrouve aussi le ZIP du corpus nettoyé déjà déposé. Les originaux restent dans son dossier personnel. [Guide de remise](deploiement_colab_drive_td01.md)
