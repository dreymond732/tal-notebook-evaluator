# Fichier: app/routes.py
import os
import json
from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app, abort
from werkzeug.utils import secure_filename
from importlib import import_module
from functools import wraps
from markupsafe import escape
from uuid import uuid4
from storage_layout import storage_id
import outils
from notebook_contract import ContractError, resolve_notebook, validate_catalog, STRICT_VERSIONED, CONTRACT_VERSIONS, strict_contract_identity, human_review_identity
main_bp = Blueprint('main', __name__)

# Dictionnaire de configuration : Clé URL -> (Nom Affiché, Nom du Module Python)
# IMPORTANT : Les noms de modules doivent utiliser des underscores (_), pas des tirets (-).
EVALUATORS = {
    'td1-s1': ('S1_TD1 — Variables et types', 'app_correction_TD1_S1'),
    'td2-s1': ('S1_TD2 — Chaînes et séquences', 'app_correction_TD2_S1'),
    'td3-one-s1': ('S1_TD3_one — Construire et transformer des listes', 'app_correction_TD3_one_S1'),
    'td3-bis-s1': ('S1_TD3_bis — Lire et recomposer des tuples', 'app_correction_TD3_bis_S1'),
    'td3-ter-s1': ('S1_TD3_ter — Associer et comparer les données', 'app_correction_TD3_ter_S1'),
    'td3-s1': ('Synthèse historique S1_TD3 — Collections', 'app_correction_TD3_S1'),
    'td4-one-s1': ('S1_TD4_A — Choisir et filtrer dans un parcours', 'app_correction_TD4_one_S1'),
    'td4-bis-s1': ('S1_TD4_B — Bornes et répétitions', 'app_correction_TD4_bis_S1'),
    'td4-ter-s1': ('S1_TD4_C — Comptages et compréhensions', 'app_correction_TD4_ter_S1'),
    'td4-s1': ('Synthèse historique S1_TD4 — Boucles et conditions', 'app_correction_TD4_S1'),
    'td5-one-s1': ('S1_TD5_A — Définir, appeler et retourner', 'app_correction_TD5_one_S1'),
    'td5-bis-s1': ('S1_TD5_B — Paramètres, défauts et portée', 'app_correction_TD5_bis_S1'),
    'td5-ter-s1': ('S1_TD5_C — Composer des fonctions pour le texte', 'app_correction_TD5_ter_S1'),
    'td5-s1': ('Synthèse historique S1_TD5 — Fonctions', 'app_correction_TD5_S1'),
    'dm-intermediaire-s1': ('Devoir maison intermédiaire S1 - Après le TD5', 'app_correction_DM_intermediaire_S1'),
    'td6-one-s1': ('S1_TD6_A — Fichiers texte', 'app_correction_TD6_one_S1'),
    'td6-bis-s1': ('S1_TD6_B — Données délimitées et regroupement', 'app_correction_TD6_bis_S1'),
    'td6-ter-s1': ('S1_TD6_C — Écrire et relire des CSV', 'app_correction_TD6_ter_S1'),
    'td6-s1': ('Synthèse historique S1_TD6 — Fichiers et données', 'app_correction_TD6_S1'),
    'td7-s1': ('S1_TD7 — Expressions régulières', 'app_correction_TD7_S1'),
    'td2-S2': ('Contrôle TD2 S2 — Algorithmique', 'app_correction_TD2_S2'),
    'td3-S2': ('TD3 S2 — Algorithmique et structures', 'app_correction_TD3_S2'),
    'td4-S2': ('Contrôle TD4 S2 — Ensembles', 'app_correction_TD4_S2'),
    'td5-S2': ('TD5 S2 — Algorithmes du texte', 'app_correction_TD5_S2'),
    'td6-S2': ('TD6 S2 — Fichiers et ressources', 'app_correction_TD6_S2'),
    'td0-s3': ('TD0 S3 - Diagnostic texte et mesures', 'app_correction_TD0_S3'),
    'td-r0-s3': ('R0 S3 - Python pour le texte', 'app_correction_R0_S3'),
    'td1-s3': ('TD1.a S3 - Annoter avec spaCy', 'app_correction_TD1_S3'),
    'td-r1-s3': ('TD1.b S3 - Parcourir un Doc spaCy (bonus facultatif)', 'app_correction_R1_S3'),
    'td1b-s3': ('TD1.c S3 - Entités, similarité et règles', 'app_correction_TD1B_S3'),
    'td-r2-s3': ('R2 S3 - Fréquences réutilisables', 'app_correction_R2_S3'),
    'td2-s3': ('TD2 S3 - Fréquences et objets recherchés', 'app_correction_TD2_S3'),
    'td3-s3': ('TD3 S3 - Concordances et citations', 'app_correction_TD3_S3'),
    'td4-s3': ('TD4 S3 - Cooccurrences définies', 'app_correction_TD4_S3'),
    'td5-s3': ('TD5 S3 - Mesures d’association', 'app_correction_TD5_S3'),
    'td6-s3': ('TD6 S3 - Lecture distante et robustesse', 'app_correction_TD6_S3'),
    'td7-s3': ('TD7 S3 - Audit textométrique reproductible', 'app_correction_TD7_S3'),
    'controle-td1-s3': ('Contrôle TD1 S3 - Acquis cumulés', 'app_correction_Controle_TD1_S3'),
    'controle-td2-s3': ('Contrôle TD2 S3 - Acquis cumulés', 'app_correction_Controle_TD2_S3'),
    'controle-td3-s3': ('Contrôle TD3 S3 - Acquis cumulés', 'app_correction_Controle_TD3_S3'),
    'controle-td4-s3': ('Contrôle TD4 S3 - Acquis cumulés', 'app_correction_Controle_TD4_S3'),
    'controle-td5-s3': ('Contrôle TD5 S3 - Acquis cumulés', 'app_correction_Controle_TD5_S3'),
    'controle-td6-s3': ('Contrôle TD6 S3 - Acquis cumulés', 'app_correction_Controle_TD6_S3'),
    'controle-td7-s3': ('Contrôle TD7 S3 - Acquis cumulés', 'app_correction_Controle_TD7_S3'),
    'Controletilt-s1': ('Contrôle TAL - S1', 'app_correction_controle_S1'),
    #'ControleS2': ('Contrôle S2', 'app_correction_controle_S2'),
    'ControleDevoirMaisonS2': ('Devoir maison S2 — Approfondissement', 'app_correction_devoirMaisonS2'),
}

