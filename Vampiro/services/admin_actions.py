# Vampiro/services/admin_actions.py
from faker import Faker
from flask import current_app
from Vampiro.database.mysql import db
from Vampiro.models.UserModel import User, Role

# CRONICAS _________________________________________________________________

def add_cronica(cronica):
    """
    Adds a new cronica to the database
    """
    db.session.add(cronica)
    db.session.commit()



