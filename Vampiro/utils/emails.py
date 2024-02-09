# /Vampiro/utils/emails.py

from flask import render_template

from Vampiro.services.game import get_current_hunt, get_player

# EMAIL SENDING THROUGH AZURE TOOL _____________________________________________________

def send_email(subject, message, recipient):
    """
    Sends an email through Azure Logic Apps
    """

    print(f"Subject: {subject}")
    print(f"Template: {message}")
    print(f"Recipient: {recipient}")

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

    subject = "Confirma tu cuenta"
    message = render_template('emails/confirmacion_instrucciones.html', user=user, token=token)
    recipient = user.email

    send_email(subject, message, recipient)   

def send_welcome_email(user):
    """
    Sends a welcome email to a just confirmed user.
    """


    subject = "Una mordidita... de bienvenida"
    message = render_template('emails/welcome.html', user=user)
    recipient = user.email

    send_email(subject, message, recipient)

def send_password_reset_instructions_email(user):
    """
    Sends an email to the user with a link to reset their password that includes a token based on them.
    """


    token = user.get_reset_password_token()

    subject = "Cambia tu contraseña"
    message = render_template('email/contraseña_reset_instrucciones.html', user=user, token=token)
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
    message = render_template('emails/game_starting_soon.html', user=user)
    recipient = user.email

    send_email(subject, message, recipient)

def send_game_finished_email(player, ganador=None):
    """
    Sends an email to the user to inform them that the game has finished with the results.
    """
    
    if ganador:
        if player == ganador:
            subject = "Y el último en pie... ¡Eres tú!"
            message = render_template('emails/game_finished_you_won.html', user=player.user)
        else:
            subject = "Y sólo quedó uno en pie..."
            message = render_template('emails/game_finished_yeswinner.html', user=player.user)
    else:
        subject = "Todo fue inundado por silencio..."
        message = render_template('emails/game_finished_nowinner.html', user=player.user)
    
    recipient = player.user.email

    send_email(subject, message, recipient)

# PLAYER EMAILS _______________________________________________________________________


#   ROUND BEGIN/END
    
def send_new_round_hunt_email(player_id):
    """
    Sends an email to the player to inform them that a new round has started.
    """
    player=get_player(player_id)
    current_hunt= get_current_hunt(player_id)
    prey=current_hunt.prey

    subject = "Empieza una nueva noche"
    message = render_template('emails/new_round.html', player=player, prey=prey)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_starvation_email(player):
        
    subject = "Muerto... de hambre"
    message = render_template('emails/starvation.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_deadline_extension_email(player):
    """
    Sends an email to the player to inform them that the deadline has been extended.
    """
    subject = "Te doy una noche más"
    message = render_template('emails/deadline_extension.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)


#   DISPUTE: START
    
def send_death_accusation_email(player, revision_group):

    if revision_group == 'DAY':
        hora = '23:00'
    else:
        hora = '11:00'

    subject = "¿Aquí termina todo?¿En serio?"
    message = render_template('emails/deadline_extension.html', player=player, hora=hora)
    recipient = player.user.email

    send_email(subject, message, recipient)

#   HUNT: COMPLETION

def send_hunt_success_email(hunter, prey):

    subject = "Tu sed de sangre no tiene final"
    message = render_template('emails/hunt_success.html', hunter=hunter, prey=prey)
    recipient = hunter.user.email

    send_email(subject, message, recipient)

def send_victim_death_email(player):

    subject = "Adiós, mundo cruel"
    message = render_template('emails/victim_death.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

#   DISPUTE: DUEL START

def send_duel_started_email(player, revision_group):

    if revision_group == 'DAY':
        hora = '23:00'
    else:
        hora = '11:00'

    subject = "Tienes un duelo esta noche"
    message = render_template('emails/duel_started.html', player=player, hora=hora)
    recipient = player.user.email

    send_email(subject, message, recipient)

#   DISPUTE: DUEL RESOLUTION

def send_duel_hunter_win_email(player):

    subject = "Victoria a medianoche"
    message = render_template('emails/duel_hunter_win.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)
    
def send_duel_prey_win_email(player):

    subject = "Victoria a medianoche"
    message = render_template('emails/duel_prey_win.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_duel_hunter_loss_email(player):

    subject = "A medianoche pasaste a mejor vida"
    message = render_template('emails/duel_hunter_loss.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_duel_prey_loss_email(player):

    subject = "A medianoche pasaste a mejor vida"
    message = render_template('emails/duel_prey_loss.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)






# ADMIN EMAILS _________________________________________________________________________
    
def send_error_email(error, jugador, pagina):
    
    subject = "QUE SE NOS CAE EL VAMPIRO"
    message = f"A {jugador} en la página {pagina} le ha saltado este error: {error}"
    recipient = "auladejuegos@gmail.com"

    send_email(subject, message, recipient)