# Mode pédagogique explicite, indépendant du nom et de l'URL.
# Les deux supports S2 ambigus portent un titre « Contrôle » : pas de retour
# pédagogique public tant que l'enseignant n'a pas arbitré leur statut.
EVALUATOR_MODES = {
    'td1-s1': 'td',
    'td2-s1': 'td',
    'td3-s1': 'td',
    'td3-ter-s1': 'td',
    'td3-bis-s1': 'td',
    'td3-one-s1': 'td',
    'td4-one-s1': 'td',
    'td4-bis-s1': 'td',
    'td4-ter-s1': 'td',
    'td4-s1': 'td',
    'td5-s1': 'td',
    'td5-ter-s1': 'td',
    'td5-bis-s1': 'td',
    'td5-one-s1': 'td',
    'dm-intermediaire-s1': 'controle',
    'td6-s1': 'td',
    'td6-ter-s1': 'td',
    'td6-bis-s1': 'td',
    'td6-one-s1': 'td',
    'td7-s1': 'td',
    'td2-S2': 'controle',
    'td3-S2': 'td',
    'td4-S2': 'controle',
    'td5-S2': 'td',
    'td6-S2': 'td',
    'td0-s3': 'td',
    'td1b-s3': 'td',
    'td1-s3': 'td',
    'td2-s3': 'td',
    'td3-s3': 'td',
    'td4-s3': 'td',
    'td5-s3': 'td',
    'td6-s3': 'td',
    'td7-s3': 'td',
    'controle-td1-s3': 'controle',
    'controle-td2-s3': 'controle',
    'controle-td3-s3': 'controle',
    'controle-td4-s3': 'controle',
    'controle-td5-s3': 'controle',
    'controle-td6-s3': 'controle',
    'controle-td7-s3': 'controle',
    'td-r0-s3': 'td',
    'td-r1-s3': 'td',
    'td-r2-s3': 'td',
    'Controletilt-s1': 'controle',
    'ControleDevoirMaisonS2': 'controle',
}


