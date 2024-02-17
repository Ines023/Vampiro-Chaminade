from flask import Blueprint, request, current_app, abort

from Vampiro.services.routinary_services import DatabaseUpdate


automation = Blueprint('automation', __name__)

@automation.route('/update', methods=['POST'])
def update():
    # Check for the secret key in the headers
    print('Se ha recibido una petición para actualizar la base de datos')
    secret_key = request.headers.get('X-Secret-Key')
    if secret_key != current_app.config['SECRET_KEY']:
        abort(403)  # Forbidden

    DatabaseUpdate()
    return 'Script has run'