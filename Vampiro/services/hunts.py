# /Vampiro/services/hunts.py

import datetime
import random
from .game import get_alive_players

from Vampiro.database.mysql import db
from Vampiro.models import Hunt

# HUNTS _______________________________________________________________________

def generate_pairs():
    """
    Returns a randomly shuffled list of hunter-prey pairs (tuples) of the alive players ids
    """
    alive_players = get_alive_players()
    rooms = [player.room for player in alive_players]
    random.shuffle(rooms)
    pairs = [(rooms[i], rooms[(i+1) % len(rooms)]) for i in range(len(rooms))]
    return pairs

def new_hunt(hunt_pair, round_number):
    """
    Creates a new hunt with the given pair of player ids and a round number
    """
    date = datetime.now().date()
    hunt = Hunt(date=date, round=round_number, room_hunter=hunt_pair[0], room_prey=hunt_pair[1], success=False)
    db.session.add(hunt)
    db.session.commit()

def kill(player):
    """
    Changes the alive property of the given player to False
    """
    player.alive = False
    db.session.commit()

def hunt_success(hunt):
    """
    Changes the success property of the given hunt to True
    """
    hunt.success = True
    db.session.commit()



def hunter_wins(dispute):
    """
    Kills the victim, marks the hunt as a success, starts a new hunt.
    """
    
    killer = dispute.hunt.hunter
    victim = dispute.hunt.prey

    new_pair = (killer.room, get_current_hunt(victim).room_prey)
    kill(victim)
    hunt_success(dispute.hunt)

    new_hunt(new_pair, get_round_number())