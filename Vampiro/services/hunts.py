import datetime
import random
from .game import get_alive_players

from Vampiro.database.mysql import db
from Vampiro.models import Hunt

# HUNTS _______________________________________________________________________

def generate_pairs():
    alive_players = get_alive_players()
    rooms = [player.room for player in alive_players]
    random.shuffle(rooms)
    pairs = [(rooms[i], rooms[(i+1) % len(rooms)]) for i in range(len(rooms))]
    return pairs

def new_hunt(hunt_pair, round_number):
        date = datetime.now().date()
        hunt = Hunt(date=date, round=round_number, room_hunter=hunt_pair[0], room_prey=hunt_pair[1], success=False)
        db.session.add(hunt)
        db.session.commit()

def kill(player):
    player.alive = False
    db.session.commit()

def hunt_success(hunt):
    hunt.success = True
    db.session.commit()