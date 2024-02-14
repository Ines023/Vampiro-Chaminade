# /Vampiro/utils/emails.py

from urllib.parse import quote_plus
from flask import render_template

# EMAIL SENDING THROUGH AZURE TOOL _____________________________________________________

def send_email(subject, message, recipient):
    """
    Sends an email through Azure Logic Apps
    """

    print(f"Subject: {subject}")
    print(f"Recipient: {recipient}")
    print(f"Template: {message}")


    # message = render_template(template, **kwargs)

    # URL of the Logic App
    # url = "https://prod-27.francesouth.logic.azure.com:443/workflows/c30aec9fd78541e19c8cbbfbcb5107e1/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=_YcSKY0B5ONCxTdTejSqtxKxGdDPPeblVFP7-lq2juA"

    # JSON payload
    # payload = {
    #     "subject": subject,
    #     "message": message,
    #     "recipient": recipient
    # }

    # Send the HTTP request
    # headers = {'Content-Type': 'application/json'}
    # response = request.post(url, headers=headers, data=json.dumps(payload))

    # Check the response
    # if response.status_code != 200:
    #     print(f"Failed to send email: {response.content}")

# USER EMAILS _________________________________________________________________________
    
def send_confirmation_instructions_email(user):
    """
    Sends an email to the user with a confirmation link that includes a timed token based on them.
    """


    token = user.get_confirmation_token()
    url_encoded_token = quote_plus(token)

    subject = "Confirma tu cuenta"
    message = render_template('email/confirmacion_instrucciones.html', user=user, token=url_encoded_token)
    recipient = user.email

    send_email(subject, message, recipient)   

def send_welcome_email(user):
    """
    Sends a welcome email to a just confirmed user.
    """


    subject = "Una mordidita... de bienvenida"
    message = render_template('email/welcome.html', user=user)
    recipient = user.email

    send_email(subject, message, recipient)

def send_password_reset_instructions_email(user):
    """
    Sends an email to the user with a link to reset their password that includes a token based on them.
    """


    token = user.get_reset_password_token()
    url_encoded_token = quote_plus(token)

    subject = "Cambia tu contraseña"
    message = render_template('email/contraseña_reset_instrucciones.html', user=user, token=url_encoded_token)
    recipient = user.email

    send_email(subject, message, recipient) 

def send_password_changed_email(user):
    """
    Sends an email to the user to confirm that their password has been changed.
    """

    subject = "Tu contraseña ha sido cambiada"
    message = render_template('email/contraseña_reset_completada.html', user=user)
    recipient = user.email

    send_email(subject, message, recipient)

def send_game_starting_soon_email(user):
    """
    Sends an email to the user to inform them that the game is about to start.
    """

    subject = "Se acerca la maldición"
    message = render_template('email/game_starting_soon.html', user=user)
    recipient = user.email

    send_email(subject, message, recipient)

def send_game_finished_email(player, ganador=None):
    """
    Sends an email to the user to inform them that the game has finished with the results.
    """
    
    if ganador:
        if player == ganador:
            subject = "Y el último en pie... ¡Eres tú!"
            message = render_template('email/game_finished_you_won.html', user=player.user)
        else:
            subject = "Y sólo quedó uno en pie..."
            message = render_template('email/game_finished_yeswinner.html', user=player.user)
    else:
        subject = "Todo fue inundado por silencio..."
        message = render_template('email/game_finished_nowinner.html', user=player.user)
    
    recipient = player.user.email

    send_email(subject, message, recipient)

# PLAYER EMAILS _______________________________________________________________________


#   ROUND BEGIN/END
    
def send_new_round_hunt_email(player,prey):
    """
    Sends an email to the player to inform them that a new round has started.
    """
    subject = "Empieza una nueva noche"
    message = render_template('email/new_round.html', player=player, prey=prey)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_starvation_email(player):
        
    subject = "Muerto... de hambre"
    message = render_template('email/starvation.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_deadline_extension_email(player):
    """
    Sends an email to the player to inform them that the deadline has been extended.
    """
    subject = "Te doy una noche más"
    message = render_template('email/deadline_extension.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)


#   DISPUTE: START
    
def send_death_accusation_email(player, revision_group):

    if revision_group == 'DAY':
        hora = '23:00'
    else:
        hora = '11:00'

    subject = "¿Aquí termina todo?¿En serio?"
    message = render_template('email/death_accusation.html', player=player, hora=hora)
    recipient = player.user.email

    send_email(subject, message, recipient)

#   HUNT: COMPLETION

def send_hunt_success_email(hunter, prey):

    subject = "Tu sed de sangre no tiene final"
    message = render_template('email/hunt_success.html', hunter=hunter, prey=prey)
    recipient = hunter.user.email

    send_email(subject, message, recipient)

def send_victim_death_email(player):

    subject = "Adiós, mundo cruel"
    message = render_template('email/victim_death.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

#   DISPUTE: DUEL START

def send_duel_started_email(player, revision_group):

    if revision_group == 'DAY':
        hora = '23:00'
    else:
        hora = '11:00'

    subject = "Tienes un duelo esta noche"
    message = render_template('email/duel_started.html', player=player, hora=hora)
    recipient = player.user.email

    send_email(subject, message, recipient)

#   DISPUTE: DUEL RESOLUTION

def send_duel_hunter_win_email(player):

    subject = "Victoria a medianoche"
    message = render_template('email/duel_hunter_win.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)
    
def send_duel_prey_win_email(player):

    subject = "Victoria a medianoche"
    message = render_template('email/duel_prey_win.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_duel_hunter_loss_email(player):

    subject = "A medianoche pasaste a mejor vida"
    message = render_template('email/duel_hunter_loss.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_duel_prey_loss_email(player):

    subject = "A medianoche pasaste a mejor vida"
    message = render_template('email/duel_prey_loss.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_hunt_available_email(player):

    subject = "Tu presa te espera"
    message = render_template('email/hunt_available.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)





# ADMIN EMAILS _________________________________________________________________________
    
def send_error_email(error, jugador, pagina):
    
    subject = "QUE SE NOS CAE EL VAMPIRO"
    message = f"A {jugador} en la página {pagina} le ha saltado este error: {error}"
    recipient = "auladejuegos@gmail.com"

    send_email(subject, message, recipient)