SEMESTERS = ('S1', 'S2', 'S3')

# Classement explicite : indépendant de la casse des URL historiques et du mode.
EVALUATOR_SEMESTERS = {
    'td1-s1': 'S1',
    'td2-s1': 'S1',
    'td3-s1': 'S1',
    'td3-ter-s1': 'S1',
    'td3-bis-s1': 'S1',
    'td3-one-s1': 'S1',
    'td4-one-s1': 'S1',
    'td4-bis-s1': 'S1',
    'td4-ter-s1': 'S1',
    'td4-s1': 'S1',
    'td5-s1': 'S1',
    'td5-ter-s1': 'S1',
    'td5-bis-s1': 'S1',
    'td5-one-s1': 'S1',
    'dm-intermediaire-s1': 'S1',
    'td6-s1': 'S1',
    'td6-ter-s1': 'S1',
    'td6-bis-s1': 'S1',
    'td6-one-s1': 'S1',
    'td7-s1': 'S1',
    'Controletilt-s1': 'S1',
    'td2-S2': 'S2',
    'td3-S2': 'S2',
    'td4-S2': 'S2',
    'td5-S2': 'S2',
    'td6-S2': 'S2',
    'ControleDevoirMaisonS2': 'S2',
    'td0-s3': 'S3',
    'td1b-s3': 'S3',
    'td1-s3': 'S3',
    'td2-s3': 'S3',
    'td3-s3': 'S3',
    'td4-s3': 'S3',
    'td5-s3': 'S3',
    'td6-s3': 'S3',
    'td7-s3': 'S3',
    'controle-td1-s3': 'S3',
    'controle-td2-s3': 'S3',
    'controle-td3-s3': 'S3',
    'controle-td4-s3': 'S3',
    'controle-td5-s3': 'S3',
    'controle-td6-s3': 'S3',
    'controle-td7-s3': 'S3',
    'td-r0-s3': 'S3',
    'td-r1-s3': 'S3',
    'td-r2-s3': 'S3',
}


def validate_evaluator_semesters():
    """Empêcher qu'un correcteur actif disparaisse du parcours par omission."""
    if set(EVALUATOR_SEMESTERS) != set(EVALUATORS):
        raise ValueError('Chaque correcteur actif doit être associé à un semestre.')
    if any(semester not in SEMESTERS for semester in EVALUATOR_SEMESTERS.values()):
        raise ValueError('Semestre de correcteur invalide : S1, S2 ou S3 attendu.')
    validate_catalog(EVALUATORS, EVALUATOR_MODES, EVALUATOR_SEMESTERS)


@main_bp.context_processor
def semester_navigation():
    return {'evaluator_semesters': EVALUATOR_SEMESTERS}


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
    return render_template('selector_template.html', semesters=SEMESTERS, semester=None)


@main_bp.route('/health', methods=['GET'])
def health():
    return {'status': 'ok', 'evaluators': len(EVALUATORS)}


def read_notebook(content_bytes):
    try:
        content_str = content_bytes.decode('utf-8-sig')
    except UnicodeDecodeError:
        content_str = content_bytes.decode('windows-1252')

    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ContractError('Le notebook contient des champs JSON dupliqués.')
            result[key] = value
        return result

    try:
        notebook = json.loads(content_str, object_pairs_hook=unique_keys)
    except (ValueError, UnicodeError) as exc:
        raise ContractError('Erreur JSON : le fichier ne contient pas un notebook JSON valide.') from exc
    return content_str, notebook


