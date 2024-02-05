# /Vampiro/utils/emails.py

from flask import render_template

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
    
    token = user.get_confirmation_token()

    subject = "Confirma tu cuenta"
    message = render_template('emails/confirmation_instructions.html', user=user, token=token)
    recipient = user.email

    send_email(subject, message, recipient)   

def send_welcome_email(user):
    
    subject = "Una mordidita... de bienvenida"
    message = render_template('emails/welcome.html', user=user)
    recipient = user.email

    send_email(subject, message, recipient)

def send_password_reset_instructions_email(user):
    
    token = user.get_reset_password_token()

    subject = "Cambia tu contraseña"
    message = render_template('emails/reset_password_instructions.html', user=user, token=token)
    recipient = user.email

    send_email(subject, message, recipient) 

def send_password_changed_email(user):
    
    subject = "Tu contraseña ha sido cambiada"
    message = render_template('emails/password_changed.html', user=user)
    recipient = user.email

    send_email(subject, message, recipient)

def send_game_starting_soon_email(user):
    
    subject = "Se acerca la maldición"
    message = render_template('emails/game_starting_soon.html', user=user)
    recipient = user.email

    send_email(subject, message, recipient)

def send_game_finished_email(user):
    
    subject = "Y sólo quedó uno en pie..."
    message = render_template('emails/game_finished.html', user=user)
    recipient = user.email

    send_email(subject, message, recipient)

# PLAYER EMAILS _______________________________________________________________________


#   ROUND BEGIN/END
    
def send_new_round_hunt_email(player):

    subject = "Empieza una nueva noche"
    message = render_template('emails/new_round.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_starvation_email(player):
        
    subject = "Muerto... de hambre"
    message = render_template('emails/starvation.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_deadline_extension_email(player, ganador=None):
        
        subject = "Te doy una noche más"
        if ganador:
            message = render_template('emails/game_over_with_winner.html', ganador=ganador)
        else:
            message = render_template('emails/game_over_without_winner.html')
        recipient = player.user.email
    
        send_email(subject, message, recipient)


#   DISPUTE: START
    
def send_death_accusation_email(player):

    subject = "¿Aquí termina todo?¿En serio?"
    message = render_template('emails/death_accusation.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

#   HUNT: COMPLETION

def send_hunt_success_email(player):

    subject = "Tu sed de sangre no tiene final"
    message = render_template('emails/hunt_success.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

def send_victim_death_email(player):

    subject = "Adiós, mundo cruel"
    message = render_template('emails/victim_death.html', player=player)
    recipient = player.user.email

    send_email(subject, message, recipient)

#   DISPUTE: DUEL START

def send_duel_started_email(player):

    subject = "Tienes un duelo esta noche"
    message = render_template('emails/duel_started.html', player=player)
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