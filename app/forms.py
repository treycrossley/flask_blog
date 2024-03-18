"""
Module for defining Flask forms used in the application.

This module defines various FlaskForm classes for different purposes, such as user login,
post creation/editing, searching, user information gathering, and user registration.

Classes:
    - LoginForm: Form for user login.
    - PostForm: Form for creating or editing a post.
    - SearchForm: Form for searching.
    - NamerForm: Form for asking user's name.
    - PasswordForm: Form for asking user's email and password.
    - UserForm: Form for creating or editing a user.

Packages:
    - FlaskForm: Base class for forms in Flask-WTF.
    - StringField: Field for string input.
    - SubmitField: Field for submit button.
    - PasswordField: Field for password input.
    - CKEditorField: Field for CKEditor input.
    - FileField: Field for file input.
    - DataRequired: Validator to ensure data is provided.
    - Email: Validator to ensure data is a valid email address.
    - EqualTo: Validator to ensure data is equal to another field.

"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_ckeditor import CKEditorField


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
