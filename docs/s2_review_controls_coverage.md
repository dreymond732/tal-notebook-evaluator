# Contrôles S2 : bilan de conservation et de classement

Mission TAL-Pedagogy-Designer sur la branche `pedagogy/s2-complete-review`, à partir de `b7650e3d035846a67014b94e463a08cd43b67fb5`. La conception suit la matrice du Prof `docs/pedagogy/s2_complete_review_coverage.md`, validée par l’orchestrateur avant modification des notebooks.

## Supports concernés

| Source historique | Cible dans `Notebooks contrôles finaux/S2/` | Questions | Placement |
|---|---|---:|---|
| `Notebooks TD/TD2 - S2.ipynb` | `Controle_TD2_S2_algorithmique.ipynb` | 13 | Après TD3 et ses consolidations obligatoires |
| `Notebooks TD/TD4_S2.ipynb` | `Controle_TD4_S2_ensembles.ipynb` | 14 | Après TD5 et le travail sur les ensembles |
| `Notebooks TD/devoirMaisonS2.ipynb` | `Devoir_maison_S2_approfondissement.ipynb` | 30 | Après TD5, transposition comprise |
| `Notebooks contrôles finaux/ControleFinalS2.ipynb` | `Controle_final_S2_algorithmique_fichiers.ipynb` | 18 | Après TD6 ; source inactive, hors distribution |

Les numéros TD2 et TD4 sont des identifiants historiques de contrôles. Ils ne signifient pas que ces contrôles doivent précéder les TD3 et TD5 qui en préparent les acquis.

## Contrat de conservation

Les 75 activités, données, consignes et cellules de réponse sont conservées dans leur ordre relatif. Les sources pédagogiques historiques restent intégralement présentes, avec deux exceptions de forme validées avant conception : le titre du contrôle TD4 indique désormais S2 au lieu de S3 ; les 57 affichages `print(f"Résultat Qn : {variable}")` des trois supports actifs deviennent `print("Résultat Qn :", variable)`. Ce changement ne modifie ni calcul, ni donnée, ni activité. Une précision est ajoutée après la consigne Q9 du contrôle TD4 : le coût de recherche O(1) est moyen et ne signifie pas instantanéité. Les cellules d’identité et de tuteur sont régénérables pour la version 2. Aucun exemple, quiz, indice, corrigé ou étayage supplémentaire n’est introduit dans un contrôle. Les commentaires d’aide historiques ne sont pas supprimés. Les barèmes des trois contrôles actifs restent à 20, 40 et 40 points.

Chaque cellule possède un identifiant stable et des métadonnées de rôle ; les réponses Q1 à Qn sont uniques. Le contrôle final reçoit les identifiants manquants sans déclarer de correcteur actif. Les métadonnées du notebook portent la version 2. L’identité comprend nom, prénom, classe et numéro étudiant. La première cellule Markdown porte le refus strict d’assistance, synchronisé avec les métadonnées du tuteur. La dernière cellule contient la restitution HTML canonique avec le seul substitut `__TAL_PUBLIC_URL__` ; aucune adresse réelle ni sortie HTML exécutée n’est enregistrée dans la source.

## Limite explicite du contrôle final

Le sujet final contient 18 questions. Le module ancien qui semble lui correspondre porte sur 11 autres questions : aucun rattachement n’est inventé. Le final reste `active: false`, `evaluator: null`, hors génération automatique de `dist/`. Sa cellule d’organisation indique que diffusion et correction nécessitent la décision de l’enseignant. La présence du dispositif HTML dans la source ne vaut pas activation du dépôt ni publication du sujet. Une prochaine intervention devra définir un barème par question et un correcteur adapté avant activation.

## Vérification et relais

La vérification du producteur porte sur le nombre et l’ordre des 75 questions, les sources historiques, les identifiants, la cohérence des métadonnées et les cellules de restitution. Elle ne remplace pas les revues indépendantes : verdict de couverture demandé au Pedagogy-Reviewer, validation des évaluateurs à l’auditeur code, puis gouvernance et intégration. Aucun notebook étudiant n’est exécuté.

## Résultat du contrôle de production

Les quatre nouveaux fichiers contiennent respectivement 34, 36, 37 et 29 cellules, soit les cellules d’origine plus une cellule d’organisation et une restitution finale. Les 75 cellules-réponses gardent leurs données, leur ordre et leurs expressions de calcul ; seuls les 57 affichages mentionnés ci-dessus sont normalisés. Les identifiants existants sont préservés (`cell.id`, sinon ancien `metadata.id`) ; les absents reçoivent un identifiant stable lié au support et à l’indice de la cellule d’origine. Le contrôle final conserve ses dix-huit affichages historiques, puisqu’aucun évaluateur ne lui est rattaché.
