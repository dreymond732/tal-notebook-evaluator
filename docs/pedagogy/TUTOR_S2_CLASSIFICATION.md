# Classement des supports S2 pour le tuteur

Le contenu des sujets et le registre `EVALUATOR_MODES` de `app/routes.py` fondent le classement ci-dessous. L'ajout des deux représentations des instructions conserve les activités, données, cellules étudiantes, marqueurs et barèmes. Les corrigés sont exclus. Aucun code étudiant n'a été exécuté.

| Support | Mode | Couverture source → cible | Justification |
|---|---|---|---|
| `Notebooks TD/TD3_S2.ipynb` | TD | Q1–Q30 : conservées | Trente exercices de renforcement ; registre `td3-S2` formatif. |
| `Notebooks TD/TD5_S2.ipynb` | TD | Q1–Q25 : conservées | Vingt-cinq exercices d'approfondissement ; registre `td5-S2` formatif. |
| `Notebooks TD/TD6_S2.ipynb` | TD | Q1–Q10 et préparation des données : conservées | Dix exercices de fichiers et ressources ; registre `td6-S2` formatif. |
| `Notebooks TD/TD2 - S2.ipynb` | Contrôle | Q1–Q13 : conservées | Titre « Contrôle S2 » et registre `td2-S2` sommatif. |
| `Notebooks TD/TD4_S2.ipynb` | Contrôle | Q1–Q14 : conservées | Titre « Contrôle S3 », mais fichier et registre `td4-S2` dans le parcours S2 ; le profil conserve le semestre 2, sans réécrire le sujet. |
| `Notebooks TD/devoirMaisonS2.ipynb` | Contrôle | Q1–Q30 : conservées | Devoir noté ; registre `ControleDevoirMaisonS2` explicitement en mode contrôle. |
| `Notebooks contrôles finaux/ControleFinalS2.ipynb` | Contrôle | Q1–Q18 et données : conservées | Titre, durée et consignes de contrôle final S2. |

Les trois TD reçoivent un profil par exercice, sans réponse attendue. Les quatre contrôles ne reçoivent aucun guidage, quiz, cours, exemple, correction ou validation de réponse ; leurs profils n'exposent aucune progression tutorielle.

Pour TD3, les importations initiales `math` et `collections.Counter` sont des éléments fournis. Seul `math` est autorisé pour l'exercice 22 qui utilise explicitement `math.sqrt` ; aucun autre exercice n'autorise de bibliothèque. La présence de `Counter` importé ne constitue pas une autorisation de résoudre les exercices avec ce raccourci. TD5 et TD6 ne nécessitent aucune bibliothèque. TD6 exclut explicitement les expressions régulières et `Counter` à Q8 ; la lecture et l'écriture CSV reposent sur les fonctions natives demandées.

Les instructions TD s'appliquent aux exercices existants : elles ne corrigent pas leurs incohérences historiques et n'introduisent pas de nouvelle progression curriculaire. Les notions `introduced_here` repèrent les notions mobilisées explicitement par la question ; elles ne constituent pas la preuve qu'un cours détaillé les précède.

## Exclusions et limites

- Les fichiers portant « corrigé » dans leur nom restent exclus et inchangés.
- `Notebooks contrôles finaux/DevoirS2.ipynb` est un corrigé enseignant mal nommé : son texte débute par « TD6 […] (CORRIGÉ) », « Version Enseignant / Solution », et une identité `CORRECTION`. Le JSON est tronqué à la ligne 382. Il reste exclu et n'est pas réparé dans cette mission.
- L'incohérence S3/S2 du titre de TD4 est signalée, sans décision de reclassement ni changement de route.
- Le comportement effectif dans Colab reste à essayer sur ces supports ; une instruction embarquée n'est pas un contrôle d'accès.

Critères d'acceptation : 7 profils S2 (3 TD, 4 contrôles), 65 exercices TD cartographiés, contenu étudiant inchangé, instructions identiques dans les métadonnées et la première cellule Markdown, aucun corrigé modifié. La validation indépendante relève du réviseur pédagogique.