@main_bp.route('/submit', methods=['GET', 'POST'])
def submit_notebook():
    if request.method == 'GET':
        return render_template('submit_template.html', semesters=SEMESTERS)
    file = request.files.get('file')
    try:
        if not file or not file.filename:
            raise ContractError('Aucun fichier sélectionné.')
        if not file.filename.lower().endswith('.ipynb'):
            raise ContractError('Le fichier doit être au format .ipynb.')
        content_bytes = file.read()
        _, notebook = read_notebook(content_bytes)
        entry = resolve_notebook(notebook)
        if entry.get('assessment') == 'human_review':
            identity = human_review_identity(notebook)
            from human_review_submission import receive_submission
            try:
                receive_submission(entry, notebook, content_bytes, file.filename, identity)
            except OSError:
                current_app.logger.exception('Échec du dépôt pour relecture enseignante : %s', entry['id'])
                flash("Le dépôt n'a pas pu être confirmé. Contactez l'enseignant.", 'error')
                return render_template('submit_template.html', semesters=SEMESTERS), 503
            return render_template('human_review_receipt_template.html', title=entry['title'])
        # The same legacy handler owns correction, confidentiality and storage.
        file.stream.seek(0)
        return route_evaluator(entry['evaluator'])
    except (ContractError, UnicodeError) as exc:
        flash(str(exc), 'error')
        return render_template('submit_template.html', semesters=SEMESTERS), 400


@main_bp.route('/semestre/<semester>', methods=['GET'])
def semester_evaluators(semester):
    if semester not in SEMESTERS:
        abort(404)
    evaluators = {name: config for name, config in EVALUATORS.items()
                  if EVALUATOR_SEMESTERS[name] == semester}
    return render_template('selector_template.html', semester=semester,
                           evaluators=evaluators, evaluator_modes=EVALUATOR_MODES)


