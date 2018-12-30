from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from blog.models.base import Base

class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    background_field = Column(String(20))

    articles = relationship('Article',back_populates = 'category')
