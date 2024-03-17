from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for
from flask_login import current_user, login_required
from app.models import Users
from app.forms import UserForm
from app.extensions import db, bcrypt
from werkzeug.utils import secure_filename
import uuid as uuid
import os

users_bp = Blueprint("users", __name__, url_prefix='/users', template_folder="../../templates")


@users_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_pizza_place = request.form['favorite_pizza_place']
        name_to_update.username = request.form['username']
        name_to_update.profile_pic = request.files['profile_pic']
        
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']

			# Grab Image Name
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
			# Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
			# Save That Image
            saver = request.files['profile_pic']
			

			# Change it to a string to save to db
            name_to_update.profile_pic = pic_name

            try:
                db.session.commit()
                saver.save(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfully!")
                return render_template("dashboard.html")
            except BaseException:
                flash("ERROR! TRY AGAIN!")
                return render_template('users/update.html', form=form, name_to_update=name_to_update)
        else:
            try:
                name_to_update.profile_pic = None
                db.session.commit()
                flash("User updated!!")
                return render_template('dashboard.html')
            except BaseException:
                flash("ERROR! TRY AGAIN!")
                return render_template('users/update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('users/update.html', form=form, name_to_update=name_to_update,id=id)

@users_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if id == current_user.id or current_user.is_admin:
        user_to_delete = Users.query.get_or_404(id)
        name = None
        form = UserForm()
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("USER DELETED")
            our_users = Users.query.order_by(Users.date_added)
            return render_template('add_user.html', form=form, name=name, our_users=our_users)
        except BaseException:
            flash("OOPSIES. SOMETHING WENT WRONG")
            return render_template('users/add_user.html', form=form, name=name, our_users=our_users)
    else:
            flash("You don't have permission to delete this user")
            return redirect(url_for('general.dashboard'))

@users_bp.route('/<name>')
def user(name):
    """directs to user page"""
    return render_template("users/user.html", name=name)

@users_bp.route('adminify/<int:id>/<int:setAdmin>')
@login_required
def alter_admin(id, setAdmin=True):
    if not current_user.is_admin:
        flash("You don't have permission to alter admin access to this user")
        return redirect(url_for('general.dashboard'))
    
    user = Users.query.get_or_404(id)
    if not user:
        flash("User does not exist in DB")
        return redirect(url_for('general.dashboard'))
    if user.is_admin and setAdmin:
        flash("User is already admin")
        return redirect(url_for('general.admin'))
    if not user.is_admin and not setAdmin:
        flash("User already is not an admin")
        return redirect(url_for('general.admin'))
    try:
        user.is_admin = setAdmin
        db.session.commit()
        flash("User admin privileges have been updated!")
    except Exception:
        flash("Something went wrong! Sorry!")
    return redirect(url_for('general.admin'))



@users_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = Users(name=form.name.data, username=form.username.data, email=form.email.data, favorite_pizza_place=form.favorite_pizza_place.data, password_hash = hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_pizza_place.data=''
        form.password.data = ''
        form.username.data=''
        flash("User added!!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template('users/add_user.html', form=form, name=name, our_users=our_users)

