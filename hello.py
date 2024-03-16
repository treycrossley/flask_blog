"""For flask library and template rendering for our web app"""
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create Flask instance
app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"

# Form Class
class NamerForm(FlaskForm):
    """class for asking user their name"""
    name = StringField("What's your name", validators=[DataRequired()])
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

