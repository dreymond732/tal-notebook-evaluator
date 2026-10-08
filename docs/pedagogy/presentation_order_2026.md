# Présentation et ordre du parcours — cadrage du 7 octobre 2026

## Sources et périmètre

Référence technique : `1ee4581`. Référence de présentation de l'enseignant : les six notebooks de `drive-download-20261007T062707Z-1-001.zip`, comparés aux sources actuelles (toutes différences textuelles et code inspectées). Les versions anciennes R0/R1/R2 v1 dans l'archive Devoirs ne sont pas réimportées : elles ne constituent pas une référence technique compatible. Les sources originelles 2025 ne sont pas nécessaires pour cette modification de présentation, qui ne recompose aucune activité.

Ce lot adapte la présentation des douze supports S3 et leur ordre ; le placement titre + contexte caché s'applique aux 35 sujets à profil tuteur, sans révision implicite de leurs contenus pédagogiques. Les règles pérennes relèvent du producteur normatif autorisé, pas de TAL-Prof. Aucune nouvelle notion, bibliothèque, question ou exigence évaluée. Aucun changement des identifiants internes, versions, barèmes, routes ou AST pédagogiques. Les données et tâches restent intégrales, y compris observations, essais et interprétations.

## Matrice préalable source → cible

Les numéros de question ci-dessous désignent exactement les questions de la référence technique : chaque Q conserve données, production, prérequis, guidage/autonomie et obligations. Les changements portent seulement sur noms, ordre, notices et placement du contexte.

| Ordre | Source sous `Notebooks TD/S3/` | Cible | Activités conservées | Statut d'usage |
|---:|---|---|---|---|
| 1 | TD0_S3_diagnostic_texte.ipynb | Identique | Q1–Q7 : lecture/découpage, formes/fréquences, normalisation, critique/transfert | Entrée du S3 ; présentation visible Gemini ici seulement. |
| 2 | R0_S3_python_texte.ipynb | Identique | Q1–Q4 : fonctions et comptages Python | Remédiation après TD0, avant TD1.a selon besoins. |
| 3 | TD1_S3_fondations_spacy.ipynb | TD1.a_S3_fondations_spacy.ipynb | Q1–Q6 : annotations, phrases, filtres, dépendances et transfert | Introduction spaCy. |
| 4 | R1_S3_doc_spacy.ipynb | TD1.b_S3_doc_spacy.ipynb | Q1–Q4 : Doc, forme/lemme/POS, noms et verbes | Bonus facultatif après TD1.a ; aucun prérequis obligatoire créé pour la suite. |
| 5 | TD1B_S3_entites_similarite_regles.ipynb | TD1.c_S3_entites_similarite_regles.ipynb | Q1–Q4 : entités, extraction, similarité, règles | Après TD1.a, avant R2/TD2 ; ne suppose pas le bonus TD1.b. |
| 6 | R2_S3_frequences_reutilisables.ipynb | Identique | Q1–Q4 : fonctions de fréquences et filtres | Avant TD2, après initiation spaCy ; ne suppose pas TD1.b. |
| 7 | TD2_S3_analyse_corpus.ipynb | Identique | Q1–Q7 intégrales | Après R2. |
| 8 | TD3_S3_concordances_citations.ipynb | Identique | Q1–Q7 intégrales | Après TD2. |
| 9 | TD4_S3_cooccurrences.ipynb | Identique | Q1–Q7 intégrales | Après TD3. |
| 10 | TD5_S3_associations.ipynb | Identique | Q1–Q7 intégrales | Après TD4. |
| 11 | TD6_S3_visualisations.ipynb | Identique | Q1–Q7 intégrales | Après TD5. |
| 12 | TD7_S3_audit_llm.ipynb | Identique | Q1–Q7 intégrales | Après TD6. |

Total : 71 questions inchangées. Les trois renommages sont des changements de noms et chemins, pas des déplacements de contenus dans un support futur. Tous les supports restent livrés immédiatement. Les identifiants `TD1_S3`, `R1_S3`, `TD1B_S3` du manifeste et `td1-s3`, `td-r1-s3`, `td1b-s3` des évaluateurs demeurent stables.

## Arbitrages de présentation explicitement demandés

