"""Métriques globales vérifiables : tokens, types, hapax, phrases et ratios.

Le calcul n'infère jamais le protocole qui a produit les chiffres d'un LLM.
Le texte brut est conservé ; une éventuelle recomposition des lignes garde
strictement la longueur de la chaîne et donc les offsets caractères originaux.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP
from hashlib import sha256
import re
from typing import TYPE_CHECKING, Literal, Mapping, Sequence

if TYPE_CHECKING:
    from spacy.language import Language

from .io_corpus import Corpus
from .pretraitements import (
    OperationPretraitement, PlanPretraitement, executer_pretraitements,
)


@dataclass(frozen=True)
class ProtocoleGlobal:
    """Toutes les conventions qui influencent les valeurs observées.

    alphabetiques : Token.is_alpha (exclut ponctuation, chiffres, mots mixtes).
    sans_ponctuation : exclut seulement Token.is_space et Token.is_punct.
    tous_sans_espaces : inclut la ponctuation.
    minuscules : comparaison des formes en minuscules, sans lemmatisation.
    lemmes : dépend d'un pipeline spaCy doté d'un lemmatiseur.
    recomp_ositions : non ; voir retours ci-dessous.
    """

    tokens: Literal["alphabetiques", "sans_ponctuation", "tous_sans_espaces"] = "alphabetiques"
    formes: Literal["minuscules", "exactes", "lemmes"] = "minuscules"
    retours: Literal["conserver", "recomposer_lignes"] = "conserver"
    ignorer_phrases_sans_mots: bool = True

    def __post_init__(self) -> None:
        if self.tokens not in {"alphabetiques", "sans_ponctuation", "tous_sans_espaces"}:
            raise ValueError("Politique de tokens inconnue")
        if self.formes not in {"minuscules", "exactes", "lemmes"}:
            raise ValueError("Politique de formes inconnue")
        if self.retours not in {"conserver", "recomposer_lignes"}:
            raise ValueError("Politique de retours inconnue")


def _plan_retours(retours: str) -> PlanPretraitement:
    if retours == "conserver":
        return PlanPretraitement(identifiant="global-conserver-v1")
    if retours == "recomposer_lignes":
        return PlanPretraitement(
            identifiant="global-recomposer-v1",
            operations=(OperationPretraitement(
                "recomposer_lignes",
                "Explorer les retours de ligne typographiques sans déplacer les offsets",
            ),),
        )
    raise ValueError("Retours : conserver ou recomposer_lignes")


def preparer_texte_pour_analyse(texte: str, retours: str = "conserver") -> str:
    """API historique : même résultat, moteur de prétraitement partagé."""
    return executer_pretraitements(texte, plan=_plan_retours(retours)).analyse


def _retenir(token: object, protocole: ProtocoleGlobal) -> bool:
    if token.is_space:  # type: ignore[attr-defined]
        return False
    if protocole.tokens == "alphabetiques":
        return bool(token.is_alpha)  # type: ignore[attr-defined]
    if protocole.tokens == "sans_ponctuation":
        return not bool(token.is_punct)  # type: ignore[attr-defined]
    return True


def _forme(token: object, protocole: ProtocoleGlobal) -> str:
    if protocole.formes == "exactes":
        return token.text  # type: ignore[attr-defined]
    if protocole.formes == "minuscules":
        return token.text.lower()  # type: ignore[attr-defined]
    lemme = token.lemma_  # type: ignore[attr-defined]
    if not lemme:
        raise ValueError("Aucun lemme disponible pour un token : pipeline spaCy incomplet")
    return lemme.lower()


def _rapport(numerateur: int, denominateur: int) -> float | None:
    return numerateur / denominateur if denominateur else None


def calculer_metriques_globales(
    source: Corpus | str,
    nlp: Language,
    *,
    protocole: ProtocoleGlobal | None = None,
    max_exemples: int = 8,
) -> dict:
    """Retourne résultats, conventions et traces originales auditables.

    Le nombre de phrases est celui des segments spaCy contenant au moins un
    token retenu (sauf politique ignorer_phrases_sans_mots=False).
    La longueur moyenne = N(tokens retenus) / N(phrases comptées).
    Le TTR = types / tokens ; les hapax sont les TYPES de fréquence 1.
    Aucun résultat n'utilise les chiffres de Gemini.
    """
    import spacy

    protocole = protocole or ProtocoleGlobal()
    if max_exemples < 0:
        raise ValueError("max_exemples doit être positif ou nul")
    if isinstance(source, Corpus):
        original, empreinte, origine = source.texte, source.sha256, source.origine
    elif isinstance(source, str):
        original = source
        empreinte = sha256(original.encode("utf-8")).hexdigest()
        origine = "texte fourni en mémoire"
    else:
        raise TypeError("source doit être Corpus ou str")

    preparation = executer_pretraitements(source, plan=_plan_retours(protocole.retours))
    analyse = preparation.analyse
    if len(analyse) != len(original):
        raise AssertionError("Décalage des offsets : texte d'analyse de taille différente")
    if len(analyse) >= nlp.max_length:
        raise ValueError("Taille supérieure à nlp.max_length : ajuster explicitement le pipeline")

    doc = nlp(analyse)
    try:
        segments = list(doc.sents)
    except ValueError as exc:
        raise ValueError("Le pipeline doit segmenter les phrases (sentencizer, senter ou parser)") from exc

    selection = [token for token in doc if _retenir(token, protocole)]
    formes = [_forme(token, protocole) for token in selection]
    distribution = Counter(formes)
    tokens = len(formes)
    types = len(distribution)
    hapax = sum(1 for n in distribution.values() if n == 1)
    compte_phrases = 0
    traces_phrases: list[dict] = []

    for segment in segments:
        n_retenus = sum(_retenir(token, protocole) for token in segment)
        if protocole.ignorer_phrases_sans_mots and not n_retenus:
            continue
        compte_phrases += 1
        if len(traces_phrases) < max_exemples:
            traces_phrases.append({
                "debut": segment.start_char,
                "fin": segment.end_char,
                "tokens_retenus": n_retenus,
                "extrait_original": original[segment.start_char:segment.end_char],
            })

    traces_tokens = []
    for token in selection[:max_exemples]:
        traces_tokens.append({
            "debut": token.idx,
            "fin": token.idx + len(token.text),
            "forme_originale": original[token.idx: token.idx + len(token.text)],
            "forme_comptee": _forme(token, protocole),
        })

    metriques = {
        "tokens": tokens,
        "types": types,
        "hapax": hapax,
        "phrases": compte_phrases,
        "ttr": _rapport(types, tokens),
        "ttr_pourcent": None if not tokens else 100 * types / tokens,
        "hapax_types_pourcent": None if not types else 100 * hapax / types,
        "mots_par_phrase": _rapport(tokens, compte_phrases),
    }
    return {
        "provenance": {"origine": origine, "sha256_utf8_original": empreinte},
        "protocole": asdict(protocole),
        "pretraitements": preparation.manifeste(),
        "logiciel": {
            "spacy": spacy.__version__,
            "modele": nlp.meta.get("name", nlp.lang),
            "version_modele": nlp.meta.get("version", "inconnue"),
            "pipeline": list(nlp.pipe_names),
        },
        "metriques": metriques,
        "controles": {
            "total_frequences_egal_tokens": sum(distribution.values()) == tokens,
            "hapax_inferieurs_aux_types": hapax <= types,
            "types_inferieurs_aux_tokens": types <= tokens,
            "offsets_originaux_inchanges": len(analyse) == len(original),
        },
        "traces": {
            "tokens": traces_tokens,
            "phrases": traces_phrases,
            "top_formes": [{"forme": terme, "effectif": effectif} for terme, effectif
                          in sorted(distribution.items(), key=lambda r: (-r[1], r[0]))[:max_exemples]],
        },
    }


def comparer_annonces(
    resultat: Mapping[str, object],
    annonces: Sequence[Mapping[str, object]],
    *, origine_reference: str = "gemini",
) -> list[dict]:
    """Compare les valeurs affichées APRÈS l'arrondi publié.

    Une égalité numérique n'établit pas une méthode Gemini identique.
    Les lignes d'annonces portent cle, valeur, decimales et unite.
    """
    valeurs = resultat["metriques"]
    if not origine_reference.strip():
        raise ValueError("Indiquer la provenance des références")
    comparaisons: list[dict] = []
    for annonce in annonces:
        cle = str(annonce["cle"])
        if cle not in valeurs:
            raise KeyError(f"Mesure absente du moteur : {cle}")
        precision = int(annonce["decimales"])
        if precision < 0:
            raise ValueError("Précision négative")
        mesure = valeurs[cle]
        declare = annonce["valeur"]
        if mesure is None:
            affichee = None
            statut = "NON_CALCULABLE"
        else:
            quantum = Decimal(1).scaleb(-precision)
            affichee = Decimal(str(mesure)).quantize(quantum, rounding=ROUND_HALF_UP)
            annonce_affichee = Decimal(str(declare)).quantize(quantum, rounding=ROUND_HALF_UP)
            statut = "MEME_VALEUR_A_L_ARRONDI" if affichee == annonce_affichee else "ECART"
        comparaisons.append({
            "cle": cle,
            "unite": annonce["unite"],
            "valeur_reference": declare,
            "origine_reference": origine_reference,
            "observe_brut": mesure,
            "observe_affiche": None if affichee is None else str(affichee),
            "decimales": precision,
            "statut_numerique": statut,
            "protocole_reference": "INCONNU" if origine_reference == "gemini"
                                  else "DECLARATION_A_VERIFIER",
        })
    return comparaisons
