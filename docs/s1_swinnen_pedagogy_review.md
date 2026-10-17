# Handoff — revue pédagogique indépendante

Mission : neuf nouveaux cahiers TD3/TD5/TD6 S1, branche `pedagogy/s1-swinnen-renforcement`, source `c81c386`. Ce document consigne le verdict transmis par le sous-agent indépendant `pedagogy`, rôle TAL-Pedagogy-Reviewer ; il n'est pas une auto-validation du producteur.

**ACCEPT — COUVERTURE_PÉDAGOGIQUE_CONSERVÉE** sur les neuf cahiers, les 54 questions, cours, exemples, essais, vérifications et bilans. Les trois sujets historiques ont été comparés à leur contenu actuel, inchangé depuis `c81c386`. Le texte de Swinnen fourni a servi à contrôler les références, numéros et pages. Aucune version antérieure plus riche non disponible n'est prétendue restaurée.

| Cahier | Preuves par question contrôlées |
|---|---|
| TD3-one | Q1 indices/tranches ; Q2 états append/pop et valeur retirée ; Q3 for/indentation/initialisation avant longueur des noms ; Q4 présentation ordonnée et vide ; Q5 entrelacement et incrément expliqués ; Q6 alias/copie/indépendance et essai copie vide. |
| TD3-bis | Q1 tuple historique/type/justification ; Q2 singleton/virgule/tranches ; Q3 parcours sans mutation ; Q4 fiche hétérogène/déballage ; Q5 paires imbriquées ; Q6 concaténation/recomposition et limite du contenu mutable. |
| TD3.ter | Q1 lexique historique complet et items avec langue/langage ; Q2 fiches-tuples ; Q3 inversion injective/collisions ; Q4 6 occurrences/4 formes et ensemble ; Q5 set vide/add/appartenance ; Q6 intersection et deux différences, limites ordre/fréquence. |
| TD5-one | Q1 def/appel/local/return/print/None et longueur3/6/vide ; Q2 répétition et0/1/accent ; Q3 volume/décimal/zéro ; Q4 maximum/trois positions/égalités/négatifs ; Q5 normaliser musée/vide/blancs/intérieurs ; Q6 composition/retour réutilisé. |
| TD5-bis | Q1 paramètres/arguments nommés et positionnels ; Q2 portée locale/extérieure sans global ; Q3 défauts0–3arguments ; Q4 saluer avec/sans défaut ; Q5 traduction connue/inconnue/BOOK/vide/second lexique ; Q6 repli/dictionnaire vide/valeur vide. |
| TD5.ter | Q1 occurrences de caractère/casse/accents/appels répétés ; Q2 nombre_mots composé/fragments/vide/blancs ; Q3 traduction composée/inconnu/vide ; Q4 résumé historique trois clés et comptes du texte normalisé ; Q5 comptes avant/après traduction expressions ; Q6 corpus/ordre/doublons/vide/entrée inchangée. |
| TD6-one | Q1 lecture historique UTF8/with/read/156 caractères ; Q2 splitlines/filtrage sans perdre ligne brute ; Q3 création/relecture/écrasement modew ; Q4 vrais blancs et conservation espaces ; Q5 ligne longue/fichier vide ; Q6 recopie/espaces/accents/lignes/source intacte. |
| TD6-bis | Q1 split limité/couples et graphies brutes ; Q2 fiches trois champs/code06000 chaîne ; Q3 sélection83000/absent/couple liste ou tuple ; Q4 quatre graphies Durand et limite identité ; Q5 regroupement de toutes personnes/doublons ; Q6 autonomie nouveau fichier avec blancs et point-virgule intérieur. |
| TD6.ter | Q1 cours writer/reader/newline/UTF8/types avant tâche ; Q2 virgules internes/quotes/accents ; Q3 sélection et exclusion en-tête ; Q4 reconstruction groupement autonome ; Q5 export historique en-tête/comptes/séparateurs/ordres libres ; Q6 nouveau cas trié avec virgules et accents. |

Deux bloqueurs relevés ont été corrigés et relus :

- **TAL-PED-001, levé** : Q3 de TD5.ter autorise boucle/append **ou compréhension** acquise au TD4 ; les rubriques Q3 et Q6 n'imposent plus `For`.
- **TAL-PED-002, levé** : Q5 de TD6.ter conserve `csv.reader` et fournit en complément l'affichage du texte CSV relu avec `repr`, après ouverture UTF8.

Les anciennes alternatives sont conservées ; les opérations nouvelles sont expliquées avant emploi, et TD3 ne suppose pas TD4 acquis. Les fonctions fournies au début de TD5.ter ont déjà été construites par l'étudiant en one/bis et rendent la session autonome. Les données TD6 permettent un démarrage à vide pour chaque cahier.

La charge est renforcée ; la faisabilité dans les huit séances initiales n'a pas été mesurée. Le parcours comporte treize cahiers de TD hors DM/contrôle, et non quatorze. Le verdict ne couvre ni comportement Colab observé, ni production, ni remaniement des évaluations finales non demandées. La relecture éditoriale, la QA des modèles, l'audit code et la gouvernance sont distincts.
