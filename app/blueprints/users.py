from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from app.models import Users
from app.forms import UserForm
from app.extensions import db, bcrypt

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
        try:
            db.session.commit()
            flash("User updated!!")
            return render_template('users/update.html', form=form, name_to_update=name_to_update)
        except BaseException:
            flash("ERROR! TRY AGAIN!")
            return render_template('users/update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('users/update.html', form=form, name_to_update=name_to_update,id=id)

@users_bp.route('/delete/<int:id>')
@login_required
def delete(id):
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

@users_bp.route('/<name>')
def user(name):
    """directs to user page"""
    return render_template("users/user.html", name=name)

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

