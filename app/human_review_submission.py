"""Receive registered, ungraded work without executing code or rendering its HTML."""
import csv
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from flask import render_template
from werkzeug.utils import secure_filename

import outils
from notebook_contract import HUMAN_REVIEW_QUESTION_COUNTS
from s3_review import review_evidence


def _csv_text(value):
    """Keep spreadsheet applications from interpreting student text as formulas."""
    return "'" + value if value.lstrip().startswith(('=', '+', '-', '@')) else value


def receive_submission(entry, notebook, raw, filename, identity):
    """Confirm only after notebook, inert evidence report and ungraded log are saved.

    A fresh receipt ID preserves successive submissions. Any storage error is
    propagated; the caller must not display a successful receipt in that case.
    """
    receipt_id = uuid4().hex
    storage_id = entry['id'] + '-v2-human-review'
    evidence = review_evidence(notebook, HUMAN_REVIEW_QUESTION_COUNTS[entry['id']],
                               additional_questions=('bilan',))
    report = render_template('human_review_report_template.html', title=entry['title'],
                             identity=identity, evidence=evidence, receipt_id=receipt_id)
    filename = secure_filename(filename) or 'copie.ipynb'
    nb_path = Path(outils.get_nb_path(storage_id, identity['classe'], receipt_id + '_' + filename))
    report_path = Path(outils.get_rapport_path(storage_id, identity['classe'], receipt_id + '.html'))
    journal_path = report_path.parent.parent / 'receptions.csv'
    nb_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    nb_path.write_bytes(raw)
    report_path.write_text(report, encoding='utf-8')
    write_header = not journal_path.exists() or journal_path.stat().st_size == 0
    with journal_path.open('a', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream, delimiter=';')
        if write_header:
            writer.writerow(['Date UTC', 'Réception', 'Sujet', 'Nom', 'Prénom', 'Classe',
                             'Numéro étudiant', 'Statut', 'Notebook', 'Rapport'])
        writer.writerow([datetime.now(timezone.utc).isoformat(), receipt_id, entry['id'],
                         *[_csv_text(identity[key]) for key in ('nom', 'prenom', 'classe', 'numero_etudiant')],
                         'À relire — aucune note automatique', nb_path.name, report_path.name])
    return receipt_id
