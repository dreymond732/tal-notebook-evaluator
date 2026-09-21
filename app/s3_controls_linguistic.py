"""Contrats C1–C3 : mesures exactes et cohérence des annotations, jamais vérité spaCy."""
from collections import Counter
import re
from s3_audit import integer, keys, same
from s3_audit_linguistic import POS
from s3_controls_data import C1, C2, C3


def fields(value, expected):
    return keys(value, expected) and all(same(value[k], v) for k, v in expected.items())


def annotations(rows, source):
    if not isinstance(rows, list):
        return False
    end = 0
    for row in rows:
        if not keys(row, ('forme', 'lemme', 'pos', 'tag', 'debut', 'fin', 'ponctuation', 'espace', 'mot_vide')):
            return False
        if not all(isinstance(row[k], str) and row[k] for k in ('forme', 'lemme', 'pos', 'tag')) or row['pos'] not in POS:
            return False
        if not all(type(row[k]) is bool for k in ('ponctuation', 'espace', 'mot_vide')):
            return False
        start, finish = row['debut'], row['fin']
        if not integer(start) or not integer(finish) or not end <= start < finish <= len(source):
            return False
        if source[start:finish] != row['forme'] or source[end:start].strip():
            return False
        if row['espace'] != row['forme'].isspace():
            return False
        if not row['espace'] and any(c.isspace() for c in row['forme']):
            return False
        if row['ponctuation'] and any(c.isalnum() for c in row['forme']):
            return False
        end = finish
    return not source[end:].strip()


def annot_value(value, source):
    return keys(value, ['annotations']) and annotations(value['annotations'], source)


def freq(rows, categories, exclusions=()):
    return dict(Counter(r['lemme'].lower() for r in rows if r['pos'] in categories
                        and not (r['mot_vide'] or r['ponctuation'] or r['espace'])
                        and r['lemme'].lower() not in exclusions))


def c1q1(v, ctx):
    words = C1['texte_musee'].lower().split()
    return fields(v, {'caracteres': len(C1['texte_musee']), 'split': C1['texte_musee'].split(),
                      'frequences': dict(Counter(words)), 'formes': len(set(words))})


def c1q3(v, ctx):
    source = C1['texte_musee']
    rows = ctx.get(2, {}).get('annotations')
    if not annotations(rows, source) or not keys(v, ['phrases', 'total_tokens']) or not isinstance(v['phrases'], list) or not v['phrases']:
        return False
    if not same(v['total_tokens'], len(rows)):
        return False
    end, token_sum = 0, 0
    for phrase in v['phrases']:
        if not keys(phrase, ('texte', 'debut', 'fin', 'tokens')):
            return False
        start, finish = phrase['debut'], phrase['fin']
        if not integer(start) or not integer(finish) or not end <= start < finish <= len(source):
            return False
        if source[start:finish] != phrase['texte'] or source[end:start].strip():
            return False
        selected = [r for r in rows if start <= r['debut'] and r['fin'] <= finish]
        if not selected or not same(phrase['tokens'], len(selected)):
            return False
        token_sum += len(selected)
        end = finish
    return not source[end:].strip() and token_sum == len(rows)


def c1q4(v, ctx):
    rows = ctx.get(2, {}).get('annotations')
    if not annotations(rows, C1['texte_musee']):
        return False
    return fields(v, {'noms': [r['lemme'].lower() for r in rows if r['pos'] == 'NOUN'],
                      'verbes': [r['lemme'].lower() for r in rows if r['pos'] == 'VERB'],
                      'contenu': [r['lemme'].lower() for r in rows if r['pos'] in {'NOUN', 'VERB', 'ADJ'} and not (r['mot_vide'] or r['ponctuation'] or r['espace'])]})


