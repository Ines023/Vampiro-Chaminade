from models import Settings

def get_active_settings():
    return Settings.query.filter_by(active=True).first()

def get_game_status():
    active_settings = get_active_settings()
    game_status = active_settings.game_status
    return game_status