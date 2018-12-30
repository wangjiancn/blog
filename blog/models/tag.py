# coding = utf-8

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from blog.models.base import Base
from blog.models.association import association_tag_article


class Tag(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    background_field = Column(String(20))

    articles = relationship('Article',
                            secondary=association_tag_article,
                            back_populates='tags')

    # todo 后期用户自定义标签
    # author_id= Column(Integer,ForeignKey('user.id'))
    def __repr__(self):
        return '<Tag {}>'.format(self.name)
