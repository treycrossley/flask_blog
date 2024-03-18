from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models import Posts
from app.forms import PostForm
from app.extensions import db

posts_bp = Blueprint(
    "posts", __name__, url_prefix="/posts", template_folder="../../templates"
)


@posts_bp.route("/")
def posts():
    """
    Renders the page displaying all posts.

    Returns:
        str: The rendered HTML page displaying all posts.
    """
    posts = Posts.query.order_by(Posts.date_posted.desc())
    return render_template("posts/posts.html", posts=posts)


@posts_bp.route("/myposts")
@login_required
def my_posts():
    """
    Renders the page displaying posts created by the current user.

    Returns:
        str: The rendered HTML page displaying posts created by the current user.
    """
    posts = (
        Posts.query.filter_by(poster_id=current_user.id)
        .order_by(Posts.date_posted.desc())
        .all()
    )
    return render_template("posts/posts.html", posts=posts)


@posts_bp.route("/<int:id>")
def post(id):
    """
    Renders the page displaying a single post.

    Args:
        id (int): The ID of the post to display.

    Returns:
        str: The rendered HTML page displaying the specified post.
    """
    post = Posts.query.get_or_404(id)
    return render_template("posts/post.html", post=post)


@posts_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    """
    Allows users to edit a post.

    Args:
        id (int): The ID of the post to edit.

    Returns:
        Response: Redirects the user to the post page after editing or back to the edit
        post page if there was an error.
    """
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data

        try:
            db.session.add(post)
            db.session.commit()
            flash("Post has been updated")
        except Exception:
            flash("DB could not update post. try again")
        return redirect(url_for("posts.post", id=post.id))

    if current_user.id == post.poster_id or current_user.is_admin:
        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template("posts/edit_post.html", form=form, post_id=id)
    flash("You are not authorized to edit this post")
    posts = Posts.query.order_by(Posts.date_posted.desc())
    return redirect(url_for("posts/posts.html", posts=posts))


@posts_bp.route("/delete/<int:id>")
@login_required
def delete_post(id):
    """
    Allows users to delete a post.

    Args:
        id (int): The ID of the post to delete.

    Returns:
        Response: Redirects the user to the posts page after deletion.
    """
    post_to_delete = Posts.query.get_or_404(id)
    if current_user.id == post_to_delete.poster.id or current_user.is_admin:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post deleted!!")
        except Exception:
            flash("Post deletion unsuccesful. Please try again!")

    else:
        flash("You can't delete this post")
    posts = Posts.query.order_by(Posts.date_posted.desc())
    return redirect(url_for("posts/posts.html", posts=posts))


@posts_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_post():
    """
    Allows users to add a new post.

    Returns:
        Response: Redirects the user to the posts page after adding the post or back to
        the add post page if there was an error.
    """
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(
            title=form.title.data,
            content=form.content.data,
            poster_id=poster,
            slug=form.slug.data,
        )
        form.title.data = ""
        form.content.data = ""
        form.slug.data = ""
        try:
            db.session.add(post)
            db.session.commit()

            flash("Post succesfully submitted!")
        except Exception:
            flash("Something went wrong!")
            return render_template("posts/add_post.html", form=form)
        return redirect(url_for("posts.post", id=post.id))
    return render_template("posts/add_post.html", form=form)
