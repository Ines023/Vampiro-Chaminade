#/Vampiro/utils/security.py
from flask import flash, request, redirect, url_for, current_app
from flask_login import current_user
from .emails import send_error_email
from authlib.jose import jwt
from authlib.jose.errors import BadSignatureError, ExpiredTokenError
import logging

from Vampiro.models.UserModel import User

from functools import wraps

logger = logging.getLogger('simple_logger')

# TOKEN HANDLERS ______________________________________________________________________________________


def verify_confirmation_token(token):
    try:
        private_key = current_app.config['SECRET_KEY']
        claims = jwt.decode(token, private_key)
        claims.validate() 
        user_id = claims['confirm_email']
        logger.info('Usuario ha usado un token valido: %s', user_id)
    except BadSignatureError:
        flash("Tu link de confirmación no es válido.", "danger")
        logger.info('Se ha usado un token de confirmación no válido')
        return None
    except ExpiredTokenError:
        flash("Tu link de confirmación ha caducado.", "warning")
        logger.info('Se ha usado un token de confirmación caducado')
        return None
    return User.query.get(user_id)

def verify_reset_token(token):
    try:
        private_key = current_app.config['SECRET_KEY']
        claims = jwt.decode(token, private_key)
        claims.validate() 
        user_id = claims['reset_password']
        logger.info('Usuario ha usado un token valido: %s', user_id)
    except BadSignatureError:
        flash("Tu link de cambio de contraseña no es válido.", "danger")
        logger.info('Se ha usado un token de cambio de contraseña no válido')
        return None
    except ExpiredTokenError:
        flash("Tu link de cambio de contraseña ha caducado.", "warning")
        logger.info('Se ha usado un token de cambio de contraseña caducado')
        return None
    return User.query.get(user_id)

# ERROR HANDLERS ______________________________________________________________________________________


def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            if current_user:
                jugador = current_user
            else:
                jugador = "Alguien random"
            pagina = request.path
            return error_management(e, jugador=jugador, pagina=pagina)
    return decorated_function



def error_management(e, jugador="Alguien random", pagina="desconocida"):
    """
    Manages the errors that are not caught by the app. Tries to send an email to the organizers with the error details, if it fails, it flashes a message to the user
    """
    logger.error('Error: ' + str(e))
    try:
        send_error_email(e, jugador, pagina)
        flash('¡Ha saltado un error inesperado! Los organizadores han recibido un correo al respecto', 'danger')
    except:
        flash('¡Ha saltado un error inesperado! Avisa a algún organizador. Error: ' + str(e), 'danger') 
     
    return redirect(url_for('public.home'))