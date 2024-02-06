# /Vampiro/views/ProfileViews.py

import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from Vampiro.models.SettingsModel import GameStatus
from Vampiro.utils.emails import send_duel_started_email, send_hunt_success_email, send_victim_death_email

from Vampiro.utils.forms import DeathAccusationForm, DeathConfirmationForm, DuelResponseForm, RoleSelectorForm, OrganizerForm

from Vampiro.services.users import change_role
from Vampiro.services.settings import get_game_status, get_round_status
from Vampiro.services.game import get_round_number, get_alive_players, get_general_number_round_kills, get_current_danger, get_current_hunt, get_number_round_kills, get_number_total_kills, new_death_accusation, get_death_accusation, get_duel_where_hunter, get_duel_where_prey, set_prey_initial_response, reached_agreement, finalise_duel, set_hunter_duel_response, set_prey_duel_response, hunter_wins, get_current_dispute_by_prey, get_current_dispute_by_hunter
from Vampiro.utils.security import handle_exceptions

profile = Blueprint('profile', __name__)

@profile.before_request
@login_required
def check_game_status_and_role():
    """
    Redirects the user to the appropriate page based on the game status and the user's role.    
    """
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
    round_status = get_round_status()
    user_role = current_user.role.name
    return dict(game_status=game_status, user_role=user_role, round_status=round_status)


# PROFILE ______________________________________________________________________________________

@profile.route('/')
@profile.route('/role_selector')
@handle_exceptions
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
@handle_exceptions
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
        'death_accusation_where_prey': get_death_accusation(player.id),
        'death_accusation_where_hunter': get_death_accusation(prey.id),
        'duel_where_hunter': get_duel_where_hunter(player.id),
        'duel_where_prey': get_duel_where_prey(player.id)
    }

    return render_template('profile/my_stats.html',death_accusation_form=death_accusation_form, duel_response_form_hunter=duel_response_form_hunter, duel_response_form_prey=duel_response_form_prey, player=player, hunter=hunter, prey=prey, kills=kills, disputes=disputes)

@profile.route('/my_stats/death_accusation', methods=['POST'])
@handle_exceptions
def death_accusation():
    """
    Handles the form submission for the death accusation form.
    If the hunter informs of a murder, the victim will be asked over email to report.
    """

    form = DeathAccusationForm()
    player = current_user.player

    if form.validate_on_submit():
        new_death_accusation(player.id)
    return redirect(url_for('profile.my_stats'))

@profile.route('/my_stats/death_confirmation', methods=['POST'])
@handle_exceptions
def death_confirmation():
    """
    Handles the form submission for the death confirmation form.
    If the prey confirms the death, the hunter wins the dispute, gets a new hunt and emails are sent.
    If the prey denies the death, the hunter is informed and the dispute becomes a duel, its revision group is updated.
    """


    form = DeathConfirmationForm
    player = current_user.player

    if form.validate_on_submit():

        set_prey_initial_response(player.id, form.response.data)
        dispute = get_current_dispute_by_prey(player.id)

        if form.response.data == True:
            hunter_wins(dispute)
            send_hunt_success_email(dispute.hunter.user)
            send_victim_death_email(player)
        else:
            dispute.set_revision_group()
            send_duel_started_email(dispute.hunter.user)
    
@profile.route('/my_stats/duel_response', methods=['POST'])
@handle_exceptions
def duel_response():
    """
    Handles the form submission for the duel response form.
    If both players agree on the duel, the dispute is finalised.
    If not in time, it will be handled by the automatic revision every 12 hours."""

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
@handle_exceptions
def game_stats():

    jugadores_vivos = len(get_alive_players())
    ronda_actual = get_round_number()
    muertos_ronda =  get_general_number_round_kills(ronda_actual)

    return render_template('profile/game_stats.html', jugadores_vivos=jugadores_vivos, ronda_actual=ronda_actual, muertos_ronda=muertos_ronda)