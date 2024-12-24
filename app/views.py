from flask import Blueprint, render_template, get_flashed_messages, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import db
from .forms import UpdateUserForm

bp = Blueprint('views', __name__)

@bp.route('/')
@login_required
def home():
    return render_template('home.html')

@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    get_flashed_messages()
    form = UpdateUserForm(obj=current_user)  # Prepopulate form with current_user data
    if form.validate_on_submit():
        form.populate_obj(current_user)  # Update user object with form data
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template('update_user.html', form=form)


@bp.route('/auth_error')
def auth_error():
    return render_template('notAuthorized.html')