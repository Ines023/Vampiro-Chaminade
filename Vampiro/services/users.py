# /Vampiro/services/users.py

import datetime

from flask import flash

from Vampiro.database.mysql import db
from Vampiro.models.UserModel import User, Role

# REGISTRATION ________________________________________________________________
def add_user(form):
    """
    Adds a new user to the database and returns it
    """

    new_user = User(id=form.room.data ,email=form.email.data, password=form.password.data, name=form.name.data, active=True)
    
    user_role = Role.query.filter_by(name='visitor').first()
    if user_role:
        new_user.role = user_role

    db.session.add(new_user)
    db.session.flush()  # Flush the session to update the role relationship
    db.session.commit()
    return new_user

def confirm_user(user):
    """
    Confirms a user by setting the confirmed_at field to the current time
    """
    user.confirmed_at = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()


# ROLE MANAGEMENT _______________________________________________________________________

def role_to_dict(role):
    return {
        'id': role.id,
        'name': role.name,
        'description': role.description
    }



def change_role(user, id):
    """
    Changes the role of a user:
        - admin
        - player
        - visitor
    """
    role = Role.query.filter_by(id=id).first()
    if role:
        user.role = role
        
        db.session.add(user)
        db.session.commit()
    else:
        flash('role no encontrado','danger')

# PASSWORD MANAGEMENT _______________________________________________________________________
    
def update_password(user, form):
    """
    Updates the password of a user
    """
    user.password = form.password.data
    
    db.session.add(user)
    db.session.commit()