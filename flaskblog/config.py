import os

class Config:
    """
    Config class for Flask application settings.

    Attributes:
        SECRET_KEY (str): A secret key used for session management and security. 
                          Defaults to 'default_secret_key' if not set in environment variables.
        SQLALCHEMY_DATABASE_URI (str): Database URI for SQLAlchemy. 
                                       Defaults to 'sqlite:///site.db' if not set in environment variables.
        MAIL_SERVER (str): SMTP server address for sending emails.
        MAIL_PORT (int): Port number for the SMTP server.
        MAIL_USERNAME (str): Username for the SMTP server authentication.
        MAIL_PASSWORD (str): Password for the SMTP server authentication.
        MAIL_USE_TLS (bool): Enables Transport Layer Security (TLS) for email communication.
        MAIL_USE_SSL (bool): Enables Secure Sockets Layer (SSL) for email communication.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key'
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI =  SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///site.db'
    MAIL_SERVER='sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '2eeb55aa8cf259'
    MAIL_PASSWORD = '02c8aa02c02800'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False 