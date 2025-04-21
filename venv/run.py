from flaskblog import create_app  # Import the create_app function from the flaskblog package

app = create_app()  # Create an instance of the Flask application using the factory function

if __name__ == '__main__':  # Ensure the app runs only when this script is executed directly
     app.run(debug=True)  # Run the Flask application in debug mode
