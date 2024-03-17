from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import Posts
from app.forms import PostForm
from app.extensions import db

posts_bp = Blueprint("posts", __name__, url_prefix='/posts', template_folder="../../templates")


@posts_bp.route('/')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    print(posts)
    return render_template("posts/posts.html", posts=posts)

@posts_bp.route('/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('posts/post.html', post=post) 

@posts_bp.route('/edit/<int:id>', methods=['GET','POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        db.session.add(post)
        db.session.commit()
        flash('Post has been updated')

        return redirect(url_for('posts.post', id=post.id))
    form.title.data=post.title
    form.author.data=post.author
    form.slug.data=post.slug
    form.content.data=post.content
    return render_template('posts/edit_post.html',form=form, post_id = id)

@posts_bp.route('/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Post deleted!!')
    except Exception:
        flash("Post deletion unsuccesful. Please try again!")
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts/posts.html", posts=posts)
    

@posts_bp.route('/add', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''

        db.session.add(post)
        db.session.commit()

        flash("Post succesfully submitted!")
    return render_template('posts/add_post.html', form=form)


