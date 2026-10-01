"""Inert v2 test copies: complete routing contract, saved traces supplied by tests."""
import copy
import re


def notebook(cells, evaluator):
    supplied = copy.deepcopy(cells)
    for cell in supplied:
        if 'tal' not in cell.get('metadata', {}):
            source = ''.join(cell.get('source', ''))
            match = re.search(r'S3_(?:TD|C)\d+_Q(\d+):', source)
            if match:
                cell.setdefault('metadata', {})['tal'] = {
                    'question': 'Q' + match[1], 'role': 'answer'}
    questions = 6 if evaluator == 'td1-s3' else 7
    present = {cell.get('metadata', {}).get('tal', {}).get('question') for cell in supplied}
    if 'identity' not in present:
        supplied.insert(0, {'cell_type': 'code', 'metadata': {'tal': {
            'question': 'identity', 'role': 'identification'}},
            'source': 'nom="Exemple"\nprenom="Alice"\nclasse="S3"\nnumero_etudiant="TEST001"',
            'outputs': []})
    for number in range(1, questions + 1):
        if f'Q{number}' not in present:
            supplied.append({'cell_type': 'code', 'metadata': {'tal': {
                'question': f'Q{number}', 'role': 'answer'}}, 'source': '', 'outputs': []})
    return {'nbformat': 4, 'nbformat_minor': 5, 'metadata': {
        'tal': {'id': evaluator, 'evaluator': evaluator, 'version': 2}}, 'cells': supplied}
