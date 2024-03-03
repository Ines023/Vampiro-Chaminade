# Vampiro/models/SettingsModel.py
from enum import Enum
from Vampiro.database.mysql import db

class Mode(Enum):
    VAMPIRO = 'VAMPIRO'
    CUPIDO = 'CUPIDO'

class GameStatus(Enum):
    NOT_STARTED = 'NOT_STARTED'
    REGISTRY_OPEN = 'REGISTRY_OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'

class RoundStatus(Enum):
    PENDING = 'PENDING'
    TO_BE_FINALISED = 'TO_BE_FINALISED'
    PROCESSED = 'PROCESSED'

class ExtensionStatus(Enum):
    EXTENDED = 'EXTENDED'
    NOT_EXTENDED = 'NOT_EXTENDED'

class Settings(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    mode = db.Column(db.Enum(Mode), nullable=False)
    game_status = db.Column(db.Enum(GameStatus), nullable=False)
    round_status = db.Column(db.Enum(RoundStatus), nullable=False)
    extension_status = db.Column(db.Enum(ExtensionStatus), nullable=False)
    timer_switch = db.Column(db.Boolean, nullable=False)
    holidays = db.Column(db.Boolean, nullable=False)

class EmailBatchType(Enum):
    NEW_ROUND = 'NEW_ROUND'
    STARVATION = 'STARVATION'
    GAME_FINISHED = 'GAME_FINISHED'

class EmailBatches(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer, nullable=False)
    batch_type = db.Column(db.Enum(EmailBatchType), nullable=False)
    total_20_batches = db.Column(db.Integer, nullable=False)
    current_20_batch = db.Column(db.Boolean, nullable=False)