| Élément source | Présentation cible | Garantie de conservation |
|---|---|---|
| Cellule initiale cachée isolée puis titre | Première cellule Markdown commence par le titre, puis le commentaire HTML complet du tuteur **dans la même cellule**, sous le titre | Contexte identique dans Colab et HTML ; texte de règles conservé hors renommages déclarés, aucune extension de permissions. |
| Minutages, durées indicatives et tableaux de temps | Retirer les durées visibles, garder l'ordre des activités sans budget affiché | Pas de retrait d'étape ni d'activité ; aucun changement de durée réelle promis. |
| Longues notices identification, formats acceptés, versions | Notices légères et cellules d'identité conservées | Champs, valeurs initiales, types et validation restent inchangés ; pas de données étudiantes importées. |
| Présentations répétées du tuteur Gemini | Présentation visible seulement dans le premier TD du parcours S3, TD0 | Tuteur caché toujours dans chaque support ; pas de nouvelle dépendance au bonus. |
| Procédure répétée d'autoévaluation | Une explication initiale utile ; restitutions finales fonctionnelles conservées | Ne pas supprimer critères locaux de vérification ou demandes d'interprétation sous prétexte d'éviter répétitions. |
| Retouches des six fichiers utilisateur | Reprendre les préférences utiles, harmoniser les titres réellement visibles TD1.a/b/c | Ne pas copier aveuglément erreurs de prose ni contenus techniques exportés. |

Les retouches utilisateur incluent une URL publique injectée dans leurs exports ; la source conserve `__TAL_PUBLIC_URL__` et le déploiement continue l'injection. Le TD1.b retouché affirme « ici vous construisez des fonctions pour filtrer et compter », alors que ses quatre exercices portent sur Doc et sélection de tokens : ne pas propager cette incohérence ; réserver cette description à R2. Les références restantes TD1/R1/TD1B dans la prose doivent être actualisées vers les noms pédagogiques sans remplacer aveuglément les identifiants techniques. Les formats et limites de réponse propres à une question restent des consignes utiles, pas des notices à effacer.

## Acceptation et vérifications

Comparer source/cible question par question ; AST des cellules code, données, identifiants de réponses, contrats et tuteurs conservés ; vérifier les chemins du catalogue, l'ordre visible et les renvois. Le manifeste ne change que chemins, titres et désignations des prérequis, après feu vert ; aucune permission de notion ou bibliothèque modifiée. Les 35 sujets doivent posséder titre puis commentaire caché dans la même première cellule Markdown, sans reliquat d'une cellule cachée isolée. La fusion du titre ne déplace que le H1 : l’introduction, les objectifs et le cours restent intégralement présents. Le retrait des présentations répétées de Gemini ne retire aucune tâche d’analyse des productions Gemini ni les noms de corpus ou fichiers correspondants. Les contrôles conservent le refus d'aide. Tester synchronisation, génération et distribution ; contrôler les douze supports S3 en lecture visible et cachée, et le placement global dans les 35 sujets.

La révision de présentation ne vaut pas restauration historique ni nouvelle validation pédagogique de tous les semestres. Elle n'oblige pas une relecture individuelle systématique des travaux et ne prouve pas le comportement effectif de Gemini dans Colab.

## Validation préalable

ACCEPT préalable indépendant de TAL-Pedagogy-Reviewer le 7 octobre 2026, avant conception : 71 questions conservées, TD1.b facultatif, changements limités à la présentation, maintien des introductions/objectifs et des activités sur les productions Gemini. Ce verdict ne valide pas encore la réalisation. Aucun notebook modifié par TAL-Prof.


## Bilan de réalisation — version gelée pour revue indépendante

Les douze supports S3 ont reçu les retouches de présentation ; les trois fichiers TD1.a/b/c sont livrés avec les identifiants et versions antérieurs. L’inventaire courant porte les nouveaux chemins, l’ordre TD1.a/b/c et le caractère facultatif du bonus. Les matrices des anciens lots restent des références historiques ; leur numérotation décrit leur version de livraison.

Le manifeste ne modifie que trois chemins et les désignations de prérequis (dont R2 qui n’exige plus le bonus). Aucun acquis ni bibliothèque autorisés ajoutés. Le mécanisme titre H1 puis commentaire caché dans la même première cellule a été synchronisé sur les 35 sujets par l’intégration. La politique de tutorat décrit cette disposition et conserve les deux copies du contexte. Les modifications normatives et techniques relèvent de leurs producteurs distincts.

### Empreintes du lot transmis aux réviseurs

