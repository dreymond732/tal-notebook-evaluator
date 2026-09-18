# S3 — matrice de couverture des TD d'origine

## Statut

- **Référence analysée** : archive fournie le 17 septembre 2026, SHA-256 `406bc452f5440fa946b257a5471a2529adace5d1e30cc049a864d10f4f40ef9d`.
- **Décision de conception** : validée par l’enseignant le 17 septembre 2026.
- **Règle** : aucun remplacement des notebooks S3 légers ne commence avant cette validation.
- **Critère** : la couverture porte sur objectifs, notions, manipulations, interprétation et autonomie ; elle ne se mesure pas au nombre de cellules.

## Références et cible

| Référence source | Rôle réel dans le corpus | Cible S3 | Statut global |
|---|---|---|---|
| `TD-0 (synthèse S2).ipynb` | Révision Python/texte et limites de `.split()` | TD0 | À renforcer |
| `TD_0_Initiation_spacy.ipynb` | Panorama spaCy et premières manipulations | TD1 puis TD3 | DÉPLACÉ |
| `TD-2 Spacy et adaptations.ipynb` | Pipeline de corpus, fonctions, filtrage et visualisation | TD2 | À renforcer |
| `TD-3_SpacyApprofondissement.ipynb` | Découverte guidée spaCy et extraction de termes | TD1–TD2 | DÉPLACÉ |
| `TD-1-exosSpacy.ipynb` | Entités, dépendances, similarité, classification | TD3 | DÉPLACÉ |
| `TD-4_Analyse critiquePlongementsLexicaux.ipynb` | Représentations, biais et contextualisation | TD4 | À réécrire fidèlement |
| `TD-5_TraductionEtAlignements.ipynb` | Corpus parallèles et alignement | TD5 | À réécrire fidèlement |
| `TD-7_Un_Projet_Complet.ipynb` | Projet terminologique bilingue et PMI | TD7 ; TD6 préparatoire nouveau | DÉPLACÉ + RENFORCÉ |

TD6 n’existe pas comme notebook source autonome : il est créé pour rendre explicites les prérequis du projet TD7, notamment la constitution d’un corpus parallèle propre, les cooccurrences et les fréquences marginales.

## Couverture détaillée

