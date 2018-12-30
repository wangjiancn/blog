from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from blog.models.base import Base


class Comment(Base):
    id = Column(Integer,primary_key=True)
    body = Column(String(200),nullable=False)
    article_id = Column(Integer,ForeignKey('article.id'))

    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship('User',back_populates = 'comments')