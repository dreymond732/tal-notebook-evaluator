# Gouvernance — tutorat dans tous les sujets

## Mission et périmètre

Branche : `pedagogy/td2-markdown-tutor-reminder`. Extension de la PR nº 9 vers `main`, référence de comparaison : `fd77df71`.

Après son retour favorable sur le pilote TD2, l'enseignant demande explicitement un tuteur adapté à tous les TD et contrôles, dans les métadonnées et dans une cellule Markdown dédiée en première position. Cette décision remplace la limitation initiale du pilote. Les TD guident dès la première demande ; le S1 interdit tout code fourni par le tuteur ; les contrôles refusent toute aide.

Le lot couvre les 21 sujets déclarés (16 TD, dont trois remédiations, et cinq contrôles), le générateur `app/tutor_metadata.py`, ses tests, le manifeste et les documents de politique, classification, couverture et utilisation. `README.md` précise aussi le processus applicable aux futurs sujets. Les neuf corrigés explicitement exclus restent inchangés. Le présent rapport complète, sans réécrire, le rapport historique du pilote.

**Aucun `CHANGEMENT_DE_CONTRAT` d'évaluation** : les correcteurs, routes, barèmes, identifications, marqueurs, données et productions étudiantes ne changent pas. Le flux de double revue est néanmoins appliqué à ce lot de code et de pédagogie. Aucun actif normatif de gouvernance n'est modifié.

## Rôles, autorisation et couverture

Le Prof `all_tutor_prof` a produit la matrice `docs/pedagogy/TUTOR_COVERAGE_MATRIX.md` avant conception ; l'Integration-Master et le réviseur indépendant `all_tutor_review_pedagogy` l'ont validée avant l'intervention du Designer. Le Prof `all_tutor_prof_s2` a établi les classifications et périmètres S2, puis a reçu le rôle déclaré de Designer après cette validation. Il reste producteur, sans auto-validation. L'Architecte `all_tutor_architect` intervient sur le générateur, les tests et la documentation technique ; l'Integration-Master produit la modification de `README.md`.

La transformation conserve intégralement les activités. Le seul ancien rappel du TD2 est déplacé vers la nouvelle cellule avec un équivalent immédiat. Les réserves héritées de progression et de titrage sont documentées sans refonte implicite. Les fichiers S2 intitulés contrôles et le devoir maison conservent leur mode sommatif existant. `DevoirS2.ipynb`, malgré son nom, est un corrigé enseignant explicitement identifié et tronqué ; il est exclu et non reconstruit.

Les agents indépendants rendent :

- `all_tutor_review_pedagogy` : **ACCEPT**, **COUVERTURE_PÉDAGOGIQUE_CONSERVÉE** ;
- `markdown_code_review` : **ACCEPT** après correction de `TAL-AUD-002`, relatif au placement de l'identifiant de la nouvelle cellule selon la version du format notebook.

Le Governance-Auditor ne modifie que le présent rapport dans `reports/governance/`.

## Preuves et limites

| Vérification | Résultat |
|---|---|
| Inventaire | PASS : 21 sujets, 16 TD et cinq contrôles ; neuf exclusions motivées. Un nouveau notebook non classé fait échouer la vérification. |
| Conservation des cellules | PASS : comparaison aux fichiers de `fd77df71` ; après retrait de la nouvelle cellule0 et du seul ancien préfixe TD2, les 512 cellules sources, dont 272 de code, sont exactement identiques, sorties et métadonnées locales comprises. Égalité reproduite par la gouvernance ; décompte fourni par le Designer. |
| Corrigés exclus | PASS : les neuf fichiers sont identiques octet par octet à la référence. Preuve reproduite par la gouvernance. |
| Instructions synchronisées | PASS : dans les 21 sujets, commentaire Markdown, contexte Colab et rendu canonique sont identiques ; métadonnées structurées cohérentes. Vérification attestée par les deux revues. |
| Périmètres et modes | PASS : permissions par exercice, S1 sans code, exemples minimaux distincts seulement après échange au S2/S3, refus total des contrôles ; aucune réponse attendue dans les profils. |
| Générateur et tests | PASS : `--check` pour les 21 sujets, idempotence des 21 transformations et suite complète de 57 tests réussis, attestés par l'auditeur code indépendant. |
| Diff | PASS : `git diff --check`, reproduit par la gouvernance. |
| Exécution étudiante | Aucune cellule étudiante exécutée ; analyses structurelles, génération des instructions et tests applicatifs seulement. |
| Essais Colab | Pilote TD2 : retour favorable rapporté par l'enseignant. Nouveau rendu généralisé : **NOT_TESTED**. Ce retour ne prouve pas l'efficacité des nouveaux profils ni un verrouillage des contrôles. |

Les deux corrigés tronqués exclus conservent leur défaut préalable. Le devoir maison possède aussi un ancien identifiant de cellule incompatible avec son format minor 4, conservé sans modification ; des avertissements d'identifiants absents sur d'autres anciennes cellules préexistent. La nouvelle cellule est adaptée au format de chaque sujet. Ces anomalies héritées ne sont pas déclarées corrigées par ce lot.

Les instructions restent modifiables dans une copie étudiante et peuvent ne pas être transmises ou respectées par Colab. Elles ne constituent pas un contrôle technique d'accès à l'assistance. Aucun déploiement ni aucune fusion n'a été réalisé dans cette mission.

## Verdict

**CONFORME** pour le périmètre et les preuves ci-dessus. Le producteur de documentation étant aussi Integration-Master, le statut d'intégration est **MAINTAINER_REVIEW**, jamais `READY_TO_MERGE`. La PR nº 9 élargie reste en brouillon vers `main` ; fusion et production relèvent du mainteneur.
