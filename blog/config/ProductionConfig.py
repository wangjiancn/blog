from .Config import BaseConfig

class ProductionConfig(BaseConfig):

    SECRET_KEY = "your secret key"
    # SQLAlchemy 配置
    SQLALCHEMY_DATABASE_URI = 'your sql url'

    # other config
    # ......
