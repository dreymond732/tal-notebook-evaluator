# Notebook 04 — préparer le TD d’audit des affirmations de Gemini

Cette fiche compare le [04 distribué avant la reprise](https://github.com/dreymond732/tal-notebook-evaluator/blob/fcf8bdf152db52c26ec17f1ffc81618a3d9458a0/PT-LLMvsPy/notebooks/04_audit_llm.ipynb) au [cahier révisé](../notebooks/04_audit_llm.ipynb). Les nombres ci-dessous proviennent du rapport et d’une exécution sur le texte nettoyé au 01. Le cahier étudiant est distribué avec les sorties vides.

## Évolution du découpage et des tâches

| Dans le 04 précédent | Dans le 04 révisé | Travail observable en classe |
|---|---|---|
| Ouverture, puis §1 sur les trois sources | Reprendre les trois fichiers des 01 à 03 et identifier séparément le rapport Studio, la proposition M4 et la transcription citée | Montrer à son binôme où figure une annonce chiffrée, une mesure laissée à réaliser et une formulation attribuée à Faguet. |
| §2, deux phrases personnelles, un entier annoncé et une convention manquante | Vérifier aussi un intervalle décimal construit sur un cas personnel, puis auditer le TTR et la longueur moyenne du §1 de Studio | Nommer le numérateur et le dénominateur, distinguer ratio et pourcentage, confronter les valeurs aux conventions des deux sources. |
| §2, volume et « 208 phrases », puis mesure M4 du 03 | Relier la preuve numérique aux passages du 03. Conserver les deux enquêtes communes et leurs conventions | Expliquer la portée de « toujours » en relisant les mots et le locuteur. Pour M4, rappeler que le résultat numérique vient du 03. |
| §3, citation personnelle, choix entre trois citations de la transcription et recherche d’une expression distinctive | Tester le rôle de la casse et des frontières de mots, puis localiser une citation, l’ancre éventuelle et son cotexte | Prévoir quelles chaînes seront retenues. Sur le livre, distinguer graphie trouvée, fidélité des mots et attribution. Documenter aussi une recherche infructueuse. |
| §4, une enquête au choix et deux passages, puis confrontation des lectures | Conserver les trois voies. Employer les concordances de mots pour la polysémie et les noms de personnes, et les concordances d’expressions pour la modalisation | Relever un indice dans chacun des deux extraits, identifier la voix, confronter une lecture au binôme et limiter la conclusion à ce que ces passages étayent. |
| Conclusion et lecture du binôme saisies dans la cellule d’export | Séparer la réponse individuelle de l’écriture du fichier, puis vérifier un commentaire en rouvrant le JSON téléchargé | Après une correction, vérifier la nouvelle version du commentaire dans la copie personnelle et dans la copie de remise. |

## Deux questions distinctes sur les ratios

Le rapport donne 8 633 types, 79 540 tokens et 3 829 phrases. Pour la convention « formes alphabétiques en minuscules » du 02, on obtient 8 380 types, 74 090 tokens et 3 416 phrases qui contiennent au moins un token alphabétique. [Tableau publié par Studio, §1](../../app/static/PT_LLMvsPy_Analyse_Gemini_source_originale.md) · [Conventions et mesures du 02](reprise_notebook_02.md)

| Mesure | Rapport publié | Quotient des effectifs du rapport | Quotient selon le 02 |
|---|---:|---:|---:|
| TTR, types / tokens | 0,1085 (10,85 %) | 8 633 / 79 540 ≈ 0,108537 | 8 380 / 74 090 ≈ 0,113106 (11,31 %) |
| Longueur moyenne, tokens retenus / phrases | 20,77 mots par phrase | 79 540 / 3 829 ≈ 20,773048 | 74 090 / 3 416 ≈ 21,689110 tokens par phrase |

Les deux quotients du rapport reproduisent ses valeurs affichées à leur précision publiée. Le filtre de tokens, la normalisation et la segmentation de Studio restent insuffisamment documentés pour imputer l’écart à une erreur de calcul. L’intervalle décimal utilisé dans le cas personnel appartient au protocole de cet exercice. Il ne constitue pas un seuil de tolérance annoncé par Studio.

La même distinction vaut pour le §4. Studio annonce 208 phrases rapprochant *femme(s)* et *homme(s)*. Le protocole du 03 en retrouve 199. Pour les lemmes *femme* et *droit*, les 48 phrases mesurées viennent du 03 et la ligne M4 de la conversation laisse sa valeur non calculée. Les passages et leurs positions restent attachés à chacun de ces deux dossiers.

## De la chaîne de caractères à son interprétation

| Sur le texte nettoyé | Sous-chaîne sensible à la casse | Sous-chaîne sans distinction de casse | Mot entier sans distinction de casse |
|---|---:|---:|---:|
| `droit` | 139 | 140 | 77 |
| `état` | 19 | 55 | 42 |

Pour isoler l’effet des frontières, faire comparer les deux dernières colonnes. *Droits* et *endroit* contiennent la chaîne *droit*. Une apostrophe délimite un mot au sens de l’expression régulière, alors que le soulignement est un caractère de mot. Dans `_En droit_ donc`, le soulignement après *droit* est présent dans le texte nettoyé. Le 02 compte 86 tokens dont la forme minuscule est *droit*. Chacun des neuf tokens supplémentaires par rapport aux 77 concordances jouxte un soulignement dans le texte nettoyé.

Pour la citation de la transcription qui se termine par *naturally*, l’ancre française « peut être naturellement » donne deux pistes. Dans la première, l’ancre occupe les caractères [21 716, 21 739[ du texte nettoyé. La mention qui précède attribue l’avis à Turgeon et Faguet le commente. Un passage candidat documente un rapprochement. L’attribution et la fidélité de la reformulation demandent chacune une justification. [Transcription, réponses 1 et 2](../../Notebooks%20TD/S3/ressources/gemini_transcription.txt)

## Bibliothèque et références mobilisées

| Référence | Ce qui évolue dans le 04 |
|---|---|
| [Fonctions de textométrie](../src/tal_toolkit/textometry.py) | `concordances_exactes` recherche un motif littéral sensible à la casse. `concordances_mot(source, mot, largeur=45)` ajoute une recherche de graphie entière insensible à la casse. Elle conserve le pivot tel qu’il est écrit et ses positions en caractères dans le texte fourni. |
| [Fonctions d’audit](../src/tal_toolkit/audit_llm.py) | `evaluer_affirmation` et `comparer_intervalle` acceptent les entiers et les décimaux, avec bornes inclusives. `champs_manquants`, `concordances_expression` et `verifier_citation` servent toujours à documenter le protocole, une locution et la fidélité d’une citation. |
| Pièces déjà étudiées | Le [rapport Studio](../../app/static/PT_LLMvsPy_Analyse_Gemini_source_originale.md), la [conversation partagée, ligne M4](https://share.gemini.google/43HURKzcfoet) et la [transcription de septembre](../../Notebooks%20TD/S3/ressources/gemini_transcription.txt) sont les trois sources des affirmations. |
| Bird, Klein et Loper (2009), *Natural Language Processing with Python* | L’ouvrage est déjà référencé dans le projet. Le 04 renvoie désormais au chapitre 1, §1.3, pour apprendre à lire une concordance. Le TD utilise les fonctions du projet. [Chapitre en ligne](https://www.nltk.org/book/ch01.html) |
| Bender et Koller (2020), « Climbing towards NLU » | Lecture ajoutée pour situer la distinction entre la forme observée et le sens attribué à un énoncé. [Article publié à l’ACL](https://aclanthology.org/2020.acl-main.463/) |
| Documentation Python | Le passage sur la frontière de mot précise le traitement des lettres accentuées, des chiffres et du soulignement. [Définition de la frontière de mot](https://docs.python.org/fr/3/library/re.html#regular-expression-syntax) |

## Sauvegarde et remise

Le JSON préserve les rubriques du 04 antérieur. `ratios_A` ajoute les quotients reconstruits avec les effectifs publiés, leur comparaison à ceux du 02 et la lecture de l’étudiant. `concordance_mot` conserve sa graphie, les trois effectifs, les témoins localisés et son interprétation. Les essais sur l’intervalle et sur le mot entier se retrouvent aussi dans `essais_personnels`.

L’étudiant télécharge `resultats_04_<numero>.json` depuis la session temporaire. Il ouvre le fichier, vérifie son numéro, sa propre conclusion et la lecture du binôme, puis importe la version vérifiée dans **Mon Drive → S3-PythonVsLLM**. En cas de correction, la nouvelle réponse doit être visible après réouverture du fichier téléchargé. À la revue finale, l’étudiant copie les trois JSON numérotés des 02 à 04 dans le dossier partagé. Il y retrouve aussi le ZIP du 01 déjà déposé. Les originaux restent dans son dossier personnel. [Guide de remise](deploiement_colab_drive_td01.md)
