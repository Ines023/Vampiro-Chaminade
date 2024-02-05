# Vampiro/models/UserModel.py
from datetime import datetime
from Vampiro.database.mysql import db
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from enum import Enum

# APP USERS DATA _____________________________________________________________

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hashed = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime())

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')

    player = db.relationship('Player', backref='user', uselist=False)
  
    @property
    def room(self):
        return self.id

    @room.setter
    def room(self, value):
        self.id = value

    @property
    def confirmed(self):
        return self.confirmed_at is not None

    @property
    def password(self):
        return self.password_hashed
    
    @password.setter
    def password(self, plaintext):
        self.password_hashed = generate_password_hash(plaintext)

    def get_confirmation_token(self, expires_sec=1800):
            s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
            return s.dumps({'confirm_email': self.id}).decode('utf-8')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'reset_password': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_confirmation_token(token):
        """
        Returns the user if the token is valid, None otherwise
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['confirm_email']
        except:
            return None
        return User.query.get(user_id)

    @staticmethod
    def verify_reset_token(token):
        """
        Returns the user if the token is valid, None otherwise
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['reset_password']
        except:
            return None
        return User.query.get(user_id)

class Role(db.Model):
    """ Posibles roles:
        - admin
        - player
        - visitor
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))

# GAME DATA _________________________________________________________________

class Player(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    alive = db.Column(db.Boolean, nullable=False)
    
    hunt_where_hunter = db.relationship('Hunt', backref='hunter', foreign_keys='Hunt.room_hunter')
    hunt_where_prey = db.relationship('Hunt', backref='prey', foreign_keys='Hunt.room_prey')

    user = db.relationship('User', backref='player', uselist=False)

    @property
    def room(self):
        return self.id

    @room.setter
    def room(self, value):
        self.id = value

class Hunt(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    round = db.Column(db.Integer, nullable=False)
    room_hunter = db.Column(db.Integer, db.ForeignKey('player.id'))
    room_prey = db.Column(db.Integer, db.ForeignKey('player.id'))
    success = db.Column(db.Boolean, nullable=False)
    
    disputes = db.relationship('Dispute', backref='hunt')

class Revision_Group(Enum):
    DAY = 'DAY'
    NIGHT = 'NIGHT'


class Dispute(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hunt_id = db.Column(db.Integer, db.ForeignKey('hunt.id'))
    date = db.Column(db.Date, nullable=False)
    prey_response = db.Column(db.Boolean)
    hunter_duel_response = db.Column(db.Boolean)
    prey_duel_response = db.Column(db.Boolean)
    active = db.Column(db.Boolean, nullable=False)
    revision_group = db.Column(db.Enum(Revision_Group), nullable=False)

    def set_revision_group(self):
        current_hour = datetime.now().hour
        if 9 <= current_hour < 21:
            self.revision_group = "DAY"
        else:
            self.revision_group = "NIGHT"

    @property
    def death_accusation(self):
        """
        Returns True if the dispute is an unresolved death accusation, False otherwise
        """
        if self.prey_response == None:
            duel = True
        else:
            duel = False
        return duel

    @property
    def duel(self):
        """
        Returns True if the dispute has become a duel, False otherwise
        """
        if self.prey_response == None or self.prey_response == True:
            duel = False
        else:
            duel = True
        return duel

    @property
    def agreed_response(self):
        """
        Returns the agreed response if both players have agreed on it, None otherwise
        """
        if self.prey_response == True:
            response = True
        elif self.prey_duel_response == self.hunter_duel_response and self.prey_duel_response != None:
            response = self.prey_duel_response
        else:
            response = None
        return response