| Source : éléments substantiels | Cible et statut | Preuve attendue dans le support cible |
|---|---|---|
| **TD0** — ouvrir un fichier texte en UTF-8 ; lire une chaîne ; `.split()` ; liste, `set`, `len` ; interpréter ponctuation, casse, contractions, mots vides et morphologie. | **TD0 : CONSERVÉ + RENFORCÉ.** Ajouter un diagnostic explicite boucle, dictionnaire de fréquences et fonction courte, requis par les TD suivants. | Un corpus fourni, quatre manipulations exécutées, une fonction simple, une comparaison liste/ensemble/fréquences et une réponse interprétative. R0 devient consolidation, non substitut du TD. |
| **Initiation spaCy** — installation ; modèle français ; tokens/lemmes ; POS et tag ; NER ; dépendances avec displaCy ; similarité ; extraction personnes/organisations ; `EntityRuler`. | **TD1 : CONSERVÉ** pour installation, `Doc`, phrases, tokens, lemmes, POS. **TD3 : DÉPLACÉ** pour NER, dépendances, similarité et `EntityRuler`. | TD1 comporte exemples et exercices autonomes sur chaque annotation fondamentale. TD3 comporte les quatre traitements avancés sur un même corpus, avec interprétation des limites. |
| **spaCy et adaptations** — visualiser un `Doc` ; créer une liste de lemmes ; agrégation de listes ; `Counter` ; fonction de fréquence des noms ; paramètres ; mots triviaux ; extraction verbes ; stopwords spaCy ; nuage de mots filtré. | **TD2 : CONSERVÉ + RENFORCÉ.** L’ensemble reste dans TD2 ; R2 ne fait qu’entraînement préparatoire. | Fonctions `frequences_noms` et `frequences_verbes` paramétrées ; comparaison brut/filtré ; `Counter` ; stopwords ; visualisation ; commentaire sur pertinence et limites. |
| **spaCy approfondissement** — segmentation en phrases ; comptage de tokens par phrase ; POS/lemmes ; noms/verbes ; groupes nominaux/noms propres ; fichier de corpus ; fréquence des POS ; top 3 ; lemmes verbaux. | **TD1 : DÉPLACÉ** (segmentation/POS/lemmes). **TD2 : DÉPLACÉ** (fichier, fréquences POS, verbes). **TD3 : DÉPLACÉ** (groupes nominaux). | Exercices distincts, non résolus, sur corpus fourni ; production de tableaux/liste et interprétation. |
| **Exercices spaCy avancés** — entités nommées sur texte long ; relation verbe–sujet ; similarité mots/phrases ; prototype de classification. | **TD3 : CONSERVÉ.** La classification reste une activité critique et limitée : elle compare une heuristique de similarité à une véritable classification, sans la présenter comme telle. | NER, relation syntaxique, similarité avec avertissement sur le modèle vectoriel, puis analyse de l’échec/limite du prototype de classement. |
| **Plongements lexicaux** — vecteurs statiques ; polysémie d’« avocat » ; voisins lexicaux ; axe de genre et projections de professions ; contextualisation BERT ; désambiguïsation ; biais et adaptation de domaine. | **TD4 : CONSERVÉ + RÉÉCRIT.** Les objectifs critiques sont maintenus, mais le protocole vectoriel doit être reproductible et les limites méthodologiques explicites. | Deux représentations comparées, mesure documentée, interprétation prudente, exercice de biais et analyse contextualisée. Les modèles, versions, ressources et langues sont déclarés. |
| **Traduction et alignements** — corpus parallèle ; deux modèles spaCy ; comptage bilingue de noms ; segmentation ; longueurs de phrases ; alignement 1–1, 1–2, 2–1 ; heuristique de longueur ; amélioration gloutonne. | **TD5 : CONSERVÉ.** Le corpus fourni est licite et local ; l’alignement par longueur est présenté comme baseline, non comme méthode fiable générale. | Corpus EN/FR, fonction bilingue, segmentation, alignements, évaluation manuelle d’erreurs et algorithme glouton. |
| **Projet final** — lire deux corpus alignés ; termes mono-mots ; cooccurrences ; glossaire par fréquence ; groupes nominaux ; fréquences EN/FR ; formule PMI ; glossaire final et comparaison. | **TD6 : RENFORCÉ** (préparation : corpus, alignement validé, cooccurrences et fréquences). **TD7 : CONSERVÉ** (groupes nominaux, PMI et analyse comparative). | TD6 produit `source.en.txt` et `cible.fr.txt` versionnés, un alignement contrôlé et les structures de fréquence. TD7 implémente les fonctions et interprète les faux positifs. |

## Éléments à retirer, soumis à arbitrage explicite

| Source | Élément | Statut proposé | Motif |
|---|---|---|---|
| `TD-4_Analyse critiquePlongementsLexicaux.ipynb` | Blocs répétés sur liens magnet/BitTorrent | `SUPPRIMÉ` | Contenu étranger aux objectifs de représentation sémantique. |
| `TD-5_TraductionEtAlignements.ipynb` | Récupération de flux torrent et longs blocs sur BitTorrent/magnet | `SUPPRIMÉ` | Ni nécessaire au corpus parallèle ni compatible avec une activité pédagogique reproductible. |
| `TD-1-exosSpacy.ipynb` | « classification » par similarité présentée comme classification | `RENFORCÉ`, non supprimé | Conserver l’exercice comme contre-exemple critique, avec explicitation de sa limite. |
| Tous les notebooks sources | Solutions intégrées au support étudiant | `DÉPLACÉ` | Conserver les solutions dans un notebook enseignant distinct ; ne pas les livrer dans la version étudiante. |

## Décisions validées par l’enseignant

1. Valider la suppression des blocs magnet/BitTorrent étrangers au cours.
2. Valider TD6 comme nouveau TD préparatoire au projet final.
3. Valider le repositionnement de NER, dépendances, similarité et `EntityRuler` en TD3.
4. Valider le maintien de la classification par similarité comme activité critique, et non comme méthode de classification.
5. Valider que les TD0–TD2 complets remplacent les versions légères fusionnées ; R0–R2 restent des passerelles facultatives/de consolidation.

## Suite engagée

- produire TD0, TD1 et TD2 complets, avec jeux de données intégrés ou versionnés ;
- conserver les versions légères uniquement comme archives de transition, jamais comme support distribué ;
- mettre à jour les correcteurs formatifs seulement pour les activités effectivement déposées ;
- transmettre la matrice remplie au Pedagogy-Reviewer pour le verdict `COUVERTURE_PÉDAGOGIQUE_CONSERVÉE`.
