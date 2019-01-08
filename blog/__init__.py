# coding = utf-8
import os

from flask import Flask

from blog.config import config_map
from blog.helpers.extensions import loginmanager, init_login_manager
from blog.helpers.extensions import mail, ckeditor, cache
from blog.models.base import db


def create_app(config_name=None):
    app = Flask(__name__)
    if config_name == None:
        config_name = os.getenv('FLASK_ENV', 'production')
    app.config.from_object(config_map.get(config_name, config_map['production']))
    app.jinja_env.add_extension('jinja2.ext.do')
    ckeditor.init_app(app)
    cache.init_app(app)
    init_login_manager(app)
    # mail.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from blog.blog_web import blog_bp
    app.register_blueprint(blog_bp)

    from blog.helpers.commands import register_commands
    register_commands(app)

    return app
