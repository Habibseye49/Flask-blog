from flask import Blueprint, render_template

# Create a Blueprint for error handling
errors = Blueprint('errors', __name__)

# Handle 404 (Not Found) errors
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

# Handle 403 (Forbidden) errors
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

# Handle 500 (Internal Server Error) errors
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500