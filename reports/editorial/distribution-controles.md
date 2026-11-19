# Revue éditoriale indépendante — Distribution des contrôles et rangement S1

## Périmètre

- Branche : `code/distribution-controles`, référence `ab18bfa1da370c457ddfb4bb7fe2e182b189a8fa` ; diff de travail relu.
- Mandat : ranger le contrôle final S1 dans le sous-dossier S1, rendre tous les sujets de contrôle du catalogue disponibles dans `dist/`, sans ouvrir le dépôt d’un sujet inactif.
- Réviseur : agent indépendant `editorial_review` ; aucun passage du produit n’a été écrit ou modifié par le réviseur.
- Sources relues : nouvelle section de distribution de `README.md`, `docs/s1_distribution.md`, `docs/pedagogy/controle_s1_rangement.md`, cellule `saving_cell()` et sélection des fichiers dans `app/prepare_student_notebooks.py`.
- Source S1 comparée : `Notebooks contrôles finaux/DevoirS1.ipynb` à la référence ci-dessus et `Notebooks contrôles finaux/S1/Controle_final_S1_python.ipynb` dans le lot courant.
- Aucune réécriture de question n’est annoncée ni observée ; la revue ne renouvelle donc pas la lecture pédagogique détaillée des 30 questions déjà validées.

## Verdict

**`ACCEPT` — `LISIBILITÉ_ÉTUDIANTE_VALIDÉE` pour la nouvelle consigne de sauvegarde ; classement et documentation de distribution compréhensibles pour l’enseignant.**

Aucun blocage rédactionnel relevé. Ce verdict ne remplace pas les tests techniques de génération, de nettoyage des anciens chemins et de refus du dépôt inactif.

## Preuves de conservation et de compréhension

| Élément | Observation vérifiée | Conséquence |
|---|---|---|
| Déplacement S1 | Après normalisation du seul `metadata.tal_tutor.session.notebook`, les JSON ancien et nouveau sont strictement égaux | Les 70 cellules, les données, les questions, les commentaires, les sorties et les autres métadonnées sont conservés ; pas de réduction pédagogique à inférer du rangement |
| Empreinte normalisée | SHA-256 `7f47d44429deacf175723feb28e3d842ac489125509e0a38a43794c5c2c5f611`, identique avant et après | La preuve annoncée dans la note de rangement correspond à la comparaison effectivement réalisée |
| Identité du contrôle S1 | `Controletilt-s1`, version 2, même évaluateur | Le nom de fichier change sans annoncer une nouvelle épreuve ni une nouvelle règle de correction |
| Choix enseignant | README : après `bash deploy.sh`, choisir les fichiers à communiquer aux étudiants dans `dist/` ; tableau par semestre et type de support | L’enseignant sait quel dossier ouvrir et quel fichier diffuser ; le final S1 est nommé explicitement `Controle_final_S1_python.ipynb` |
| Modèles de correction | README : `Corrigés modèles/`, hors de la distribution étudiante | La sélection à diffuser est distincte des corrigés ; aucune suggestion de transmettre les solutions |
| Contrôle sans dépôt actif | La cellule finale devient du Markdown intitulé « Sauvegarde du travail » | La copie ne présente pas de bouton, d’adresse ou de code de dépôt qui ne fonctionnerait pas |
| Action étudiante | Vérifier l’exécution, télécharger le `.ipynb` avec ses sorties, recevoir les modalités de remise de l’enseignant | La consigne décrit une sauvegarde locale et ne promet pas qu’elle transmet la copie ; elle n’invente ni canal de remise ni preuve de réception |
| Destinataire de la notice | Aucun mot sur le catalogue, l’activation du serveur, le manifeste ou la construction de `dist/` dans la nouvelle cellule visible | Les détails de maintenance restent dans la documentation enseignante et technique |
| État du final S2 | L’entrée courante reste `active=false`, mode contrôle, évaluateur nul | La mise à disposition du fichier est distinguée, dans la documentation, de l’ouverture d’un correcteur |
| Étendue documentaire | La sélection courante contient 47 notebooks et 46 entrées actives | Les nombres nouvellement annoncés sont cohérents avec le catalogue lu ; ils ne constituent pas une prétention d’exécution des notebooks |

## Vérifications réalisées sans exécution de notebook

Un script Python de lecture JSON et d’appel au générateur de confiance a vérifié :

1. l’égalité intégrale du contrôle S1 avant/après, à l’exception du seul chemin déclaré du profil ;
2. l’empreinte normalisée et les 70 cellules conservées ;
3. la sélection de 47 fichiers, dont le final S2 seul est inactif ;
4. la transformation en mémoire de la copie inactive avec `distributable(..., can_submit=False)` : dernière cellule Markdown, absence d’adresse injectée et de marqueur `__TAL_PUBLIC_URL__`, toutes les autres cellules identiques à la source ;
5. la source inactive toujours identique après cet appel : aucune sauvegarde du notebook source effectuée.

Le code des cellules n’a pas été exécuté. Cette vérification du texte généré n’est pas un essai de remise ni un test du correcteur.

## Limites et relais

- Aucun test visuel dans Colab ou un navigateur ; aucun déploiement, dépôt serveur ou transfert réel à un étudiant.
- La revue ne démontre pas le remplacement atomique d’une distribution complète, le retrait de l’ancien chemin sur le serveur ni l’absence de régression technique : ces points relèvent du lot de tests et de la revue de code.
- Les références historiques à l’ancien chemin restent légitimes lorsqu’elles nomment leur révision ; la documentation courante présente explicitement le nouveau chemin.
- Aucun nouveau modèle étudiant n’est nécessaire pour un déplacement dont l’identité du contenu est démontrée et pour une notice de sauvegarde sans nouvelle activité évaluée.

Transmettre le présent verdict avec les résultats techniques à la gouvernance et à l’intégration. La diffusion des fichiers, la fusion et la mise en production demeurent sous décision du mainteneur.
