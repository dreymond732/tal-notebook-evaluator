# Contrôles : suppression des consignes de dépôt

## Cadrage TAL-Prof avant adaptation

Date : 25 septembre 2026. Branche : `pedagogy/controles-sans-consigne-depot`.
Source : `origin/main`, commit `2572972`.

L'enseignant demande explicitement de vérifier l'ensemble des contrôles et de supprimer les éventuelles consignes de dépôt. Cette décision autorise le retrait de ces seules informations logistiques. Aucun retrait d'objectif, d'activité, de compétence, de trace évaluée ou de barème n'est prévu. Le futur script d'injection par variable d'environnement est hors de cette intervention.

## Inventaire et périmètre

Le contrôle couvre 17 fichiers : les 11 notebooks du dossier `Notebooks contrôles finaux/`, les 3 évaluations classées `controle` dans `docs/pedagogy/tutor_sessions.json` mais rangées dans `Notebooks TD/`, et leurs 3 variantes corrigées. L'audit porte sur le texte brut de tous les fichiers et sur les cellules et métadonnées lorsque le JSON est valide ; aucune cellule n'est exécutée.

| Fichier ou groupe | Constat source | Cible autorisée |
|---|---|---|
| `Notebooks contrôles finaux/DevoirS1.ipynb` | Cellule finale « Dépot », téléchargement, adresse de dépôt et item vide | Conserver le téléchargement du fichier `.ipynb` dans une cellule de sauvegarde ; retirer l'adresse et l'instruction de dépôt, nettoyer l'item vide |
| `Notebooks contrôles finaux/S3/Controle_TD1_S3.ipynb` | Relecture finale de 5 min, instruction et lien de dépôt | Retirer instruction et lien, conserver relecture, durée, sauvegarde, traces et grille humaine |
| `Notebooks contrôles finaux/S3/Controle_TD2_S3.ipynb` | Même organisation logistique que C1 | Même transformation que C1 |
| `Notebooks contrôles finaux/S3/Controle_TD3_S3.ipynb` | Même organisation logistique que C1 | Même transformation que C1 |
| `Notebooks contrôles finaux/S3/Controle_TD4_S3.ipynb` | Dépôt dans le minutage introductif et la cellule finale ; rappel de refus du tuteur après dépôt | Renommer le temps final en sauvegarde et relecture, retirer instruction et lien, conserver les 5 min et le refus absolu d'assistance |
| `Notebooks contrôles finaux/S3/Controle_TD5_S3.ipynb` | Même organisation logistique que C4 | Même transformation que C4 |
| `Notebooks contrôles finaux/S3/Controle_TD6_S3.ipynb` | Même organisation logistique que C4 | Même transformation que C4 |
| `Notebooks contrôles finaux/S3/Controle_TD7_S3.ipynb` | Même organisation logistique que C4 | Même transformation que C4 |
| `Notebooks contrôles finaux/ControleFinalS2.ipynb` | Aucune consigne de dépôt repérée | Conserver intégralement |
| `Notebooks contrôles finaux/DevoirS1_TILT_corrigé.ipynb` | Aucune consigne de dépôt repérée | Conserver intégralement |
| `Notebooks contrôles finaux/DevoirS2.ipynb` | JSON ancien invalide, corrigé enseignant déjà exclu par le manifeste ; aucune consigne de dépôt repérée dans le texte brut | Conserver sans réparation hors mission ; validation structurelle impossible en l'état |
| `Notebooks TD/TD2 - S2.ipynb` et `TD2 - S2 - Corrigé.ipynb` | Aucune consigne de dépôt repérée | Conserver intégralement |
| `Notebooks TD/TD4_S2.ipynb` et `TD4_S2-corrigé.ipynb` | Aucune consigne de dépôt repérée ; `os_serveur` appartient à un exercice Python | Conserver intégralement, y compris cette variable pédagogique |
| `Notebooks TD/devoirMaisonS2.ipynb` et `devoirMaisonS2-corrigé.ipynb` | Aucune consigne de dépôt repérée | Conserver intégralement |

## Matrice de conservation source → cible

| Élément source | Statut | Exigence cible et preuve de revue |
|---|---|---|
| Adresse et consigne de dépôt, mention du reçu et sélection du correcteur | Logistique supprimable, retrait explicitement demandé | Absence dans les contrôles concernés ; aucun domaine du serveur recopié dans cette documentation |
| Téléchargement et sauvegarde du notebook | Obligatoire | Conservés, avec sorties exécutées et exports lorsqu'ils sont demandés |
| Temps final de 5 min et durée totale de 2 h en S3 | Obligatoire | Temps consacré à la sauvegarde et à la relecture conservé, y compris dans le minutage introductif |
| Questions, données, exemples, autonomie et transfert | Obligatoire | Cellules pédagogiques inchangées |
| Code, sorties enregistrées, marqueurs et sept traces S3 | Obligatoire | Contenus identiques à la source ; aucun code exécuté pour l'audit |
| Grilles de relecture humaine et barèmes | Obligatoire | Conservation intégrale, y compris la réserve du détail de correction à l’enseignant ; ne pas confondre la phrase logistique sur le reçu avec la grille qualitative |
| Politique du tuteur des contrôles | Obligatoire | Métadonnées et première cellule inchangées ; conserver aussi le rappel final « y compris après un dépôt », qui renforce le refus sans constituer une consigne de dépôt |
| Installation de bibliothèques et liens de ressources | Obligatoire | Liens techniques utiles conservés ; aucune suppression globale des URL |
| Profils du tuteur, routes, correcteurs et persistance | Hors modification | Aucun changement de contrat ni de code applicatif |

## Limites et critères d'acceptation

- 8 fichiers présentent des consignes à retirer ; 9 fichiers ne nécessitent pas de modification.
- `DevoirS2.ipynb` échoue à la lecture JSON à la ligne 382 ; cette anomalie préexistante est déjà documentée dans `excluded_notebooks` du manifeste (corrigé enseignant mal nommé, hors sujets), sans réparation ni validation fictive.
- Les 8 TD principaux de S3 contiennent encore des liens de dépôt : ils sont hors du périmètre demandé, limité pour l'instant aux contrôles.
- Cette intervention supprime les références visées dans la version courante des contrôles ; elle ne réécrit pas l'historique Git.
- La revue finale doit comparer les différences de cellules, confirmer la conservation ci-dessus et rechercher les consignes restantes dans les 17 fichiers.

**Verdict TAL-Prof préalable : PÉRIMÈTRE_VALIDÉ.** Adaptation logistique autorisée selon cette matrice ; couverture pédagogique à confirmer par le réviseur indépendant après modification.
