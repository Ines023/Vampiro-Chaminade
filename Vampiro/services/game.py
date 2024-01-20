from sqlalchemy import func

from Vampiro.models import Hunt, Player, db

# GAME GENERAL GETTERS _____________________________________________________________________

def get_alive_players():
    alive_players = Player.query.filter_by(alive=True).all()
    return alive_players

def get_round_number():
    round = Hunt.query.with_entities(func.max(Hunt.round)).scalar()
    if round is None:
        round_number = 0
    else:
        round_number = round
    return round_number

def get_general_number_round_kills(round_number):
    round_kills = Hunt.query.filter_by(round=round_number, success=True).count()
    return round_kills

def get_unsuccessful_players(round_number):
    unsuccessful_players = db.session.query(Player).filter(
        Player.hunt_where_hunter.any(Hunt.round == round_number),
        ~Player.hunt_where_hunter.any(Hunt.round == round_number, Hunt.success == True)
    ).all()

    return unsuccessful_players


