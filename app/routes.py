# Fichier: app/routes.py
import os
from flask import Blueprint, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from importlib import import_module
from functools import wraps
import outils
main_bp = Blueprint('main', __name__)

# Dictionnaire de configuration : Clé URL -> (Nom Affiché, Nom du Module Python)
# IMPORTANT : Les noms de modules doivent utiliser des underscores (_), pas des tirets (-).
EVALUATORS = {
    'td2-S2': ('TD2 S2 - Bases', 'app_correction_TD2_S2'),
    'td3-S2': ('TD3 S2 - Structures', 'app_correction_TD3_S2'),
    'td4-S2': ('TD4 S2 - Logique', 'app_correction_TD4_S2'),
    'td5-S2': ('TD5 S2 - Algorithmique avancée', 'app_correction_TD5_S2'),
    'td6-S2': ('TD6 S2 - Fichiers', 'app_correction_TD6_S2'),
    'Controletilt-s1': ('Contrôle TAL - S1', 'app_correction_controle_S1'),
}


def load_evaluator(f):
    @wraps(f)
    def decorated_function(eval_name, *args, **kwargs):
        if eval_name not in EVALUATORS:
            flash(f"Évaluateur '{eval_name}' non trouvé.", 'error')
            return redirect(url_for('main.index'))

        display, module_name = EVALUATORS[eval_name]
        try:
            eval_module = import_module(module_name)
            return f(eval_module, display, eval_name, *args, **kwargs)
        except ImportError as e:
            flash(f"Module '{module_name}' introuvable : {e}", 'error')
            return redirect(url_for('main.index'))

    return decorated_function


@main_bp.route('/', methods=['GET'])
def index():
    return render_template('selector_template.html', evaluators=EVALUATORS)


@main_bp.route('/eval/<eval_name>', methods=['GET', 'POST'])
@load_evaluator
def route_evaluator(eval_module, display_name, eval_name):
    # Détection automatique du mode (TD vs Contrôle) basé sur le nom
    is_td = 'td' in eval_name.lower()
    allowed_ext = '.ipynb'
    # Utilisation du template approprié
    template = 'corrector_template.html' if is_td else 'controle_corrector_template.html'
    # Cas particulier pour le contrôle S1 qui avait son propre template dans l'ancien code
    if eval_name == 'Controletilt-s1':
        template = 'controle_corrector_template.html'

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

                    html = render_template(template, **params)
                    process_submission(file, content_bytes, html, info, score, eval_name)
                    return html
                else:
                    raise Exception("Fonction check_notebook manquante")
            except Exception as e:
                flash(f"Erreur: {e}", 'error')

            process_submission(file, content_bytes, html_rendered, info, score, eval_name)
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
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")