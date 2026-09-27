# Audit de gouvernance — Devoir maison intermédiaire S1 après le TD5

## Verdict et périmètre

**CONFORME**, le 27 septembre 2026, sur la branche
`pedagogy/s1-dm-intermediaire-td5`, par comparaison avec la référence
`b7e1664074166420ae95446737204d5cfecfddf8`. Le périmètre est le nouveau sujet,
son corrigé modèle séparé, son évaluateur, leur inscription aux catalogues,
le rapport enseignant et les adaptations de tests et de CI. Ce verdict ne vaut
ni fusion, ni exécution du corrigé, ni déploiement.

Le sujet est une création demandée explicitement par l'enseignant après le TD5,
inspirée de la difficulté et du nombre de questions de `CorrectionDM-S1.ipynb`.
Il ne remplace pas cette référence et ne modifie aucun sujet historique.

## Autorisation, cadrage et séparation des rôles

Sources normatives lues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`,
`docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et le rôle gouvernance.

- Le TAL-Prof a produit `docs/pedagogy/dm_s1_intermediaire_spec.md` avant la
  conception, ordre confirmé dans le relais de l'orchestrateur. Sa matrice
  relie la référence aux activités nouvelles et chacune aux TD1 à TD5.
- Le TAL-Pedagogy-Designer a produit le sujet ; le TAL-Code-Architect a produit
  le correcteur, ses tests ciblés et les raccordements applicatifs.
- Le TAL-Étudiant-Modèle a été lancé dans un contexte séparé, limité au sujet
  et aux TD1 à TD5, sans accès au correcteur ni aux tests. Il a écrit uniquement
  le corrigé séparé dans `Corrigés modèles/`, sans exécuter ses cellules.
- Le TAL-Pedagogy-Reviewer indépendant a rendu **ACCEPT —
  COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**. Sa remarque TAL-PED-001 sur Q14 du modèle
  a été résolue : les formulations `not` et `elif` ont été remplacées par des
  constructions attestées dans la progression, puis relues.
- Le TAL-Code-Auditor indépendant a rendu **CONFORME**, en lecture seule du
  produit. Sa sonde sur une copie mémoire du modèle avec sorties synthétiques
  attribue 20/20 ; elle n'est pas une exécution du notebook.
- Le TAL-Integration-Master a produit des adaptations des tests de catalogue,
  d'intégrité et de la CI : son verdict est donc **MAINTAINER_REVIEW**, et non
  `READY_TO_MERGE`.
- Le TAL-Governance-Auditor a lu le produit et les preuves, et écrit uniquement
  le présent rapport dans `reports/governance/`.

Les deux verdicts spécialisés et la résolution de TAL-PED-001 ont été transmis
par l'orchestrateur en fin de revue. Ce sont des preuves de session ; le présent
rapport ne prétend pas qu'elles constituent des reviews GitHub publiées.
Le nouveau contrat de réponses et le correcteur constituent un changement
mixte soumis à cette double revue. Aucun prérequis postérieur au TD5, aucune
bibliothèque nouvelle, aucune suppression de contenu historique n'est introduit.

## Preuves examinées

