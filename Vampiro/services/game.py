# Vampiro/services/game.py
import random
from datetime import datetime

from sqlalchemy import func

from Vampiro.database.mysql import db
from Vampiro.models.UserModel import Hunt, Player, Dispute
from Vampiro.services.settings import get_extension_status, get_round_status, set_extension_status, set_round_status
from Vampiro.utils.emails import send_deadline_extension_email, send_game_finished_email, send_new_round_hunt_email, send_starvation_email, send_death_accusation_email, send_duel_hunter_win_email, send_duel_hunter_loss_email, send_duel_prey_win_email, send_duel_prey_loss_email


# INDEX

# PLAYER FUNCTIONS
#       - player constructor
#       - player getters
#       - player setters

# GAME FUNCTIONS
#       - game general getters
#       - temporalisation

# HUNT FUNCTIONS
#       - hunt constructor
#       - hunt getters
#       - hunt setters
#       - hunt resolution functions

# DISPUTE FUNCTIONS
#       - dispute constructor
#       - dispute getters
#       - dispute setters
#       - duel functions

# GAME END




# PLAYER FUNCTIONS _________________________________________________________________________

# PLAYER CONSTRUCTOR - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def new_player(user_id):
    """
    Creates a new player with the given room number
    """
    player = Player(id=user_id, alive=True)
    db.session.add(player)
    db.session.commit()

# PLAYER GETTERS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_player(room_number):
    """
    Returns a player object given a room number
    """
    player = Player.query.filter_by(id=room_number).first()
    return player

def get_number_round_kills(round_number, hunter_room):
    """
    Returns the total number of kills in a round by a given hunter
    """
    round_kills = Hunt.query.filter_by(round=round_number, room_hunter=hunter_room, success=True).count()
    return round_kills

def get_number_total_kills(hunter_room):
    """
    Returns the total number of kills in the whole game by a given hunter
    """
    total_kills = Hunt.query.filter_by(room_hunter=hunter_room, success=True).count()
    return total_kills

# PLAYER SETTERS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def kill(player):
    """
    Changes the alive property of the given player to False
    """
    player.alive = False
    db.session.commit()


# HUNT FUNCTIONS ______________________________________________________________________

# HUNT CONSTRUCTOR  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def new_hunt(hunt_pair, round_number):
    """
    Creates a new hunt with the given pair of player ids and a round number
    """
    date = datetime.now().date()
    hunt = Hunt(date=date, round=round_number, room_hunter=hunt_pair[0], room_prey=hunt_pair[1], success=False)
    db.session.add(hunt)
    db.session.commit()


# HUNT GETTERS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_current_hunt(hunter_room):
    """
    Returns the current hunt object of a given hunter id
    """
    current_round = get_round_number()
    current_hunt = Hunt.query.filter_by(round=current_round, room_hunter=hunter_room, success=False).first()
    return current_hunt

def get_current_danger(prey_room):
    """
    Returns the current hunt object of a given prey id
    """
    current_round = get_round_number()
    current_danger = Hunt.query.filter_by(round=current_round, room_prey=prey_room, success=False).first()
    return current_danger

# HUNT SETTERS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def hunt_success(hunt):
    """
    Changes the success property of the given hunt to True
    """
    hunt.success = True
    db.session.commit()

# HUNT RESOLUTION FUNCTIONS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def hunter_wins(dispute):
    """
    Kills the victim, marks the hunt as a success, deactivates the dispute, starts a new hunt.
    """
    
    killer = dispute.hunt.hunter
    victim = dispute.hunt.prey

    new_pair = (killer.room, get_current_hunt(victim).room_prey)
    kill(victim)
    hunt_success(dispute.hunt)
    deactivate_dispute(dispute)

    if get_alive_players().length <= 1:
        game_over()
    else:
        new_hunt(new_pair, get_round_number())

#prey wins no es una funcion ya que supone que el registro de caza se queda como estaba.


# DISPUTE CONSTRUCTOR - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def new_death_accusation(room_hunter):
    """
    Creates a new dispute for the hunter's current hunt.
    This dispute would classify as a death accusation.
    It sets the revision group depending on the current hour.
    Sends an email to the prey.
    """
    # Database
    hunt = get_current_hunt(room_hunter)

    hunt_id = hunt.id
    date = datetime.now().date()

    dispute = Dispute(hunt_id=hunt_id, date=date, prey_response=None, hunter_duel_response=None, prey_duel_response=None, active=True)
    dispute.set_revision_group()
    db.session.add(dispute)
    db.session.commit()


    #Email
    send_death_accusation_email(hunt.prey,dispute.revision_group)

