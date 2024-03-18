"""Main entry point for running the Flask web application."""

from flask import render_template
from app import create_app

# Create Flask instance
app = create_app("dev")


# Invalid URL page
@app.errorhandler(404)
def invalid_url(error):
    """Handle error for when user goes to a non-existent page."""
    print(error)
    return render_template("404.html"), 404


# Server error
@app.errorhandler(500)
def server_err(error):
    """Handle error for when server errors occur."""
    print(error)
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
