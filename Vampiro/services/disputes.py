# Vampiro/services/disputes.py
import datetime

from .hunts import get_current_hunt
from Vampiro.database.mysql import db
from Vampiro.models import Dispute, Hunt
from Vampiro.utils.emails import send_death_accusation_email

# DISPUTE CONSTRUCTOR __________________________________________________________

def new_death_accusation(room_hunter):
    """
    Creates a new dispute for the hunter's current hunt.
    This dispute would classify as a death accusation.
    Sends an email to the prey.
    """
    # Database
    hunt = get_current_hunt(room_hunter)

    hunt_id = hunt.id
    date = datetime.now().date()

    dispute = Dispute(hunt_id=hunt_id, date=date, prey_response=None, hunter_duel_response=None, prey_duel_response=None, active=True)
    db.session.add(dispute)
    db.session.commit()

    #Email
    send_death_accusation_email(hunt.prey.user)

# DISPUTE GETTERS ____________________________________________________________________

#-------- DISPUTE INSTANCE GETTERS -----------------------------------------------------
#   GENERAL disputes depending on STAGE

def get_general_death_accusation():
    """
    Returns all the active death accusations
    """
    death_accusations = Dispute.query.filter_by(active=True, death_accusation=True).all()
    return death_accusations

def get_general_duels():
    """
    Returns all the active duels
    """
    duels = Dispute.query.filter_by(active=True, duel=True).all()
    return duels

#   PLAYER SPECIFIC disputes where a player has hunter/prey role

def get_current_dispute_by_hunter(room_hunter):
    """
    Returns the active dispute where the player is the hunter
    """
    dispute = Dispute.query.join(Hunt).filter(Hunt.room_hunter == room_hunter, Dispute.active == True).first()
    return dispute

def get_current_dispute_by_prey(room_prey):
    """
    Returns the active dispute where the player is the prey
    """
    dispute = Dispute.query.join(Hunt).filter(Hunt.room_prey == room_prey, Dispute.active == True).first()
    return dispute


#   Disputes depending on the STAGE they are in and the player's role

def get_death_accusation(room_prey):
    """
    Returns the active death accusation where the player is the prey
    """
    dispute = get_current_dispute_by_prey(room_prey)

    if dispute.death_accusation == True:
        return dispute
    else:
        return None

def get_duel_where_hunter(room_hunter):
    """
    Returns the active duel where the player is the hunter
    """
    dispute = get_current_dispute_by_hunter(room_hunter)

    if dispute.duel == True:
        return dispute
    else:
        return None

def get_duel_where_prey(room_prey):
    """
    Returns the active duel where the player is the prey
    """
    dispute = get_current_dispute_by_prey(room_prey)

    if dispute.duel == True:
        return dispute
    else:
        return None


# DISPUTE SETTERS ____________________________________________________________________

def set_prey_initial_response(room_prey, response):
    """
    Sets the initial response of the prey to the death accusation
    """
    dispute = get_current_dispute_by_prey(room_prey)
    dispute.prey_response = response
    db.session.commit()

def set_hunter_duel_response(dispute, response):
    """
    Sets the response of the hunter to the duel
    """
    dispute.hunter_duel_response = response
    db.session.commit()

def set_prey_duel_response(dispute, response):
    """
    Sets the response of the prey to the duel
    """
    dispute.prey_duel_response = response
    db.session.commit()