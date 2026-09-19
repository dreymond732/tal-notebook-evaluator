# Fichier: app/routes.py
import os
from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from importlib import import_module
from functools import wraps
from markupsafe import escape
import outils
main_bp = Blueprint('main', __name__)

# Dictionnaire de configuration : Clé URL -> (Nom Affiché, Nom du Module Python)
# IMPORTANT : Les noms de modules doivent utiliser des underscores (_), pas des tirets (-).
EVALUATORS = {
    'td1-s1': ('TD1 S1 - Variables et types', 'app_correction_TD1_S1'),
    'td2-s1': ('TD2 S1 - Chaînes et séquences', 'app_correction_TD2_S1'),
    'td3-s1': ('TD3 S1 - Collections', 'app_correction_TD3_S1'),
    'td4-s1': ('TD4 S1 - Boucles et conditions', 'app_correction_TD4_S1'),
    'td5-s1': ('TD5 S1 - Fonctions', 'app_correction_TD5_S1'),
    'td6-s1': ('TD6 S1 - Fichiers et données', 'app_correction_TD6_S1'),
    'td7-s1': ('TD7 S1 - Expressions régulières', 'app_correction_TD7_S1'),
    'td2-S2': ('TD2 S2 - Bases', 'app_correction_TD2_S2'),
    'td3-S2': ('TD3 S2 - Structures', 'app_correction_TD3_S2'),
    'td4-S2': ('TD4 S2 - Logique', 'app_correction_TD4_S2'),
    'td5-S2': ('TD5 S2 - Algorithmique avancée', 'app_correction_TD5_S2'),
    'td6-S2': ('TD6 S2 - Fichiers', 'app_correction_TD6_S2'),
    'td0-s3': ('TD0 S3 - Diagnostic texte', 'app_correction_TD0_S3'),
    'td-r0-s3': ('R0 S3 - Python pour le texte', 'app_correction_R0_S3'),
    'td-r1-s3': ('R1 S3 - Parcourir un Doc spaCy', 'app_correction_R1_S3'),
    'td-r2-s3': ('R2 S3 - Fréquences réutilisables', 'app_correction_R2_S3'),
    'Controletilt-s1': ('Contrôle TAL - S1', 'app_correction_controle_S1'),
    #'ControleS2': ('Contrôle S2', 'app_correction_controle_S2'),
    'ControleDevoirMaisonS2': ('Contrôle DM S2', 'app_correction_devoirMaisonS2'),
}

# Mode pédagogique explicite, indépendant du nom et de l'URL.
# Les deux supports S2 ambigus portent un titre « Contrôle » : pas de retour
# pédagogique public tant que l'enseignant n'a pas arbitré leur statut.
EVALUATOR_MODES = {
    'td1-s1': 'td',
    'td2-s1': 'td',
    'td3-s1': 'td',
    'td4-s1': 'td',
    'td5-s1': 'td',
    'td6-s1': 'td',
    'td7-s1': 'td',
    'td2-S2': 'controle',
    'td3-S2': 'td',
    'td4-S2': 'controle',
    'td5-S2': 'td',
    'td6-S2': 'td',
    'td0-s3': 'td',
    'td-r0-s3': 'td',
    'td-r1-s3': 'td',
    'td-r2-s3': 'td',
    'Controletilt-s1': 'controle',
    'ControleDevoirMaisonS2': 'controle',
}


def load_evaluator(f):
    @wraps(f)
    def decorated_function(eval_name, *args, **kwargs):
        if eval_name not in EVALUATORS:
            flash(f"Évaluateur '{eval_name}' non trouvé.", 'error')
            return redirect(url_for('main.index'))

        display, module_name = EVALUATORS[eval_name]
        if EVALUATOR_MODES.get(eval_name) not in {'td', 'controle'}:
            current_app.logger.error("Mode pédagogique absent ou invalide : %s", eval_name)
            return "Évaluation temporairement indisponible. Contactez l'enseignant.", 503
        try:
            eval_module = import_module(module_name)
        except ImportError:
            current_app.logger.exception("Chargement impossible : %s", eval_name)
            return "Évaluation temporairement indisponible. Contactez l'enseignant.", 503
        return f(eval_module, display, eval_name, *args, **kwargs)

    return decorated_function


