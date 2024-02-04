# Vampiro/models/SettingsModel.py
from sqlalchemy import Enum
from Vampiro.database.mysql import db

class GameStatus(Enum):
    NOT_STARTED = 'NOT_STARTED'
    REGISTRY_OPEN = 'REGISTRY_OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'

class RoundStatus(Enum):
    PENDING = 'PENDING'
    TO_BE_FINALISED = 'TO_BE_FINALISED'
    PROCESSED = 'PROCESSED'

class Mode(Enum):
    VAMPIRO = 'VAMPIRO'
    CUPIDO = 'CUPIDO'

class Settings(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    mode = db.Column(db.String(80), nullable=False)
    game_status = db.Column(Enum(GameStatus), nullable=False)
    round_status = db.Column(Enum(RoundStatus), nullable=False)