| Support S3 | Questions | SHA-256 |
|---|---:|---|
| `R0_S3_python_texte.ipynb` | 4 | `ac4081b73115dcdabeb245c75490bf8d1a47645a3e777c7862682cad56281301` |
| `R2_S3_frequences_reutilisables.ipynb` | 4 | `c73877a7cda40928f7dcae07b82dd4ee8700c39898a17a5d355234c06f92c079` |
| `TD0_S3_diagnostic_texte.ipynb` | 7 | `9b61a6e1d1f5ccd7e37535219425b0c4166b984416b0ee90560271e4a1b27c7e` |
| `TD1.a_S3_fondations_spacy.ipynb` | 6 | `538e1e2df525066a2d96d341691316a3f860d6ca8201b70aecd4b9ae7b827ccd` |
| `TD1.b_S3_doc_spacy.ipynb` | 4 | `ed74ea3148b20467e359045f94d46ad94faf641d5a0d19fd375a3e753ec3a981` |
| `TD1.c_S3_entites_similarite_regles.ipynb` | 4 | `e213bd45b1c153256f10f74f294a2d0a3f96b5db34481941cf2148041199b5e5` |
| `TD2_S3_analyse_corpus.ipynb` | 7 | `c75dd20ea2bf45243cd1298c9960c8688e283bf9508ae295ae82794d948c1107` |
| `TD3_S3_concordances_citations.ipynb` | 7 | `1d1ce7f366e4614df55817ca8a0314991951caec514edb3485311da417d165ed` |
| `TD4_S3_cooccurrences.ipynb` | 7 | `3102cfb711cc8c20498b8fc25dd2a1d603e591b9a95e5af860fd435195286e3d` |
| `TD5_S3_associations.ipynb` | 7 | `948aa55de73748ab686f111d668e859db02896b8676f4824134f68177e0d1615` |
| `TD6_S3_visualisations.ipynb` | 7 | `107b1812439b39401ae1389a365490ecde1912bce76625dd52e7ac453386efcf` |
| `TD7_S3_audit_llm.ipynb` | 7 | `25cb948f91f2832e6adc60bdf5a743013b27ad2dcf2b2e996cbc991efdf89bca` |

### Verdicts de réalisation

**Pédagogie : ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE**, rendu indépendamment par TAL-Pedagogy-Reviewer (`s1_ped_reviewer`) après comparaison de `1ee4581`, des six fichiers de l’enseignant et des douze supports. Les 71 questions gardent données, exemples, essais, productions et interprétations. Les retraits concernent minutages et notices ; formats et critères locaux restent présents. TD1.b reste facultatif, sans prérequis implicite pour R2 ou TD2. Les références à Gemini comme matériau d’analyse sont conservées. Les corrections éditoriales finales précisent le caractère facultatif de R0 et retirent les dernières notices ; aucune activité supplémentaire supprimée.

**Technique : ACCEPT**, rendu indépendamment par TAL-Code-Auditor (`s1_code_auditor`) : 43 tests ciblés réussis ; les 35 snapshots sont identiques au parent Git ; migration idempotente et conservation vérifiée, exception bornée au libellé du prérequis TD1.a dans le contrôle. Aucun mécanisme d’exécution de code étudiant ajouté. Le constat TAL-AUD-P01 concernant les anciennes empreintes de contrôles est résolu sans recalcul des fixtures historiques.

**Éditorial : ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE**, rendu indépendamment par TAL-Editorial-Reviewer (`s1_editorial`) : douze supports, 449 cellules et 71 questions, ainsi que la structure des 35 profils. Rapport et empreintes finales : `reports/editorial/presentation-order-2026.md`. Lecture indépendante question par question : `Corrigés modèles/TD/presentation-order-2026/lecture.md`.

Les réserves de vérification des acquis antérieurs (lemme en TD0, `is_alpha` en TD4) ne sont pas présentées comme résolues par cette modification de forme. La cellule fonctionnelle de restitution reste canonique, y compris son commentaire technique et ses étapes de dépôt ; l’allègement concerne les notices pédagogiques répétées. Cette limite est explicitement consignée par la revue éditoriale.

Intégration : **302 tests réussis** ; synchronisation des 35 profils vérifiée ; `check`, `render` et `verify` réussis pour 34 notebooks distribuables avec l’URL neutre `https://example.org/tal`. Aucune nouvelle exécution des exercices spaCy ; le code est conservé. `git diff --check` sans erreur. Les sources ne reprennent aucune URL de déploiement des copies de l’enseignant. La présentation n’établit pas une restauration historique ni une nouvelle validation des contrôles ou des contenus S1/S2 ; l’application effective du tuteur par Colab reste non vérifiée.
