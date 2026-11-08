# Audit de l'exhaustivité du suivi des TD S1, S2 et S3

## Périmètre et justification

Le TD4 S1 n'était qu'un cas révélateur. Le consolidateur doit
comptabiliser tous les travaux effectivement évalués à partir des
journaux de notes : les 19 TD du S1 (TD initiaux et approfondissements),
3 TD du S2 et 12 TD du S3 (dont les révisions R0/R1/R2).

Le script audit_progressions.py parcourt le **catalogue actif**, pas une
liste manuelle de noms de fichiers. Il utilise storage_layout.storage_id()
et contrôle les journaux notes_<dossier>.csv de chaque correcteur.
Les changements de nomenclature S1 vers S1_TD... sont donc pris
en compte sans modifier les anciennes données sources.

Le filtrage des TD3–TD6 initiaux du S1 a déjà été corrigé dans la PR #40.
L'ancien contrôle Controletilt-s1 reste exclu.

## Exécution sur le NAS

Après déploiement de la PR d'audit :

    docker-compose exec -T corrector-tal \
      python audit_progressions.py --annee 2026-2027

Pour obtenir le bilan de toutes les évaluations, incluant DM et contrôles :

    docker-compose exec -T corrector-tal \
      python audit_progressions.py --annee 2026-2027 --toutes-evaluations

Pour restreindre au S1 :

    docker-compose exec -T corrector-tal \
      python audit_progressions.py --annee 2026-2027 --semestre S1

La sortie JSON anonymisée est obtenue avec --json.

**Le script n'effectue aucun recalcul ni aucune écriture**. Il lit le
verrou de consolidation existant en mode partagé lorsque possible.
Si les résultats sont manifestement périmés, on peut demander un
recalcul séparé, qui modifie uniquement les exports privés :

    docker-compose exec -T corrector-tal \
      python progression.py --annee 2026-2027

Relancer ensuite l'audit pour comparer les mêmes données à jour.

## Contrôles pour chaque évaluateur

- Existence du dossier physique attendu (S1_TD4_A, TD3_S2, etc.).
- Nombre de cahiers archivés sous nb/ et de rapports HTML sous rapport/.
- Existence, présence d'un en-tête canonique et nombre de lignes du
  journal notes_<dossier>.csv.
- Versions du contrat, périodes académiques, score, identité et numéro
  étudiant ; recours aux correspondances **déjà validées**, jamais aux
  seules suggestions automatiques.
- Nombre d'essais, de personnes distinctes, et comparaison des
  compteurs individuels et scores min/max entre le journal et le
  relevé progression_S1/S2/S3.
- Présence éventuelle d'anciennes archives dont le journal canonique
  n'est pas encore disponible.

L'audit n'infère pas un essai à partir du seul nombre de cahiers :
la présence de 5 notebooks et 3 rapports ne prouve ni la présence de
5 notes CSV valides ni 3 numéros étudiant distincts.

## Interprétation des états

- OK : journal présent et concordant avec le suivi, sans rejet.
- SANS_DEPOT : aucun journal ni archive dans le dossier attendu.
- A_VERIFIER : lignes de contrat ancien, hors année, numéro absent,
  ou autres lignes ne participant pas à la synthèse. Cela n'implique
  pas nécessairement une erreur du correcteur.
- ECART : divergence entre les lignes éligibles et le relevé
  consolidé, dossier de cahiers sans CSV, ancienne archive sans
  journal canonique, export manquant ou schéma corrompu.

Le programme retourne un code d'erreur 2 si un ECART est détecté,
pour éviter qu'une anomalie silencieuse soit prise pour un succès.
Il affiche les **noms des évaluations**, mais **aucun nom, prénom,
numéro étudiant ou score individuel**.

Il ne change ni les règles d'évaluation, ni la confidentialité des
contrôles, ni le calcul des min/max. Les résultats des versions
antérieures restent dans les archives ; leur exclusion est affichée,
pas masquée.

## Validation

Le fichier tests/test_audit_progressions.py simule un dépôt pour
**chacun des 34 TD**, puis vérifie les effectifs par semestre, la
concordance des notes, l'année, les anciennes versions, les
correspondances validées et les causes de divergence. Il simule
également le cas du TD4 : cinq essais et trois étudiants, malgré
trois rapports et cinq cahiers.

    python -m unittest discover -s tests -p test_audit_progressions.py -v
    python -m unittest discover -s tests -v

La CI teste des données fictives ; seul le rapport généré **sur le NAS**
pourra confirmer les résultats réellement manquants et les
nouvelles interventions à prévoir. Ne pas publier les relevés
complets nominatifs dans une issue GitHub.