@main_bp.route('/eval/<eval_name>', methods=['GET', 'POST'])
@load_evaluator
def route_evaluator(eval_module, display_name, eval_name):
    is_td = EVALUATOR_MODES[eval_name] == 'td'
    allowed_ext = '.ipynb'
    # Exception strictement réservée au DM intermédiaire S1 : correction
    # formative immédiatement visible. Les contrôles restent privés.
    student_dm = eval_name == 'dm-intermediaire-s1'
    template = ('corrector_template.html' if is_td else
                'dm_s1_student_report_template.html' if student_dm else
                'controle_receipt_template.html')

    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename:
            flash("Aucun fichier sélectionné.", 'error')
            return render_eval_template(template, display_name, eval_name, allowed_ext, is_td)

        if file.filename.lower().endswith(allowed_ext):
            try:
                content_bytes = file.read()
                content_str, notebook = read_notebook(content_bytes)
                resolve_notebook(notebook, expected_evaluator=eval_name, require_metadata=False)
                identity = strict_contract_identity(notebook, eval_name) if eval_name in STRICT_VERSIONED else None

                # Appel de la fonction de correction du module chargé
                if hasattr(eval_module, 'check_notebook'):
                    score, details, max_s, info, err = eval_module.check_notebook(content_str, file.filename)
                    if err: raise Exception(err)
                    if identity is not None:
                        info = dict(info, **identity, contract_version=CONTRACT_VERSIONS[eval_name])

                    params = {"score": score, "details": details, "max_score": max_s,
                              "filename": file.filename, "student_info": info,
                              "display_name": display_name, "evaluator_name": eval_name,
                              "allowed_extension": allowed_ext, "is_td": is_td}

                    report_template = 'corrector_template.html' if is_td else 'controle_corrector_template.html'
                    if not is_td and info.get('score_nature') == 'technique_provisoire':
                        report_template = 's3_controle_report_template.html'
                        if hasattr(eval_module, 'HUMAN_REVIEW'):
                            params['human_review'] = eval_module.HUMAN_REVIEW
                        else:
                            # Compatibility for the existing S3 control modules.
                            from s3_controls import HUMAN_REVIEW
                            params['human_review'] = HUMAN_REVIEW
                        params['human_review_dimensions'] = getattr(eval_module, 'HUMAN_REVIEW_DIMENSIONS', None)
                    if not is_td:
                        # Le template historique rend student_answer avec |safe.
                        # Un rapport enseignant ne doit pas exécuter du HTML étudiant.
                        params['details'] = [dict(d, student_answer=escape(d.get('student_answer', '')))
                                             for d in details]
                    # Construire le rapport sans consommer les messages de la
                    # réponse publique avant de savoir si la sauvegarde réussit.
                    params['get_flashed_messages'] = lambda **kwargs: []
                    html = render_template(report_template, **params)
                    process_submission(file, content_bytes, html, info, score, eval_name)
                    if is_td:
                        params.pop('get_flashed_messages')
                        return render_template(report_template, **params)
                    if student_dm:
                        # Le rapport détaillé enseignant a déjà été sauvegardé.
                        # Seuls les 18 bilans techniques des questions sont
                        # publiés au déposant, jamais les critères AST ou les
                        # indications de relecture humaine.
                        feedback = eval_module.student_feedback(details)
                        return render_template(
                            template, display_name=display_name,
                            evaluator_name=eval_name, filename=file.filename,
                            score=score, max_score=max_s,
                            student_feedback=feedback,
                        )
                    # Ne transmettre aucun résultat des contrôles au public.
                    return render_template(template, display_name=display_name,
                                           evaluator_name=eval_name, received=True,
                                           allowed_extension=allowed_ext)
                else:
                    raise Exception("Fonction check_notebook manquante")
            except ContractError as e:
                flash(str(e), 'error')
                return render_eval_template(template, display_name, eval_name, allowed_ext, is_td)
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
    """Journal et fichiers regroupés par évaluation, sans répertoire de classe."""
    from progression import progression_lock, refresh_progression

    with progression_lock():
        ident = storage_id(eval_name)
        classe = info.get('classe', 'SANS_CLASSE')
        s_nom = secure_filename(info.get('nom', 'NON_RENSEIGNE')).upper()
        s_prenom = secure_filename(info.get('prenom', 'NON_RENSEIGNE')).capitalize()
        student_suffix = ('_' + secure_filename(info['numero_etudiant'])) if info.get('numero_etudiant') else ''
        receipt = uuid4().hex
        nb_name = f"{s_nom}_{s_prenom}{student_suffix}_{receipt}_{secure_filename(file.filename)}"
        rep_name = f"{s_nom}_{s_prenom}{student_suffix}_{receipt}_{eval_name}.html"
        nb_path = outils.get_nb_path(ident, classe, nb_name)
        rep_path = outils.get_rapport_path(ident, classe, rep_name)
        created = []
        try:
            # Un identifiant par réception empêche l'écrasement de deux essais,
            # y compris lorsque les étudiants changent la classe renseignée.
            os.makedirs(os.path.dirname(nb_path), exist_ok=True)
            os.makedirs(os.path.dirname(rep_path), exist_ok=True)
            with open(nb_path, 'xb') as stream:
                created.append(nb_path)
                stream.write(nb_bytes)
            with open(rep_path, 'x', encoding='utf-8') as stream:
                created.append(rep_path)
                stream.write(html_report)
            outils.log_grade_to_csv(ident, dict(info, submission_id=receipt), score)
        except (OSError, ValueError) as exc:
            for path in created:
                try:
                    os.unlink(path)
                except OSError:
                    current_app.logger.exception("Nettoyage d'un dépôt incomplet : %s", eval_name)
            raise RuntimeError(f"Erreur lors de la sauvegarde : {exc}") from exc
        try:
            refresh_progression()
        except Exception:
            current_app.logger.exception(
                "Consolidation privée indisponible après dépôt : %s", eval_name
            )
