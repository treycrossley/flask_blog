"""
Module level docstring describing the authentication blueprint.

This blueprint handles user authentication including login and logout routes.

Attributes:
    auth_bp (Blueprint): Blueprint object for authentication routes.

"""

from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.models import Users
from app.forms import LoginForm
from app.extensions import bcrypt


# Create a Blueprint for authentication-related routes
auth_bp = Blueprint(
    "auth", __name__, url_prefix="/auth", template_folder="../../templates"
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Route for user login.

    Renders the login form for GET requests and processes
    login attempts for POST requests.

    """
    form = LoginForm()

    if form.validate_on_submit():
        # Attempt to retrieve the user from the database
        user = Users.query.filter_by(username=form.username.data).first()

        if user:
            # Check if the provided password matches the stored hash
            if bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login successful!")

                # Redirect to the appropriate page based on user role
                if current_user.is_admin:
                    return redirect(url_for("general.admin"))
                else:
                    return redirect(url_for("general.home"))
            else:
                flash("Wrong Password - Try again!")
        else:
            flash("User does not exist")

    return render_template("login.html", form=form)


@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Route for user logout.

    Logs out the current user and redirects to the login page.

    """
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("auth.login"))
