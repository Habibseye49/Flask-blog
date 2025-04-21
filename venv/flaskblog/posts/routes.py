from flask import(render_template, url_for, flash, 
                  redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

# Create a Blueprint for posts
posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    # Form to create a new post
    form = PostForm()
    if form.validate_on_submit():
        # Create a new post and save it to the database
        post = Post(title = form.title.data, content = form.content.data, author =  current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend = 'New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    # Retrieve a specific post by its ID
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',  title=post.title,  post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # Retrieve the post to be updated
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        # Abort if the current user is not the author
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        # Update the post's title and content
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        # Pre-fill the form with the current post data
        form.title.data = post.title
        form.content.data = post.title
    return render_template('create_post.html', title='Update Post', form=form,
                           legend = 'Update Post')

@posts.route("/post/<int:post_id>/delete", methods=[ 'POST'])
@login_required
def delete_post(post_id):
     # Retrieve the post to be deleted
     post = Post.query.get_or_404(post_id)
     if post.author != current_user:
        # Abort if the current user is not the author
        abort(403)
     # Delete the post from the database
     db.session.delete(post)
     db.session.commit()
     flash('Your post has been deleted!', 'success')
     return redirect(url_for('main.home'))
