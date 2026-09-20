# Évaluation formative du parcours S3 d’audit textométrique

## Changement de contrat

La progression TD0–TD7 utilise huit évaluateurs `td0-s3` à `td7-s3`, les modules
`app_correction_TD0_S3.py` à `app_correction_TD7_S3.py` et le moteur `s3_audit.py`.
L’entrée `td0-s3` est conservée avec son nouveau contrat JSON. Les anciens marqueurs
`Résultat Qn :` ne sont plus évalués pour ce sujet. Les passerelles R0, R1, R2 et
leurs évaluateurs sont conservés ; les contrats S1, S2 et des contrôles ne changent pas.

Chaque module expose `check_notebook(content_str, filename)` et retourne le tuple
`(score, details, max_score, student_info, error_msg)`.

| Séance | Points maximum | Objet du contrôle automatique |
|---|---:|---|
| TD0 | 7 | Diagnostic sur un texte fixé et preuve des limites du découpage |
| TD1 | 6 | Conformité structurelle des annotations et cohérence avec les textes |
| TD2 | 7 | Fréquences et cohérence des synthèses ; annotations à vérifier humainement |
| TD3 | 7 | Localisation, concordances et citations sur des microcas |
| TD4 | 7 | Marges, paires, union, fenêtres, frontières et invariants |
| TD5 | 7 | Proportions, normalisation, sensibilité et dénominateur nul |
| TD6 | 7 | Données des représentations, positions et retour au texte |
| TD7 | 7 | Contrat de mesure, moteur, citation, cas de transfert et verdict conditionnel |

Un point est attribué par trace conforme au contrat détaillé dans le sujet et le
module. Les productions sur Faguet, l’analyse de Gemini, les commentaires et la
qualité visuelle doivent être relus par l’enseignant. Le score n’est pas une note
sur la qualité scientifique de l’audit ou sur sa capacité à détecter des erreurs
chez un LLM. Les checks de structure sont annoncés comme tels : ils ne certifient
pas la justesse linguistique de spaCy.

## Traces enregistrées

Chaque question affiche exactement un objet JSON sur une ligne, par exemple :

```python
print('S3_TD4_Q1:', json.dumps(resultat_Q1, ensure_ascii=False))
```

Le `print` explicite est placé au niveau principal d’une cellule de code, avec
exactement deux arguments ; le marqueur est une chaîne littérale. Le correcteur
attend le marqueur de la séance déposée. Les sorties Jupyter doivent être
conservées. Les blocs `stream/stdout` d’une cellule sont concaténés avant lecture
pour supporter leur fragmentation par Jupyter.

Il faut un affichage reconnu et une seule ligne correspondante, dans la même
cellule, sans erreur d’exécution enregistrée. Les commentaires, les cellules
Markdown, les sorties `stderr`, les fonctions d’affichage non appelées et les
marqueurs dupliqués ne satisfont pas ce contrat. Une cellule au Python invalide
n’est pas reconnue. Les sorties non JSON, les clés répétées et les nombres non
finis (`NaN`, `Infinity`) sont refusés. Un booléen n’est pas un entier. Les valeurs
réelles admettent une tolérance numérique de `1e-8` après l’arrondi à six décimales
lorsqu’il est demandé ; les comptages entiers exigent des entiers. L’ordre des clés
d’un objet JSON n’a pas d’importance ; l’ordre d’une liste compte lorsqu’il fait
partie du contrat.

## Sécurité et limites

Le serveur ne charge aucun modèle spaCy et n’exécute jamais le code soumis. Il
lit le JSON, analyse la syntaxe avec `ast.parse` et compare les résultats déjà
enregistrés. Aucune installation de spaCy n’est requise pour le serveur.

Le lien entre un `print` et sa sortie reste documentaire : une sortie périmée ou
fabriquée mais plausible peut être acceptée. Le correcteur ne prouve ni que la
fonction a été exécutée ni qu’elle généralise au-delà des cas contrôlés. Un test
explicite documente cette limite. Pour le projet final, l’enseignant examine le
code, les cas supplémentaires, le protocole, les preuves et les interprétations.

Les sorties affichées passent par l’échappement automatique du template Jinja ;
le moteur n’utilise ni `Markup` ni `|safe` pour du contenu étudiant. Une trace JSON
est plafonnée à 100 000 caractères ; son extrait visible à 2 500 caractères.

L’identité provient de la vraie cellule d’identification du sujet, selon le
contrat partagé d’`outils.extract_identification_info`. La persistance conserve
la copie, le rapport et le CSV dans `soumissions/<évaluation>/<classe>/`.
Les routes et liens de navigation fonctionnent avec le préfixe `/universite/tal`.

## Vérification

Les tests dédiés couvrent les traces exactes et incorrectes, les types, les
marqueurs absents ou dupliqués, les erreurs enregistrées, les cellules distinctes,
les marqueurs d’une autre séance, les sorties fragmentées et les données JSON
mal formées. Ils vérifient les huit routes GET, le sélecteur sous proxy, un POST
réel à partir de la cellule d’identité du sujet, les trois fichiers persistés,
l’échappement HTML et des différences conceptuelles de comptage.

Les tests ne constituent pas une exécution des solutions étudiantes. Le comportement
réel du tuteur dans Colab, la durée en classe et l’exécution de l’ensemble des
notebooks avec les modèles distants restent des validations distinctes.

## Ressource de référence et dépendances entre traces

Le TD3 lit `faguet_source.txt` comme octets puis décode en UTF-8, **sans convertir
les CRLF en LF**. Les positions désignent des caractères Unicode du texte original,
début inclus et fin exclue. L’empreinte SHA-256 du fichier original est vérifiée
avant toute correction de cette séance. Le Dockerfile copie les ressources vers
`/app/s3_resources/` ; dans un checkout, le repli pointe vers
`Notebooks TD/S3/ressources/`. Si le fichier manque ou si son empreinte diffère,
l’évaluation retourne une erreur explicite, jamais un score de réussite.
L’ensemble est mis en cache par processus après sa première validation.

Plusieurs questions recoupent des traces précédentes : TD1 Q3 reprend Q1 ; TD2 Q3
reprend Q2, Q6 reprend Q3, Q7 reprend Q2. Une trace absente ou contradictoire peut
donc empêcher la validation du recoupement suivant. Cela ne prouve pas que les
fonctions étudiantes sont justes : cela vérifie la cohérence des valeurs fournies.
Les sujets demandent de recalculer les sorties concernées après modification.

Aucun build Docker n’a été exécuté dans cette session (commande Docker absente).
Les tests valident le chemin de développement et le refus d’une ressource absente
ou altérée ; le build et le démarrage en conteneur restent à vérifier au déploiement.
