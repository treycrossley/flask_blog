from flask import Blueprint, render_template, redirect, request, flash, url_for
from app.models import Users
from app.forms import LoginForm
from app.extensions import db, bcrypt
from flask_login import login_required, login_user, logout_user

auth_bp = Blueprint("auth", __name__, url_prefix='/auth', template_folder="../../templates")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password_hash, form.password.data):
                    login_user(user)
                    flash("Login sucessful!")
                    return redirect(url_for('general.dashboard'))
                else: 
                    flash("Wrong Password - Try again!")
            else: 
                flash("User does not exist")
        except Exception:
            flash("Could not get User from db")
    return render_template('login.html',form=form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('auth.login'))