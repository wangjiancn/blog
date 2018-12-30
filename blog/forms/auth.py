# coding = utf-8

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Length, DataRequired, equal_to, EqualTo, ValidationError

from blog.models.user import User


class LoginForm(FlaskForm):
    username = StringField('账号', validators=[Length(min=1, max=2000)])
    password = PasswordField('密码', validators=[Length(min=1, max=2000)])
    remember = BooleanField('记住密码',default=False)
    submit_login = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired(), Length(min=1, max=20), ])
    email = EmailField('电子邮箱', validators=[DataRequired()])
    password1 = PasswordField('密码', validators=[DataRequired(), Length(min=1, max=20)])
    password2 = PasswordField('确认密码', validators=[DataRequired(), Length(min=1, max=20),
                EqualTo('password1', message='两次密码不同，请确认后输入')])
    submit_register = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')
