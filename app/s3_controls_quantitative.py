"""Références recalculées sur les corpus fixes des contrôles C4–C7."""
from collections import Counter
import math
from s3_controls_data import C4, C5, C6, C7


def equivalent(actual, expected):
    """Comptages typés ; mesures réelles acceptées exactes ou arrondies à six décimales."""
    if type(expected) is float:
        return type(actual) in (int, float) and math.isfinite(actual) and math.isclose(actual, expected, rel_tol=0, abs_tol=1e-6)
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(equivalent(actual[k], v) for k, v in expected.items())
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(equivalent(a, b) for a, b in zip(actual, expected))
    return actual == expected


def occurrences(tokens, expression):
    size = len(expression)
    return [i for i in range(len(tokens) - size + 1) if tokens[i:i+size] == expression] if size else []


def measure(contexts, pivots, associates):
    p = {i for i, row in enumerate(contexts) if any(occurrences(row, expr) for expr in pivots)}
    a = {i for i, row in enumerate(contexts) if any(occurrences(row, expr) for expr in associates)}
    return {'N': len(contexts), 'marge_pivot': len(p), 'marge_associe': len(a), 'cooc': len(p & a), 'indices': sorted(p & a)}


def pair(contexts, pivot, associate):
    return measure(contexts, [[pivot]], [[associate]])


def sum_pairs(contexts, pivots, associates):
    return sum(measure(contexts, [p], [a])['cooc'] for p in pivots for a in associates)


def positional_pairs(tokens, pivot, associate, width):
    return [[i, j] for i, left in enumerate(tokens) for j, right in enumerate(tokens)
            if left == pivot and right == associate and 0 < abs(i-j) <= width]


def divide(numerator, denominator):
    return numerator / denominator if denominator else None


def covered(tokens, pivot, associate, width):
    indices = sorted({r[0] for r in positional_pairs(tokens, pivot, associate, width)})
    total = tokens.count(pivot)
    return {'indices_pivots': indices, 'couverts': len(indices), 'total': total, 'proportion': divide(len(indices), total)}


def contingency(m):
    common, left, right, size = m['cooc'], m['marge_pivot'], m['marge_associe'], m['N']
    return [[common, left-common], [right-common, size-left-right+common]]


def c4_expected():
    rows = C4['mobilite']
    br, ba = pair(rows, 'bus', 'retard'), pair(rows, 'bus', 'accès')
    union = measure(rows, [['bus']], [['retard'], ['accès']])
    window = {f'k{k}': {'effectif': len(positional_pairs(C4['flux_mobilite'], 'bus', 'retard', k)), 'paires': positional_pairs(C4['flux_mobilite'], 'bus', 'retard', k)} for k in (1, 3)}
    dossiers = [[term for i in members for term in rows[i]] for members in C4['dossiers_mobilite']]
    grouped = pair(dossiers, 'bus', 'retard')
    archives = C4['archives_sonores']
    union_archives = measure(archives, [['voix']], [['bruit'], ['silence']])
    return [
        {'N': len(rows), 'frequences': dict(Counter(t for row in rows for t in row)), 'marge_bus': br['marge_pivot']},
        {'bus_retard': br, 'bus_acces': ba},
        {'somme_paires': br['cooc'] + ba['cooc'], 'union': union['cooc'], 'indices_union': union['indices'], 'indices_plusieurs_paires': sorted(set(br['indices']) & set(ba['indices']))},
        window,
        {'par_fiche': br['cooc'], 'par_dossier': grouped['cooc'], 'indices_dossiers': grouped['indices'], 'N_dossiers': grouped['N']},
        {'formes_retard': sum(r['forme'] == 'retard' for r in C4['annotations_mobilite']), 'lemmes_retard': sum(r['lemme'] == 'retard' for r in C4['annotations_mobilite']), 'expressions': [[i, j] for i, row in enumerate(C4['acces_mobilite']) for j in occurrences(row, ['accès', 'libre'])]},
        {'voix_bruit': pair(archives, 'voix', 'bruit'), 'somme_paires': sum_pairs(archives, [['voix']], [['bruit'], ['silence']]), 'union': union_archives['cooc'], 'indices_union': union_archives['indices'], 'notices_memoire_orale': [i for i, row in enumerate(archives) if occurrences(row, ['mémoire', 'orale'])]},
    ]


