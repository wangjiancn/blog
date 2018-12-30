from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from blog.models.base import Base


class Message(Base):
    id = Column(Integer, primary_key=True)
    body = Column(String(200), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='messages')

    # todo 定义双向关系‘user’替代get_username方法
    # @property
    # def get_username(self):
    #     return User.query.get(self.user_id)

    @classmethod
    def get_count(cls):
        return cls.query.count()
