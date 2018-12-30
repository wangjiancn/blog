from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    body = TextAreaField('评论', validators=[DataRequired()])
    submit_comment = SubmitField('提交评论')
