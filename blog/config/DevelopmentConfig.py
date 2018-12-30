from .Config import BaseConfig


class DevelopmentConfig(BaseConfig):

    DEBUG =True
    SECRET_KEY = 'secret key'

    # SQLAlchemy config
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_TIME_LIMIT	= 600



