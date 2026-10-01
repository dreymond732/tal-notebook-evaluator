"""Reproduire la référence enseignante fixe (commande manuelle, jamais une copie étudiante).

Exécuter avec spaCy 3.8.7 et fr_core_news_sm 3.8.0 installés.
Ce script ne lit que trois constantes du dépôt et écrit un fichier de référence.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'app'))
from s3_audit_data import TEXT0, TEXT1, TEXT2


def build():
    import spacy
    nlp = spacy.load('fr_core_news_sm')
    if spacy.__version__ != '3.8.7' or nlp.meta['version'] != '3.8.0':
        raise RuntimeError('Référence réservée à spaCy 3.8.7 / fr_core_news_sm 3.8.0.')

    def rows(doc, include_punctuation=False):
        return [dict(forme=t.text, lemme=t.lemma_, pos=t.pos_, tag=t.tag_,
                     debut=t.idx, fin=t.idx + len(t.text)) for t in doc if include_punctuation or not t.is_punct]

    d0, d1, d2 = map(nlp, (TEXT0, TEXT1, TEXT2))
    return {
        'provenance': {
            'spacy': '3.8.7', 'model': 'fr_core_news_sm', 'model_version': '3.8.0',
            'text_sha256': {str(i): hashlib.sha256(t.encode()).hexdigest()
                            for i, t in enumerate((TEXT0, TEXT1, TEXT2))}},
        'td1': {
            'annotations': rows(d1), 'all_annotations': rows(d1, include_punctuation=True),
            'phrases': [{'texte': s.text, 'tokens': len(s)} for s in d1.sents],
            'filters': {
                'noms': [t.lemma_ for t in d1 if t.pos_ == 'NOUN'],
                'verbes': [t.lemma_ for t in d1 if t.pos_ == 'VERB'],
                'mots_pleins': [t.lemma_ for t in d1 if t.pos_ in {'NOUN', 'VERB', 'ADJ'} and not t.is_stop]},
            'counts': {'split': len(TEXT0.split()), 'tokens': len(d0),
                       'non_ponctuation': sum(not t.is_punct and not t.is_space for t in d0)}},
        'td2': {
            'caracteres': len(TEXT2), 'phrases': len(list(d2.sents)), 'tokens': len(d2),
            'annotations': rows(d2), 'all_annotations': rows(d2, include_punctuation=True),
            'frequencies': {key: dict(Counter(t.lemma_ for t in d2 if t.pos_ == pos
                                             and not t.is_punct and not t.is_stop))
                            for key, pos in [('noms', 'NOUN'), ('verbes', 'VERB')]},
            'pos': dict(Counter(t.pos_ for t in d2 if not t.is_punct and not t.is_space)),
            'lemmes': [t.lemma_ for t in d2 if t.pos_ in {'NOUN', 'VERB', 'ADJ'}
                       and not t.is_punct and not t.is_stop]}}


if __name__ == '__main__':
    destination = ROOT / 'app/s3_spacy_reference.json'
    destination.write_text(json.dumps(build(), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(destination)
