from sqlalchemy import Column, Integer, String, Text
from xplur.database import db
from .base import Base

class Category(Base):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Category {self.name!r}>'


    def create(data):
        instance = Base.create(data, Product)
        return instance