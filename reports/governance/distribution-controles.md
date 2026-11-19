# Gouvernance — Rangement S1 et distribution des contrôles

**Verdict : `CONFORME`.**

Audit indépendant du 19 novembre 2026, rôle `TAL-Governance-Auditor`. Le réviseur n'a produit ni générateur, ni support, ni tests ; son écriture se limite au présent rapport. Ce verdict permet de poursuivre vers la revue du mainteneur. Il ne vaut ni fusion, ni déploiement réel du service, ni communication des fichiers aux étudiants.

## Mandat et référence

L'enseignant demande de ranger correctement le contrôle S1 et de préparer les contrôles dans `dist/` via le déploiement, en conservant le choix des fichiers à distribuer.

- Branche observée : `code/distribution-controles`.
- Référence immédiate : `ab18bfa1da370c457ddfb4bb7fe2e182b189a8fa`.
- Déplacement approuvé : `Notebooks contrôles finaux/DevoirS1.ipynb` → `Notebooks contrôles finaux/S1/Controle_final_S1_python.ipynb`.
- Preuve de conservation examinée : `docs/pedagogy/controle_s1_rangement.md`, avec mapping source–cible, référence Git et comparaison JSON limitée au chemin du profil.
- Sources normatives relues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et fiche `TAL-Governance-Auditor`.

La préparation d'une copie dans `dist/` est distinguée de l'activation d'un correcteur et de la diffusion effective à une classe. Aucun nouveau destinataire, envoi ou partage n'est ajouté à ce mandat.

## Périmètre et rôles

Le diff examiné contient le générateur `app/prepare_student_notebooks.py`, le catalogue, le manifeste des sessions, le déplacement du sujet S1, le chemin correspondant du modèle et sa lecture préalable, les références documentaires courantes, les adaptations de tests et les deux rapports de revue.

Les rôles de production et les revues code, pédagogique et éditoriale sont distincts selon les relais reçus. La revue éditoriale indépendante est archivée dans `reports/editorial/distribution-controles.md`. Le présent auditeur n'a modifié aucun fichier audité.

Aucun actif normatif n'est changé. Les fixtures historiques restent gelées : les tests passent par un mapping explicite des chemins courants et historiques. Il n'est pas nécessaire de retirer une protection historique pour accepter une modification de contenu : l'égalité intégrale des objets JSON après normalisation du seul chemin démontre ici qu'aucune modification de contenu pédagogique n'a eu lieu.

## Conservation du sujet et du modèle

Comparaison indépendante reproduite entre le sujet à la référence et le fichier courant, après normalisation **uniquement** de `metadata.tal_tutor.session.notebook` : **égalité JSON stricte**.

- Les 70 cellules, leurs identifiants, leurs sources, leurs sorties et leurs autres métadonnées restent identiques.
- Les 30 questions, le barème de 36 points, l'évaluateur `Controletilt-s1` et sa version 2 sont inchangés.
- Le titre et les deux contextes du tuteur de contrôle restent identiques ; seul le chemin de fichier du profil est actualisé.
- SHA-256 du JSON normalisé, clés triées et séparateurs compacts : `7f47d44429deacf175723feb28e3d842ac489125509e0a38a43794c5c2c5f611`, identique à la note de rangement.
- La même comparaison a été reproduite pour le modèle : seul son chemin de profil change. Ses solutions, cellules, identité fictive et état non exécuté sont conservés.

Le catalogue, le manifeste du tuteur et la documentation courante pointent vers le nouveau chemin. Les références explicitement historiques restent liées à leur ancienne révision. L'ancien corrigé v1 reste une archive hors distribution.

Ce lot ne supprime ni ne déplace une activité évaluée vers un support futur. La note de rangement et l'égalité du contenu suffisent à caractériser le reclassement ; il n'est pas présenté comme une nouvelle validation curriculaire des 30 questions.

## Distribution et activation

