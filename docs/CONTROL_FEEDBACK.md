# Dépôts de contrôle et restitution

## Comportement

`app/routes.py` associe chaque évaluateur à un mode explicite dans
`EVALUATOR_MODES`. Un identifiant absent ou un mode invalide bloque l'accès
avec un message d'indisponibilité. Le nom de l'URL ne détermine plus le mode.

Pour un TD, le retour formatif existant est conservé. Pour un contrôle,
la page publique affiche seulement le formulaire ou, après sauvegarde réussie,
« Copie reçue et enregistrée ». Aucun score, statut de question, réponse,
solution ou détail du correcteur n'est transmis au template public.
Les exceptions et erreurs renvoyées par le correcteur donnent un message
générique ; leur diagnostic reste dans les journaux serveur.
Les erreurs administratives de dépôt (fichier absent ou extension incorrecte)
restent explicites.

La copie, le CSV et le rapport HTML détaillé historique sont conservés dans
`soumissions/<évaluation>/<classe>/`. Le rapport comporte le score et le détail
des validations, selon le correcteur ; les solutions attendues ne sont pas
ajoutées au template historique. Les réponses étudiantes sont échappées avant
rendu, car ce template utilise historiquement `safe`.
Une erreur de sauvegarde ne produit jamais d'accusé de réception positif.
La persistance existante n'est pas transactionnelle : un échec tardif peut
laisser un CSV ou une copie partielle, à contrôler par l'enseignant.

## Supports ambigus du semestre 2

| Identifiant | Support | Titre présent | Mode provisoire |
|---|---|---|---|
| `td2-S2` | `Notebooks TD/TD2 - S2.ipynb` | Contrôle S2 : renforcement et algorithmique | `controle` |
| `td4-S2` | `Notebooks TD/TD4_S2.ipynb` | Contrôle S3 : manipulation des ensembles | `controle` |

Ces deux supports sont traités comme des contrôles pour ne pas divulguer de
retour pendant une épreuve. L'enseignant doit arbitrer leur statut et le
semestre annoncé avant une éventuelle reclassification. Leurs URL, modules
et titres du sélecteur restent inchangés pour préserver les liens existants.

## Restitution après clôture

Aucune route publique de téléchargement des copies ou rapports n'est ajoutée.
L'application ne dispose pas d'une authentification enseignant/étudiant
permettant une publication individualisée. Aucun commutateur global de
publication n'est donc introduit.

Après clôture décidée par l'enseignant, celui-ci récupère les rapports sur le
serveur avec son accès habituel, vérifie l'identité du destinataire et remet
chaque résultat par son canal institutionnel individuel. Le répertoire
`soumissions/` et les journaux doivent rester hors des répertoires publics du
reverse proxy. Ce changement ne peut garantir une configuration extérieure
à Flask. Une restitution web future demanderait une authentification et
des autorisations par copie.

Ce dispositif contrôle uniquement le retour de l'application de dépôt.
Il ne désactive pas l'assistant Colab et ne garantit pas l'absence d'aide
extérieure. Les instructions pédagogiques embarquées sont un autre mécanisme.

## Vérification

`tests/test_control_feedback.py` utilise des correcteurs simulés, sans
exécuter de code étudiant. Les tests vérifient : GET/POST, conservation privée
des résultats, absence de route publique de rapport, masquage des erreurs,
échecs de persistance, mode explicite même pour une URL contenant `td`,
maintien du retour TD, extension incorrecte et préfixe du reverse proxy.
