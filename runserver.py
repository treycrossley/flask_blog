"""For flask library and template rendering for our web app"""

from flask_login import login_required, login_user, logout_user
from app import create_app
from flask import render_template, redirect, url_for, flash
from app.extensions import login_manager, bcrypt
from app.models import Users
from app.forms import LoginForm

errorLocation = "app/templates/errors/"

# Create Flask instance
app = create_app()

# Invalid URL page
@app.errorhandler(404)
def invalid_url(e):
    """handles error case for when user goes to a non-existent page"""
    return render_template("404.html"), 404

# Server error
@app.errorhandler(500)
def server_err(e):
    """handles error case for when server errors occur"""
    return render_template("{}500.html".format(errorLocation)), 500


if __name__ == "__main__":
    app.run(debug=True)