def c1q5(v, ctx):
    rows = ctx.get(2, {}).get('annotations')
    if not annotations(rows, C1['texte_musee']) or not keys(v, ['verbe', 'verbe_debut', 'dependant', 'dependant_debut', 'relation']):
        return False
    sentence_start = C1['texte_musee'].index('.') + 1
    sentence_end = C1['texte_musee'].index('.', sentence_start)
    selected = {}
    for field in ('verbe', 'dependant'):
        if not integer(v[field + '_debut']) or not isinstance(v[field], str):
            return False
        selected[field] = next((r for r in rows if r['debut'] == v[field + '_debut'] and r['forme'] == v[field] and sentence_start <= r['debut'] and r['fin'] <= sentence_end), None)
    return bool(selected['verbe'] and selected['dependant'] and selected['verbe']['debut'] != selected['dependant']['debut'] and selected['verbe']['pos'] in {'VERB', 'AUX'} and isinstance(v['relation'], str) and v['relation'].strip())


def c1q6(v, ctx):
    source = C1['texte_transport']
    return (annot_value(v, source) and fields(v, {'split': len(source.split()), 'tokens': len(v['annotations']),
            'lexicaux': sum(not (r['ponctuation'] or r['espace']) for r in v['annotations'])}))


def c1q7(v, ctx):
    if not keys(v, ['bilans']) or not isinstance(v['bilans'], list) or len(v['bilans']) != 4:
        return False
    sources = {'musee': C1['texte_musee'], 'transport': C1['texte_transport'], 'meteo': C1['texte_meteo'], 'vide': ''}
    if {r.get('id') for r in v['bilans'] if isinstance(r, dict)} != set(sources):
        return False
    for row in v['bilans']:
        source = sources[row['id']]
        if not annot_value(row, source) or not keys(row, ['phrases']):
            return False
        if not fields(row, {'caracteres': len(source), 'split': len(source.split()), 'tokens': len(row['annotations'])}):
            return False
        if source and not (integer(row['phrases'], 1) and row['phrases'] <= len(row['annotations'])):
            return False
        if not source and not same(row['phrases'], 0):
            return False
    return True


def c2q1(v, ctx):
    return annot_value(v, C2['texte_atelier']) and fields(v, {'caracteres': len(C2['texte_atelier'])})


def c2q2(v, ctx):
    rows = ctx.get(1, {}).get('annotations')
    return annotations(rows, C2['texte_atelier']) and fields(v, {'noms': freq(rows, {'NOUN'}), 'verbes': freq(rows, {'VERB'})})


def c2q3(v, ctx):
    rows = ctx.get(1, {}).get('annotations')
    return (annotations(rows, C2['texte_atelier']) and fields(v, {'exclusions': ['atelier'], 'avant': freq(rows, {'NOUN'}), 'apres': freq(rows, {'NOUN'}, ['atelier'])}))


def c2q4(v, ctx):
    rows = ctx.get(1, {}).get('annotations')
    if not annotations(rows, C2['texte_atelier']) or not keys(v, ['pos', 'top3']):
        return False
    counts = dict(Counter(r['pos'] for r in rows if not (r['ponctuation'] or r['espace'])))
    top = v['top3']
    return (same(v['pos'], counts) and isinstance(top, list) and len(top) == min(3, len(counts))
            and all(isinstance(r, list) and len(r) == 2 and r[0] in counts and same(r[1], counts[r[0]]) for r in top)
            and len({r[0] for r in top}) == len(top) and [r[1] for r in top] == sorted(counts.values(), reverse=True)[:3])


def c2q5(v, ctx):
    return fields(v, {'noms': {'marin': 1, 'caisse': 2}, 'verbes': {'charger': 1, 'rester': 1},
                      'combine': {'marin': 1, 'caisse': 2, 'charger': 1, 'rester': 1},
                      'exclus': {'marin': 1, 'charger': 1, 'rester': 1}, 'vide': {}})


def c2q6(v, ctx):
    rows = ctx.get(1, {}).get('annotations')
    return annotations(rows, C2['texte_atelier']) and fields(v, {'frequences': freq(rows, {'NOUN'}, ['atelier'])})


