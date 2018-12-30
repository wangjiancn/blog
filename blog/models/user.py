from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from blog import db, loginmanager
from blog.models.base import Base


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    password = Column(String(128))
    nickname = Column(String(30))
    info = Column(String(128))
    email = Column(String(50), nullable=False)
    phone_number = Column(db.String(20), unique=True)

    articles = relationship('Article', back_populates='author')

    comments = relationship('Comment', back_populates='user')

    messages = relationship('Message', back_populates='user')

    # todo 用于增加微信登陆 和 角色管理 后期加入
    # wx_id = db.Column(db.String(30),unique=True)
    # role = db.Column(db.SmallInteger,default=5)

    def keys(self):
        return ['username','nickname','email','create_datetime']




@loginmanager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
