import os
import secrets
from PIL import Image
from flask import url_for,current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    # Generate a random hex for the new picture filename
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  # Extract the file extension
    picture_fn = random_hex + f_ext  # Combine random hex and file extension
    # Define the path to save the picture
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)  # Resize image to 125x125 pixels
    i = Image.open(form_picture)  # Open the uploaded image
    i.thumbnail(output_size)  # Resize the image
    i.save(picture_path)  # Save the resized image to the defined path

    return picture_fn  # Return the filename of the saved picture


def send_reset_email(user):
    token = user.get_reset_token()  # Generate a password reset token for the user
    # Create a password reset email message
    msg = Message('Password Reset Request',
                   sender='habibseye49@gmail.com',
                   recipients=[user.email]  )
    # Email body with a link to reset the password
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made. 
'''
    mail.send(msg)  # Send the email