def c2q7(v, ctx):
    if not annot_value(v, C2['texte_alimentation']):
        return False
    rows = v['annotations']
    return fields(v, {'noms': freq(rows, {'NOUN'}), 'verbes': freq(rows, {'VERB'}), 'combine': freq(rows, {'NOUN', 'VERB'}), 'vide': {}})


def concordances(source, motif, width):
    if not motif:
        return []
    rows = []
    for m in re.finditer(re.escape(motif), source):
        start, end = m.span()
        rows.append({'debut': start, 'fin': end, 'pivot': motif, 'gauche': source[max(0, start-width):start], 'droite': source[end:end+width]})
    return rows


def citations(source, quotes):
    return [dict(q, debut=source.find(q['citation']), exacte=q['citation'] in source) for q in quotes]


def by_id(actual, expected):
    if not isinstance(actual, list) or len(actual) != len(expected) or not all(isinstance(r, dict) and isinstance(r.get('id'), str) for r in actual):
        return False
    got = {r['id']: r for r in actual}
    return len(got) == len(actual) and all(r['id'] in got and fields(got[r['id']], r) for r in expected)


def c3q1(v, ctx):
    source = C3['texte_patrimoine']
    return fields(v, {'caracteres': len(source), 'split': len(source.split()), 'formes': len(set(source.lower().split())), 'citations': [q['id'] for q in C3['citations']]})


def c3q2(v, ctx):
    return fields(v, {'concordances': concordances(C3['texte_patrimoine'], 'plan', 12), 'absent': []})


def spans(source, motif, whole=False):
    pattern = (r'(?<!\w)' if whole else '') + re.escape(motif) + (r'(?!\w)' if whole else '')
    return [{'forme': m[0], 'debut': m.start(), 'fin': m.end()} for m in re.finditer(pattern, source, re.I if whole else 0)]


def valid_spans(rows, source):
    if not isinstance(rows, list):
        return False
    end = 0
    for r in rows:
        if not keys(r, ['forme', 'debut', 'fin']) or not integer(r['debut']) or not integer(r['fin']) or not end <= r['debut'] < r['fin'] <= len(source) or source[r['debut']:r['fin']] != r['forme']:
            return False
        end = r['fin']
    return True


def c3q3(v, ctx):
    source = C3['texte_patrimoine']
    return (fields(v, {'fragment': spans(source, 'plan'), 'forme': spans(source, 'plan', True), 'expression': spans(source, 'comptes rendus', True)})
            and keys(v, ['lemme']) and bool(v['lemme']) and valid_spans(v['lemme'], source))


def c3q4(v, ctx):
    return keys(v, ['citations']) and by_id(v['citations'], citations(C3['texte_patrimoine'], C3['citations']))


def normalize(source):
    return ' '.join(source.lower().replace('’', "'").split())


def c3q5(v, ctx):
    source = C3['texte_patrimoine']
    normalized = normalize(source)
    expected = [{'id': q['id'], 'retrouvee': normalize(q['citation']) in normalized, 'debut_normalise': normalized.find(normalize(q['citation']))} for q in C3['citations']]
    if not keys(v, ['normalisees', 'candidats']) or not by_id(v['normalisees'], expected):
        return False
    candidates = v['candidats']
    if not isinstance(candidates, list) or len(candidates) != 2 or {r.get('id') for r in candidates if isinstance(r, dict)} != {'P2', 'P3'}:
        return False
    return all(keys(r, ['passage', 'debut', 'fin']) and valid_spans([dict(r, forme=r['passage'])], source) for r in candidates)


def c3q6(v, ctx):
    expected = [{'id': t['id'], 'resultats': concordances(t['source'], t['motif'], t['largeur']), 'erreur': not bool(t['motif'])} for t in C3['tests_concordance']]
    return keys(v, ['tests']) and by_id(v['tests'], expected)


def c3q7(v, ctx):
    source = C3['texte_radio']
    return (fields(v, {'fragment': concordances(source, 'port', 10), 'forme': spans(source, 'port', True)})
            and keys(v, ['citations']) and by_id(v['citations'], citations(source, C3['citations_radio'])))
