from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from sqlalchemy.exc import IntegrityError
from .methods import send_token_email
from itsdangerous import SignatureExpired
from app import URL_SERIALIZER
from flask_login import current_user
from .forms import LoginForm, RegistrationForm, ForgetPasswordForm, ResetPasswordForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            address=form.address.data,
            role=form.role.data,
            pincode=form.pincode.data,
            password=hashed_password,
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully.', 'success')
            return redirect(url_for('auth.login'))
        except IntegrityError:
            flash('Email already exists.', 'danger')
        except Exception as e:
            print(e)
            flash('An error occurred!', 'danger')

    return render_template('signup.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route("/forgetpassword", methods = ["GET", "POST"])
def forgetpassword():
    form = ForgetPasswordForm()

    if form.validate_on_submit():  # Use Flask-WTF's built-in form validation
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user:
            token = URL_SERIALIZER.dumps(email, salt='email-confirm')
            reset_link = url_for('auth.reset_password', token=token, _external=True)

            try:
                send_token_email(email, user.firstname, reset_link)
                flash('Password reset link sent to your email.', 'success')
            except Exception as e:
                flash('Error sending email. Please try again later.', 'danger')
        else:
            flash('No account found with that email address.', 'danger')

    return render_template("forgetpassword.html", form=form)
    

@bp.route("/reset-password/<token>", methods = ["GET", "POST"])
def reset_password(token):
    form = ResetPasswordForm()

    if request.method == "GET":
        return render_template("reset_password.html", form=form)

    if request.method == "POST" and form.validate_on_submit():
        try:
            # Deserialize token to get email
            email = URL_SERIALIZER.loads(token, salt='email-confirm', max_age=3600)
        except SignatureExpired:
            flash("The token has expired.", "danger")
            return redirect(url_for('auth.login'))

        # Get the new password from the form
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Update user password in the database
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hashed_password
            try:
                db.session.commit()
                flash("Your password has been updated successfully!", "success")
                return redirect(url_for('auth.login'))
            except IntegrityError:
                db.session.rollback()
                flash("An error occurred while updating your password. Please try again.", "danger")
        else:
            flash("User not found.", "danger")

    return render_template("reset_password.html", form=form)
    
@login_required
@bp.route("/change-password", methods = ["GET", "POST"])
def change_password():
    form = ResetPasswordForm()

    if request.method == "GET":
        return render_template("reset_password.html", form=form)
    
    if request.method == "POST" and form.validate_on_submit():
        # Get the new password from the form
        password = form.password.data
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        user = current_user

        if user:
            user.password = hashed_password
            try:
                db.session.commit()
                flash("Your password has been updated successfully!", "success")
                return redirect(url_for('auth.logout'))
            except IntegrityError:
                db.session.rollback()
                flash("An error occurred while updating your password. Please try again.", "danger")
        else:
            flash("User not found.", "danger")
    
    return render_template("reset_password.html", form=form)