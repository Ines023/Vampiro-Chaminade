from flask import Blueprint, request, current_app, abort
import logging

from Vampiro.services.routinary_services import DatabaseUpdate

logger = logging.getLogger('simple_logger')

automation = Blueprint('automation', __name__)

@automation.route('/update', methods=['POST'])
def update():
    # Check for the secret key in the headers
    logger.info('Se ha recibido una petición para actualizar la base de datos')
    secret_key = request.headers.get('X-Secret-Key')
    if secret_key != current_app.config['SECRET_KEY']:
        logger.info('Alguien ha intentado actualizar la base de datos sin la clave secreta. Se ha abortado la petición.')
        abort(403)  # Forbidden

    DatabaseUpdate()
    return 'Script has run'