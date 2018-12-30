# coding = utf-8

from flask_login import LoginManager
from flask_mail import Mail
from flask_ckeditor import CKEditor

loginmanager = LoginManager()
mail = Mail()
ckeditor = CKEditor()


def init_login_manager(app):
    loginmanager.init_app(app)
    loginmanager.login_view = "blog.login"
    loginmanager.login_message = "登录后才能访问该页面."
    loginmanager.login_message_category='auth_error'
    loginmanager.needs_refresh_message='验证后才能访问该页面.'
    loginmanager.needs_refresh_message_category='auth_error'