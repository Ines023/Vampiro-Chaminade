import datetime

from .hunts import get_current_hunt
from Vampiro.database.mysql import db
from Vampiro.models import Dispute, Hunt

# DISPUTE CONSTRUCTOR __________________________________________________________

def new_death_accusation(room_hunter):
    hunt = get_current_hunt(room_hunter)

    id = hunt.id
    date = datetime.now().date()

    dispute = Dispute(id=id, date=date, prey_response=None, hunter_duel_response=None, prey_duel_response=None, active=True)
    db.session.add(dispute)
    db.session.commit()

# DISPUTE GETTERS ____________________________________________________________________

#-------- DISPUTE INSTANCE GETTERS -----------------------------------------------------
#   GENERAL disputes depending on STAGE

def get_general_death_accusation():
    death_accusations = Dispute.query.filter_by(active=True, prey_response=None).all()
    return death_accusations

def get_general_duels():
    duels = Dispute.query.filter_by(active=True, prey_response=False).all()
    return duels

#   PLAYER SPECIFIC disputes where a player has hunter/prey role

def get_current_dispute_by_hunter(room_hunter):
    dispute = Dispute.query.join(Hunt).filter(Hunt.room_hunter == room_hunter, Dispute.active == True).first()
    return dispute

def get_current_dispute_by_prey(room_prey):
    dispute = Dispute.query.join(Hunt).filter(Hunt.room_prey == room_prey, Dispute.active == True).first()
    return dispute


#   Disputes depending on the STAGE they are in and the player's role

def get_death_accusation(room_prey):
    dispute = get_current_dispute_by_prey(room_prey)

    if dispute == None or active_duel(dispute) == True:
        return None
    else:
        return dispute

def get_duel_where_hunter(room_hunter):
    dispute = get_current_dispute_by_hunter(room_hunter)

    if dispute != None and active_duel(dispute) == True:
        return dispute
    else:
        return None

def get_duel_where_prey(room_prey):
    dispute = get_current_dispute_by_prey(room_prey)

    if dispute != None and active_duel(dispute) == True:
        return dispute
    else:
        return None

#-------- DISPUTE PROPERTY GETTERS --------------------------------------------------

def active_duel(dispute):
    if dispute.prey_response == None:
        return False
    else:
        return True

def get_agreed_response(dispute):
    return dispute.hunter_duel_response

# DISPUTE SETTERS ____________________________________________________________________

def set_prey_initial_response(room_prey, response):
    dispute = get_current_dispute_by_prey(room_prey)
    dispute.prey_response = response
    db.session.commit()

def set_hunter_duel_response(dispute, response):
    dispute.hunter_duel_response = response
    db.session.commit()

def set_prey_duel_response(dispute, response):
    dispute.prey_duel_response = response
    db.session.commit()