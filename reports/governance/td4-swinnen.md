# Audit de gouvernance — TD4 S1 renforcé avec Swinnen

Mission : `pedagogy/s1-td4-swinnen`. Auditeur indépendant : sous-agent `/root/governance_td4`, rôle `TAL-Governance-Auditor`. Le présent audit ne produit ni sujet, ni correcteur, ni référence étudiante, ni règle normative. Son seul fichier écrit est ce rapport.

Base : `126cf63cbae085cf095a4488d547296a7ce7df02`, branche de la PR #31 `pedagogy/s1-swinnen-renforcement`. La nouvelle PR doit cibler cette branche tant que la PR #31 n'est pas fusionnée. Aucune fusion ni mise en production n'est autorisée par cet audit.

## Sources normatives et périmètre

Sources lues : `AGENTS.md`, `docs/AGENT_PERMISSION_MATRIX.md`, `docs/EVALUATOR_CONTRACT.md`, `docs/agents/WORKFLOW.md` et `docs/agents/TAL-Governance-Auditor.md`. Aucun de ces actifs n'est modifié par la mission.

Périmètre : trois sujets TD4-one/bis/ter, dix-huit questions, trois correcteurs de six points sous contrats v2 distincts, catalogue/routes/distribution, profils et double contexte du tuteur, références étudiantes et preuves de revue. Le TD4 historique, son correcteur et les neuf sujets de la PR #31 doivent rester inchangés.

## Séparation des rôles et autorisation

L'instruction enseignante « Passe au TD4 » prolonge explicitement le renforcement Swinnen des TD3, TD5 et TD6. Le cadrage antérieur à la conception est consigné dans `docs/pedagogy/s1-td4-swinnen.md` : les sept activités historiques, exemples, prédictions, essais et vérifications sont conservés ou renforcés. Aucune réduction, bibliothèque nouvelle ou changement de barème historique n'est annoncé ; aucun arbitrage supplémentaire de suppression n'est donc requis.

Les producteurs et réviseurs sont distincts : `/root/designer_td4` pour les supports ; `/root/prof_td4` pour le cadrage ; `/root/pedagogy_td4` pour la couverture ; `/root/editorial_td4` pour la rédaction ; `/root/code_td4` pour le code ; `/root/student_td4` pour la lecture/résolution limitée aux ressources autorisées ; `/root/governance_td4` pour cet audit. L'orchestrateur assure des écritures productrices déclarées sous les rôles Prof, Designer et Architecte ; il archive les handoffs sans s'attribuer leurs verdicts. Sa conclusion d'intégration doit rester `MAINTAINER_REVIEW`, jamais `READY_TO_MERGE`.

Les droits d'écriture observés correspondent à la matrice : sujets et documentation pédagogique pour le Designer ; cadrage/manifeste sous Prof ; application/tests sous Architecte ; références sous Étudiant-Modèle ; rapport éditorial sous Editorial-Reviewer ; présent rapport sous Governance-Auditor. Les auditeurs spécialisés n'ont pas réécrit les produits qu'ils valident.

## Preuves indépendamment contrôlées

- Branche de travail dédiée vérifiée : `pedagogy/s1-td4-swinnen`, hors `main`.
- Les douze empreintes de `tests/fixtures/td4_swinnen_source_baseline.json` ont été recalculées depuis les objets Git `126cf63`, puis comparées aux fichiers de travail : TD4 historique, correcteur historique, `app/s1_reference.py` et neuf sujets précédents identiques octet pour octet.
- Les neuf rubriques antérieures ont été comparées entre l'objet Git de base et le manifeste courant ; leurs empreintes canoniques concordent. Les trois nouvelles rubriques sont des ajouts.
- Les trois sujets possèdent chacun 43 cellules et aucune sortie enregistrée. Leurs SHA-256 concordent avec les empreintes du rapport éditorial et du rapport Étudiant-Modèle : one `1e9b4ef1f8ec4e1740b88bfc18021ac0e75338bd14b050fdccb6d2274c3a20e4` ; bis `de787ab06945e2e8c6934b4199c00cf738d94a27951ca3b2cc3446344caa46c1` ; ter `0eb734bbc132d8b83f04081f0bc617d2709aa65718c362d8059490dea19dcefd`.
- Les huit exercices Swinnen et leurs pages sont identifiés dans la matrice ; les adaptations sont distinguées des renforcements propres au cours. Dans chaque annexe, le contenu décodé du bloc `<pre>` reproduit intégralement `docs/swinnen/NOTICE_PREFACE_LICENCE.txt`, avec seulement une nouvelle ligne d'encadrement avant et après le fichier canonique. Le fichier de notice existant n'est pas modifié. Ce constat d'intégrité n'est pas un avis juridique.
- Revue pédagogique indépendante dans `docs/td4_swinnen_reviews.md` : `ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`, avec correspondance des sept activités et preuve des dix-huit questions.
- Revue rédactionnelle indépendante dans `reports/editorial/td4-swinnen.md` : `ACCEPT — LISIBILITÉ_ÉTUDIANTE_VALIDÉE`, lecture exhaustive des cellules et reprise des trois erreurs rédactionnelles. L'observation sur le commentaire canonique de restitution est explicitement mineure et ne demande pas de modification locale.
- Rapport `Corrigés modèles/TD/td4-swinnen/lecture.md` : dix-huit lectures préalables, données/productions/prérequis/essais explicités et aucun blocage déclaré. L'accès se limite aux sujets et ressources permises ; les copies restent non exécutées. Les prédictions manuelles ne sont pas présentées comme des sorties observées.
- Les trois wrappers utilisent `check_saved_notebook` ; le delta du moteur porte sur des inspections syntaxiques AST. Aucun appel d'exécution du code soumis n'est ajouté. L'exécution locale éventuelle de copies temporaires par l'intégration doit rester distincte du fonctionnement du serveur et préserver les références non exécutées.
- `git diff --check` ne signale pas de défaut d'espacement.

