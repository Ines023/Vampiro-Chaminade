from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from Vampiro.models import Cronicas, User
from Vampiro.utils.forms import LoginForm, handle_form_errors, SignUpForm, EmailForm, NewPasswordForm
from Vampiro.utils.emails import send_confirmation_instructions, send_welcome_email, send_password_reset_instructions
from Vampiro.services.users import add_user, confirm_user, update_password

public = Blueprint('admin', __name__)

@public.route('/')
@public.route('/home')
def home():
    return render_template('public/home.html')

@public.route('/')
@public.route('/home')
def home():
    return render_template('public/normas.html')

@public.route('/cronicas')
def cronicas():
    cronicas = Cronicas.query.order_by(Cronicas.date.desc()).all()
    return render_template('public/cronicas.html', cronicas=cronicas)

# LOGIN _________________________________________________________________

@public.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():

        user = User.query.filter_by(room=form.room.data).first()

        if user and check_password_hash(user.password_hashed, form.password.data):
            if user.confirmed:
                login_user(user, remember=form.remember_me.data)
                return redirect(request.args.get('next') or url_for('profile.role_selector'))
            else:
                flash('Por favor confirma tu correo antes de iniciar sesión.', 'warning')
                return redirect(url_for('public.resend_confirmation'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    else:
        handle_form_errors(form)

@public.route('/logout')
def logout():

    logout_user()
    flash('Has cerrado sesión. ¡Chao pescao!', 'success')

    return redirect(url_for('public.home'))

# SIGN UP _____________________________________________________________________

@public.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_user = add_user(form)
        send_confirmation_instructions(new_user)
        flash('Te has registrado con éxito. Por favor, confirma tu correo.', 'success')
        return redirect(url_for('public.home'))
    else:
        handle_form_errors(form)

    return render_template('public/signup_and_login/signup.html', form=form)

@public.route('/resend-confirmation', methods=['GET', 'POST'])
def resend_confirmation():
    
    form = EmailForm()
    if request.method=='POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.confirmed:
                flash ('Mejor más que menos, pero tu cuenta ya estaba confirmada. No hacer falta RE-confirmar. ¡Puedes iniciar sesión si quieres!', 'success')
                return redirect(url_for('public.login'))
            else:
                send_confirmation_instructions(user)
                flash('Se han reenviado las instrucciones de confirmación a tu correo.', 'success')
    else:
        handle_form_errors(form)
    return render_template('public/resend_confirmation.html', form=form)

@public.route('/confirm/<token>')
def confirm(token):

    user = user.verify_confirmation_token(token)
    if not user:
        flash('Tu código de confirmación no es válido o ha caducado.', 'danger')
        return redirect(url_for('public.resend_confirmation'))
    if user.confirmed:
        flash ('Mejor más que menos, pero tu cuenta ya estaba confirmada. No hace falta RE-confirmar. ¡Puedes iniciar sesión si quieres!', 'success')
        return redirect(url_for('public.login'))
    else:
        confirmed = confirm_user(user)
        flash ('Acabas de confrimar tu cuenta... ¡Qué guay!', 'success')
        send_welcome_email(user)
            
    return redirect(url_for('public.home'))

# RESET PASSWORD ______________________________________________________________

@public.route('/reset-password', methods=['GET', 'POST'])
def reset_password():

    print('inside try reset password')
    form = EmailForm() #Reset password form
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_instructions(user)
            flash('Por favor comprueba tu correo. Has recibido un link para cambiar tu contraseña', 'success')
        else:
            flash('No hay ningún usuario con ese email', 'danger')
        return redirect(url_for('public.home'))
    else:
        handle_form_errors(form)
    
    return render_template('public/reset/reset_password.html', form=form)

@public.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    user = user.verify_reset_token(token)

    if not user:
        flash('Tu código de confirmación no es válido o ha caducado.', 'danger')
        return redirect(url_for('public.reset_password'))
    
    form = NewPasswordForm() #Reset password form

    if request.method == 'POST' and form.validate_on_submit():
        update_password(user, form)
        flash('Tu contraseña ha sido cambiada.', 'success')
        return redirect(url_for('public.login'))
    else:
        handle_form_errors(form)

    return render_template('public/reset/reset_password_token.html', form=form, token=token)