# Vampiro/services/game.py
from sqlalchemy import func

from Vampiro.models import Hunt, Player, db

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


# GAME SETTERS ___________________________________________________________________________

def deaths_from_starvation():
    """
    Kills all players who didn't kill in the last round
    """
    round_number = get_round_number()
    unsuccessful_players = get_unsuccessful_players(round_number)

    for player in unsuccessful_players:
        player.alive = False
    db.session.commit()

def new_round():
    """
    Starts a new round
    """
    new_round_number = get_round_number() + 1
    



    return new_round