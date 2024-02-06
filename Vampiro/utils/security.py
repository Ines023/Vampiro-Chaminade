#/Vampiro/utils/security.py
from flask import flash, request, redirect, url_for
from flask_login import current_user
from .emails import send_error_email


from functools import wraps

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
    print('Error: ' + str(e))
    try:
        send_error_email(e, jugador, pagina)
        flash('¡Ha saltado un error inesperado! Los organizadores han recibido un correo al respecto', 'danger')
    except:
        flash('¡Ha saltado un error inesperado! Avisa a algún organizador. Error: ' + str(e), 'danger') 
     
    return redirect(url_for('public.home'))