def c5_expected():
    rows = C5['mediation']
    m = pair(rows, 'visite', 'audio')
    associations = {}
    for name in ('audio', 'atelier'):
        item = pair(rows, 'visite', name)
        conditional, base = divide(item['cooc'], item['marge_pivot']), divide(item['marge_associe'], item['N'])
        associations[name] = {'cooc': item['cooc'], 'marge_associe': item['marge_associe'], 'conditionnelle': conditional, 'base': base, 'ecart': conditional-base}
    rates = {}
    for name, tokens in C5['sections_musee'].items():
        rates[name] = {'effectif': tokens.count('visite'), 'taille': len(tokens), 'pour_mille': 1000*divide(tokens.count('visite'), len(tokens))}
    total_count, total_size = sum(r['effectif'] for r in rates.values()), sum(r['taille'] for r in rates.values())
    rates['global'] = {'effectif': total_count, 'taille': total_size, 'pour_mille': 1000*divide(total_count, total_size)}
    rare = pair(rows, 'guide', 'plan')
    absent = pair(rows, 'navette', 'audio')
    none = pair(rows, 'guide', 'atelier')
    window = {f'k{k}': covered(C5['flux_musee'], 'visite', 'audio', k) for k in (1, 2, 4)}
    window['paires_k4'] = len(positional_pairs(C5['flux_musee'], 'visite', 'audio', 4))
    transfer = pair(C5['bulletins_littoral'], 'plage', 'vent')
    alert = pair(C5['bulletins_littoral'], 'plage', 'alerte')
    return [m,
        {'audio_sachant_visite': divide(m['cooc'], m['marge_pivot']), 'visite_sachant_audio': divide(m['cooc'], m['marge_associe']), 'table': contingency(m)},
        associations, rates,
        {'sans_pivot': divide(absent['cooc'], absent['marge_pivot']), 'sans_associe': divide(none['cooc'], none['marge_pivot']), 'rare': divide(rare['cooc'], rare['marge_pivot']), 'rare_effectif': rare['cooc'], 'rare_denominateur': rare['marge_pivot']},
        window,
        {'plage_vent': transfer, 'vent_sachant_plage': divide(transfer['cooc'], transfer['marge_pivot']), 'plage_sachant_vent': divide(transfer['cooc'], transfer['marge_associe']), 'base_vent': divide(transfer['marge_associe'], transfer['N']), 'alerte_sachant_plage': divide(alert['cooc'], alert['marge_pivot']), 'base_alerte': divide(alert['marge_associe'], alert['N']), 'table': contingency(transfer)},
    ]


