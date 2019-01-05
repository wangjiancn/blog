# coding = utf-8
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from blog.models.base import Base, db
from blog.models.association import association_tag_article


class Article(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    body = Column(Text)
    markdown = Column(Text)
    summary = Column(String(200))
    img_url = Column(String(255))
    # last_edit_date = Column(Date,default=datetime.utcnow().timestamp())
    # fav_count = Column(Integer,default=0)
    # praise_count = Column(Integer,default=0)
    # fav
    # praise
    category_field = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='articles')

    tags = relationship('Tag', secondary=association_tag_article,
                        back_populates='articles')

    comments = relationship('Comment')

    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', back_populates='articles')

    @classmethod
    def get_count(cls):
        return cls.query.filter_by(status=1).count()

    @classmethod
    def last_article_id(cls,author_id):
        '''
        接受用户的id，找到该用户最后创建的文章，返回id
        :param author_id: User模型的id
        :return: 对应用户最新创建的文章id
        '''
        last_article = db.session.query(cls.id).filter_by(author_id=author_id).order_by(cls.create_time.desc()).first()
        last_article_id = last_article[0]
        return last_article_id