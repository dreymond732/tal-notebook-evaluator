"""Invariants et références figées sans spaCy serveur ; vérité linguistique à relire."""
from collections import Counter
import json
from pathlib import Path

from s3_audit import integer, keys, string, same

# Référence enseignante calculée hors serveur sur les seuls textes fixes.
SPACY_REFERENCE = json.loads(Path(__file__).with_name("s3_spacy_reference.json").read_text(encoding="utf-8"))

POS = {'ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X', 'SPACE'}


def strings(value):
    return isinstance(value, list) and all(isinstance(v, str) and v for v in value)


def frequencies(value, allow_empty=False):
    return isinstance(value, dict) and (bool(value) or allow_empty) and all(isinstance(k, str) and k and integer(v, 1) for k, v in value.items())


def annotations(rows, source, count=None, offsets=False, full=False, extra=()):
    if not isinstance(rows, list) or not rows or (count is not None and len(rows) != count):
        return False
    end = 0
    for row in rows:
        if not keys(row, ('forme', 'lemme', 'pos', *extra)) or not all(isinstance(row[k], str) and row[k] for k in ('forme', 'lemme', 'pos')) or row['pos'] not in POS:
            return False
        start = row.get('debut') if offsets else source.find(row['forme'], end)
        finish = row.get('fin') if offsets else start + len(row['forme'])
        if (not integer(start) or not integer(finish) or start < end or not start < finish <= len(source)
                or finish - start != len(row['forme']) or source[start:finish] != row['forme']):
            return False
        if full and any(ch.isalnum() for ch in source[end:start]):
            return False
        end = finish
    return not full or not any(ch.isalnum() for ch in source[end:])


def q1_td1(value, source, expected=None):
    return (keys(value, ['annotations']) and annotations(value['annotations'], source, offsets=True, full=True, extra=('tag',))
            and all(isinstance(row['tag'], str) for row in value['annotations'])
            and (expected is None or projected_rows(value['annotations'], expected, ('forme', 'lemme', 'pos', 'tag', 'debut', 'fin'))))


def phrases(value, source, expected=None):
    if not keys(value, ['phrases']) or not isinstance(value['phrases'], list) or not value['phrases']:
        return False
    rows = value['phrases']
    return (all(keys(r, ['texte', 'tokens']) and string(r['texte']) and integer(r['tokens'], 1)
                and len(r['texte'].split()) <= r['tokens'] <= len(r['texte']) for r in rows)
            and ' '.join(r['texte'].strip() for r in rows) == source
            and (expected is None or same(rows, expected)))


def ordered_subsequence(wanted, items):
    """Préserve l'ordre et la multiplicité sans imposer les mots vides."""
    remaining = iter(items)
    return all(any(item == word for item in remaining) for word in wanted)


def filters(value, context, expected=None):
    prior = context.get(1)
    annotation = prior.get('annotations', []) if isinstance(prior, dict) else []
    if (not annotation_context(prior) or not keys(value, ['noms', 'verbes', 'mots_pleins'])
            or not all(strings(value[k]) for k in ('noms', 'verbes', 'mots_pleins'))):
        return False
    content = [r['lemme'] for r in annotation if r['pos'] in {'NOUN', 'VERB', 'ADJ'}]
    return (value['noms'] == [r['lemme'] for r in annotation if r['pos'] == 'NOUN']
            and value['verbes'] == [r['lemme'] for r in annotation if r['pos'] == 'VERB']
            and bool(value['mots_pleins']) and ordered_subsequence(value['mots_pleins'], content)
            and (expected is None or same(value, expected)))


def dependency(value, source):
    if not keys(value, ['verbe', 'verbe_debut', 'dependant', 'dependant_debut', 'relation', 'interpretation']):
        return False
    # Un point pour des repères effectivement retrouvables, pas pour leur interprétation.
    return all(isinstance(value[k], str) and value[k] and integer(value[k + '_debut'])
               and source[value[k + '_debut']:value[k + '_debut'] + len(value[k])] == value[k]
               for k in ['verbe', 'dependant']) and isinstance(value['relation'], str) and bool(value['relation'].strip()) and isinstance(value['interpretation'], str)

def dependency_td1(value, source):
    if not dependency(value, source):
        return False
    first_end = len(SPACY_REFERENCE['td1']['phrases'][0]['texte'])
    tokens = {(r['forme'], r['debut']) for r in SPACY_REFERENCE['td1']['all_annotations'] if r['fin'] <= first_end}
    verb, dependent = (value['verbe'], value['verbe_debut']), (value['dependant'], value['dependant_debut'])
    return verb != dependent and verb in tokens and dependent in tokens


def counts_td1(value, source, expected=None):
    return (keys(value, ['split', 'tokens', 'non_ponctuation', 'interpretation'])
            and type(value['split']) is int and value['split'] == len(source.split())
            and integer(value['tokens'], value['split']) and value['tokens'] <= len(source)
            and integer(value['non_ponctuation'], 1) and value['non_ponctuation'] <= value['tokens']
            and isinstance(value['interpretation'], str)
            and (expected is None or all(same(value[k], v) for k, v in expected.items())))


def initial_annotations(rows, source):
    """Aucune omission dans le préfixe ; segmentation lexicale relue humainement."""
    if not annotations(rows, source, count=5, offsets=True):
        return False
    end = 0
    for row in rows:
        if source[end:row['debut']].strip():
            return False
        end = row['fin']
    return True


