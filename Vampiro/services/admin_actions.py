# Vampiro/services/admin_actions.py
from faker import Faker
from flask import current_app
from Vampiro.database.mysql import db
from Vampiro.models.UserModel import User, Role
from Vampiro.services.settings import set_holidays, set_timer_switch_value
from Vampiro.utils.emails import send_game_starting_soon_email

# CRONICAS _________________________________________________________________

def add_cronica(cronica):
    """
    Adds a new cronica to the database
    """
    db.session.add(cronica)
    db.session.commit()

# USERS _______________________________________________________________________
    
def avisar_a_usuarios():
    """
    Avisa a todos los usuarios de la nueva partida
    """
    users = User.query.all()
    for user in users:
        send_game_starting_soon_email(user)
    return True

# AUTOMATIONS _______________________________

def activate_automation():
    set_timer_switch_value(True) 

def deactivate_automation():
    set_timer_switch_value(False) 

# VACACIONES _______________________________________________________________    

def activate_holidays():
    set_holidays(True)

def deactivate_holidays():
    set_holidays(False)
