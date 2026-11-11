"""Audit des citations et des nombres annoncés par un LLM.

Une proximité n'est jamais une validation automatique de citation.
Une comparaison numérique exige un protocole explicitement comparable.
"""
from __future__ import annotations

import re
from typing import Mapping, Sequence, TypedDict


class VerdictCitation(TypedDict):
    citation: str
    statut: str
    debut: int
    fin: int
    passage_source: str


CHAMPS_PROTOCOLE: tuple[str, ...] = (
    "unite", "fenetre", "normalisation", "agregation"
)


def _normaliser_avec_positions(texte: str) -> tuple[str, list[tuple[int, int]]]:
    """Normalisation TD3 : minuscules, apostrophes, espaces comprimés.

    Chaque caractère normalisé garde sa tranche de provenance dans l'original.
    """
    resultat: list[str] = []
    positions: list[tuple[int, int]] = []
    for bloc in re.finditer(r"\S+|\s+", texte):
        if bloc.group().isspace():
            if resultat and bloc.end() < len(texte):
                resultat.append(" ")
                positions.append((bloc.start(), bloc.end()))
            continue
        for i, caractere in enumerate(bloc.group()):
            for produit in caractere.replace("’", "'").lower():
                resultat.append(produit)
                positions.append((bloc.start() + i, bloc.start() + i + 1))
    return "".join(resultat), positions


def verifier_citation(
    source: str, citation: str, *, candidat: tuple[int, int] | None = None
) -> VerdictCitation:
    """Retourne EXACTE, NORMALISEE, CANDIDAT_APPROCHE ou NON_RETROUVEE.

    NORMALISEE veut seulement dire égalité après transformation typographique.
    CANDIDAT_APPROCHE requiert une plage fournie par un analyste ; le module
    ne choisit pas de candidat flou et n'en valide jamais automatiquement la fidélité.
    Les positions et passages sont toujours dans le texte SOURCE ORIGINAL.
    """
    if not citation:
        raise ValueError("La citation ne peut pas être vide")
    debut = source.find(citation)
    if debut >= 0:
        fin = debut + len(citation)
        return {"citation": citation, "statut": "EXACTE", "debut": debut,
                "fin": fin, "passage_source": source[debut:fin]}

    normalise_source, positions = _normaliser_avec_positions(source)
    normalise_citation, _ = _normaliser_avec_positions(citation)
    if normalise_citation:
        indice = normalise_source.find(normalise_citation)
        if indice >= 0:
            debut = positions[indice][0]
            fin = positions[indice + len(normalise_citation) - 1][1]
            return {"citation": citation, "statut": "NORMALISEE", "debut": debut,
                    "fin": fin, "passage_source": source[debut:fin]}

    if candidat is not None:
        debut, fin = candidat
        if not (0 <= debut < fin <= len(source)):
            raise ValueError("Bornes de candidat invalides")
        return {"citation": citation, "statut": "CANDIDAT_APPROCHE",
                "debut": debut, "fin": fin, "passage_source": source[debut:fin]}

    return {"citation": citation, "statut": "NON_RETROUVEE",
            "debut": -1, "fin": -1, "passage_source": ""}


def champs_manquants(
    affirmation: Mapping[str, object],
    champs: Sequence[str] = CHAMPS_PROTOCOLE,
) -> list[str]:
    """Absent ou None seulement : n'invente aucun paramètre non documenté."""
    return [champ for champ in champs
            if champ not in affirmation or affirmation[champ] is None]


def comparer_intervalle(valeur: int, borne_basse: int, borne_haute: int) -> str:
    """Valeur et bornes déjà comparables ; bornes inclusives."""
    if borne_basse > borne_haute:
        raise ValueError("Intervalle inversé")
    return ("compatible selon le protocole"
            if borne_basse <= valeur <= borne_haute
            else "contredit selon le protocole")


def evaluer_affirmation(
    affirmation: Mapping[str, object],
    valeur: int,
    *,
    protocole_comparable: bool,
) -> str:
    """Statut de l'annonce originale ; ne substitue pas un protocole proposé."""
    if champs_manquants(affirmation):
        return "INSUFFISAMMENT_DEFINI"
    if not protocole_comparable:
        return "NON_COMPARABLE"
    bornes = affirmation.get("intervalle")
    if (not isinstance(bornes, (list, tuple)) or len(bornes) != 2
            or any(not isinstance(x, int) or isinstance(x, bool) for x in bornes)):
        return "NON_COMPARABLE"
    return comparer_intervalle(valeur, bornes[0], bornes[1])
