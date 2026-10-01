"""Collecte inerte et bornée des preuves à relire ; aucun HTML soumis rendu."""

MAX_SOURCE = 16000
MAX_OUTPUT = 4000
MAX_CELLS_PER_QUESTION = 12


def _text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return ''.join(value)
    return ''


def review_evidence(notebook, questions):
    """Rassemble code, analyses explicitement rattachées et présence des figures.

    Les cellules libres sont présentées séparément : leur position n'est pas une
    preuve d'appartenance à un exercice. Les chaînes restent du texte, jamais du
    Markup ; les templates les échappent, y compris SVG/HTML displaCy.
    """
    groups = {f'Q{q}': [] for q in range(1, questions + 1)}
    groups['Cellules non attribuées (consignes comprises)'] = []
    omitted = {question: 0 for question in groups}
    for index, cell in enumerate(notebook.get('cells', [])):
        metadata = cell.get('metadata', {})
        tal = metadata.get('tal', {})
        review = metadata.get('tal_review', {})
        question = tal.get('question') if tal.get('role') == 'answer' else review.get('question') if isinstance(review, dict) else None
        if not isinstance(question, str) or question not in groups:
            # Ne présenter ni préparation, ni consignes, ni cellules de dépôt.
            if tal or 'tal_tutor' in metadata:
                continue
            question = 'Cellules non attribuées (consignes comprises)'
        if len(groups[question]) >= MAX_CELLS_PER_QUESTION:
            omitted[question] += 1
            continue
        source = _text(cell.get('source', ''))
        outputs, figures, outputs_truncated = [], [], False
        if len(cell.get('outputs', [])) > 30:
            outputs_truncated = True
        for output in cell.get('outputs', [])[:30]:
            data = output.get('data', {})
            if isinstance(data, dict):
                figures.extend(mime for mime in data if mime.startswith('image/') or mime == 'text/html')
                plain = _text(data.get('text/plain', ''))
                if plain:
                    outputs_truncated |= len(plain) > MAX_OUTPUT
                    outputs.append(plain[:MAX_OUTPUT])
            if output.get('output_type') == 'stream':
                stream = _text(output.get('text', ''))
                outputs_truncated |= len(stream) > MAX_OUTPUT
                outputs.append(stream[:MAX_OUTPUT])
            elif output.get('output_type') == 'error':
                error_name = str(output.get('ename', 'Erreur enregistrée'))
                outputs_truncated |= len(error_name) > 200
                outputs.append(error_name[:200])
        output_text = '\n'.join(outputs)
        groups[question].append({
            'cell_number': index + 1, 'cell_id': str(cell.get('id', 'sans identifiant'))[:120],
            'kind': cell.get('cell_type', ''), 'source': source[:MAX_SOURCE],
            'source_truncated': len(source) > MAX_SOURCE,
            'outputs': output_text[:MAX_OUTPUT],
            'outputs_truncated': outputs_truncated or len(output_text) > MAX_OUTPUT,
            'figures': sorted(set(figures)),
        })
    return [{'question': question, 'cells': cells, 'omitted': omitted[question]}
            for question, cells in groups.items() if cells or omitted[question]]
