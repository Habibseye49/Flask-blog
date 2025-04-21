from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer
from flask import current_app 
from flaskblog import db, login_manager
from flask_login import UserMixin

# Function to load a user by their ID for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model representing a user in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    username = db.Column(db.String(20), unique=True, nullable=False)  # Username must be unique
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email must be unique
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')  # Profile image
    password = db.Column(db.String(60), nullable=False)  # Hashed password
    posts = db.relationship('Post', backref='author',  lazy=True)  # Relationship to the Post model

    # Generate a password reset token with an expiration time
    def get_reset_token(self, expires_sec = 1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}, salt='reset-password-salt')
    
    # Verify the password reset token
    @staticmethod
    def verify_reset_token(token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='reset-password-salt')['user_id']
        except:
            return None
        return User.query.get(user_id)

    # String representation of the User object
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}' )"
    
# Post model representing a blog post in the database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the post
    title = db.Column(db.String(100), nullable=False)  # Title of the post
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)  # Date the post was created
    content = db.Column(db.Text, nullable=False)  # Content of the post
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)  # Foreign key linking to the User model

    # String representation of the Post object
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"