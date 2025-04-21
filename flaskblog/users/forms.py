from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

# Form for user registration
class RegistrationForm(FlaskForm):
    # Username field with validation for required input and length constraints
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # Email field with validation for required input and valid email format
    email = StringField('Email',validators=[DataRequired(), Email()]) 
    # Password field with validation for required input
    password = PasswordField('Password', validators=[DataRequired()])
    # Confirm password field with validation to match the password field
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Submit button
    submit = SubmitField('Sign Up')

    # Custom validation to check if the username is already taken
    def validate_username(self, username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please Choose a different one.')

    # Custom validation to check if the email is already taken
    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken. Please Choose a different one.')

# Form for user login
class LoginForm(FlaskForm):
    # Email field with validation for required input and valid email format
    email = StringField('Email',validators=[DataRequired(), Email()]) 
    # Password field with validation for required input
    password = PasswordField('Password', validators=[DataRequired()])
    # Remember me checkbox
    remember = BooleanField('Remember Me')
    # Submit button
    submit = SubmitField('Login')

# Form for updating user account details
class UpdateAccountForm(FlaskForm):
    # Username field with validation for required input and length constraints
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # Email field with validation for required input and valid email format
    email = StringField('Email',validators=[DataRequired(), Email()]) 
    # File field for updating profile picture with allowed file extensions
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    # Submit button
    submit = SubmitField('Update')

    # Custom validation to check if the username is already taken (excluding current user's username)
    def validate_username(self, username):
        if username.data != current_user.username:   
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken. Please Choose a different one.')

    # Custom validation to check if the email is already taken (excluding current user's email)
    def validate_email(self, email):
        if email.data != current_user.email:      
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken. Please Choose a different one.')

# Form for requesting a password reset
class RequestResetForm(FlaskForm):
     # Email field with validation for required input and valid email format
     email =  StringField('Email', validators=[DataRequired(), Email()])
     # Submit button
     submit = SubmitField('Request Password Reset')

     # Custom validation to check if the email exists in the database
     def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user is None:
                 raise ValidationError('There is no account with that email. You must register first.')

# Form for resetting the password
class ResetPasswordForm(FlaskForm):
     # Password field with validation for required input
     password = PasswordField('Password', validators=[DataRequired()])
     # Confirm password field with validation to match the password field
     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
     # Submit button
     submit = SubmitField('Reset Password')
