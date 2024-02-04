# /Vampiro/services/players.py

from Vampiro.models import Hunt, Player
from .game import get_round_number

# PLAYER GETTERS _____________________________________________________________________

def get_player(room_number):
    """
    Returns a player object given a room number
    """
    player = Player.query.filter_by(room=room_number).first()
    return player



def get_number_round_kills(round_number, hunter_room):
    """
    Returns the total number of kills in a round by a given hunter
    """
    round_kills = Hunt.query.filter_by(round=round_number, room_hunter=hunter_room, success=True).count()
    return round_kills

def get_number_total_kills(hunter_room):
    """
    Returns the total number of kills in the whole game by a given hunter
    """
    total_kills = Hunt.query.filter_by(room_hunter=hunter_room, success=True).count()
    return total_kills



# PLAYER SETTERS _____________________________________________________________________

def kill(player):
    """
    Changes the alive property of the given player to False
    """
    player.alive = False
    db.session.commit()

