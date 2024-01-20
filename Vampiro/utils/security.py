


# ERROR HANDLERS ______________________________________________________________________________________

def error_management(e, jugador="Alguien random", pagina="desconocida"):
    print('Error: ' + str(e))
    try:
        send_error_email(e, jugador, pagina)
        flash('¡Ha saltado un error inesperado! Los organizadores han recibido un correo al respecto', 'danger')
    except:
        flash('¡Ha saltado un error inesperado! Avisa a algún organizador. Error: ' + str(e), 'danger')  