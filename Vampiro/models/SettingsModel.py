# Vampiro/models/SettingsModel.py
from sqlalchemy import Enum
from Vampiro.database.mysql import db

class GameStatus(Enum):
    NOT_STARTED = 'NOT_STARTED'
    REGISTRY_OPEN = 'REGISTRY_OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'

class Settings(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True, nullable=False)

    mode = db.Column(db.String(80), nullable=False)
    game_status = db.Column(Enum(GameStatus), nullable=False)


