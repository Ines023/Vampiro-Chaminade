# /Vampiro/services/settings.py

import logging
import math


from Vampiro.database.mysql import db
from Vampiro.models.SettingsModel import EmailBatches, Settings


logger = logging.getLogger('simple_logger')

# SETTINGS GETTERS _________________________________________________________________________

def get_settings():
    """
    Returns the settings object
    """
    return Settings.query.first()

def get_mode():
    """
    Returns the game mode: VAMPIRO, CUPIDO
    """
    settings = get_settings()
    mode = settings.mode
    return mode

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

def get_timer_switch_value():
    """
    Returns the timer switch value: True, False
    """
    settings = get_settings()
    timer_switch_value = settings.timer_switch
    return timer_switch_value

def get_holidays():
    """
    Returns the vacaciones value: True, False
    """
    settings = get_settings()
    vacaciones = settings.holidays
    return vacaciones

def get_batch_size():
    """
    Returns the batch size
    """
    settings = get_settings()
    batch_size = settings.batch_size
    return batch_size

# SETTINGS SETTERS _________________________________________________________________________


def set_mode(mode):
    """
    Changes the game mode: VAMPIRO, CUPIDO
    """
    settings = get_settings()
    settings.mode = mode
    db.session.commit()
    logger.info('Modo de juego cambiado a: %s', mode)

def set_game_status(game_status):
    """
    Changes the game status: NOT_STARTED, REGISTRY_OPEN, IN_PROGRESS, FINISHED
    """
    settings = get_settings()
    settings.game_status = game_status
    db.session.commit()
    logger.info('Estado de juego cambiado a: %s', game_status)

def set_round_status(round_status):
    """
    Changes the round status: PENDING, TO_BE_FINALISED, PROCESSED
    """
    settings = get_settings()
    settings.round_status = round_status
    db.session.commit()
    logger.info('Estado de ronda cambiado a: %s', round_status)

def set_extension_status(extension_status):
    """
    Changes the extension status: EXTENDED, NOT_EXTENDED
    """
    settings = get_settings()
    settings.extension_status = extension_status
    db.session.commit()
    logger.info('Estado de extension cambiado a: %s', extension_status)

def set_timer_switch_value(value):
    """
    Changes the timer switch value: True, False
    """
    settings = get_settings()
    settings.timer_switch = value
    db.session.commit()
    logger.info('Timer switch cambiado a: %s', value)

def set_holidays(value):
    """
    Changes the vacaciones value: True, False
    """
    settings = get_settings()
    settings.holidays = value
    db.session.commit()
    logger.info('Vacaciones cambiado a: %s', value)



#Email Batches _________________________________________________________________
    
def count_total_batches(recepients):
    """
    Returns the total number of batches
    """
    BATCH_SIZE = get_batch_size()
    Total = math.ceil(recepients.count()/BATCH_SIZE)
    logger.info('Total batches: %s', Total)
    return Total


def new_email_batch_group(round_number, batch_type, recepients):

    total_batches = count_total_batches(recepients)
    emailbatches = EmailBatches( round_number = round_number, batch_type = batch_type, total_batches = total_batches, current_batch = 0)
    db.session.add(emailbatches)
    logger.info('New email batch group created for round %s and batch type %s', round_number, batch_type)

def get_total_batches(round_number, batch_type):
    """
    Returns the total number of batches
    """
    emailbatches = EmailBatches.query.filter_by(round_number = round_number, batch_type = batch_type).first()
    total_batches = emailbatches.total_batches
    return total_batches

def get_current_batch(round_number, batch_type):
    """
    Returns the current batch
    """
    emailbatches = EmailBatches.query.filter_by(round_number = round_number, batch_type = batch_type).first()
    current_batch = emailbatches.current_batch
    return current_batch

def set_current_batch(round_number, batch_type, current_batch):
    """
    Changes the current batch
    """
    emailbatches = EmailBatches.query.filter_by(round_number = round_number, batch_type = batch_type).first()
    emailbatches.current_batch = current_batch
    db.session.commit()
    logger.info('Current batch changed to: %s', current_batch)