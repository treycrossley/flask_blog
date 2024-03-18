from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from app.models import Users, Posts
from app.forms import SearchForm
from app.extensions import login_manager

general_bp = Blueprint(
    "general", __name__, url_prefix="/", template_folder="../../templates"
)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@general_bp.route("/")
def index():
    """Directs to home page"""
    return redirect(url_for("posts.posts"))


@general_bp.route("/about")
def about():
    """Directs to home page"""
    return render_template("about.html")


@general_bp.route("/home")
def home():
    return redirect(url_for("posts.posts"))


@general_bp.route("/admin")
@login_required
def admin():
    our_users = Users.query.order_by(Users.date_added.desc())
    """Directs to admin page"""
    if current_user.is_admin:
        return render_template("admin.html", our_users=our_users)
    else:
        flash("You do not have admin privileges")
        return redirect(url_for("general.dashboard"))


@general_bp.app_context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@general_bp.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        searched = form.searched.data
        search_regex = "%" + searched + "%"
        posts = posts.filter(
            Posts.content.like(search_regex), Posts.title.like(search_regex)
        )
        posts = posts.order_by(Posts.title).all()
        return render_template("search.html", form=form, searched=searched, posts=posts)


@general_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")
