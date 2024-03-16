"""For flask library and template rendering for our web app"""
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Create Flask instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config["SECRET_KEY"] = "1234"

db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Name %r>' % self.name


# Form Class
class NamerForm(FlaskForm):
    """class for asking user their name"""
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


# Create a route decorator
@app.route('/')
def index():
    """Directs to home page"""
    first_name = "Trey"
    return render_template("index.html", first_name=first_name)

@app.route('/name', methods=['GET', 'POST'])
def name():
    """directs to user form"""
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data 
        form.name.data = ''
        flash("Form succesfully submitted!!")
    return render_template("name.html", name = name, form = form)

@app.route('/user/<name>')
def user(name):
    """directs to user page"""
    return render_template("user.html", name=name)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added!!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)

# Invalid URL page
@app.errorhandler(404)
def invalid_url(e):
    """handles error case for when user goes to a non-existent page"""
    return render_template("404.html"), 404

# Server error
@app.errorhandler(500)
def server_err(e):
    """handles error case for when server errors occur"""
    return render_template("500.html"), 500

