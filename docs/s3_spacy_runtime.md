# Compatibilité du rendu displaCy dans les pilotes S3

La validation des exemples fournis utilise spaCy 3.8.7, les modèles français `fr_core_news_sm` et `fr_core_news_md` 3.8.0 et IPython 8.37.0.

Un essai avec IPython 9.17.1 a montré que `displacy.render(..., jupyter=True)` de spaCy 3.8.7 échoue avec une `ImportError` : son rendu Jupyter importe `display` depuis `IPython.core.display`, où ce nom n’est plus disponible. La même API fonctionne avec IPython 8.37.0. Cette observation porte sur les versions effectivement testées, pas sur l’ensemble des versions d’IPython 9.

La cellule de préparation fournie `c4eb9544f889` du TD1 ajoute donc exactement `IPython==8.37.0` aux paquets installés. L’étudiant conserve l’API displaCy enseignée ; cette dépendance de préparation n’autorise aucune nouvelle bibliothèque dans ses réponses. Après l’installation, le redémarrage de la session permet de charger la version installée d’IPython.

Le test de conservation compare l’AST de chaque cellule originale à sa référence historique inchangée. Sa seule exception d’exécution pour les deux pilotes est cet argument supplémentaire, à la fin de la liste de l’unique appel `subprocess.check_call` de la cellule identifiée du TD1. Un autre paquet, une autre version, un autre emplacement ou un changement des instructions exécutables reste refusé. Le fichier de référence et les métadonnées du notebook ne sont pas réécrits pour intégrer cette exception.
