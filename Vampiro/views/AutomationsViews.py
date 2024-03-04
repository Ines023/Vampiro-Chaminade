from flask import Blueprint, request, current_app, abort
import logging
from Vampiro.services.game import next_emails_batch, process_round_continuation

from Vampiro.services.routinary_services import DatabaseUpdate
from Vampiro.utils.security import handle_exceptions

logger = logging.getLogger('simple_logger')

automation = Blueprint('automation', __name__)



@automation.route('/email_batch', methods=['POST'])
@handle_exceptions
def email_batch():
    # Check for the secret key in the headers
    logger.info('Se ha recibido una petición para enviar un batch de emails parte primera')
    secret_key = request.headers.get('X-Secret-Key')
    if secret_key != current_app.config['SECRET_KEY']:
        logger.info('Alguien ha intentado enviar un batch de emails sin la clave secreta. Se ha abortado la petición.')
        abort(403)

    # Get the batch type from the request
    batch_type = request.headers.get('batch_type')
    if batch_type is None:
        logger.info('Se ha recibido una petición para enviar un batch de emails sin el tipo de batch. Se ha abortado la petición.')
        abort(400)
    
    # Get the round number from the request
    round = request.headers.get('round')
    if round is None:
        logger.info('Se ha recibido una petición para enviar un batch de emails sin el número de ronda. Se ha abortado la petición.')
        abort(400)

    logger.info('Todos los parametros eran correctos')

    response = next_emails_batch(round, batch_type)
    return response

@automation.route('/process_round_end', methods=['POST'])
@handle_exceptions
def process_round_end():
    # Check for the secret key in the headers
    logger.info('Se ha recibido una petición para enviar un batch de emails parte segunda')
    secret_key = request.headers.get('X-Secret-Key')
    if secret_key != current_app.config['SECRET_KEY']:
        logger.info('Alguien ha intentado enviar un batch de emails sin la clave secreta. Se ha abortado la petición.')
        abort(403)
    
    process_round_continuation()
    return 'Script has run'

@automation.route('/update', methods=['POST'])
@handle_exceptions
def update():
    # Check for the secret key in the headers
    logger.info('Se ha recibido una petición para actualizar la base de datos')
    secret_key = request.headers.get('X-Secret-Key')
    if secret_key != current_app.config['SECRET_KEY']:
        logger.info('Alguien ha intentado actualizar la base de datos sin la clave secreta. Se ha abortado la petición.')
        abort(403)  # Forbidden

    DatabaseUpdate()
    return 'Script has run'