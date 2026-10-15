# Diaporamas d’organisation S1, S2 et S3

## Objet et périmètre

Demande : intégrer le diaporama S3 validé dans une PR et réaliser les équivalents S1/S2. Branche `pedagogy/semester-overview-slides`, base `590b9a6c78fc6b27f8985e060c6ea2325367f652`.

Les trois fichiers `Notebooks TD/S*/Organisation_progression_S*.html` sont des supports d’orientation autonomes. Ils présentent l’ordre, les objectifs, la portée partielle des correcteurs et les traces à réutiliser. Ils complètent les notebooks sans remplacer leurs énoncés, activités ou exigences. Aucun notebook, correcteur, barème, contrat de restitution ou profil de tutorat n’est modifié.

Le S3 reprend exactement le fichier validé après réparation de la vue d’ensemble et ajout des diapositives consacrées à la correction partielle. Son SHA-256 est `eed123016fc7a789f2584f137adbc042bb4401af9bbb6ac767b7fd1cf5011877`. Tous ses liens pointent vers le dossier Drive fourni. Aucun dossier S1/S2 n’ayant été fourni, leurs titres restent sans lien.

Les HTML sont distribués séparément des copies produites par `prepare_student_notebooks.py`. Le README donne accès aux trois sources. Une fois téléchargés, ils s’ouvrent directement dans le navigateur ; aucune ressource distante n’est nécessaire à leur affichage.

## Références et limites

Le cadrage préalable est dans [la matrice de couverture](pedagogy/semester_slides_coverage.md). Il compare les supports actuels, leur historique disponible, le catalogue actif et les correcteurs. L’inventaire des 233 questions sert à délimiter les contenus ; il ne vaut pas validation indépendante de chacune d’elles.

Le parcours S1 place le devoir intermédiaire après TD5 et avant TD6. Le S2 conserve les numéros historiques TD3, TD5 et TD6, avec les contrôles TD2 et TD4 intercalés et le devoir d’approfondissement. Le contrôle final S2 inactif reste exclu du parcours actif. L’anomalie de total du contrôle S1 relevée dans la matrice préexiste à ce lot : aucun total n’est annoncé dans les diapositives et aucun barème n’est corrigé ici.

## Vérification reproductible

Le script `tests/check_semester_slides.cjs` utilise Node.js et Playwright avec Chromium. Il reste indépendant de la suite Python et de la CI existante ; aucune nouvelle dépendance n’est nécessaire au serveur.

Dans un environnement disposant de Playwright et de son navigateur :

```bash
node tests/check_semester_slides.cjs
```

Pour choisir un Chromium déjà installé et conserver les captures/PDF :

```bash
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/chemin/vers/chromium \
SLIDES_ARTIFACT_DIR=/tmp/semester-slides \
node tests/check_semester_slides.cjs
```

Le script accepte aussi une liste de chemins HTML pour une vérification ciblée. Il contrôle les liens, l’autonomie du fichier, les identifiants, le sélecteur, la vue d’ensemble, le retour par sélection et Échap, la navigation au clavier, le fonctionnement lorsque l’API History est refusée, la vue d’ensemble sur écran de 390 pixels, l’absence de débordement horizontal et le placement du contenu avant le pied de page à l’écran et à l’impression. Il détecte les erreurs JavaScript et peut produire un PDF par semestre. Le code des notebooks étudiants n’est jamais exécuté.

## Résultats et revues

Vérifications du 8 octobre 2026 après gel des HTML :

- Test Playwright réussi sur les 36 diapositives, puis reproduit indépendamment par TAL-Code-Auditor. Vue d’ensemble, sélection, Échap, navigation, API History refusée, vue d’ensemble mobile, impression et absence d’erreur JavaScript vérifiés. Un essai complémentaire de l’auditeur dans de vrais iframes d’origine opaque confirme le fonctionnement du script partagé.
- Inspection visuelle des 24 nouvelles diapositives S1/S2 et contre-vérification des pages corrigées. L’espacement des libellés « Contrôle » dans les récapitulatifs a été corrigé ; une assertion de régression vérifie ce chevauchement. Le parcours S2 montre désormais la jonction des deux évaluations avant TD6. Le rendu S3 validé est conservé à l’identique.
- Trois PDF de 12 pages produits, sans page supplémentaire ; absence de chevauchement avec le pied de page contrôlée sur toutes les diapositives. Inspection de la page imprimée la plus dense du S1 (tableau des sept correcteurs).
- Aucune ressource externe d’affichage ; aucun lien S1/S2 ; 25 liens S3 vers le seul dossier fourni. Aucun code étudiant exécuté.

Empreintes SHA-256 des supports revus :

| Support | SHA-256 |
|---|---|
| S1 | `1680dcc4163824e389038a3500039dea0a2838c1292300d7488b3022aca90457` |
| S2 | `a2e9fe91e7986fb38c0e257bc44f6558dd40c275e1e5bf98b68fc562906c9e04` |
| S3 | `eed123016fc7a789f2584f137adbc042bb4401af9bbb6ac767b7fd1cf5011877` |

Avis indépendants : TAL-Pedagogy-Reviewer a rendu `ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE` après lecture des 36 diapositives ; TAL-Code-Auditor a rendu `ACCEPT` après exécution indépendante du test final. Les rapports [éditorial](../reports/editorial/semester-overview-slides.md), [lecture étudiante](../Corrig%C3%A9s%20mod%C3%A8les/TD/semester-overview-slides/lecture.md) et [gouvernance](../reports/governance/semester-overview-slides.md) consignent leurs constats et leurs verdicts distincts.

Limites : ces essais utilisent Chromium et ne constituent pas une validation exhaustive de tous les navigateurs. Ils ne remplacent pas la relecture question par question des notebooks. La suite Python et les contrôles Docker existants sont exécutés par la CI de la PR ; le test navigateur reste une commande séparée.

L’intégrateur a également produit des éléments techniques de ce lot : le verdict d’intégration applicable est `MAINTAINER_REVIEW`. La fusion et la mise en production restent sous décision du mainteneur.
