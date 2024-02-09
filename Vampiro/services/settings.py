# /Vampiro/services/settings.py

from Vampiro.database.mysql import db
from Vampiro.models.SettingsModel import Settings

# SETTINGS GETTERS _________________________________________________________________________

def get_settings():
    """
    Returns the settings object
    """
    return Settings.query.first()

def get_game_status():
    """
    Returns the game status: NOT_STARTED, REGISTRY_OPEN, IN_PROGRESS, FINISHED
    """
    settings = get_settings()
    game_status = settings.game_status
    return game_status

def get_round_status():
    """
    Returns the round status: PENDING, TO_BE_FINALISED, PROCESSED
    """
    settings = get_settings()
    round_status = settings.round_status
    return round_status

def get_extension_status():
    """
    Returns the extension status: EXTENDED, NOT_EXTENDED
    """
    settings = get_settings()
    extension_status = settings.extension_status
    return extension_status

# SETTINGS SETTERS _________________________________________________________________________

def set_mode(mode):
    """
    Changes the game mode: VAMPIRO, CUPIDO
    """
    settings = get_settings()
    settings.mode = mode
    db.session.commit()

def set_game_status(game_status):
    """
    Changes the game status: NOT_STARTED, REGISTRY_OPEN, IN_PROGRESS, FINISHED
    """
    settings = get_settings()
    settings.game_status = game_status
    db.session.commit()

def set_round_status(round_status):
    """
    Changes the round status: PENDING, TO_BE_FINALISED, PROCESSED
    """
    settings = get_settings()
    settings.round_status = round_status
    db.session.commit()

def set_extension_status(extension_status):
    """
    Changes the extension status: EXTENDED, NOT_EXTENDED
    """
    settings = get_settings()
    settings.extension_status = extension_status
    db.session.commit()