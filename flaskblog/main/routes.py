from flask import render_template, request, Blueprint  # Import necessary modules from Flask
from flaskblog.models import Post  # Import the Post model from flaskblog.models

main = Blueprint('main', __name__)  # Create a Blueprint for the main routes

@main.route("/")
@main.route("/home")
def home():
    # Get the current page number from the request arguments, default to 1
    page = request.args.get('page', 1, type=int)
    # Query posts from the database, order by date posted in descending order, and paginate
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # Render the home.html template with the posts
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    # Render the about.html template with a title
    return render_template('about.html', title='About')
