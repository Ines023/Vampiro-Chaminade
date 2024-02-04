# Vampiro/services/game.py
import random

from sqlalchemy import func

from Vampiro.models import Hunt, Player, db
from Vampiro.services.disputes import deactivate_dispute, finalise_duel, get_general_death_accusation, get_general_death_accusations, get_general_disputes, get_general_duels
from Vampiro.services.hunts import hunter_wins, new_hunt
from Vampiro.services.settings import get_round_status, set_round_status
from Vampiro.utils.emails import send_new_round_hunt_email, send_starvation_email

# GAME GENERAL GETTERS _____________________________________________________________________

def get_alive_players():
    """
    Returns a list of all alive players (player objects)
    """

    alive_players = Player.query.filter_by(alive=True).all()
    return alive_players

def get_round_number():
    """
    Returns the current round number. If the game hasn't started yet, returns 0.
    """
    round = Hunt.query.with_entities(func.max(Hunt.round)).scalar()
    if round is None:
        round_number = 0
    else:
        round_number = round
    return round_number

def get_general_number_round_kills(round_number):
    """
    Returns the collective number of kills in a given round
    """
    round_kills = Hunt.query.filter_by(round=round_number, success=True).count()
    return round_kills

def get_unsuccessful_players(round_number):
    """
    Returns a list of all players who didn't kill in a given round
    """
    unsuccessful_players = db.session.query(Player).filter(
        Player.hunt_where_hunter.any(Hunt.round == round_number),
        ~Player.hunt_where_hunter.any(Hunt.round == round_number, Hunt.success == True)
    ).all()

    return unsuccessful_players


# GAME FUNCTIONS _________________________________________________________________________

def deaths_from_starvation():
    """
    Kills all players who didn't kill in the last round, and sends them an email
    """
    round_number = get_round_number()
    unsuccessful_players = get_unsuccessful_players(round_number)

    for player in unsuccessful_players:
        player.alive = False
        send_starvation_email(player)
    db.session.commit()

def generate_pairs():
    """
    Returns a randomly shuffled list of hunter-prey pairs (tuples) of the alive players ids
    """
    alive_players = get_alive_players()
    rooms = [player.room for player in alive_players]
    random.shuffle(rooms)
    pairs = [(rooms[i], rooms[(i+1) % len(rooms)]) for i in range(len(rooms))]
    return pairs

def new_round():
    """
    Generates new pairs, updates the hunt table with the new round number and pairs
    """
    new_round_number = get_round_number() + 1
    
    round_pairs = generate_pairs()

    for pair in round_pairs:
        new_hunt(pair, new_round_number)
        send_new_round_hunt_email(pair[0])


def process_round():
    """
    Processes the round only if the round status is TO_BE_FINALISED. If so, all hunters win death accusations, all duels are finalised and sets the round status to PROCESSED.
    """


    round_status = get_round_status()
    if round_status == 'TO_BE_FINALISED':

        acusaciones_pendientes = get_general_death_accusations()
        if acusaciones_pendientes:
            for acusacion in acusaciones_pendientes:
                hunter_wins(acusacion)

        duelos_pendientes = get_general_duels()
        if duelos_pendientes:
            for duelo in duelos_pendientes:
                finalise_duel(duelo)

        deaths_from_starvation()

        set_round_status('PROCESSED')
    else:
        pass

def round_end():
    """
    Executes at the end of the round. Checks if a dispute revision period is needed. If not, processes the round.
    """


    disputas_pendientes = get_general_disputes()
    if disputas_pendientes:
        set_round_status('PENDING')
    else:
        set_round_status('TO_BE_FINALISED')
    
    process_round()

def revision_period_done():
    """
    Executes at the end of the dispute revision period. If the revision period had been activated, it sets the round status to TO_BE_FINALISED and processes the round. If not, it doesn't do anything.
    """
    round_status = get_round_status()
    if round_status == 'PENDING':
        set_round_status('TO_BE_FINALISED')
    
    process_round()