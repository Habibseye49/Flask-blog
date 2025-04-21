import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config  # Importing configuration settings

# Initializing extensions
db = SQLAlchemy()  # Database instance
bcrypt = Bcrypt()  # Password hashing
login_manager = LoginManager()  # Login management
login_manager.login_view = 'users.login'  # Redirect to 'users.login' for unauthorized access
login_manager.login_message_category = 'info'  # Flash message category for login messages

mail = Mail()  # Email handling

def create_app(config_class=Config):
    app = Flask(__name__)  # Create Flask application instance
    app.config.from_object(Config)  # Load configuration from Config class

    # Initialize extensions with the app instance
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Import and register blueprints
    from flaskblog.users.routes import users  # User-related routes
    from flaskblog.posts.routes import posts  # Post-related routes
    from flaskblog.main.routes import main  # Main application routes
    from flaskblog.errors.handlers import errors  # Error handling routes

    app.register_blueprint(users)  # Register 'users' blueprint
    app.register_blueprint(posts)  # Register 'posts' blueprint
    app.register_blueprint(main)  # Register 'main' blueprint
    app.register_blueprint(errors)  # Register 'errors' blueprint

    return app  # Return the Flask application instance
