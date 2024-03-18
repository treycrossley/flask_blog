"""
Blueprint for general routes and views.

This module defines routes and views for general pages such as home, about, and admin pages.

Attributes:
    general_bp (Blueprint): Blueprint object for general routes.
"""

from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_
from ..models import Users, Posts
from ..forms import SearchForm
from ..extensions import login_manager
import pdb

general_bp = Blueprint(
    "general", __name__, url_prefix="/", template_folder="../../templates"
)


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user by its ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        User: The user corresponding to the given ID.
    """
    return Users.query.get(int(user_id))


@general_bp.route("/")
def index():
    """Directs to the home page."""
    return redirect(url_for("posts.posts"))


@general_bp.route("/about")
def about():
    """Directs to the about page."""
    return render_template("about.html")


@general_bp.route("/home")
def home():
    """Directs to the home page."""
    return redirect(url_for("posts.posts"))


@general_bp.route("/admin")
@login_required
def admin():
    """
    Directs to the admin page if the current user is an admin.

    Returns:
        Response: The admin page template if the user is an admin, otherwise redirects
        to the dashboard.
    """
    our_users = Users.query.order_by(Users.date_added.desc())
    if current_user.is_admin:
        return render_template("admin.html", our_users=our_users)
    flash("You do not have admin privileges")
    return redirect(url_for("general.dashboard"))


@general_bp.app_context_processor
def base():
    """
    Injects the search form into the context of all templates in the blueprint.

    Returns:
        dict: A dictionary containing the search form.
    """
    form = SearchForm()

    return {"form": form}


@general_bp.route("/search", methods=["POST"])
def search():
    """
    Handles searching for posts.

    Returns:
        Response: The search results page template.
    """
    form = SearchForm()
    posts = Posts.query.order_by(Posts.date_posted.desc())
    if form.validate_on_submit():
        searched = form.searched.data
        search_regex = "%" + searched + "%"
        posts = posts.filter(
            or_(Posts.content.like(search_regex), Posts.title.like(search_regex))
        )
        posts = posts.order_by(Posts.title).all()
    return render_template("search.html", form=form, searched=searched, posts=posts)


@general_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """
    Directs to the dashboard page.

    Returns:
        Response: The dashboard page template.
    """
    return render_template("dashboard.html")
