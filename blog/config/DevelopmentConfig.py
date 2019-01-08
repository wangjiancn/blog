import os

from .Config import BaseConfig, basedir


class DevelopmentConfig(BaseConfig):

    DEBUG =True
    SECRET_KEY = 'secret key'
    WTF_CSRF_TIME_LIMIT	= 600   #测试csrf
    PER_PAGE_POST_COUNT = 5     #测试分页

    # SQLAlchemy 配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Flask-Caching配置
    # 参考 https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching
    CACHE_TYPE = 'filesystem'   #缓存类型默认为文件系统，其他类型配置可参考官方文档
    CACHE_DIR = os.path.normpath(os.path.join(basedir, '..' + os.sep + 'resource')) # 文件系统缓存的路径