# DISPUTE GETTERS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#-------- DISPUTE INSTANCE GETTERS -----------------------------------------------------
#   GENERAL disputes depending on STAGE

def get_general_disputes(revision_group=None):
    """
    Returns all the active disputes
    """
    if revision_group:
        disputes = Dispute.query.filter_by(active=True, revision_group=revision_group).all()
    else:
        disputes = Dispute.query.filter_by(active=True).all()
    return disputes

def get_general_death_accusations(revision_group=None):
    """
    Returns all the active death accusations
    """
    if revision_group:
        death_accusations = Dispute.query.filter_by(active=True, death_accusation=True, revision_group=revision_group).all()
    else:
        death_accusations = Dispute.query.filter_by(active=True, death_accusation=True).all()
    return death_accusations

def get_general_duels(revision_group=None):
    """
    Returns all the active duels
    """
    if revision_group:
        duels = Dispute.query.filter_by(active=True, duel=True, revision_group=revision_group).all()
    else:
        duels = Dispute.query.filter_by(active=True, duel=True).all()
    return duels

#   PLAYER SPECIFIC disputes where a player has hunter/prey role

def get_current_dispute_by_hunter(room_hunter):
    """
    Returns the active dispute where the player is the hunter
    """
    dispute = Dispute.query.join(Hunt).filter(Hunt.room_hunter == room_hunter, Dispute.active == True).first()
    return dispute

def get_current_dispute_by_prey(room_prey):
    """
    Returns the active dispute where the player is the prey
    """
    dispute = Dispute.query.join(Hunt).filter(Hunt.room_prey == room_prey, Dispute.active == True).first()
    return dispute

def get_dispute_by_id(dispute_id):
    """
    Returns the dispute object with the given id
    """
    dispute = Dispute.query.filter_by(id=dispute_id).first()
    return dispute

#   Disputes depending on the STAGE they are in and the player's role

def get_death_accusation(room_prey):
    """
    Returns the active death accusation where the player is the prey
    """
    dispute = get_current_dispute_by_prey(room_prey)

    if dispute.death_accusation == True:
        return dispute
    else:
        return None

def get_duel_where_hunter(room_hunter):
    """
    Returns the active duel where the player is the hunter
    """
    dispute = get_current_dispute_by_hunter(room_hunter)

    if dispute.duel == True:
        return dispute
    else:
        return None

def get_duel_where_prey(room_prey):
    """
    Returns the active duel where the player is the prey
    """
    dispute = get_current_dispute_by_prey(room_prey)

    if dispute.duel == True:
        return dispute
    else:
        return None


# DISPUTE SETTERS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def set_prey_initial_response(room_prey, response):
    """
    Sets the initial response of the prey to the death accusation
    """
    dispute = get_current_dispute_by_prey(room_prey)
    dispute.prey_response = response
    db.session.commit()

def set_hunter_duel_response(dispute, response):
    """
    Sets the response of the hunter to the duel
    """
    dispute.hunter_duel_response = response
    db.session.commit()

def set_prey_duel_response(dispute, response):
    """
    Sets the response of the prey to the duel
    """
    dispute.prey_duel_response = response
    db.session.commit()

def deactivate_dispute(dispute):
    """
    Sets the active status of the dispute to False
    """
    dispute.active = False
    db.session.commit()




# DUEL FUNCTIONS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def reached_agreement(dispute):
    """
    Returns True if both players have agreed on a response, False otherwise
    """
    if dispute.agreed_response == None:
        reached = False
    else:
        reached = True
    return reached

def random_duel_winner(dispute):
    """
    Returns a random winner (player object) for the duel
    """
    winner = random.choice([dispute.hunt.hunter, dispute.hunt.prey])
    return winner

def duel_winner(dispute):
    """
    Returns the winner (player object) of the duel
    """
    if reached_agreement(dispute) == True:
        if dispute.agreed_response == True:
            winner = dispute.hunt.hunter
        else:
            winner = dispute.hunt.prey
    else:
        winner = random_duel_winner(dispute)
    return winner



