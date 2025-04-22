from flaskblog import create_app  # Import the create_app function from the flaskblog package
from flask_migrate import upgrade

app = create_app()  # Create an instance of the Flask application using the factory function

with app.app_context():
    upgrade()
    
if __name__ == '__main__':  # Ensure the app runs only when this script is executed directly
     app.run(debug=True)  # Run the Flask application in debug mode
