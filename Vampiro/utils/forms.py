from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo,  NumberRange

from Vampiro.models import User


# ___ VALIDATORS _________________________________________________________________

class Unique(object):
    def __init__(self, model, field, message="Este elemento ya existe."):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)
        
class Registered(object):
    def __init__(self, model, field, message=u'Este elemento no existe.'):
        self.model = model
        self.field = field
        self.message = message
    
    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if not check:
            raise ValidationError(self.message)
        
def handle_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{error}", 'danger')

# ___ FORMS ______________________________________________________________________

# FORM: REGISTRO DE USUARIO
        
class SignUpForm(FlaskForm):
    name = StringField('Nombre y Apellidos', validators=[DataRequired(message='Debes introducir tu nombre'), Length(min=1, max=80)])
    room = IntegerField('Habitación', validators=[DataRequired(message='Debes introducir un número de habitación'), NumberRange(min=100, max=900), Unique(User, User.room, message='Ya hay un jugador con esta habitación')])
    email = StringField('Email', validators=[DataRequired(message='Debes introducir un email'), Email(message='Por favor introduce un email válido'), Length(min=1, max=120), Unique(User, User.email, message='Ya hay un jugador con este email')])
    password = PasswordField('Password',validators=[DataRequired(message='Debes introducir una contraseña'),Length(min=8, max=128, message='Tu contraseña debe tener al menos 8 caracteres')])
    confirm_password = PasswordField('Confirma la contraseña', validators=[DataRequired(message='Debes confirmar tu contraseña'), EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Registrarse')        

# FORM: INICIO DE SESIÓN

class LoginForm(FlaskForm):
    room = IntegerField('Habitación', validators=[DataRequired(message='Debes introducir un número de habitación'), NumberRange(min=100, max=900), Registered(User, User.room, message='No hay ningún jugador con esa habitación')])
    password = PasswordField('Password', validators=[DataRequired(message='Debes introducir tu contraseña')])
    remember_me = BooleanField('Recuérdame') 
    submit = SubmitField('Iniciar Sesión')  

# FORM: SOLICITAR CAMBIO DE CONTRASEÑA
    
class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=120), Registered(User, User.email, message='No hay ningún jugador con este email')])
    submit = SubmitField('Enviar')

# FORM: PROCESAR CAMBIO DE CONTRASEÑA
    
class NewPasswordForm(FlaskForm):
    password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=1, max=128)])
    confirm_password = PasswordField('Confirma la contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Enviar')

# FORM: UNIRSE A LA PARTIDA
    
class RoleSelectorForm(FlaskForm):
    role = StringField('Rol')

# FORM: IDENTIFICARSE COMO ORGANIZADOR
    
class OrganizerForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired(message='Debes introducir la clave'), Length(min=1, max=128)])
    submit = SubmitField('Enviar')
    
# FORM: ACCIONES DE LOS JUGADORES
    
class DeathAccusationForm(FlaskForm):
    response = SubmitField()
    
class DuelResponseForm(FlaskForm):
    type = HiddenField()




# ADMIN_FORM: NUEVA CRÓNICA

class NewCronicaForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=1, max=80)])
    content = TextAreaField('Contenido', validators=[DataRequired(), Length(min=1, max=5000)])
    submit = SubmitField('Publicar')