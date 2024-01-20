import datetime

from Vampiro.database.mysql import db
from Vampiro.models.UserModel import User, Role

# REGISTRATION ________________________________________________________________
def add_user(form):
    new_user = User(email=form.email.data, password=form.password.data, name=form.name.data, active=True)
    
    user_role = Role.query.filter_by(name='visitor').first()
    if user_role:
        new_user.role = user_role

    db.session.add(new_user)
    db.session.commit()
    return new_user

def confirm_user(token):
    user = User.query.filter_by(token=token).first_or_404()
    user.confirmed_at = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()


# ROLE MANAGEMENT _______________________________________________________________________

def change_role(user, role_name):
    role = Role.query.filter_by(name=role_name).first()
    user.role = role
    
    db.session.add(user)
    db.session.commit()

# PASSWORD MANAGEMENT _______________________________________________________________________
    
def update_password(user, form):
    user.password = form.password.data
    
    db.session.add(user)
    db.session.commit()