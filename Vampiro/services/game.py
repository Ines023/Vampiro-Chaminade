# Vampiro/services/game.py
import random

from sqlalchemy import func

from Vampiro.models import Hunt, Player, db
from Vampiro.services.disputes import deactivate_dispute, finalise_duel, get_general_death_accusation, get_general_death_accusations, get_general_duels
from Vampiro.services.hunts import hunter_wins, new_hunt
from Vampiro.utils.emails import send_new_round_hunt_email

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
    Kills all players who didn't kill in the last round
    """
    round_number = get_round_number()
    unsuccessful_players = get_unsuccessful_players(round_number)

    for player in unsuccessful_players:
        player.alive = False
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

    acusaciones_pendientes = get_general_death_accusations()
    if acusaciones_pendientes:
        for acusacion in acusaciones_pendientes:
            hunter_wins(acusacion)

    duelos_pendientes = get_general_duels()
    if duelos_pendientes:
        for duelo in duelos_pendientes:
            finalise_duel(duelo)

def round_end():
    
    disputas_pendientes = get_general_disputes()
    if disputas_pendientes:
        for dispute in disputas_pendientes:
            deactivate_dispute(dispute)