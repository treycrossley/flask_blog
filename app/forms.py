from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField


class LoginForm(FlaskForm):
    """Form for user login"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    """Form for creating or editing a post"""

    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    """Form for searching"""

    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NamerForm(FlaskForm):
    """Form for asking user's name"""

    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    """Form for asking user's email and password"""

    email = StringField("What's your email", validators=[DataRequired()])
    pw = PasswordField("What's your password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    """Form for creating or editing a user"""

    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    favorite_pizza_place = StringField("Favorite Pizza Place")
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords must match!"),
        ],
    )
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")
    submit = SubmitField("Submit")
