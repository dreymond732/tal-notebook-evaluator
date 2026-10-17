"""Read saved answer evidence for reports, without evaluating submitted code."""
import json


def _text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return ''.join(value)
    return json.dumps(value, ensure_ascii=False)


def answer_evidence(notebook, question):
    """Return exact sources and saved textual outputs of explicit answer cells.

    Validation remains the evaluator's responsibility. In particular, malformed
    JSON traces, duplicate prints and errors must stay visible in the report.
    Rich HTML and executable output formats are never rendered as HTML here.
    """
    question = str(question)
    if not question.startswith('Q'):
        question = 'Q' + question
    sources, outputs, numbers = [], [], []
    for number, cell in enumerate(notebook.get('cells', []), 1):
        metadata = cell.get('metadata', {})
        tal = metadata.get('tal', {}) if isinstance(metadata, dict) else {}
        if not isinstance(tal, dict) or tal.get('role') != 'answer' or tal.get('question') != question:
            continue
        numbers.append(number)
        sources.append(_text(cell.get('source', '')))
        saved = cell.get('outputs', [])
        if not isinstance(saved, list):
            outputs.append(_text(saved))
            continue
        for output in saved:
            if not isinstance(output, dict):
                outputs.append(_text(output))
            elif output.get('output_type') == 'stream':
                outputs.append(_text(output.get('text', '')))
            elif output.get('output_type') == 'error':
                traceback = output.get('traceback', [])
                outputs.append('\n'.join(traceback) if isinstance(traceback, list) and traceback and all(isinstance(line, str) for line in traceback)
                               else _text(traceback) if traceback
                               else f"{output.get('ename', 'Erreur')}: {output.get('evalue', '')}")
            else:
                data = output.get('data', {})
                if isinstance(data, dict) and 'text/plain' in data:
                    outputs.append(_text(data['text/plain']))
    return {'student_code': '\n\n'.join(sources),
            'student_output': ''.join(outputs), 'answer_cells': numbers}
