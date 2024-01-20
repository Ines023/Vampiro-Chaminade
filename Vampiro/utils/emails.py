from flask import render_template

# EMAIL SENDING THROUGH AZURE TOOL _____________________________________________________

def send_email(subject, template, recipient, **kwargs):
    print(f"Subject: {subject}")
    print(f"Template: {template}")
    print(f"Recipient: {recipient}")
    print(f"Kwargs: {kwargs}")

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
    
def send_confirmation_instructions(user):
    
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

def send_password_reset_instructions(user):
    
    token = user.get_reset_password_token()

    subject = "Resetea tu contraseña"
    message = render_template('emails/reset_password_instructions.html', user=user, token=token)
    recipient = user.email

    send_email(subject, message, recipient) 

def send_password_changed_email(user):
    
    subject = "Tu contraseña ha sido cambiada"
    message = render_template('emails/password_changed.html', user=user)
    recipient = user.email

    send_email(subject, message, recipient)



# PLAYER EMAILS _______________________________________________________________________
    
def send_victim_email(player):
        
    subject = "¡Eres la víctima!"
    message = render_template('emails/victim.html', player=player)
    recipient = player.email

    send_email(subject, message, recipient)

def send_hunt_email(player):
        
    subject = "¡Eres el cazador!"
    message = render_template('emails/hunt.html', player=player)
    recipient = player.email

    send_email(subject, message, recipient)

def send_starvation_email(player):
        
    subject = "¡Estás muerto de hambre!"
    message = render_template('emails/starvation.html', player=player)
    recipient = player.email

    send_email(subject, message, recipient)



# ADMIN EMAILS _________________________________________________________________________
    
def send_error_email(error, jugador, pagina):
    
    subject = "QUE SE NOS CAE EL VAMPIRO"
    message = f"A {jugador} en la página {pagina} le ha saltado este error: {error}"
    recipient = "auladejuegos@gmail.com"

    send_email(subject, message, recipient)