def transfer(value):
    return (keys(value, ['texte', 'phrases', 'annotations', 'noms', 'verbes', 'question']) and string(value['texte'])
            and integer(value['phrases'], 2) and value['phrases'] <= 4
            and initial_annotations(value['annotations'], value['texte'])
            and strings(value['noms']) and strings(value['verbes']) and isinstance(value['question'], str))


def summary_td2(value, source, expected=None):
    return (keys(value, ['caracteres', 'phrases', 'tokens', 'annotations'])
            and type(value['caracteres']) is int and value['caracteres'] == len(source)
            and integer(value['phrases'], 1) and value['phrases'] <= len(source.split())
            and integer(value['tokens'], len(source.split())) and value['tokens'] <= len(source)
            and annotations(value['annotations'], source, count=10)
            and (expected is None or (all(same(value[k], expected[k]) for k in ('caracteres', 'phrases', 'tokens'))
                 and projected_rows(value['annotations'], expected['annotations'][:10], ('forme', 'lemme', 'pos')))))


def two_frequencies(value, source, expected=None):
    return (keys(value, ['noms', 'verbes']) and frequencies(value['noms']) and frequencies(value['verbes'])
            and sum(value['noms'].values()) + sum(value['verbes'].values()) <= len(source.split())
            and (expected is None or same(value, expected)))


def exclusions(value, context):
    return (keys(value, ['exclusions', 'avant', 'apres', 'justification'])
            and strings(value['exclusions']) and bool(value['exclusions'])
            and frequencies(value['avant']) and frequencies(value['apres'], allow_empty=True)
            and frequency_context(context.get(2))
            and same(value['avant'], context[2]['noms'])
            and any(k in value['avant'] for k in value['exclusions'])
            and all(k == k.lower() for k in value['exclusions'])
            and same(value['apres'], {k: v for k, v in value['avant'].items() if k.lower() not in value['exclusions']})
            and isinstance(value['justification'], str))


def pos_counts(value, source, expected=None):
    if not keys(value, ['pos', 'top3', 'limite']) or not frequencies(value['pos']):
        return False
    counts, top = value['pos'], value['top3']
    return (set(counts) <= POS - {'PUNCT', 'SPACE'} and sum(counts.values()) <= len(source.split())
            and isinstance(top, list) and len(top) == min(3, len(counts))
            and all(isinstance(row, list) and len(row) == 2 and integer(row[1], 1) and counts.get(row[0]) == row[1] for row in top)
            and len({r[0] for r in top}) == len(top)
            and [r[1] for r in top] == sorted(counts.values(), reverse=True)[:3]
            and isinstance(value['limite'], str) and (expected is None or same(counts, expected)))


def linguistic_review(value, source, expected=None):
    return (keys(value, ['lemmes', 'controle', 'limite_modele']) and strings(value['lemmes']) and bool(value['lemmes'])
            and len(value['lemmes']) <= len(source.split())
            and isinstance(value['controle'], list) and len(value['controle']) == 5
            and all(keys(row, ['forme', 'lemme', 'pos', 'jugement'])
                    and all(isinstance(row[k], str) and row[k] for k in ['forme', 'lemme', 'pos'])
                    and row['forme'] in source and row['pos'] in POS and isinstance(row['jugement'], str)
                    for row in value['controle'])
            and isinstance(value['limite_modele'], str)
            and (expected is None or (same(value['lemmes'], expected['lemmes'])
                 and occurrence_subset(value['controle'], expected['all_annotations']))))


def chart_data(value, context):
    return (keys(value, ['frequences', 'hypothese', 'verification']) and frequencies(value['frequences'])
            and keys(context.get(3), ['apres']) and frequencies(context[3]['apres'])
            and same(value['frequences'], context[3]['apres'])
            and isinstance(value['hypothese'], str) and isinstance(value['verification'], str))


def generalization(value, context):
    required = ['general_noms', 'specialise_noms', 'general_verbes', 'specialise_verbes', 'combine', 'comparaison']
    if not keys(value, required) or not all(frequencies(value[k]) for k in required[:-1]):
        return False
    if not frequency_context(context.get(2)):
        return False
    nouns, verbs = context[2]['noms'], context[2]['verbes']
    return (nouns is not None and verbs is not None
            and same(value['general_noms'], nouns) and same(value['specialise_noms'], nouns)
            and same(value['general_verbes'], verbs) and same(value['specialise_verbes'], verbs)
            and same(value['combine'], dict(Counter(nouns) + Counter(verbs)))
            and isinstance(value['comparaison'], str))


def frequency_context(value):
    return keys(value, ['noms', 'verbes']) and frequencies(value['noms']) and frequencies(value['verbes'])


def projected_rows(rows, expected, fields):
    return (len(rows) == len(expected) and all(
        all(k in row and same(row[k], ref[k]) for k in fields)
        for row, ref in zip(rows, expected)))


def occurrence_subset(rows, expected):
    fields = ('forme', 'lemme', 'pos')
    observed = Counter(tuple(row[k] for k in fields) for row in rows)
    available = Counter(tuple(row[k] for k in fields) for row in expected)
    return not (observed - available)


def annotation_context(value):
    return (keys(value, ['annotations']) and isinstance(value['annotations'], list)
            and bool(value['annotations']) and all(keys(r, ['lemme', 'pos'])
            and isinstance(r['lemme'], str) and isinstance(r['pos'], str) and r['pos'] in POS
            for r in value['annotations']))
