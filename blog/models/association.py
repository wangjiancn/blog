# 多对多关联表
from sqlalchemy import Table, Column, ForeignKey, Integer
from blog.models.base import db

association_tag_article = Table('tag_article',
                                db.metadata,
                                Column('tag_id', Integer, ForeignKey('tag.id')),
                                Column('article_id', Integer, ForeignKey('article.id')))

