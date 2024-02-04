# Vampiro/services/admin_actions.py
from Vampiro.database.mysql import db

# CRONICAS _________________________________________________________________

def add_cronica(cronica):
    """
    Adds a new cronica to the database
    """
    db.session.add(cronica)
    db.session.commit()



