# Vampiro/services/admin_actions.py
from faker import Faker
from flask import current_app
from Vampiro.database.mysql import db
from Vampiro.models.UserModel import User, Role
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

