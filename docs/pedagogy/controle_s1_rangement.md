# Contrôle S1 — Rangement par semestre

## Décision et périmètre

Le 19 novembre 2026, l'enseignant autorise le rangement du contrôle final S1 dans le dossier S1 et l'export de tous les contrôles dans `dist/`. Le déplacement ci-dessous est un reclassement de fichiers : il ne constitue pas une révision curriculaire, ne change aucune question et ne modifie pas le contrat v2 approuvé.

| Source avant rangement | Emplacement courant | Statut |
|---|---|---|
| `Notebooks contrôles finaux/DevoirS1.ipynb` | `Notebooks contrôles finaux/S1/Controle_final_S1_python.ipynb` | DÉPLACÉ, contenu pédagogique intégralement conservé |
| Références historiques liées à `2445c9e18357dc6a99a8e516bf0d7bd7e462fd42` | Références historiques inchangées | CONSERVÉES ; elles désignent bien l'ancien emplacement à cette révision |
| `Notebooks contrôles finaux/DevoirS1_TILT_corrigé.ipynb` | Inchangé | Archive du corrigé v1, hors distribution |

La référence de comparaison immédiate est le sujet v2 à la révision `ab18bfa1da370c457ddfb4bb7fe2e182b189a8fa`. La matrice pédagogique de la révision reste `controle_s1_td1_5_coverage.md` ; les objectifs, acquis, données, productions, autonomie et barème de ses 30 questions sont inchangés.

## Preuve de conservation

La comparaison JSON avant/après normalise **uniquement** `metadata.tal_tutor.session.notebook` pour tenir compte du nouveau chemin. Après cette normalisation, les deux objets sont strictement égaux. Aucun autre champ du notebook n'est modifié.

- Les 70 cellules, leurs identifiants, leurs sources, leurs sorties et leurs métadonnées sont conservés.
- Les 30 questions, le barème de 36 points, l'identité d'évaluateur `Controletilt-s1` et le contrat version 2 sont conservés.
- Le contexte caché du tuteur, sa copie Colab et son profil sont identiques, à l'exception du seul chemin de notebook dans le profil.
- L'empreinte SHA-256 du JSON normalisé (clés triées, séparateurs compacts, UTF-8) est `7f47d44429deacf175723feb28e3d842ac489125509e0a38a43794c5c2c5f611` pour les deux versions.
- Le fichier reste en JSON compact. Aucune exécution, aucune soumission et aucune sortie nouvelle ne sont produites par ce rangement.

Le manifeste des sessions et les références documentaires courantes sont mis à jour. Les références historiques des rapports antérieurs restent datées et ne sont pas réécrites. L'alignement du catalogue, du modèle et du générateur, ainsi que les tests de distribution, sont contrôlés séparément dans la même mission.

## Formulation de sauvegarde des contrôles sans correcteur

La notice prévue pour le contrôle final S2 est une consigne de sauvegarde, distincte d'un dépôt : « Vérifiez que toutes les cellules ont été exécutées, puis téléchargez votre notebook au format .ipynb avec ses sorties. Les modalités de remise vous seront précisées par l’enseignant. » Elle est compréhensible sans promettre une transmission automatique ou inventer une modalité de remise. Sa présence dans une copie générée ne vaut pas preuve de réception du travail.
