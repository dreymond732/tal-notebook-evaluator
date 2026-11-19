# Revue éditoriale indépendante — Archives et progression courante

## Périmètre et verdict

- Branche : `code/archives-progression`, référence de comparaison `501413c3e5c216138595e68bee714d7902e9a393`.
- Mandat : ranger les versions remplacées et anciens corrigés dans `historique/`, laisser les seuls supports courants dans les dossiers de semestre et dans `dist/`, préserver les copies commencées et les notes.
- Réviseur indépendant : `editorial_review`, rôle TAL-Editorial-Reviewer ; aucun texte du produit ni notebook n’a été modifié par ce réviseur.
- Documents relus : `historique/README.md`, `docs/pedagogy/archives_progression.md`, section distribution et passage stockage S1 de `README.md`, `Notebooks TD/README.md`, `Notebooks TD/S1/README.md`, `Notebooks TD/S2/README.md`, `Notebooks contrôles finaux/S2/README.md`, `docs/s1_distribution.md`, ainsi que leurs différences de travail.
- Vérifications complémentaires : mapping des douze fichiers archivés, empreintes, sélection de distribution et existence des supports courants mentionnés. Aucun exercice de notebook n’est réécrit ; il ne s’agit pas d’une nouvelle revue pédagogique des questions.

**Verdict : `ACCEPT` — `LISIBILITÉ_DOCUMENTATION_PROGRESSION_VALIDÉE`.**

Les trois incohérences documentaires signalées pendant la revue sont corrigées et relues. Aucun blocage rédactionnel ne demeure dans le périmètre déclaré. Ce verdict ne vaut pas essai du déploiement, de la migration des soumissions ou des routes de correction.

## Preuves de lecture et de conservation

| Élément | Preuve observée | Effet pour le lecteur |
|---|---|---|
| Emplacement des anciens supports | `historique/README.md` annonce d’abord leur exclusion du parcours et de la distribution ; les douze lignes donnent source, archive, raison et référence courante | Les anciennes synthèses et les corrigés ne sont pas présentés comme des travaux à commencer |
| Passage S1 courant | README S1 : quinze cahiers, ordre A → B → C pour TD3–TD6, liens vers les noms A/B/C existants ; DM après TD5-C | Le parcours courant est identifiable sans suivre les anciennes variantes one/bis/ter |
| Récapitulatif général S1 | `Notebooks TD/README.md` présente sept thèmes répartis en quinze cahiers, avec liste des fichiers courants | Le nombre de thèmes n’est pas confondu avec le nombre de notebooks à parcourir |
| Copies déjà commencées | Les README distinguent archives hors parcours et correcteurs de compatibilité conservés ; le lecteur est averti de ne pas changer les métadonnées d’une ancienne copie | Le rangement ne laisse pas entendre qu’il faut recommencer ou convertir manuellement un travail entamé |
| Conservation des notes | README et note de classement annoncent l’absence de recalcul et de déplacement des copies remises | La conservation pédagogique est distinguée d’une migration de résultats ; le comportement effectif reste à confirmer par les tests techniques |
| Nature des anciennes solutions | Les huit lignes de corrigés ne prétendent pas résoudre automatiquement les supports courants ; les correspondances non revalidées le signalent | Une simple correspondance de nom ne devient pas une promesse de corrigé courant |
| Archives illisibles | Deux JSON invalides sont explicitement nommés comme tels, avec conservation sans réparation | L’archivage n’est pas présenté comme une remise en état de fichiers tronqués |
| S3 | R0 et R2 sont des remédiations distinctes conservées ; TD1.b est un bonus facultatif, avec noms actuels et renvoi au parcours S3 | Les révisions/remédiations ne sont pas assimilées à des versions remplacées sur le seul critère de leur nom |
| Final S2 | Sujet courant à dix-huit questions, conservé et exporté, correction automatique inactive ; archive tronquée `DevoirS2.ipynb` explicitement distincte | Absence de correcteur et ancien intitulé ne conduisent pas à supprimer le sujet courant ni à lui appliquer un corrigé d’un autre contrôle |
| Choix des fichiers à diffuser | README racine et document de distribution : `dist/`, quarante-trois notebooks courants, quinze TD S1 ; modèles et archives hors distribution | Les enseignants savent où prendre les versions destinées aux étudiants |
| Référence historique et rangement | Les chemins internes des archives sont annoncés comme provenance figée ; leurs nouvelles adresses physiques sont données séparément | Un ancien chemin dans une archive n’est pas présenté comme un lien courant à réparer en réécrivant le fichier |

