"""Inspection du nettoyage après export d'une vue lisible.

Les fréquences de motifs sont des estimations *opérationnelles* : une chaîne
littérale ou un regex compte ses correspondances, pas toutes les erreurs
sémantiquement apparentées. L'attribution à une fonction est un diagnostic
calculé sur la zone source, jamais une validation automatique de bug.
"""
from __future__ import annotations

from dataclasses import asdict
import re
from typing import Literal

from .pretraitements import PlanPretraitement, ResultatPretraitement, executer_pretraitements


def localiser_dans_original(
    original: str, ancre: str, *, occurrence: int = 1, contexte: int = 100,
) -> dict:
    """Retrouve une chaîne exacte et retourne une fenêtre source vérifiable.

    Les positions retournées sont des offsets caractères (début inclus).
    La numérotation des occurrences commence à 1.
    """
    if not isinstance(original, str):
        raise TypeError("Le texte original doit être une chaîne")
    if not isinstance(ancre, str) or not ancre or len(ancre) > 300:
        raise ValueError("Choisir une ancre non vide de 300 caractères au maximum")
    if not isinstance(occurrence, int) or occurrence < 1:
        raise ValueError("L'occurrence demandée commence à 1")
    if not isinstance(contexte, int) or contexte < 0 or contexte > 1000:
        raise ValueError("Le contexte doit être compris entre 0 et 1000 caractères")
    positions = [m.start() for m in re.finditer(re.escape(ancre), original)]
    if not positions:
        raise ValueError("L'ancre ne figure pas dans le corpus original")
    if occurrence > len(positions):
        raise ValueError(f"Il n'existe que {len(positions)} occurrences de l'ancre")
    debut = positions[occurrence-1]
    fin = debut + len(ancre)
    a, b = max(0, debut-contexte), min(len(original), fin+contexte)
    return {
        "ancre": ancre,
        "nombre_correspondances": len(positions),
        "occurrence_choisie": occurrence,
        "debut": debut,
        "fin": fin,
        "fenetre_debut": a,
        "fenetre_fin": b,
        "fenetre_originale": original[a:b],
    }


def fonctions_ayant_modifie_zone(
    resultat: ResultatPretraitement, debut: int, fin: int,
) -> list[dict]:
    """Rejoue chaque prétraitement, dans l'ordre, sur le corpus original entier.

    Le rejeu sur l'original complet, plutôt que sur un extrait isolé, évite
    qu'un découpage au milieu d'une ligne modifie les regex d'ancrage.
    """
    from .pretraitements import OperationPretraitement
    operations = tuple(
        OperationPretraitement(
            op["nom"], op["justification"], tuple(op.get("cibles", ()))
        )
        for op in resultat.plan["operations"]
    )
    if not (0 <= debut < fin <= len(resultat.original)):
        raise ValueError("Fenêtre source invalide")
    ancien = resultat.original
    candidats = []
    for i, operation in enumerate(operations):
        plan = PlanPretraitement(
            operations[:i+1], identifiant=resultat.plan["identifiant"]
        )
        courant = executer_pretraitements(resultat.original, plan=plan,
                                          max_exemples=0).analyse
        n = sum(a != b for a, b in zip(ancien[debut:fin], courant[debut:fin]))
        if n:
            candidats.append({"operation": operation.nom,
                              "caracteres_modifies_dans_la_fenetre": n})
        ancien = courant
    return candidats


def compter_motif(
    original: str, epure: str, motif: str,
    *, mode: Literal["litteral", "regex"] = "litteral",
) -> dict:
    """Compte le même motif dans les deux textes, sans généraliser les cas."""
    if not isinstance(motif, str) or not motif or len(motif) > 250:
        raise ValueError("Motif non vide de longueur inférieure ou égale à 250")
    if mode not in {"litteral", "regex"}:
        raise ValueError("Mode de recherche : litteral ou regex")
    expression = re.escape(motif) if mode == "litteral" else motif
    regex = re.compile(expression)
    if regex.match("") is not None:
        raise ValueError("Un motif susceptible de correspondre au vide est interdit")
    a = [m.start() for m in regex.finditer(original)]
    b = [m.start() for m in regex.finditer(epure)]
    return {
        "motif": motif, "mode": mode,
        "occurrences_original": len(a),
        "occurrences_epure": len(b),
        "difference": len(b)-len(a),
        "exemples_positions_original": a[:10],
        "exemples_positions_epure": b[:10],
        "limite": (
            "Comptage exact des correspondances du motif ; un autre motif "
            "ou un changement de mise en forme peut modifier l'estimation."
        ),
    }


def valider_inspection(inspection: dict) -> None:
    """Exige une décision interprétable, y compris si aucun problème n'est vu."""
    if not isinstance(inspection, dict):
        raise ValueError("Journal d'inspection requis")
    if inspection.get("decision") not in {"conserver", "reviser"}:
        raise ValueError("Décision attendue : conserver ou reviser")
    if len(str(inspection.get("methode_inspection", "")).strip()) < 30:
        raise ValueError("Décrire les vérifications réalisées sur le texte entier")
    if len(str(inspection.get("justification_decision", "")).strip()) < 30:
        raise ValueError("Motiver la décision de conserver ou réviser")
    anomalies = inspection.get("anomalies")
    if not isinstance(anomalies, list):
        raise ValueError("La liste des anomalies inspectées est requise (éventuellement vide)")
    for numero, anomalie in enumerate(anomalies, 1):
        if not isinstance(anomalie, dict):
            raise ValueError(f"Anomalie {numero} mal formée")
        for champ in ("ancre", "debut", "fin", "fonction_suspectee", "commentaire",
                      "estimation"):
            if champ not in anomalie:
                raise ValueError(f"Anomalie {numero} : {champ} manquant")
        if not (isinstance(anomalie["debut"], int)
                and isinstance(anomalie["fin"], int)
                and 0 <= anomalie["debut"] < anomalie["fin"]):
            raise ValueError(f"Anomalie {numero} : indices invalides")
        if len(str(anomalie["commentaire"]).strip()) < 15:
            raise ValueError(f"Anomalie {numero} : commentaire insuffisant")
        if not isinstance(anomalie["estimation"], dict) or (
            not isinstance(anomalie["estimation"].get("occurrences_original"), int)
            or not isinstance(anomalie["estimation"].get("occurrences_epure"), int)
        ):
            raise ValueError(f"Anomalie {numero} : décompte absent")
