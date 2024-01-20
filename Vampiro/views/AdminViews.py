from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from Vampiro.models import Cronicas
from Vampiro.utils.forms import NewCronicaForm
from Vampiro.services.admin_actions import add_cronica

admin = Blueprint('admin', __name__)



@admin.before_request
@login_required
def check_role():
    if current_user.role.name != 'admin':
        return redirect(url_for('profile.my_stats'))

@admin.route('/cronicas')
def admin_cronicas():   

    form = NewCronicaForm(request.form)
    
    if request.method == 'POST' and form.validate_on_submit():
        cronica = Cronicas(date=form.date.data, title=form.title.data, content=form.content.data)
        add_cronica(cronica)
        return redirect(url_for('public.cronicas'))
                
    return render_template('admin/new_cronica.html', form=form)