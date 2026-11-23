"""Adaptateur spaCy : les indices des tokens et phrases restent ceux du Doc source."""
from __future__ import annotations

from collections import OrderedDict
from hashlib import sha256
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacy.language import Language
    from spacy.tokens import Doc


class DocCache:
    """Cache local borné ; un pipeline spaCy différent ne partage pas ses Doc."""

    def __init__(self, capacite: int = 8) -> None:
        if capacite < 1:
            raise ValueError("capacite doit être >= 1")
        self.capacite = capacite
        self._cache: OrderedDict[tuple[int, str], Doc] = OrderedDict()

    def analyser(self, nlp: Language, texte: str) -> Doc:
        cle = (id(nlp), sha256(texte.encode("utf-8")).hexdigest())
        if cle in self._cache:
            self._cache.move_to_end(cle)
            return self._cache[cle]
        doc = nlp(texte)
        self._cache[cle] = doc
        if len(self._cache) > self.capacite:
            self._cache.popitem(last=False)
        return doc

    def vider(self) -> None:
        self._cache.clear()


def tokeniser_phrases(
    doc: Doc, *, mode: str = "forme", tokens: str = "tous_sans_espaces",
) -> list[list[str]]:
    """Phrases en formes minuscules ou lemmes, dans les frontières du Doc.

    Nécessite un analyseur de phrases (parser/senter/sentencizer) actif.
    Par défaut, tous les tokens hors espaces sont conservés. Le filtre
    « sans_ponctuation » exclut en plus les signes de ponctuation, tandis
    que « alphabetiques » sélectionne les tokens dont la FORME est alphabétique.
    Une phrase devenue vide garde sa place afin de préserver les indices.
    """
    if mode not in {"forme", "lemme"}:
        raise ValueError("mode attendu : forme ou lemme")
    if tokens not in {"tous_sans_espaces", "sans_ponctuation", "alphabetiques"}:
        raise ValueError("Politique de tokens inconnue")
    sorties: list[list[str]] = []
    for phrase in doc.sents:
        valeurs: list[str] = []
        for token in phrase:
            if token.is_space:
                continue
            if tokens == "sans_ponctuation" and token.is_punct:
                continue
            if tokens == "alphabetiques" and not token.is_alpha:
                continue
            if mode == "lemme":
                if not token.lemma_:
                    raise ValueError("Lemmes absents : charger un pipeline avec lemmatiseur")
                valeurs.append(token.lemma_.lower())
            else:
                valeurs.append(token.text.lower())
        sorties.append(valeurs)
    return sorties
