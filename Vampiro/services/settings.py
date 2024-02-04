# /Vampiro/services/settings.py

from models import Settings

def get_active_settings():
    """
    Returns the active settings object
    """
    return Settings.query.filter_by(active=True).first()

def get_game_status():
    """
    Returns the game status
    """
    active_settings = get_active_settings()
    game_status = active_settings.game_status
    return game_status


def set_game_status(status):
    """
    Changes the game status
    """
    active_settings = get_active_settings()
    active_settings.game_status = status
    db.session.commit()