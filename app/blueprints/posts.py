"""
Posts Blueprint

This blueprint handles routes related to posts, including creating, editing,
deleting, and viewing posts. It also provides functionality for searching
posts and displaying individual posts.

Routes:
    - /posts: Renders the list of posts.
    - /posts/<int:id>: Renders the details of a specific post.
    - /submit_post: Handles the submission of a new post.
    - /edit_post/<int:id>: Handles the editing of an existing post.
    - /delete_post/<int:id>: Handles the deletion of an existing post.
    - /search: Handles searching for posts based on keywords.

Attributes:
    - posts_bp: Blueprint object representing the posts blueprint.
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import exc
from ..models import Posts
from ..forms import PostForm
from ..extensions import db

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
    post_list = Posts.query.order_by(Posts.date_posted.desc())
    print(post_list)
    return render_template("posts/posts.html", posts=post_list)


@posts_bp.route("/myposts")
@login_required
def my_posts():
    """
    Renders the page displaying posts created by the current user.

    Returns:
        str: The rendered HTML page displaying posts created by the current user.
    """
    post_list = (
        Posts.query.filter_by(poster_id=current_user.id)
        .order_by(Posts.date_posted.desc())
        .all()
    )
    return render_template("posts/posts.html", posts=post_list)


@posts_bp.route("/<int:post_id>")
def post(post_id):
    """
    Renders the page displaying a single post.

    Args:
        id (int): The ID of the post to display.

    Returns:
        str: The rendered HTML page displaying the specified post.
    """
    post_single = Posts.query.get_or_404(post_id)
    return render_template("posts/post.html", post=post_single)


@posts_bp.route("/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    """
    Allows users to edit a post.

    Args:
        id (int): The ID of the post to edit.

    Returns:
        Response: Redirects the user to the post page after editing or back to the edit
        post page if there was an error.
    """
    post_to_edit = Posts.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post_to_edit.title = form.title.data
        post_to_edit.slug = form.slug.data
        post_to_edit.content = form.content.data

        try:
            db.session.add(post_to_edit)
            db.session.commit()
            flash("Post has been updated")
        except exc.SQLAlchemyError:
            flash("DB could not update post. try again")
        return redirect(url_for("posts.post", post_id=post_to_edit.id))

    if current_user.id == post_to_edit.poster_id or current_user.is_admin:
        form.title.data = post_to_edit.title
        form.slug.data = post_to_edit.slug
        form.content.data = post_to_edit.content
        return render_template("posts/edit_post.html", form=form, post_id=post_id)
    flash("You are not authorized to edit this post")
    post_list = Posts.query.order_by(Posts.date_posted.desc())
    return redirect(url_for("posts/posts.html", posts=post_list))


@posts_bp.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    """
    Allows users to delete a post.

    Args:
        id (int): The ID of the post to delete.

    Returns:
        Response: Redirects the user to the posts page after deletion.
    """
    post_to_delete = Posts.query.get_or_404(post_id)
    if current_user.id == post_to_delete.poster.id or current_user.is_admin:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Post deleted!!")
        except exc.SQLAlchemyError:
            flash("Post deletion unsuccesful. Please try again!")

    else:
        flash("You can't delete this post")
    post_list = Posts.query.order_by(Posts.date_posted.desc())
    return redirect(url_for("posts.posts", posts=post_list))


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
        post_to_add = Posts(
            title=form.title.data,
            content=form.content.data,
            poster_id=poster,
            slug=form.slug.data,
        )
        form.title.data = ""
        form.content.data = ""
        form.slug.data = ""
        try:
            db.session.add(post_to_add)
            db.session.commit()

            flash("Post succesfully submitted!")
        except exc.SQLAlchemyError:
            flash("Something went wrong!")
            return render_template("posts/add_post.html", form=form)
        return redirect(url_for("posts.post", post_id=post_to_add.id))
    return render_template("posts/add_post.html", form=form)
