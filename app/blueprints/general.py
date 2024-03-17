from flask import Blueprint, render_template, redirect, request, flash, url_for
from app.models import Users
from app.forms import LoginForm, NamerForm, PasswordForm
from app.extensions import db, bcrypt, login_manager
from flask_login import login_required, login_user, logout_user

general_bp = Blueprint("general", __name__, url_prefix='/', template_folder="../../templates")


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@general_bp.route('/')
def index():
    """Directs to home page"""
    first_name = "Trey"
    return render_template("index.html", first_name=first_name)



@general_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@general_bp.route('/date')
def get_current_date():
    fav_pizza_place = {
        'trey': "Youre my favorite pizza place",
        'john': "papa johns"
    }
    return fav_pizza_place


@general_bp.route('/name', methods=['GET', 'POST'])
def name():
    """directs to user form"""
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data 
        form.name.data = ''
        flash("Form succesfully submitted!!")
    return render_template("name.html", name = name, form = form)

@general_bp.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    """directs to user form"""
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data 
        password = form.pw.data
        form.email.data = ''
        form.pw.data = ''

        pw_to_check = Users.query.filter_by(email=email).first()
        passed = bcrypt.check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pw.html", email=email, pw=password, form=form, pw_to_check=pw_to_check, passed=passed)

