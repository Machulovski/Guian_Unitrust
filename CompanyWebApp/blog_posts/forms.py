#blog_posts/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    text = TextAreaField('博客内容', validators=[DataRequired()])
    submit = SubmitField('提交')