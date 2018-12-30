# coding = utf-8
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length


class MessageForm(FlaskForm):
    body = TextAreaField('留言',validators=[Length(min=1,max=2000)])
    submit_message = SubmitField('提交')