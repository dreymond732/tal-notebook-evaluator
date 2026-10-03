# Portée du retour automatique : R1, TD1 et TD1B S3

La révision éditoriale de R1 et les ajustements de TD1/TD1B ne changent aucun barème, validateur, contrat de métadonnées, marqueur de sortie ni mode de dépôt. Les formulations ne doivent pas transformer une limite de l’automatisation en promesse de correction individuelle par l’enseignant.

| Support | Retour existant | Ce qui n’est pas jugé automatiquement |
| --- | --- | --- |
| R1 | 4 points : calcul du nombre de tokens, annotations et sélections `NOUN`/`VERB`, sur le texte et le pipeline fixés. Concordance entre certaines constructions du code et les sorties enregistrées. | Justesse du commentaire linguistique, validité générale de tout le programme et authenticité de son exécution. |
| TD1, Q1–Q3 et Q5 | Concordance des traces avec la référence du pipeline fixé, selon les critères du correcteur. | Vérité linguistique de cette référence ; pertinence des critiques et interprétations. |
| TD1, Q4 | Un point pour deux tokens distincts localisables dans la première phrase et une relation renseignée. | Pertinence linguistique du verbe choisi, de la relation et de l’interprétation. |
| TD1, Q6 | Un point technique : structure attendue, nombre de phrases déclaré entre 2 et 4, cinq annotations couvrant le début du texte sans omission hors blancs, positions/formes concordantes, catégories connues, listes et champ de question. | Justesse de la segmentation, des lemmes et des catégories sur le texte libre ; pertinence de la question de corpus et de l’interprétation. |
| TD1B | Réception du notebook et conservation des productions. Aucune note automatique. | Justesse de toutes les réponses. Le reçu ne promet aucun retour individuel systématique. |

Le nombre de phrases de Q6 est une valeur déclarée dans la trace : le serveur ne relance pas spaCy pour le vérifier. Le serveur n’exécute jamais le code soumis. « Exercice non autocorrigé sur le fond linguistique » peut donc qualifier Q6, à condition de maintenir la précision sur sa vérification technique et son point dans le total de six.

Le dépôt et l’accès aux productions restent disponibles pour une consultation ciblée. Leur conservation ne crée pas une obligation de relecture de toutes les copies. Le type technique `human_review` de TD1B et les champs internes historiques relatifs à la relecture ne sont pas modifiés.

## Preuve de conservation éditoriale

`tests/fixtures/s3_r1_editorial_source_baseline.json` contient les octets UTF-8 de R1 extraits du parent `2c7dc3c696ef0f5f70046a2c6ef005f7e21cc1ac`, avant réécriture. La fixture historique S2 conserve son empreinte inchangée et la vérifie sur ce parent. Le test S3 compare ensuite le R1 actuel à ce parent : mêmes cellules originales, dans le même ordre, mêmes identifiants et métadonnées, mêmes quatre réponses et même AST du code fourni. Les ajouts sont permis ; la réécriture de prose et commentaires ne dispense pas des revues pédagogique et éditoriale indépendantes.

Les protections existantes de TD1 et R2 et l’exception précise du pin IPython restent inchangées. Les autres supports et les contrôles ne gagnent aucune exception de réécriture.