## Observations résolues pendant la revue

| ID | Constat initial | Gravité et reprise demandée | Résolution observée |
|---|---|---|---|
| TAL-EDIT-ARCH-001 | `Notebooks TD/README.md` citait encore `TD1_S3_fondations_spacy.ipynb` et `R1_S3_doc_spacy.ipynb`, absents sous ces noms | Important pour la navigation : les renommer dans la documentation selon les fichiers existants, en préservant le statut facultatif de TD1.b | Noms `TD1.a_S3_fondations_spacy.ipynb` et `TD1.b_S3_doc_spacy.ipynb` présents ; R0/R2 distincts et renvoi au README S3 courant |
| TAL-EDIT-ARCH-002 | README racine, section migration : « les 19 TD du S1 » pouvait contredire les quinze cahiers courants | Clarification nécessaire : distinguer le périmètre de stockage historique du parcours à distribuer | Le passage nomme désormais « les 15 cahiers courants et les 4 anciennes synthèses du S1 » ; il reste dans la section de migration des répertoires |
| TAL-EDIT-ARCH-003 | `docs/s1_distribution.md`, section historique : « Le parcours utilise désormais treize cahiers TD » paraissait décrire le présent | Mineur : dater grammaticalement l’étape passée sans changer ses informations | « Lors de cette étape, le parcours comportait treize cahiers TD » ; l’extension TD4 est également formulée au passé |

## Vérifications statiques effectivement réalisées

Un script de lecture des fichiers et de Git, sans exécution de cellule, a comparé les douze chemins du manifeste `tests/fixtures/archives_progression_source_sha256.json` à la révision de référence :

- les douze archives sont présentes sous `historique/<ancien chemin>`, leurs octets strictement identiques à ceux du parent Git et leurs deux empreintes SHA-256 égales à la valeur enregistrée ;
- les douze anciens emplacements physiques ont disparu, sans duplication dans les dossiers de semestre ;
- les soixante-trois autres notebooks suivis au parent sont tous présents et strictement identiques en octets ; aucune source courante, aucun modèle restant ni notice source n’est réécrit ;
- `distribution_sources()` sélectionne quarante-trois notebooks, dont treize contrôles, sans entrée archivée ;
- `Notebooks TD/S1/` contient quinze notebooks ;
- R0, R2 et TD1.b S3 appartiennent toujours à la sélection courante ;
- le final S2 demeure la seule entrée courante inactive pour la correction automatique.

Les deux JSON invalides n’ont pas été réécrits ni exécutés : la vérification de conservation porte sur leurs octets. La lecture de la sélection du générateur n’a lancé aucun notebook ni déployé de service.

## Limites et relais

- Pas de test visuel dans Colab ou navigateur, pas de génération/diffusion réelle à des étudiants et pas de vérification du serveur vivant.
- Le maintien effectif des anciennes routes, l’affichage du menu, le remplacement des anciennes distributions et la conservation du stockage sont des propriétés techniques : les annonces documentaires ont été relues, leurs tests relèvent de l’audit de code et de l’intégration.
- Les documents historiques datés peuvent conserver les anciens chemins à leur révision. Cette revue ne les convertit pas en documentations courantes et ne revalide pas le fond des anciens corrigés.
- La consigne de sauvegarde S2 produite par la mission de distribution précédente n’est pas modifiée dans ce lot ; aucun nouveau texte étudiant de notebook n’est soumis à validation ici.

Relais à la gouvernance avec les preuves techniques. Aucun ajustement rédactionnel supplémentaire n’est requis dans le périmètre examiné ; la fusion et le déploiement restent sous décision du mainteneur.