@main_bp.route('/', methods=['GET'])
def index():
    return render_template('selector_template.html', evaluators=EVALUATORS)


@main_bp.route('/eval/<eval_name>', methods=['GET', 'POST'])
@load_evaluator
def route_evaluator(eval_module, display_name, eval_name):
    is_td = EVALUATOR_MODES[eval_name] == 'td'
    allowed_ext = '.ipynb'
    template = 'corrector_template.html' if is_td else 'controle_receipt_template.html'

    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename:
            flash("Aucun fichier sélectionné.", 'error')
            return render_eval_template(template, display_name, eval_name, allowed_ext, is_td)

        if file.filename.endswith(allowed_ext):
            try:
                content_bytes = file.read()
                try:
                    content_str = content_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    content_str = content_bytes.decode('windows-1252', errors='ignore')

                # Appel de la fonction de correction du module chargé
                if hasattr(eval_module, 'check_notebook'):
                    score, details, max_s, info, err = eval_module.check_notebook(content_str, file.filename)
                    if err: raise Exception(err)

                    params = {"score": score, "details": details, "max_score": max_s,
                              "filename": file.filename, "student_info": info,
                              "display_name": display_name, "evaluator_name": eval_name,
                              "allowed_extension": allowed_ext, "is_td": is_td}

                    report_template = 'corrector_template.html' if is_td else 'controle_corrector_template.html'
                    if not is_td:
                        # Le template historique rend student_answer avec |safe.
                        # Un rapport enseignant ne doit pas exécuter du HTML étudiant.
                        params['details'] = [dict(d, student_answer=escape(d.get('student_answer', '')))
                                             for d in details]
                        # Le rendu privé ne doit pas consommer/cacher les messages
                        # de dépôt avant une éventuelle erreur de sauvegarde.
                        params['get_flashed_messages'] = lambda **kwargs: []
                    html = render_template(report_template, **params)
                    process_submission(file, content_bytes, html, info, score, eval_name)
                    if is_td:
                        return html
                    # Ne transmettre aucun résultat au template public, même caché.
                    return render_template(template, display_name=display_name,
                                           evaluator_name=eval_name, received=True,
                                           allowed_extension=allowed_ext)
                else:
                    raise Exception("Fonction check_notebook manquante")
            except Exception as e:
                if is_td:
                    flash(f"Erreur: {e}", 'error')
                else:
                    current_app.logger.exception("Échec du dépôt de contrôle : %s", eval_name)
                    flash("Le dépôt n'a pas pu être confirmé. Contactez l'enseignant.", 'error')
                return render_eval_template(template, display_name, eval_name, allowed_ext, is_td)
        else:
            flash("Le fichier doit être au format .ipynb.", 'error')
    return render_eval_template(template, display_name, eval_name, allowed_ext, is_td)

def render_eval_template(template, display_name, eval_name, ext, is_td):
    return render_template(template, display_name=display_name, evaluator_name=eval_name,
                           allowed_extension=ext, is_td=is_td, score=None, student_info={}, details=[])


def process_submission(file, nb_bytes, html_report, info, score, eval_name):
    """Sauvegarde les fichiers et log la note."""
    try:
        outils.log_grade_to_csv(eval_name, info, score)

        classe = info.get('classe', 'SANS_CLASSE')
        # Nettoyage des noms pour éviter les problèmes de chemin de fichier
        s_nom = secure_filename(info.get('nom', 'NON_RENSEIGNE')).upper()
        s_prenom = secure_filename(info.get('prenom', 'NON_RENSEIGNE')).capitalize()

        # 1. Sauvegarde Notebook
        nb_name = f"{s_nom}_{s_prenom}_{secure_filename(file.filename)}"
        nb_path = outils.get_nb_path(eval_name, classe, nb_name)
        os.makedirs(os.path.dirname(nb_path), exist_ok=True)
        with open(nb_path, 'wb') as f:
            f.write(nb_bytes)

        # 2. Sauvegarde Rapport HTML
        rep_name = f"{s_nom}_{s_prenom}_{eval_name}.html"
        rep_path = outils.get_rapport_path(eval_name, classe, rep_name)
        os.makedirs(os.path.dirname(rep_path), exist_ok=True)
        with open(rep_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
    except OSError as e:
        raise RuntimeError(f"Erreur lors de la sauvegarde : {e}") from e
