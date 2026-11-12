"""Analyses descriptives du projet Faguet à partir du texte nettoyé du notebook 01.

Les textes ne sont jamais transformés silencieusement. Les positions de preuve
désignent la version analysée (nettoyée), pas directement l'original.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import re
from typing import Mapping

from .epuration import composer_texte_epure
from .pretraitements import PlanPretraitement, executer_pretraitements

# Sélections proposées dans les parties 2 et 3 du rapport Gemini.
# Elles sont NON EXCLUSIVES et ne constituent pas des catégories validées.
CHAMPS_LEXICAUX: dict[str, tuple[str, ...]] = {
    "genre_anthropologie": (
        "femme", "homme", "sexe", "viril", "féminin", "masculin",
        "mâle", "femelle", "mari", "épouse", "fille", "garçon",
    ),
    "droit_institutions": (
        "loi", "droit", "code", "législation", "législateur",
        "décret", "contrat", "tribunal", "juge", "magistrature",
        "république", "constitution", "électeur", "électorat",
        "éligibilité", "suffrage", "état",
    ),
    "moeurs_famille": (
        "famille", "ménage", "mariage", "marier", "divorce",
        "divorcer", "répudiation", "répudier", "amour", "adultère",
        "enfant", "obéissance", "autorité", "mœurs", "maison",
        "foyer", "célibat",
    ),
    "travail_education": (
        "profession", "métier", "carrière", "travail", "travailler",
        "ouvrier", "ouvrière", "médecin", "docteur", "avocat",
        "pharmacien", "professeur", "enseignement", "école",
        "lycée", "lettre", "auteur", "littérature", "salon",
    ),
    "feminisme_ideologies": (
        "féminisme", "féministe", "antiféminisme", "antiféministe",
        "égalité", "égal", "liberté", "indépendance", "émancipation",
        "progrès", "société", "préjugé", "vanité", "crise", "anarchie",
    ),
}

LOCUTIONS: dict[str, str] = {
    "il_faut": r"\bil\s+faut\b",
    "il_faudrait": r"\bil\s+faudrait\b",
    "je_crois": r"\bje\s+crois\b",
    "je_ne_crois_pas": r"\bje\s+ne\s+crois\s+pas\b",
    "egalite_des_sexes": r"\bégalité\s+des\s+(?:deux\s+)?sexes\b",
    "division_du_travail": r"\bdivision\s+du\s+travail\b",
    "droits_de_la_femme": r"\bdroits?\s+de\s+la\s+femme\b",
}

PERSONNES: dict[str, tuple[str, ...]] = {
    "Charles Turgeon": ("Charles Turgeon", "M. Turgeon", "Turgeon"),
    "Théodore Joran": ("Théodore Joran", "M. Joran", "Joran"),
    "Paul et Victor Margueritte": (
        "Paul et Victor Margueritte", "MM. Margueritte", "Margueritte",
    ),
    "Voltaire": ("Voltaire",),
    "Rousseau": ("Jean-Jacques Rousseau", "Rousseau"),
    "Montesquieu": ("Montesquieu",),
}


def _preuve(texte: str, debut: int, fin: int, *, rayon: int = 55) -> dict:
    return {
        "debut": debut, "fin": fin,
        "extrait": texte[max(0, debut - rayon):min(len(texte), fin + rayon)],
    }


def auditer_reapplication(texte: str, plan: PlanPretraitement) -> dict:
    """Tester F(F(x))=F(x), sans écraser x et sans supposer l'identité.

    Le test couvre aussi la composition finale, qui compacte les blancs.
    Il est relatif au plan fourni et au texte observé.
    """
    if not isinstance(texte, str):
        raise TypeError("texte doit être une chaîne")
    resultat = executer_pretraitements(texte, plan=plan, max_exemples=5)
    vue = composer_texte_epure(resultat)
    n = sum(x["modifications"] for x in resultat.execution)
    # Premier écart utile si la deuxième application a un effet.
    i = next((i for i, (a, b) in enumerate(zip(texte, vue.texte))
              if a != b), min(len(texte), len(vue.texte)))
    return {
        "idempotent_sur_ce_texte": vue.texte == texte,
        "sha256_entree": sha256(texte.encode("utf-8")).hexdigest(),
        "sha256_reapplication": vue.sha256_texte_utf8,
        "operations": [
            {"nom": x["operation"], "modifications": x["modifications"]}
            for x in resultat.execution
        ],
        "total_modifications_operations": n,
        "longueur_entree": len(texte),
        "longueur_apres": len(vue.texte),
        "premier_ecart_position": None if vue.texte == texte else i,
        "avant": "" if vue.texte == texte else texte[max(0, i-35):i+80],
        "apres": "" if vue.texte == texte else vue.texte[max(0, i-35):i+80],
    }


def _occurrences_orthographiques(texte: str, motifs: Mapping[str, str]) -> dict:
    resultat = {}
    for nom, motif in motifs.items():
        captures = list(re.finditer(motif, texte, flags=re.IGNORECASE))
        resultat[nom] = {
            "occurrences": len(captures),
            "preuves": [_preuve(texte, m.start(), m.end()) for m in captures[:3]],
            "methode": "expression régulière sur texte nettoyé",
        }
    return resultat


def _mentions(texte: str, variantes: tuple[str, ...]) -> dict:
    # Repérer les variantes longues d'abord pour éviter de compter deux fois
    # "Charles Turgeon" puis "Turgeon" à la même position.
    candidats = []
    for variante in variantes:
        expr = r"(?<!\w)" + re.escape(variante) + r"(?!\w)"
        for m in re.finditer(expr, texte, flags=re.IGNORECASE):
            candidats.append((m.start(), m.end(), variante))
    selection = []
    for debut, fin, variante in sorted(candidats, key=lambda x: (x[0], -(x[1]-x[0]))):
        if selection and debut < selection[-1][1]:
            continue
        selection.append((debut, fin, variante))
    return {
        "mentions": len(selection),
        "variantes": dict(Counter(v for _, _, v in selection)),
        "preuves": [_preuve(texte, a, b) for a, b, _ in selection[:3]],
        "methode": "correspondances orthographiques, sans reconnaissance d'entités",
    }


def analyser_lexique_pt02(
    texte: str, nlp: object, *, taille_sttr: int = 1000,
    calculer_lemmes: bool = False,
) -> dict:
    """Calculs sur le texte reçu ; ne retélécharge ni ne renettoie le corpus.

    Les champs lexicaux du rapport sont décomptés par formes minuscules.
    Si calculer_lemmes=True, les lemmes sont rendus uniquement si un modèle
    effectivement annotant est disponible. Pas de repli sur des lemmes vides.
    """
    if not isinstance(texte, str):
        raise TypeError("texte doit être une chaîne")
    if taille_sttr <= 0:
        raise ValueError("taille_sttr doit être positive")
    if len(texte) >= nlp.max_length:
        raise ValueError("Augmenter explicitement nlp.max_length")
    doc = nlp(texte)
    try:
        phrases = list(doc.sents)
    except ValueError as exc:
        raise ValueError("Segmentateur de phrases absent") from exc

    lex = [t for t in doc if t.is_alpha]
    formes = [t.text.lower() for t in lex]
    frequences = Counter(formes)
    n = len(formes)
    v = len(frequences)
    hapax = sum(c == 1 for c in frequences.values())
    phrases_non_vides = [p for p in phrases if any(t.is_alpha for t in p)]
    sttr_segments = [
        len(set(formes[i:i+taille_sttr])) / taille_sttr
        for i in range(0, n - taille_sttr + 1, taille_sttr)
    ]
    globales = {
        "tokens_bruts_spacy": len(doc),
        "tokens_lexicaux": n,
        "types_minuscules": v,
        "hapax": hapax,
        "ttr": v/n if n else None,
        "part_hapax_types_pct": 100*hapax/v if v else None,
        "phrases_non_vides": len(phrases_non_vides),
        "longueur_moyenne_phrase": n/len(phrases_non_vides) if phrases_non_vides else None,
        "sttr": sum(sttr_segments)/len(sttr_segments) if sttr_segments else None,
        "sttr_taille_bloc": taille_sttr,
        "sttr_nombre_blocs_complets": len(sttr_segments),
        "sttr_reliquat_exclu": n - taille_sttr*len(sttr_segments),
    }
    champs = {}
    for nom, cibles in CHAMPS_LEXICAUX.items():
        details = {w: frequences[w] for w in cibles}
        champs[nom] = {
            "occurrences": sum(details.values()),
            "part_tokens_lexicaux_pct": 100*sum(details.values())/n if n else None,
            "details": details,
            "definition": "formes minuscules exactes, sans lemmatisation",
        }

    # Compter des formes d'adresse, sans prétendre détecter les catégories
    # morphosyntaxiques ou intentions de l'énonciateur.
    formes_gram = Counter(t.text.lower().rstrip("'’") for t in doc
                          if not t.is_space)
    enonciation = {
        "premiere_personne_formes": {
            k: formes_gram[k] for k in ("je", "j", "moi", "me", "m", "mon", "ma", "mes")
        },
        "adresse_formes": {
            k: formes_gram[k] for k in ("vous", "votre", "vos", "madame", "monsieur")
        },
    }
    enonciation["premiere_personne_total"] = sum(
        enonciation["premiere_personne_formes"].values()
    )
    enonciation["adresse_total"] = sum(enonciation["adresse_formes"].values())

    lemmes = {"statut": "NON_CALCULE", "raison": "mode facultatif désactivé"}
    if calculer_lemmes:
        a_un_lemmatiseur = any(nlp.has_pipe(p) for p in
                              ("lemmatizer", "trainable_lemmatizer"))
        if not a_un_lemmatiseur:
            lemmes = {
                "statut": "NON_CALCULE",
                "raison": "Aucun lemmatiseur installé : spacy.blank('fr') ne suffit pas",
            }
        elif any(not t.lemma_ for t in lex):
            lemmes = {
                "statut": "NON_CALCULE",
                "raison": "Annotations de lemmatisation incomplètes",
            }
        else:
            compte_lemmes = Counter(t.lemma_.lower() for t in lex)
            lemmes = {
                "statut": "CALCULE",
                "types_lemmes": len(compte_lemmes),
                "champs": {
                    nom: {
                        "occurrences": sum(compte_lemmes[w] for w in cibles),
                        "details": {w: compte_lemmes[w] for w in cibles},
                    }
                    for nom, cibles in CHAMPS_LEXICAUX.items()
                },
            }

    return {
        "schema": "analyse-lexicale-pt02-v1",
        "source_nettoyee_sha256": sha256(texte.encode("utf-8")).hexdigest(),
        "longueur_caracteres": len(texte),
        "logiciel": {
            "spacy": __import__("spacy").__version__,
            "modele": nlp.meta.get("name", nlp.lang),
            "version_modele": nlp.meta.get("version", "inconnue"),
            "pipeline": list(nlp.pipe_names),
        },
        "conventions": {
            "mots": "token.is_alpha",
            "formes": "token.text.lower()",
            "stopwords": "conservés",
            "segmentation": "spaCy, phrases comportant au moins un token alphabétique",
            "pretraitement_supplementaire": "aucun",
        },
        "globales": globales,
        "top_formes": frequences.most_common(30),
        "champs_lexicaux": champs,
        "enonciation": enonciation,
        "locutions": _occurrences_orthographiques(texte, LOCUTIONS),
        "onomastique": {
            nom: _mentions(texte, variantes) for nom, variantes in PERSONNES.items()
        },
        "lemmatisation": lemmes,
        "controles": {
            "tokens_egalent_somme_frequences": n == sum(frequences.values()),
            "types_egalent_distrib": v == len(frequences),
            "hapax_borne": 0 <= hapax <= v <= n,
            "source_inchangee": sha256(texte.encode("utf-8")).hexdigest() ==
                                sha256(doc.text.encode("utf-8")).hexdigest(),
        },
    }
