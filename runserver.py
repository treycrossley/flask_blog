"""For flask library and template rendering for our web app"""
from app import create_app
from flask import render_template
from app.extensions import db,bcrypt
from datetime import datetime,timezone
from flask_login import UserMixin


# Create Flask instance
app = create_app('dev')

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

if __name__ == "__main__":
    app.run(debug=True)