| Exigence | Preuve et résultat |
|---|---|
| Branche et normes | Vérification propre : branche dédiée ; les 12 fichiers normatifs (`AGENTS.md`, matrice, contrat, fichiers de `docs/agents/`) sont identiques octet par octet à la référence Git. |
| Périmètre pédagogique | Spécification lue : 18 questions, cinq parties, réemploi des TD1 à TD5 ; données locales et synthétiques ; aucune dépendance à `input`, `eval`, import, fichier ou réseau. Charge de 3 à 4 heures explicitement indicative. |
| Couverture | Matrice source → cible et matrice TD → questions présentes ; la transformation du jeu en recherche bornée conserve conditions, essais et arrêts, sans exiger l'aléatoire absent de la progression. Verdict de couverture indépendant obtenu. |
| Intégrité historique | Vérification propre : aucun notebook historique dans le diff. Intégration : les 42 empreintes historiques restent vérifiées, fixture inchangée ; sujet nouveau et corrigé explicitement distingués de cette référence. |
| Sujet et modèle | Vérification propre des deux JSON de 45 cellules : syntaxe des cellules de code valide, sorties vides et compteurs nuls. Intégration : validation `nbformat` réussie. Le modèle est explicitement non exécuté. |
| Tuteur | Vérification propre : refus d'assistance contrôle dans la première cellule ; commande `python app/tutor_metadata.py --check` réussie pour 34 profils, dont le nouveau DM. Les instructions textuelles ne sont pas présentées comme un verrouillage technique du LLM. |
| Identification et routage | Lecture du catalogue et des registres : `dm-intermediaire-s1`, version 1, semestre S1, mode `controle`, soumis à `/submit`. Le correcteur exige nom, prénom, classe et numéro étudiant, et n'utilise pas le nom du fichier pour sélectionner le sujet. |
| Contrat du correcteur | Lecture : tuple de cinq éléments, maximum 20 ; Q1–Q14 à 1 point et Q15–Q18 à 1,5 point, points partiels bornés. Score déclaré technique provisoire, cinq explications regroupées pour relecture privée. |
| Non-exécution | Lecture du module : parsing JSON, AST et `ast.literal_eval` de littéraux sauvegardés ; aucun lancement du code étudiant. Les sondes et fixtures ajoutent des sorties synthétiques en mémoire sans exécuter les cellules. |
| Confidentialité et persistance | Tests inspectés : accusé de dépôt seul dans la réponse publique, rapport détaillé privé avec grille adaptée, numéro étudiant et caractère provisoire dans le CSV. Aucun retour automatique d'explication de contrôle à l'étudiant. |
| Tests | Intégration : 154 tests réussis, compilation réussie. Après la correction Q14 du modèle, l'orchestrateur a relancé les 10 tests ciblés du DM avec succès. Couverture notamment des doublons, erreurs et traces ambiguës, alternatives de paramètres, cas vides, ensembles, fonctions, absence d'exécution et dépôt privé. |
| Distribution | Intégration : 33 copies distribuables générées et vérifiées avec une adresse neutre ; corrigé exclu. Sources sans cellule contenant l'adresse réelle du serveur ; cellule de dépôt réservée aux copies générées. |
| Qualité du diff | Vérification propre : `git diff --check` réussi, sans diagnostic. |

## Limites et relais

Le modèle n'a pas été exécuté. La compatibilité de son code avec les critères
AST et les sorties canoniques injectées ne prouve pas ses résultats à
l'exécution. Une exécution de vérification par l'enseignant reste nécessaire
avant diffusion de son corrigé. Les points techniques ne certifient ni
l'authenticité ni la fraîcheur des sorties étudiantes, ni la généralité des
fonctions ; une solution valable non reconnue doit être réexaminée. Les cinq
explications sont à apprécier, leur seule présence ne rapporte aucun point.

Docker est absent de l'environnement local : conteneur, Colab et proxy réel
restent **NOT_TESTED localement**. La CI doit être observée après publication
de la branche ; aucun résultat distant non encore disponible n'est assimilé
à un succès. Les barèmes historiques, notamment l'anomalie préexistante du
contrôle S1, ne sont pas corrigés ou approuvés par cette mission.

Le libellé d'exclusion a été rectifié par le Prof et relu par la gouvernance :
il précise désormais que le corrigé enseignant est séparé, non exécuté et exclu
de la distribution étudiante. Il ne prétend plus que le modèle, qui conserve
le contexte contrôle du sujet, serait dépourvu de tuteur.

Absence de veto de gouvernance sur le lot examiné. Relais
**MAINTAINER_REVIEW** du fait des écritures de l'intégration. Fusion et
production restent sous décision du mainteneur ; aucun commit, aucune fusion
et aucun déploiement n'ont été effectués par la gouvernance. Toute modification
substantielle ultérieure nécessite de réévaluer les preuves concernées.
