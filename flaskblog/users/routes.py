from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)  # Create a Blueprint for user-related routes


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # Redirect authenticated users to the home page
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():  # Check if the registration form is valid
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash the password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # Create a new user
        db.session.add(user)  # Add the user to the database
        db.session.commit()  # Commit the changes to the database
        flash(f'Your account has been created! You are now able to log in', 'success')  # Show success message
        return redirect(url_for('users.login'))  # Redirect to the login page
    return render_template('register.html', title='Register', form=form)  # Render the registration page


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # Redirect authenticated users to the home page
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():  # Check if the login form is valid
        user = User.query.filter_by(email=form.email.data).first()  # Find the user by email
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # Verify the password
            login_user(user, remember=form.remember.data)  # Log in the user
            next_page = request.args.get('next')  # Redirect to the next page if specified
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')  # Show error message
    return render_template('login.html', title='Login', form=form)  # Render the login page


@users.route("/logout")
def logout():
    logout_user()  # Log out the current user
    return redirect(url_for('main.home'))  # Redirect to the home page


@users.route("/account", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to access this route
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():  # Check if the account update form is valid
        if form.picture.data:  # Check if a new profile picture is uploaded
            picture_file = save_picture(form.picture.data)  # Save the new profile picture
            current_user.image_file = picture_file  # Update the user's profile picture
        current_user.username = form.username.data  # Update the username
        current_user.email = form.email.data  # Update the email
        db.session.commit()  # Commit the changes to the database
        flash('Your account has been updated!', 'success')  # Show success message
        return redirect(url_for('users.account'))  # Redirect to the account page
    elif request.method == 'GET':  # Pre-fill the form with current user data
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # Get the profile picture URL
    return render_template('account.html', title='Account', image_file=image_file, form=form)  # Render the account page


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # Get the current page number
    user = User.query.filter_by(username=username).first_or_404()  # Find the user or return 404
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)  # Paginate the posts
    return render_template('user_posts.html', posts=posts, user=user)  # Render the user's posts page


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:  # Redirect authenticated users to the home page
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():  # Check if the reset request form is valid
        user = User.query.filter_by(email=form.email.data).first()  # Find the user by email
        send_reset_email(user)  # Send the password reset email
        flash('An email has been sent with instructions to reset your password', 'info')  # Show info message
        return redirect(url_for('users.login'))  # Redirect to the login page
    return render_template('reset_request.html', title='Reset Password', form=form)  # Render the reset request page


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:  # Redirect authenticated users to the home page
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)  # Verify the reset token
    if user is None:  # Check if the token is invalid or expired
        flash('That is an invalid or expired token', 'warning')  # Show warning message
        return redirect(url_for('users.reset_request'))  # Redirect to the reset request page
    form = ResetPasswordForm()
    if form.validate_on_submit():  # Check if the reset password form is valid
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash the new password
        user.password = hashed_password  # Update the user's password
        db.session.commit()  # Commit the changes to the database
        flash(f'Your password has been updated! You are now able to log in', 'success')  # Show success message
        return redirect(url_for('users.login'))  # Redirect to the login page
    return render_template('reset_token.html', title='Reset Password', form=form)  # Render the reset token page