def finalise_duel(dispute):
    
    """
    Determines the duel winner, modifies the hunt registry as proceeded, sends emails and desactivates the dispute
    """
    winner = duel_winner(dispute)

    killer = dispute.hunt.hunter
    victim = dispute.hunt.prey


    if winner == killer:
        hunter_wins(dispute)
        
        send_duel_hunter_win_email(killer)
        send_duel_prey_loss_email(victim)
    else:
        # prey wins

        send_duel_hunter_loss_email(killer)
        send_duel_prey_win_email(victim)

    deactivate_dispute(dispute)


def admin_intervention(dispute, winner):
    """
    Determines the winner of the duel, modifies the hunt registry as proceeded, sends emails and desactivates the dispute
    """

    killer = dispute.hunt.hunter
    victim = dispute.hunt.prey

    if winner == 'Hunter':
        hunter_wins(dispute)
                
        send_duel_hunter_win_email(killer)
        send_duel_prey_loss_email(victim)
    elif winner == 'Prey':
        # prey wins
        send_duel_hunter_loss_email(dispute.hunt.hunter)
        send_duel_prey_win_email(dispute.hunt.prey)

    deactivate_dispute(dispute)




# GAME FUNCTIONS _____________________________________________________________________
    
# GAME GENERAL GETTERS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_alive_players():
    """
    Returns a list of all alive players (player objects)
    """

    alive_players = Player.query.filter_by(alive=True).all()
    return alive_players

def get_round_number():
    """
    Returns the current round number. If the game hasn't started yet, returns 0.
    """
    round = Hunt.query.with_entities(func.max(Hunt.round)).scalar()
    if round is None:
        round_number = 0
    else:
        round_number = round
    return round_number

def get_general_number_round_kills(round_number):
    """
    Returns the collective number of kills in a given round
    """
    round_kills = Hunt.query.filter_by(round=round_number, success=True).count()
    return round_kills

def get_unsuccessful_players(round_number):
    """
    Returns a list of all players who didn't kill in a given round
    """
    unsuccessful_players = db.session.query(Player).filter(
        Player.hunt_where_hunter.any(Hunt.round == round_number),
        ~Player.hunt_where_hunter.any(Hunt.round == round_number, Hunt.success == True)
    ).all()

    return unsuccessful_players


# GAME HUNT GETTERS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def get_hunts_filtered(round_filter=None, room_filter=None, date_filter=None, success_filter=None, order_by=None):
    """
    Returns a list of hunts filtered by the given parameters
    
    round_filter: int
    room_filter: int
    date_filter: string (YYYY-MM-DD)
    successful_filter: bool
    order_by: string  ('date', 'round', 'success')
    """
    hunts_query = Hunt.query
    
    if round_filter is not None:
        hunts_query = hunts_query.filter_by(round=round_filter)

    if room_filter is not None:
        hunts_query = hunts_query.filter_by(room_hunter=room_filter)
        hunts_query = hunts_query.filter_by(room_prey=room_filter)

    if date_filter:
        date = datetime.strptime(date_filter, '%Y-%m-%d')
        hunts_query = hunts_query.filter(Hunt.date == date)

    if success_filter is not None:
        hunts_query = hunts_query.filter_by(success=success_filter)

    if order_by is not None:
        if order_by == 'date':
            hunts_query = hunts_query.order_by(Hunt.date.desc())
        elif order_by == 'round':
            hunts_query = hunts_query.order_by(Hunt.round.desc())
        elif order_by == 'success':
            hunts_query = hunts_query.order_by(Hunt.success.desc())

    return hunts_query

def get_disputes_filtered( round_filter=None, hunt_filter=None, hunter_filter=None, prey_filter=None, active_filter=None, order_by=None):
    """
    Returns a list of disputes filtered by the given parameters

    round_filter: int
    hunter_filter: int
    prey_filter: int
    active_filter: string
    order_by: string  ('date', 'round', 'active')
    """

    disputes_query = Dispute.query

    if round_filter is not None:
        disputes_query = disputes_query.filter_by(round=round_filter)

    if hunt_filter is not None:
        disputes_query = disputes_query.filter_by(hunt_id=hunt_filter)

    if hunter_filter is not None:
        disputes_query = disputes_query.filter(Hunt.room_hunter == hunter_filter)
    
    if prey_filter is not None:
        disputes_query = disputes_query.filter(Hunt.room_prey == prey_filter)

    if active_filter:
        disputes_query = disputes_query.filter(Dispute.active == active_filter)
    
    if order_by is not None:
        if order_by == 'date':
            hunts_query = hunts_query.order_by(Hunt.date.desc())
        elif order_by == 'round':
            hunts_query = hunts_query.order_by(Hunt.round.desc())
        elif order_by == 'active':
            hunts_query = hunts_query.order_by(Hunt.active.desc())

    return disputes_query