| Point audité | Observation dans le code et les tests | Conclusion |
|---|---|---|
| Sélection des sources | `distribution_sources()` sélectionne les entrées actives ou de mode contrôle, exclusivement depuis le catalogue de confiance | 47 notebooks autorisés : 34 TD et 13 contrôles |
| Liste autorisée | Le vérificateur compare l'ensemble réel des `.ipynb` à la sélection exacte du catalogue | Aucun modèle, corrigé historique ou notebook étranger exporté |
| Activation serveur | `active_sources()` reste limité aux entrées actives ; le catalogue conserve le final S2 inactif avec évaluateur nul | 46 évaluateurs actifs, aucune activation implicite |
| Contrôle inactif | La copie générée remplace uniquement sa cellule finale par une consigne Markdown de sauvegarde | Pas d'URL de dépôt fictive, de marqueur non remplacé ou de code de soumission inopérant |
| Source du final S2 | Inchangée ; toutes les autres cellules et métadonnées sont conservées dans la copie générée | Aucun changement de question ou de contrat évalué |
| Dépôt du final S2 | Le test POST sur `/submit` reçoit HTTP400 et n'appelle pas la persistance | La préparation du fichier ne contourne pas le refus d'un dépôt inactif |
| Génération complète | Préparation dans un répertoire temporaire, vérification avant remplacement, manifeste explicite | La distribution doit être cohérente avant installation |
| Ancien lot de 46 fichiers | Le test migre le manifeste précédent, retire l'ancien chemin racine S1 et ajoute le final S2 | Le rangement ne laisse pas l'ancienne copie gérée en doublon |
| Fichiers étrangers | Destination non gérée, fichiers étrangers et liens symboliques restent des motifs de refus | Pas de nettoyage arbitraire d'un dossier utilisateur |
| Incident d'installation | Auditeur code : panne I/O simulée après préparation ; restauration de l'ancienne distribution et de son manifeste | Pas de perte observée dans ce scénario contrôlé |
| Commande de déploiement | `deploy.sh` appelle déjà check/render/verify ; le générateur élargi est utilisé par ce chemin | Aucun changement de commande nécessaire pour préparer les 47 fichiers |

Les copies distribuables sont vérifiées par comparaison à une transformation attendue de chaque source. Le programme ne parcourt pas arbitrairement tous les `.ipynb` du dépôt pour les transmettre. Aucun dossier de soumissions n'est lu ou déplacé par ce rangement.

## Revues spécialisées reçues

- **Pédagogique : `ACCEPT` / `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`.** La conservation des contenus est démontrée ; aucun acquis, résultat, point ou niveau d'autonomie n'est retiré.
- **Éditoriale : `ACCEPT` / `LISIBILITÉ_ÉTUDIANTE_VALIDÉE` pour la nouvelle notice de sauvegarde.** Rapport indépendant relu : le texte demande une sauvegarde locale avec sorties et renvoie les modalités de remise à l'enseignant, sans promettre une transmission. La documentation indique clairement où choisir les fichiers et distingue les modèles de la distribution.
- **Technique : `ACCEPT`.** Relais final de l'auditeur indépendant : 62 tests réussis, dont les cinq nouveaux tests ; revue de la liste autorisée, de la migration du manifeste, du final S2 inactif et de la restauration après incident I/O. Aucune réserve bloquante transmise.

Aucun verdict négatif non résolu ne subsiste dans les relais reçus. Les preuves techniques ne remplacent pas les verdicts de contenu ou de lisibilité.

## Vérifications effectives

Reproduites par le présent auditeur, sans exécution du code de cellule d'un notebook :

- `python -m unittest discover -s tests -p '*distribution*.py' -q` : **19 tests, OK**.
- `python app/tutor_metadata.py --check` : réussi, code de sortie 0.
- `python app/prepare_student_notebooks.py check` : **47 notebooks, check OK**.
- Génération et vérification indépendantes dans un répertoire temporaire avec `https://example.test/universite/tal` : **47 fichiers, render/verify réussis**.
- Calcul de la sélection : 47 fichiers exacts, 34 TD, 13 contrôles, 46 entrées actives et aucun chemin de modèle.
- Comparaisons JSON strictes sujet et modèle avant/après normalisation du seul chemin ; empreinte normalisée concordante.
- `git diff --check` : réussi.

Observé dans le journal final du producteur, sans revendiquer une seconde exécution complète par la gouvernance :

- `python -m unittest discover -s tests -v` : **498 tests en 19,323 s, OK**, journal de session `distribution-tests.log`.
- Relais du producteur : compilation, check/render/verify 47 et appel réel de `bash deploy.sh` avec Docker **simulé uniquement**, ayant produit la distribution attendue. Les tests reproduits par le présent auditeur comprennent également des simulations des commandes Compose V1/V2 ; leurs messages ne sont pas une preuve de démarrage d'un service réel.

## Limites et relais

Aucun conteneur ou service de production n'a été démarré par ces vérifications ; aucune copie étudiante n'a été exécutée ou soumise au serveur réel. Le test du contrôle inactif utilise un client Flask local et un stockage de test. Aucun fichier n'a été envoyé à un étudiant.

La nouvelle notice de sauvegarde ne constitue pas une remise du travail ni une preuve de réception. L'enseignant choisit les fichiers à distribuer et les modalités de remise. Le correcteur final S2 reste inactif.

Le lot peut poursuivre vers la PR avec **`MAINTAINER_REVIEW`**, l'intégration étant auto-produite. Le présent auditeur ne rend pas `READY_TO_MERGE`. La fusion, le déploiement réel et la diffusion des fichiers restent sous décision du mainteneur.
