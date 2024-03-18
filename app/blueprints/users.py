"""
Users Blueprint

This blueprint handles routes related to users, including user registration,
login, logout, and user administration. It also provides functionality for
viewing and managing user profiles.

Routes:
    - /auth/register: Renders the user registration form and handles user registration.
    - /auth/login: Renders the login form and handles user login.
    - /auth/logout: Handles user logout.
    - /users: Renders the list of users.
    - /users/<int:id>: Renders the details of a specific user.
    - /edit_user/<int:id>: Handles the editing of user profile information.
    - /delete_user/<int:id>: Handles the deletion of a user account.
    - /profile: Renders the user profile page.

Attributes:
    - auth_bp: Blueprint object representing the authentication-related routes.
    - users_bp: Blueprint object representing the users blueprint.

Functions:
    - load_user: Load a user by its ID.
"""

import uuid
import os
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    current_app,
    redirect,
    url_for,
)
from flask_login import current_user, login_required, login_user
from werkzeug.utils import secure_filename
from sqlalchemy import exc
from ..models import Users
from ..forms import UserForm
from ..extensions import db, bcrypt


users_bp = Blueprint(
    "users", __name__, url_prefix="/users", template_folder="../../templates"
)


@users_bp.route("/update/<int:user_id>", methods=["GET", "POST"])
@login_required
def update(user_id):
    """
    Allows users to update their profile information.

    Args:
        id (int): The ID of the user to update.

    Returns:
        Response: Redirects the user to the dashboard page after updating their profile
        information or renders the update page with an error message if the update
        fails.
    """
    form = UserForm()
    name_to_update = Users.query.get_or_404(user_id)
    if request.method == "POST":
        name_to_update.name = request.form["name"]
        name_to_update.email = request.form["email"]
        name_to_update.favorite_pizza_place = request.form["favorite_pizza_place"]
        name_to_update.username = request.form["username"]
        name_to_update.profile_pic = request.files["profile_pic"]

        if request.files["profile_pic"]:
            name_to_update.profile_pic = request.files["profile_pic"]

            # Grab Image Name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            # Save That Image
            saver = request.files["profile_pic"]

            # Change it to a string to save to db
            name_to_update.profile_pic = pic_name

            try:
                db.session.commit()
                saver.save(os.path.join(current_app.config["UPLOAD_FOLDER"], pic_name))
                flash("User Updated Successfully!")
                return render_template("dashboard.html")
            except exc.SQLAlchemyError:
                flash("ERROR! TRY AGAIN!")
                return render_template(
                    "users/update.html", form=form, name_to_update=name_to_update
                )
        else:
            try:
                name_to_update.profile_pic = None
                db.session.commit()
                flash("User updated!!")
                return render_template("dashboard.html")
            except exc.SQLAlchemyError:
                flash("ERROR! TRY AGAIN!")
                return render_template(
                    "users/update.html", form=form, name_to_update=name_to_update
                )
    else:
        return render_template(
            "users/update.html", form=form, name_to_update=name_to_update, id=user_id
        )


@users_bp.route("/delete/<int:user_id>")
@login_required
def delete(user_id):
    """
    Allows users to delete their account.

    Args:
        id (int): The ID of the user to delete.

    Returns:
        Response: Redirects the user to the add user page after deletion.
    """
    if user_id == current_user.id or current_user.is_admin:
        user_to_delete = Users.query.get_or_404(user_id)
        name = None
        form = UserForm()
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("USER DELETED")
            our_users = Users.query.order_by(Users.date_added.desc())
            return render_template(
                "add_user.html", form=form, name=name, our_users=our_users
            )
        except exc.SQLAlchemyError:
            flash("OOPSIES. SOMETHING WENT WRONG")
            return render_template(
                "users/add_user.html", form=form, name=name, our_users=our_users
            )
    else:
        flash("You don't have permission to delete this user")
        return redirect(url_for("general.dashboard"))


@users_bp.route("/<name>")
def user(name):
    """Directs to user page."""
    return render_template("users/user.html", name=name)


@users_bp.route("adminify/<int:user_id>/<int:set_admin>")
@login_required
def alter_admin(user_id, set_admin=True):
    """
    Allows admin users to grant or revoke admin privileges to other users.

    Args:
        id (int): The ID of the user to modify admin privileges.
        setAdmin (bool, optional): Indicates whether to set the user as admin or not.
            Defaults to True.

    Returns:
        Response: Redirects the user to the admin page.
    """
    if not current_user.is_admin:
        flash("You don't have permission to alter admin access to this user")
        return redirect(url_for("general.dashboard"))

    user_to_alter = Users.query.get_or_404(user_id)
    if not user_to_alter:
        flash("User does not exist in DB")
        return redirect(url_for("general.dashboard"))
    if user_to_alter.is_admin and set_admin:
        flash("User is already admin")
        return redirect(url_for("general.admin"))
    if not user_to_alter.is_admin and not set_admin:
        flash("User already is not an admin")
        return redirect(url_for("general.admin"))
    try:
        user_to_alter.is_admin = set_admin
        db.session.commit()
        flash("User admin privileges have been updated!")
    except exc.SQLAlchemyError:
        flash("Something went wrong! Sorry!")
    return redirect(url_for("general.admin"))


@users_bp.route("/add", methods=["GET", "POST"])
def add_user():
    """View function for adding a new user.

    Handles both GET and POST requests. If the request method is POST and the form is
    validated successfully, a new user is created and added to the database. If the
    email provided in the form is not already associated with an existing user, the
    user is added. Otherwise, an appropriate flash message is displayed.

    Returns:
        A rendered template for the "add_user.html" page with the user form, name,
        and a list of all users sorted by date added.

    """
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user_to_add = Users.query.filter_by(email=form.email.data).first()
        if user_to_add is None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            user_to_add = Users(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                favorite_pizza_place=form.favorite_pizza_place.data,
                password_hash=hashed_password,
            )
            try:
                db.session.add(user_to_add)
                db.session.commit()
                flash("User added!!")
                if current_user is None:
                    login_user(user_to_add)
            except exc.SQLAlchemyError:
                flash("Something went wrong")
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.favorite_pizza_place.data = ""
        form.password.data = ""
        form.username.data = ""
    our_users = Users.query.order_by(Users.date_added.desc())
    return render_template(
        "users/add_user.html", form=form, name=name, our_users=our_users
    )
