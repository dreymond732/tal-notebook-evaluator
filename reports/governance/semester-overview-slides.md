# Gouvernance — diaporamas d’organisation S1, S2 et S3

8 octobre 2026. Auditeur indépendant : TAL-Governance-Auditor. **Verdict : CONFORME** sur les trois HTML de synthèse et les éléments de livraison de ce lot.

## Autorisation, périmètre et rôles

Demande enseignante explicite transmise dans la mission : « mets çà dans une PR. Puis fais de même avec le S1 et le S2 », après validation du diaporama S3 corrigé. Elle autorise l'intégration et la publication en PR des trois présentations. Elle n'autorise pas leur fusion ni un déploiement.

Branche et parent vérifiés directement : `pedagogy/semester-overview-slides`, `590b9a6c78fc6b27f8985e060c6ea2325367f652`. Les modifications concernent trois HTML d'organisation, le README d'accès, un test navigateur séparé et les rapports/cadrages associés. Aucun notebook, correcteur, module applicatif, profil de tuteur ou actif normatif modifié. Aucun contrat évaluateur, barème, nouvelle bibliothèque ou activité n'est introduit par cette synthèse.

TAL-Prof a établi `docs/pedagogy/semester_slides_coverage.md`, accepté indépendamment avant conception par TAL-Pedagogy-Reviewer. Les 233 questions recensées délimitent les sources : elles ne sont pas déclarées réévaluées par cette mission. Le Designer a rédigé les deux HTML S1/S2 ; l'intégration a repris la copie S3 validée et produit README/test/documentation. Les réviseurs pédagogique, éditorial, technique et le lecteur étudiant sont distincts des producteurs. L'auditeur de gouvernance n'a écrit que ce rapport.

L'intégration ayant produit des éléments du lot, son statut de livraison est **MAINTAINER_REVIEW**, et non `READY_TO_MERGE`. Les avis favorables indépendants ne remplacent pas la décision de fusion du mainteneur.

## Preuves finales indépendantes

| Rôle | Verdict et preuve consultée | Portée |
|---|---|---|
| TAL-Pedagogy-Reviewer | Statut final de `semester_ped_review` consulté directement : `ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` | 36 diapositives confrontées au cadrage et aux sources ; fidélité de la synthèse, pas nouvelle évaluation de chaque question |
| TAL-Editorial-Reviewer | `reports/editorial/semester-overview-slides.md` : `ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE` | Lecture exhaustive des 36 diapositives, destinataire étudiant, titres, portée des correcteurs et traces à garder |
| TAL-Étudiant-Modèle | `Corrigés modèles/TD/semester-overview-slides/lecture.md` : lecture finale favorable, A1 levée | Lecture des seuls HTML et règles du rôle ; aucun notebook, correcteur, test ni corrigé consulté ; aucune réponse ou soumission |
| TAL-Code-Auditor | Statut final consulté directement : `ACCEPT` après exécution indépendante du test navigateur final | Navigation, impression, vue d'ensemble mobile, History refusée et vrais iframes opaques ; aucun changement applicatif |

Les corrections finales sont relues et intégrées aux empreintes finales : titre TD5 explicite sur la diapositive S2 n°6 ; jonction contrôle TD4 et DM après TD5 et avant TD6, sans dépendance entre ces deux évaluations ; espacement des libellés « Contrôle » dans les récapitulatifs S1/S2. Le test comporte une assertion sur le dernier chevauchement constaté. Le défaut visuel n'a pas été déclaré résolu par une seule annonce de modification CSS : l'intégration rapporte un nouveau rendu vérifié et l'auditeur technique reproduit le contrôle.

La suggestion A2 du lecteur sur « citations exactes » en S3 reste non bloquante : l'éditorial l'a examinée dans l'ensemble du support, notamment la diapositive 11. Elle ne justifie pas de modifier silencieusement le S3 validé, conservé exactement.

## Vérifications directement effectuées par la gouvernance

- Lecture des règles communes, du workflow, des permissions, de la fiche gouvernance, du cadrage, du rapport technique, du rapport éditorial et de la note étudiante finale.
- Inspection de la branche, du parent, du diff et des fichiers nouveaux ; périmètre limité à cette mission et absence de modification de notebook/code évaluateur/tuteur/normes.
- Comparaison SHA-256 de la source S3 validée `/workspace/scratch/299f4372d5c4/s3-revision/Organisation_progression_S3.html` et de la copie intégrée : égalité exacte `eed123016fc7a789f2584f137adbc042bb4401af9bbb6ac767b7fd1cf5011877`.
- Recalcul des trois empreintes, concordant avec le rapport éditorial et le bilan technique : S1 `1680dcc4163824e389038a3500039dea0a2838c1292300d7488b3022aca90457` ; S2 `a2e9fe91e7986fb38c0e257bc44f6558dd40c275e1e5bf98b68fc562906c9e04` ; S3 empreinte ci-dessus.
- Comptage de 12 sections dans chacun des trois HTML ; aucun lien S1/S2 et 25 liens S3. Le lien Drive S3 provient de la version validée ; aucun lien de dossier non fourni n'est inventé. Les permissions effectives de ce dossier ne sont pas vérifiées par la gouvernance.
- Lecture du test navigateur et des accès README : HTML autonomes distribués séparément de `prepare_student_notebooks.py`, sans nouvelle dépendance serveur. `git diff --check` réussi.

Ces contrôles propres sont distincts des essais de rendu, que la gouvernance n'a pas réexécutés.

## Vérifications rapportées et limites

L'intégration rapporte une exécution Playwright finale sur les 36 diapositives, reproduite par le Code-Auditor : sélection, vue d'ensemble, Échap, clavier, History indisponible, mobile 390 px, absence d'erreur JavaScript et de chevauchement avec les pieds de page. Le contrôle des libellés des récapitulatifs est également réussi. Aucun code étudiant n'est exécuté. L'auditeur confirme l'absence de ressources distantes nécessaires à l'affichage.

L'intégration rapporte une inspection visuelle des 24 nouvelles diapositives et des pages corrigées, puis trois PDF de 12 pages chacun et une inspection de la page imprimée S1 la plus dense. Ces résultats sont consignés dans `docs/semester_overview_slides.md`. Les tests sont sous Chromium ; ils ne constituent pas une certification de tous les navigateurs ni des conditions réelles de projection.

Les parcours restent ceux des sources : DM S1 après TD5 ; numérotation historique S2 ; final S2 inactif absent du parcours distribué ; R0 conditionnel et TD1.b facultatif dans S3. La portée partielle des correcteurs et les traces à conserver ne sont pas transformées en garantie de maîtrise, de généralité des programmes ou de qualité des interprétations. L'anomalie préexistante du barème du contrôle S1 demeure documentée hors périmètre, sans total erroné publié dans les slides.

La suite Python et Docker existante n'est pas annoncée exécutée localement pour ce lot ; leur CI doit être observée après publication. Le test navigateur reste une commande distincte, non implicitement ajoutée à cette CI. Aucun essai en classe, observation de Gemini/Colab, contrôle de droits Drive, restauration historique ou révalidation intégrale des notebooks n'est revendiqué.
