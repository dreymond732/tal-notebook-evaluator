# Révisions S3 : évaluation et distribution v2

## Mise en service

R0, R1 et R2 changent de contrat : **ne pas redistribuer les anciennes copies de `dist/`**. Après fusion et déploiement du correctif, régénérer la distribution avec `app/prepare_student_notebooks.py` et la configuration `TAL_PUBLIC_URL`, puis vérifier les copies produites. Distribuer les trois notebooks **version 2**. Les sources Git n’ont ni URL privée ni cellule de dépôt ; le générateur injecte cette cellule HTML finale dans les copies. Aucune copie ancienne n’est migrée.

Le routage automatique `/submit` refuse une version absente ou périmée avec le texte exact `mauvaise version du notebook`. Les routes directes de tous les sujets S3 exigent désormais les métadonnées du notebook et la version du catalogue : ce refus ne doit pas pouvoir être contourné par `/eval/...`. Les routes historiques explicitement choisies en S1/S2 conservent leur compatibilité. Les correcteurs autres que R0–R2 ne changent pas de critères ni de barème.

R0–R2 exigent aussi l’identité complète (nom, prénom, classe, numéro étudiant) et les quatre cellules de réponse identifiées. Le numéro est une chaîne de 1 à 64 lettres ASCII, chiffres, tirets ou soulignements ; il reste inchangé dans le CSV et le nom des fichiers. Les versions v1 ou absentes sont refusées avant correction ; une identité incomplète empêche la persistance.

Les nouvelles soumissions sont stockées dans `soumissions/td-r0-s3-v2/<classe>/`, `soumissions/td-r1-s3-v2/<classe>/` et `soumissions/td-r2-s3-v2/<classe>/`. Cela sépare les CSV v2 enrichis des CSV v1 existants. Les anciennes données restent intactes. Les fichiers notebook et rapport comportent le numéro étudiant pour distinguer les homonymes. Les routes publiques ne changent pas.

## Méthode et limites

`app/revision_s3.py` sélectionne une réponse par `metadata.tal.question` et `role: answer`. Il analyse son AST et une sortie marquée unique enregistrée dans cette cellule. Les cellules d’exemple, d’infrastructure et les sorties d’autres questions ne contribuent pas. La dépendance d’une sortie envers ses calculs est recherchée en remontant les affectations précédant le `print` ; une affectation écrasée, un calcul sans rapport avec la sortie ou une fonction à retour constant ne suffisent pas. Les fonctions antérieures explicitement autorisées sont disponibles même si leur propre trace manque, afin de ne pas propager artificiellement les pertes de points. Les cellules peuvent être déplacées.

Le barème reste quatre points techniques. Types et valeurs des résultats sont vérifiés ; booléens et nombres ne sont pas assimilés. L’ordre des clés et les permutations des ex æquo de `most_common()` sont acceptés. Le retour montre le code et les observations Q4 pour relecture, avec échappement HTML par le template. Le score ne note ni le sens ni la longueur d’une explication. Les rapports et CSV annoncent le caractère technique provisoire.

Le serveur n’exécute jamais les cellules ni les expressions Python déposées. `ast.literal_eval` sert uniquement à lire les résultats littéraux enregistrés et bornés en taille. L’analyse statique n’est pas une preuve d’exécution authentique ni de correction pour toutes les entrées. Une autre solution correcte non reconnue requiert une relecture ; ce mécanisme ne prétend pas empêcher la falsification délibérée des traces.

## Provenance de la référence spaCy

Références produites le 1er octobre 2026 par du **code enseignant indépendant**, exécuté séparément des notebooks étudiants : Python 3.12.14, spaCy 3.8.7, `fr_core_news_sm` 3.8.0, thinc 8.3.11, numpy 2.5.3, typer et typer-slim 0.16.1. Pipeline : tok2vec, morphologizer, parser, attribute_ruler, lemmatizer, ner. L’architecte a reproduit les annotations dans cet environnement. Aucune dépendance spaCy n’est ajoutée au serveur de correction : il utilise la référence canonique enregistrée.

Code de référence (données exclusivement fournies par l’enseignant) :

```python
import spacy
nlp = spacy.load("fr_core_news_sm")
for texte in [
    "Les traducteurs analysent rapidement les nouveaux documents.",
    "Les corpus contiennent des textes. Les textes contiennent des termes et des répétitions.",
]:
    print([(t.text, t.lemma_, t.pos_, t.is_stop) for t in nlp(texte)])
```

Les triples forme/lemme/POS complets figurent dans `R1_TOKENS` et `R2_TOKENS` du moteur. Pour `is_stop`, les valeurs vraies sont les tokens `Les`, `les`, `des`, `et` ; les autres sont fausses dans ces deux textes. Aucun NOUN retenu n’est donc supprimé par `is_stop` dans le texte R2. Le retrait mesurable de `texte` est dû aux exclusions personnalisées.

Le modèle produit ici des annotations discutables : `analysent` est étiqueté ADV, et `corpus` PRON. La référence vérifie une reproduction de ces annotations, pas une vérité grammaticale : R1 Q4 attend bien une liste VERB vide ; R2 exclut `corpus` du décompte NOUN. Les sujets demandent de constater les limites du modèle.

## Vérification

`tests/test_revision_s3_v2.py` contient des fixtures de code et des traces écrites séparément, **sans exécution des solutions étudiantes** : références complètes, faux résultats, marqueurs seuls, exemples trompeurs, variantes d’espaces, paramètres renommés, alias de lemme, ex æquo, cellules déplacées, métadonnées invalides, erreurs et types malformés, dépendances sans trace, retours constants, affectations écrasées, ancien contrat, persistance v2 et échappement HTML. Les tests d’intégrité conservent la fixture historique ; les seules exceptions explicites sont les trois supports dont le contrat évolue, contrôlés séparément contre la spécification pédagogique.
