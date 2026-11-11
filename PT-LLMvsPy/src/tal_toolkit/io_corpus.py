"""Charger un corpus sans en altérer les octets ni les positions."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path


@dataclass(frozen=True)
class Corpus:
    """Texte décodé, empreinte des octets originaux et provenance."""

    texte: str
    sha256: str
    origine: str


def charger_corpus(
    chemin: str | Path, *, sha256_attendu: str | None = None, encodage: str = "utf-8"
) -> Corpus:
    """Conserve les fins de ligne originales ; refuse une empreinte différente."""
    fichier = Path(chemin)
    original = fichier.read_bytes()
    empreinte = hashlib.sha256(original).hexdigest()
    if sha256_attendu is not None and empreinte.lower() != sha256_attendu.lower():
        raise ValueError(f"Empreinte SHA-256 différente pour {fichier}")
    return Corpus(original.decode(encodage), empreinte, str(fichier))


def corpus_depuis_texte(texte: str, *, origine: str = "microcorpus") -> Corpus:
    """Pour les tests ; le hachage porte sur le texte encodé en UTF-8."""
    if not isinstance(texte, str):
        raise TypeError("Le corpus doit être une chaîne")
    return Corpus(texte, hashlib.sha256(texte.encode("utf-8")).hexdigest(), origine)
