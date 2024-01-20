import random

from Vampiro import db

from .game import get_round_number
from .players import get_current_hunt
from .hunts import new_hunt, kill, hunt_success
from .disputes import get_agreed_response



# DUELS ________________________________________________________________

def reached_agreement(dispute):
    if dispute.hunter_duel_response == dispute.prey_duel_response and dispute.hunter_duel_response != None:
        return True
    else:
        return False

def random_duel_winner(dispute):
    winner = random.choice([dispute.hunt.room_hunter, dispute.hunt.room_prey])
    return winner

def duel_winner(dispute):
    if reached_agreement(dispute) == True:
        if get_agreed_response(dispute) == True:
            winner = dispute.hunt.room_hunter
        else:
            winner = dispute.hunt.room_prey
    else:
        winner = random_duel_winner(dispute)
    return winner


def hunter_wins(dispute):
    killer = dispute.hunt.hunter
    victim = dispute.hunt.prey

    new_pair = (killer.room, get_current_hunt(victim).room_prey)
    kill(victim)
    hunt_success(dispute.hunt)

    new_hunt(new_pair, get_round_number())

    #send_email(killer, victim)

def prey_wins(dispute):
    pass
    #send_email(killer, victim)


def deactivate_dispute(dispute):
    dispute.active = False
    db.session.commit()


def finalise_duel(dispute):
    winner = duel_winner(dispute)

    if winner == dispute.hunt.room_hunter:
        hunter_wins(dispute)
    else:
        prey_wins(dispute)

    deactivate_dispute(dispute)