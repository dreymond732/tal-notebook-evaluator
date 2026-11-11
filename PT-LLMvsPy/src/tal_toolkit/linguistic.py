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


def tokeniser_phrases(doc: Doc, *, mode: str = "forme") -> list[list[str]]:
    """Phrases en tokens : formes minuscules ou lemmes, ponctuation conservée.

    Nécessite un analyseur de phrases (parser/senter/sentencizer) actif.
    Les tokens d'espacement seuls sont exclus ; une expression ne saute pas
    silencieusement la ponctuation.
    """
    if mode not in {"forme", "lemme"}:
        raise ValueError("mode attendu : forme ou lemme")
    sorties: list[list[str]] = []
    for phrase in doc.sents:
        tokens: list[str] = []
        for token in phrase:
            if token.is_space:
                continue
            if mode == "lemme":
                if not token.lemma_:
                    raise ValueError("Lemmes absents : charger un pipeline avec lemmatiseur")
                tokens.append(token.lemma_.lower())
            else:
                tokens.append(token.text.lower())
        sorties.append(tokens)
    return sorties
