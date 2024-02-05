# /Vampiro/services/hunts.py

import datetime
import random
from Vampiro.services.disputes import deactivate_dispute

from Vampiro.services.players import kill
from .game import game_over, get_alive_players, get_round_number

from Vampiro.database.mysql import db
from Vampiro.models import Hunt

# HUNT CONSTRUCTOR _______________________________________________________________

def new_hunt(hunt_pair, round_number):
    """
    Creates a new hunt with the given pair of player ids and a round number
    """
    date = datetime.now().date()
    hunt = Hunt(date=date, round=round_number, room_hunter=hunt_pair[0], room_prey=hunt_pair[1], success=False)
    db.session.add(hunt)
    db.session.commit()


# HUNT GETTERS _______________________________________________________________________

def get_current_hunt(hunter_room):
    """
    Returns the current hunt object of a given hunter id
    """
    current_round = get_round_number()
    current_hunt = Hunt.query.filter_by(round=current_round, room_hunter=hunter_room, success=False).first()
    return current_hunt

def get_current_danger(prey_room):
    """
    Returns the current hunt object of a given prey id
    """
    current_round = get_round_number()
    current_danger = Hunt.query.filter_by(round=current_round, room_prey=prey_room, success=False).first()
    return current_danger

# HUNT SETTERS ________________________________________________________________

def hunt_success(hunt):
    """
    Changes the success property of the given hunt to True
    """
    hunt.success = True
    db.session.commit()




# HUNT FUNCTIONS ______________________________________________________________________

def hunter_wins(dispute):
    """
    Kills the victim, marks the hunt as a success, deactivates the dispute, starts a new hunt.
    """
    
    killer = dispute.hunt.hunter
    victim = dispute.hunt.prey

    new_pair = (killer.room, get_current_hunt(victim).room_prey)
    kill(victim)
    hunt_success(dispute.hunt)
    deactivate_dispute(dispute)

    if get_alive_players().length <= 1:
        game_over()
    else:
        new_hunt(new_pair, get_round_number())

#prey wins no es una funcion ya que supone que el registro de caza se queda como estaba.