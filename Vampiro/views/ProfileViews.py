import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from Vampiro.models.SettingsModel import GameStatus

from Vampiro.utils.forms import DeathAccusationForm, DuelResponseForm, RoleSelectorForm, OrganizerForm

from Vampiro.services.users import change_role
from Vampiro.services.settings import get_game_status
from Vampiro.services.game import get_round_number, get_alive_players, get_general_number_round_kills
from Vampiro.services.players import get_current_hunt, get_current_danger, get_number_round_kills, get_number_total_kills
from Vampiro.services.disputes import get_death_accusation, get_duel_where_hunter, get_duel_where_prey, new_death_accusation, set_hunter_duel_response, set_prey_duel_response, get_current_dispute_by_hunter, get_current_dispute_by_prey
from Vampiro.services.duels import  reached_agreement, finalise_duel


profile = Blueprint('admin', __name__)

@profile.before_request
@login_required
def check_game_status_and_role():
    game_status = get_game_status()
    if current_user.role.name == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif current_user.role.name == 'visitor' or game_status != GameStatus.IN_PROGRESS:
        if request.endpoint != 'profile.role_selector':
            return redirect(url_for('profile.role_selector'))
    elif current_user.role.name == 'player' and game_status == GameStatus.IN_PROGRESS:
        if request.endpoint == 'profile.role_selector':
            return redirect(url_for('profile.my_stats'))

@profile.context_processor
def inject_game_status_and_user_role():
    game_status = get_game_status()
    user_role = current_user.role.name
    return dict(game_status=game_status, user_role=user_role)

@profile.route('/')
@profile.route('/role_selector')
def role_selector():
    form = RoleSelectorForm()
    organizer_form = OrganizerForm()

    if form.validate_on_submit():
        role = form.role.data
        change_role(current_user, role)

        return redirect(url_for('profile/role_selector.html'))

    if organizer_form.validate_on_submit():
        if organizer_form.password.data == os.getenv('ADMIN_CODE'):
            role = 'organizer'
            change_role(current_user, role)

            return redirect(url_for('admin/dashboard.html'))
        
    return render_template('profile/role_selector.html')

@profile.route('/my_stats')
def my_stats():

    # Form setup
    death_accusation_form = DeathAccusationForm()
    duel_response_form_hunter = DuelResponseForm()
    duel_response_form_prey = DuelResponseForm()

    # Passing data to template
    player = current_user.player
    hunter = get_current_danger(player.id).hunter.user
    prey = get_current_hunt(player.id).prey.user
    ronda = get_round_number()
    kills = {
        'round': get_number_round_kills(ronda, player.id),
        'total': get_number_total_kills(player.id)
    }
    disputes = {
        'death_accusation': get_death_accusation(player.id),
        'duel_where_hunter': get_duel_where_hunter(player.id),
        'duel_where_prey': get_duel_where_prey(player.id)
    }

    return render_template('profile/my_stats.html',death_accusation_form=death_accusation_form, duel_response_form_hunter=duel_response_form_hunter, duel_response_form_prey=duel_response_form_prey, player=player, hunter=hunter, prey=prey, kills=kills, disputes=disputes)

@profile.route('/my_stats/death_accusation', methods=['POST'])
def death_accusation():
    form = DeathAccusationForm()
    player = current_user.player

    if form.validate_on_submit():
        new_death_accusation(player.id)
    return redirect(url_for('profile.my_stats'))


@profile.route('/my_stats/duel_response', methods=['POST'])
def duel_response():
    form = DuelResponseForm()

    if form.validate_on_submit():
        type = form.type.data
        response = form.response.data
        player = current_user.player

        if type == 'hunter':
            dispute = get_current_dispute_by_hunter(player.id)
            set_hunter_duel_response(dispute, response)
        elif type == 'prey':
            dispute = get_current_dispute_by_prey(player.id)
            set_prey_duel_response(dispute, response)

        if reached_agreement(dispute):
            finalise_duel(dispute)

    return redirect(url_for('profile.my_stats'))


@profile.route('/game_stats')
def game_stats():

    jugadores_vivos = len(get_alive_players())
    ronda_actual = get_round_number()
    muertos_ronda =  get_general_number_round_kills(ronda_actual)

    return render_template('profile/game_stats.html', jugadores_vivos=jugadores_vivos, ronda_actual=ronda_actual, muertos_ronda=muertos_ronda)