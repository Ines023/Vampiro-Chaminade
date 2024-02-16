# /Vampiro/views/AdminViews.py

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename


from Vampiro.models.NewsletterModel import Cronicas
from Vampiro.utils.forms import NewCronicaForm, DisputeInterventionForm, SettingsForm, UploadForm, handle_form_errors
from Vampiro.services.admin_actions import activate_automation, activate_holidays, add_cronica, avisar_a_usuarios, deactivate_automation, deactivate_holidays, download_data, reset_tables, upload_data
from Vampiro.utils.security import handle_exceptions
from Vampiro.services.settings import get_game_status, get_mode, set_mode, set_game_status
from Vampiro.services.game import admin_intervention, dispute_revision, get_alive_players, get_dispute_by_id, get_disputes_filtered, get_hunts_filtered, get_round_number, get_general_number_round_kills, revision_period_done, round_end, start_game

admin = Blueprint('admin', __name__)



@admin.before_request
@login_required
def check_role():
    if current_user.role.name != 'admin':
        return redirect(url_for('profile.my_stats'))


# ADMIN ______________________________________________________________________________________

@admin.route('/dashboard')
@handle_exceptions
def dashboard():   
    game_mode = get_mode()
    game_status = get_game_status()
    jugadores_vivos = len(get_alive_players())
    ronda_actual = get_round_number()
    muertos_ronda =  get_general_number_round_kills(ronda_actual)

    return render_template('admin/dashboard.html', game_mode=game_mode, game_status=game_status, jugadores_vivos=jugadores_vivos, ronda_actual=ronda_actual, muertos_ronda=muertos_ronda)



@admin.route('/aviso a usuarios')
@handle_exceptions
def aviso_a_usuarios():   
    avisar_a_usuarios()
    return redirect(url_for('admin.dashboard'))


@admin.route('/cazas', methods=['GET'])
@handle_exceptions
def cazas():
    page = request.args.get('page', 1, type=int)
    round_filter = request.args.get('round', type=int)
    player_filter = request.args.get('player', type=int)
    date_filter = request.args.get('date')
    success_filter = request.args.get('success')
    order_by = request.args.get('order_by')

    hunts_query = get_hunts_filtered(round_filter, player_filter, date_filter, success_filter, order_by)

    hunts = hunts_query.paginate(page=page, per_page=10, error_out=False, count=True)

    return render_template('admin/cazas.html', hunts=hunts)


@admin.route('/disputas')
@handle_exceptions
def disputas(): 
    page = request.args.get('page', 1, type=int)
    round_filter = request.args.get('round', type=int)
    hunt_filter = request.args.get('hunt_id', type=int)
    hunter_filter = request.args.get('hunter', type=int)
    prey_filter = request.args.get('prey', type=int)
    active_filter = request.args.get('active')
    order_by = request.args.get('order_by')

    disputas_query = get_disputes_filtered(round_filter, hunt_filter, hunter_filter, prey_filter, active_filter, order_by)

    disputas = disputas_query.paginate(page=page, per_page=10, error_out=False, count=True)

    admin_intervention_form = DisputeInterventionForm()

    return render_template('admin/disputas.html', disputas=disputas, admin_intervention_form=admin_intervention_form)  


@admin.route('/dispute_intervention', methods=['POST'])
@handle_exceptions
def dispute_intervention():   

    form = DisputeInterventionForm()

    if form.validate_on_submit():
        dispute_id = form.dispute_id.data
        if form.presa.data:
            response = 'Prey'
        elif form.cazador.data:
            response = 'Hunter'
        print(response)
        dispute = get_dispute_by_id(dispute_id)

        admin_intervention(dispute, response)
    else:
        handle_form_errors(form)
                
    return redirect(url_for('admin.disputas'))


@admin.route('/cronicas', methods=['GET', 'POST'])
@handle_exceptions
def cronicas():   

    form = NewCronicaForm(request.form)
    
    if request.method == 'POST' and form.validate_on_submit():
        date = datetime.now()
        cronica = Cronicas(date=date, title=form.title.data, content=form.content.data)
        add_cronica(cronica)
        flash ('Crónica añadida', 'success')	
        return redirect(url_for('public.cronicas'))
                
    return render_template('admin/new_cronica.html', form=form)

@admin.route('/settings', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()

    if request.method == 'POST':

        if form.validate_on_submit():

            game_mode = form.game_mode.data
            game_status = form.game_status.data

            old_game_status = get_game_status().name

            set_mode(game_mode)
            set_game_status(game_status)

            if old_game_status=='NOT_STARTED' and game_status=='REGISTRY_OPEN':
                avisar_a_usuarios()

            if old_game_status=='REGISTRY_OPEN' and game_status=='IN_PROGRESS':
                start_game()
            
            flash ('Cambios guardados', 'success')

    return render_template('admin/settings.html', form=form)


# ULTIMOS RECURSOS ______________________________________________________________________________________

@admin.route('/intervencion_divina/<accion>')
@handle_exceptions
def intervencion_divina(accion):

    if accion == 'finalizar_ronda':
        round_end()
    elif accion == 'revision_period_done':
        revision_period_done()
    elif accion == 'dispute_revision_day':
        dispute_revision('DAY')
    elif accion == 'dispute_revision_night':
        dispute_revision('NIGHT')
    elif accion == 'activate_automation':
        activate_automation()
    elif accion == 'deactivate_automation':
        deactivate_automation()
    elif accion == 'holidays':
        activate_holidays()
    elif accion == 'vuelta_al_cole':
        deactivate_holidays()
    else:
        pass

    return render_template('admin/intervencion_divina.html')


@admin.route('/database_management', methods=['GET', 'POST'])
@handle_exceptions
def database_management():

    form = UploadForm()
    
    if form.validate_on_submit():
        print('form validated')
        return upload_data(form.file.data)
    else:
        print('form not validated')
        print(form.errors)
    return render_template('admin/upload.html', form=form)

@admin.route('/download_data', methods=['GET'])
@handle_exceptions
def handle_download_data():
    return download_data()

@admin.route('/reset_tables', methods=['GET'])
@handle_exceptions
def handle_reset_tables():
    reset_tables()
    flash('Tablas reseteadas', 'success')
    return redirect(url_for('admin.dashboard'))