# TEMPORALISATION - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# Routinary dispute management ---------------------------------- AT 11AM AND 11PM

def death_accusation_revision(revision_group):
    acusaciones_pendientes = get_general_death_accusations(revision_group=revision_group)

    if acusaciones_pendientes:
        for acusacion in acusaciones_pendientes:
            hunter_wins(acusacion)

def duel_revision(revision_group):
    duelos_pendientes = get_general_duels(revision_group=revision_group)

    if duelos_pendientes:
        for duelo in duelos_pendientes:
            finalise_duel(duelo)

def dispute_revision(revision_group):
    """
    Revises all disputes of a revision group
    Death accusations: Hunters win as prey didn't answer in time.
    Duels: A random winner is selected as they didn't come to an agreement in time.
    """
    death_accusation_revision(revision_group)
    duel_revision(revision_group)

# Routinary round management ---------------------------------- AT 12AM AND 12PM
    
def deaths_from_starvation():
    """
    Kills all players who didn't kill in the last round, and sends them an email.
    If all players didn't kill, it sends them all an email with a last chance.
    This only happens once, controlled by the extension_status variable.
    """
    round_number = get_round_number()
    unsuccessful_players = get_unsuccessful_players(round_number)
    jugadores_vivos = get_alive_players()
    extension_status = get_extension_status()

    if unsuccessful_players.length == jugadores_vivos.length and extension_status == 'NOT_EXTENDED':
        for player in unsuccessful_players:
            send_deadline_extension_email(player)
        set_extension_status('EXTENDED')
    else:  
        for player in unsuccessful_players:
            kill(player)
            send_starvation_email(player)
        db.session.commit()


def generate_pairs():

    """
    Returns a randomly shuffled list of hunter-prey pairs (tuples) of the alive players ids
    """
    alive_players = get_alive_players()
    rooms = [player.room for player in alive_players]
    random.shuffle(rooms)
    pairs = [(rooms[i], rooms[(i+1) % len(rooms)]) for i in range(len(rooms))]
    return pairs

def new_round():
    """
    Generates new pairs, updates the hunt table with the new round number and pairs
    """
    new_round_number = get_round_number() + 1
    
    round_pairs = generate_pairs()

    for pair in round_pairs:
        new_hunt(pair, new_round_number)
        hunter = get_player(pair[0])
        prey = get_player(pair[1])
        send_new_round_hunt_email(hunter, prey)


def process_round():
    """
    Processes the round only if the round status is TO_BE_FINALISED.
    If so, starvation deaths are processed, it sets the round status to PROCESSED, and a new round is started.
    """

    round_status = get_round_status()
    if round_status == 'TO_BE_FINALISED':

        deaths_from_starvation()

        set_round_status('PROCESSED')
        new_round()

    else:
        pass

# SUNDAY 00:00

def round_end():
    """
    Checks if a dispute revision period is needed.
    If not, processes the round.
    """

    disputas_pendientes = get_general_disputes()
    if disputas_pendientes:
        set_round_status('PENDING')
    else:
        set_round_status('TO_BE_FINALISED')
    
    process_round()

# SUNDAY 12:00

def revision_period_done():
    """
    If the revision period had been activated, it sets the round status to TO_BE_FINALISED and processes the round.
    If not, it doesn't do anything.
    """
    round_status = get_round_status()
    if round_status == 'PENDING':
        set_round_status('TO_BE_FINALISED')
    
    process_round()


# GAME START _________________________________________________________________________
    
def start_game():
    # Creates Player objects for all users with the player role
    # Creates the first round of hunts
    # Starts temporalisation
    pass


# GAME END _________________________________________________________________________
    
def game_over():
    
    # Stop dispute revisions
    # Stop round processing

    jugadores_vivos = get_alive_players()

    if jugadores_vivos.length == 1:
        ganador = jugadores_vivos[0]
    else:
        ganador = None
    

    players = Player.query.all()
    for player in players:
        send_game_finished_email(player, ganador=ganador)
    pass