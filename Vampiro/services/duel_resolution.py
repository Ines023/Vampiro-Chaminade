# Vampiro/services/duel_resolution.py
import random

from Vampiro import db

from .game import get_round_number
from .players import get_current_hunt
from .hunts import new_hunt, kill, hunt_success

from Vampiro.utils.emails import send_duel_hunter_win_email, send_duel_prey_loss_email, send_duel_hunter_loss_email, send_duel_prey_win_email


# DUELS ________________________________________________________________

def reached_agreement(dispute):
    """
    Returns True if both players have agreed on a response, False otherwise
    """
    if dispute.agreed_response == None:
        reached = False
    else:
        reached = True
    return reached

def random_duel_winner(dispute):
    """
    Returns a random winner (player object) for the duel
    """
    winner = random.choice([dispute.hunt.hunter, dispute.hunt.prey])
    return winner

def duel_winner(dispute):
    """
    Returns the winner (player object) of the duel
    """
    if reached_agreement(dispute) == True:
        if dispute.agreed_response == True:
            winner = dispute.hunt.hunter
        else:
            winner = dispute.hunt.prey
    else:
        winner = random_duel_winner(dispute)
    return winner





#prey wins no es una funcion ya que supone que el registro de caza se queda como estaba.


def deactivate_dispute(dispute):
    """
    Sets the active status of the dispute to False
    """
    dispute.active = False
    db.session.commit()


def finalise_duel(dispute):
    """
    Determines the duel winner, modifies the hunt registry as proceeded, sends emails and desactivates the dispute
    """
    winner = duel_winner(dispute)

    killer = dispute.hunt.hunter
    victim = dispute.hunt.prey


    if winner == killer:
        hunter_wins(dispute)
        
        send_duel_hunter_win_email(killer)
        send_duel_prey_loss_email(victim)
    else:
        # prey wins

        send_duel_hunter_loss_email(killer)
        send_duel_prey_win_email(victim)

    deactivate_dispute(dispute)