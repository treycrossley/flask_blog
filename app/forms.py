from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    """class for asking user their name"""
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    """class for asking user their name"""
    email = StringField("What's your email", validators=[DataRequired()])
    pw = PasswordField("What's your password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    favorite_pizza_place = StringField("Favorite Pizza Place")
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match!')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")