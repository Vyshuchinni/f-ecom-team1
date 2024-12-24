from flask import Blueprint, render_template, get_flashed_messages, request, redirect, url_for
from flask_login import login_required, current_user
from .models import db, User

bp = Blueprint('views', __name__)

@bp.route('/')
@login_required
def home():
    return render_template('home.html')

@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    
    get_flashed_messages()

    if request.method == "POST":
        
       current_user.firstname = request.form.get('firstname')
       current_user.lastname = request.form.get('lastname')
       current_user.address = request.form.get('address')
       current_user.pincode = request.form.get('pincode')
       db.session.commit()
       return redirect(url_for('views.home'))

    return render_template('update_user.html', context = {'current_user': current_user})