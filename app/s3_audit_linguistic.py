"""Invariants lisibles sans charger spaCy ; ils ne certifient pas ses prédictions."""
from collections import Counter
from s3_audit import integer, keys, string

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
        if not integer(start) or not integer(finish) or start < end or finish <= start or source[start:finish] != row['forme']:
            return False
        if full and any(ch.isalnum() for ch in source[end:start]):
            return False
        end = finish
    return not full or not any(ch.isalnum() for ch in source[end:])


def q1_td1(value, source):
    return keys(value, ['annotations']) and annotations(value['annotations'], source, offsets=True, full=True, extra=('tag',))


def phrases(value, source):
    if not keys(value, ['phrases']) or not isinstance(value['phrases'], list) or not value['phrases']:
        return False
    rows = value['phrases']
    return (all(keys(r, ['texte', 'tokens']) and string(r['texte']) and integer(r['tokens'], 1)
                and len(r['texte'].split()) <= r['tokens'] <= len(r['texte']) for r in rows)
            and ' '.join(r['texte'].strip() for r in rows) == source)


def filters(value, context):
    annotation = context.get(1, {}).get('annotations', [])
    if not annotation or not keys(value, ['noms', 'verbes', 'mots_pleins']) or not all(strings(value[k]) for k in value):
        return False
    content = [r['lemme'] for r in annotation if r['pos'] in {'NOUN', 'VERB', 'ADJ'}]
    return (value['noms'] == [r['lemme'] for r in annotation if r['pos'] == 'NOUN']
            and value['verbes'] == [r['lemme'] for r in annotation if r['pos'] == 'VERB']
            and bool(value['mots_pleins']) and not (Counter(value['mots_pleins']) - Counter(content)))


def dependency(value, source):
    if not keys(value, ['verbe', 'verbe_debut', 'dependant', 'dependant_debut', 'relation', 'interpretation']):
        return False
    # Un point pour des repères effectivement retrouvables, pas pour leur interprétation.
    return all(isinstance(value[k], str) and value[k] and integer(value[k + '_debut'])
               and source[value[k + '_debut']:value[k + '_debut'] + len(value[k])] == value[k]
               for k in ['verbe', 'dependant']) and string(value['relation']) and isinstance(value['interpretation'], str)


def counts_td1(value, source):
    return (keys(value, ['split', 'tokens', 'non_ponctuation', 'interpretation'])
            and type(value['split']) is int and value['split'] == len(source.split())
            and integer(value['tokens'], value['split']) and value['tokens'] <= len(source)
            and integer(value['non_ponctuation'], 1) and value['non_ponctuation'] <= value['tokens']
            and isinstance(value['interpretation'], str))


def transfer(value):
    return (keys(value, ['texte', 'phrases', 'annotations', 'noms', 'verbes', 'question']) and string(value['texte'])
            and integer(value['phrases'], 2) and value['phrases'] <= 4
            and annotations(value['annotations'], value['texte'], count=5, offsets=True)
            and strings(value['noms']) and strings(value['verbes']) and isinstance(value['question'], str))


def summary_td2(value, source):
    return (keys(value, ['caracteres', 'phrases', 'tokens', 'annotations'])
            and type(value['caracteres']) is int and value['caracteres'] == len(source)
            and integer(value['phrases'], 1) and value['phrases'] <= len(source.split())
            and integer(value['tokens'], len(source.split())) and value['tokens'] <= len(source)
            and annotations(value['annotations'], source, count=10))


def two_frequencies(value, source):
    return (keys(value, ['noms', 'verbes']) and frequencies(value['noms']) and frequencies(value['verbes'])
            and sum(value['noms'].values()) + sum(value['verbes'].values()) <= len(source.split()))


def exclusions(value, context):
    return (keys(value, ['exclusions', 'avant', 'apres', 'justification'])
            and strings(value['exclusions']) and bool(value['exclusions'])
            and frequencies(value['avant']) and frequencies(value['apres'], allow_empty=True)
            and value['avant'] == context.get(2, {}).get('noms')
            and any(k in value['avant'] for k in value['exclusions'])
            and all(k == k.lower() for k in value['exclusions'])
            and value['apres'] == {k: v for k, v in value['avant'].items() if k.lower() not in value['exclusions']}
            and isinstance(value['justification'], str))


def pos_counts(value, source):
    if not keys(value, ['pos', 'top3', 'limite']) or not frequencies(value['pos']):
        return False
    counts, top = value['pos'], value['top3']
    return (set(counts) <= POS - {'PUNCT', 'SPACE'} and sum(counts.values()) <= len(source.split())
            and isinstance(top, list) and len(top) == min(3, len(counts))
            and all(isinstance(row, list) and len(row) == 2 and integer(row[1], 1) and counts.get(row[0]) == row[1] for row in top)
            and len({r[0] for r in top}) == len(top)
            and [r[1] for r in top] == sorted(counts.values(), reverse=True)[:3]
            and isinstance(value['limite'], str))


def linguistic_review(value, source):
    return (keys(value, ['lemmes', 'controle', 'limite_modele']) and strings(value['lemmes']) and bool(value['lemmes'])
            and len(value['lemmes']) <= len(source.split())
            and isinstance(value['controle'], list) and len(value['controle']) == 5
            and all(keys(row, ['forme', 'lemme', 'pos', 'jugement'])
                    and all(isinstance(row[k], str) and row[k] for k in ['forme', 'lemme', 'pos'])
                    and row['forme'] in source and row['pos'] in POS and isinstance(row['jugement'], str)
                    for row in value['controle'])
            and isinstance(value['limite_modele'], str))


def chart_data(value, context):
    return (keys(value, ['frequences', 'hypothese', 'verification']) and frequencies(value['frequences'])
            and value['frequences'] == context.get(3, {}).get('apres')
            and isinstance(value['hypothese'], str) and isinstance(value['verification'], str))


def generalization(value, context):
    required = ['general_noms', 'specialise_noms', 'general_verbes', 'specialise_verbes', 'combine', 'comparaison']
    if not keys(value, required) or not all(frequencies(value[k]) for k in required[:-1]):
        return False
    nouns, verbs = context.get(2, {}).get('noms'), context.get(2, {}).get('verbes')
    return (nouns is not None and verbs is not None
            and value['general_noms'] == value['specialise_noms'] == nouns
            and value['general_verbes'] == value['specialise_verbes'] == verbs
            and value['combine'] == dict(Counter(nouns) + Counter(verbs))
            and isinstance(value['comparaison'], str))