def segments(tokens, terms, count):
    size = len(tokens)
    bounds = [[j*size//count, (j+1)*size//count] for j in range(count)]
    chunks = [tokens[start:end] for start, end in bounds]
    return {'bornes': bounds, 'tailles_flux': [len(row) for row in chunks],
            'tailles_alpha': [sum(t.isalpha() for t in row) for row in chunks],
            'effectifs': {term: [sum(t.lower() == term for t in row) for row in chunks] for term in terms}}


def rates_for_segments(s):
    return {term: [1000*divide(n, size) if size else None for n, size in zip(counts, s['tailles_alpha'])] for term, counts in s['effectifs'].items()}


def token_offsets(source, tokens):
    result, last = [], 0
    for token in tokens:
        start = source.find(token, last)
        if start < 0 or source[last:start].strip():
            raise ValueError('Flux enseignant non aligné au texte source.')
        result.append([start, start+len(token)])
        last = start+len(token)
    if source[last:].strip():
        raise ValueError('Flux enseignant incomplet.')
    return result


def c6_expected():
    tokens, terms = C6['flux_exposition'], C6['termes_exposition']
    lower = [t.lower() for t in tokens]
    positions = {term: [i for i, t in enumerate(lower) if t == term] for term in terms}
    s = segments(tokens, terms, 4)
    window = {'k': [1, 3, 6], **{term: [len(positional_pairs(lower, 'affiche', term, k)) for k in (1, 3, 6)] for term in ('public', 'atelier')}, 'couverture_public_k6': covered(lower, 'affiche', 'public', 6)['proportion']}
    offsets = token_offsets(C6['texte_exposition'], tokens)
    concordances = []
    for index in (positions['affiche'][0], positions['affiche'][-1]):
        start, end = max(0, index-2), min(len(tokens), index+3)
        left, right = offsets[start][0], offsets[end-1][1]
        concordances.append({'indice': index, 'debut_token': start, 'fin_token': end, 'debut_caractere': left, 'fin_caractere': right, 'passage': C6['texte_exposition'][left:right]})
    matrix = [[pair(C6['fiches_exposition'], a, b)['cooc'] if a != b else 0 for b in terms] for a in terms]
    transfer = segments(C6['flux_ateliers'], C6['termes_ateliers'], 3)
    transfer.pop('tailles_flux')
    transfer['taux'] = rates_for_segments(transfer)
    transfer['global'] = {term: {'effectif': sum(counts), 'taille_alpha': sum(transfer['tailles_alpha']), 'pour_mille': 1000*divide(sum(counts), sum(transfer['tailles_alpha'])), 'moyenne_taux_segmentaires': sum(transfer['taux'][term])/3} for term, counts in transfer['effectifs'].items()}
    return [{'N': len(tokens), 'termes': {term: {'positions': values, 'relatives': [i/len(tokens) for i in values]} for term, values in positions.items()}}, s, rates_for_segments(s), window,
            {'concordances': concordances}, {'termes': terms, 'matrice': matrix, 'preuves_affiche_public': pair(C6['fiches_exposition'], 'affiche', 'public')['indices']}, transfer]


def missing(announcement):
    return [k for k in ('unite', 'fenetre', 'normalisation', 'agregation') if announcement.get(k) is None]


def verdict(announcement, value):
    if missing(announcement):
        return 'insuffisamment défini'
    lower, upper = announcement['intervalle']
    return 'compatible selon le protocole' if lower <= value <= upper else 'contredit selon le protocole'


def quote(source, text, identifier):
    start = source.find(text)
    normalized = lambda s: ' '.join(s.lower().split())
    return {'id': identifier, 'exacte': start >= 0, 'debut': start if start >= 0 else None, 'fin': start+len(text) if start >= 0 else None, 'normalisee': normalized(text) in normalized(source)}


def c7_expected():
    contexts, announcements = C7['phrases_mediatheque'], C7['affirmations_mediatheque']
    measures = {a['id']: measure(contexts, a['pivots'], a['associes']) for a in announcements}
    expression_indices = [i for i, row in enumerate(contexts) if occurrences(row, ['accès', 'libre'])]
    word_indices = [i for i, row in enumerate(contexts) if 'accès' in row and 'libre' in row]
    garden = C7['phrases_jardin']
    gm = measure(garden, [['eau']], [['sol'], ['compost']])
    audit_garden = []
    for a in C7['affirmations_jardin']:
        m = measure(garden, a['pivots'], a['associes'])
        audit_garden.append({'id': a['id'], 'mesure_union': m, 'verdict': verdict(a, m['cooc'])})
    garden_quote = quote(C7['texte_jardin'], C7['citation_jardin'], 'jardin')
    return [
        {'annonces': [{'id': a['id'], 'manquants': missing(a), 'mesurable': not missing(a)} for a in announcements]},
        {'mesures': measures},
        {'citations': [quote(C7['texte_mediatheque'], q['texte'], q['id']) for q in C7['citations_mediatheque']]},
        {'verdicts': {a['id']: verdict(a, measures[a['id']]['cooc']) for a in announcements}},
        {'union_M3': measures['M3']['cooc'], 'somme_M3': sum_pairs(contexts, [['livre']], [['atelier'], ['public']]), 'expressions_acces_libre': expression_indices, 'mots_acces_libre': word_indices, 'faux_rapprochements': sorted(set(word_indices)-set(expression_indices)), 'silence_singulier': pair(contexts, 'livre', 'silence')['cooc'], 'silence_groupe': measures['M4']['cooc']},
        {'union_jardin': gm, 'conditionnelle': divide(gm['cooc'], gm['marge_pivot']), 'somme_paires': sum_pairs(garden, [['eau']], [['sol'], ['compost']]), 'expression_compost': measure(garden, [['eau', 'de', 'pluie']], [['compost']])['cooc'], 'vide': measure([], [['eau']], [['sol']]), 'conditionnelle_vide': None, 'conditionnelle_pivot_absent': None},
        {'audit_jardin': audit_garden, 'citation_exacte': garden_quote['exacte'], 'debut_citation': garden_quote['debut'], 'fin_citation': garden_quote['fin']},
    ]


EXPECTED = {4: c4_expected(), 5: c5_expected(), 6: c6_expected(), 7: c7_expected()}


def validate(number, question, value):
    return equivalent(value, EXPECTED[number][question-1])