## Validations finales

Le handoff technique final de `/root/code_td4`, archivé dans `docs/td4_swinnen_reviews.md`, rend **ACCEPT** après correction et nouvelle vérification de TAL-AUD-001 (deux constructions distinctes pour ter Q4) et TAL-AUD-002 (maximum par parcours sans raccourci `max`/tri pour ter Q2). Il précise 32 tests du dépôt, 19 sondes initiales et 7 sondes de correction ; les GET/POST, préfixes de proxy, noms libres de fichiers, persistance et échec de sauvegarde ont été sondés. Le réviseur n'a pas écrit les corrections.

L'intégration rapporte la commande globale `python -m pytest -q --disable-warnings --maxfail=2` : **314 tests réussis, 7 ignorés, 2 283 sous-tests réussis**, en 6,34 secondes. Les sept absences sont limitées aux contrôles optionnels de `git_filter_repo`, indisponible ; aucun nouveau test n'est neutralisé. L'auditeur de gouvernance lit ces preuves attribuées aux rôles responsables et ne revendique pas une nouvelle exécution de toute la suite.

Le fichier local de QA `../qa_td4/results.json` a été lu indépendamment : les trois contrats obtiennent chacun **6/6**, sans erreur ni échec. L'intégration décrit l'exécution locale des copies dans trois processus distincts, chacun en dossier vierge avec délai limite de 20 secondes. Les six sujets/références suivis ont été relus après cette QA : toutes leurs sorties restent vides et leurs compteurs d'exécution nuls. L'exécution de validation n'est donc pas une exécution par le serveur et ne transforme pas les copies auteur.

Les autres preuves d'intégration consignées dans le handoff sont : schéma nbformat des six fichiers valide ; inventaire du tuteur et `python app/tutor_metadata.py --check` réussis ; génération temporaire puis vérification des **46 sujets actifs**, avec URL factice sous `/universite/tal`, sans aucun corrigé distribué. Les trois fichiers livrés sont présents, les routes et wrappers sont enregistrés, et chaque correcteur expose le contrat de retour commun avec maximum de six points. Les empreintes des sujets revus et les douze baselines historiques ont été recalculées encore après ces opérations : concordance complète.

L'ambiguïté temporelle de `docs/s1_distribution.md` (ancienne étape à treize cahiers, parcours courant à quinze) a été levée. Les identifiants d'évaluation distincts et la version 2 sont explicités. Aucun point bloquant ne reste ouvert.

## Limites

L'audit ne certifie ni le comportement réel de Gemini dans Colab, ni un déploiement, ni la durée effective des exercices. Quinze cahiers ne démontrent pas la faisabilité dans les huit séances initiales. L'enseignant conserve la répartition des activités, la décision de fusion et celle de production. Un score automatique ne valide pas à lui seul les explications ou l'auteur des sorties.

## Verdict de gouvernance

**CONFORME** pour le périmètre TD4 et les empreintes contrôlées ci-dessus. Matrice préalable, couverture conservée, rédaction étudiante validée, revue technique indépendante et passage Étudiant-Modèle sont présents ; les preuves techniques finales et la distribution sont consignées sans confusion avec un test de production. Les rôles de production et de revue sont séparés et aucune règle normative n'est modifiée.

Le relais à l'intégration est **MAINTAINER_REVIEW** : l'orchestrateur est producteur de l'intégration et ne peut s'autodéclarer indépendant. La PR doit rester empilée sur la branche de la PR #31 tant que cette dernière n'est pas fusionnée. La décision finale de fusion et de déploiement appartient au mainteneur.
