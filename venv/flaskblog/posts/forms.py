from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
     """
     PostForm is a FlaskForm that represents a form for creating or editing a blog post.

     Attributes:
          title (StringField): A text input field for the post title. It is required.
          content (TextAreaField): A text area input field for the post content. It is required.
          submit (SubmitField): A button to submit the form.
     """
     title = StringField('Title', validators=[DataRequired()])
     content = TextAreaField('Content', validators=[DataRequired()])
     submit = SubmitField('Post')

