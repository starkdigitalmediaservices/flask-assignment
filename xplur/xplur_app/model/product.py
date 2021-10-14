from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import validates
from xplur.database import db
from .base import Base

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True)
    name = Column(String(120), unique=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Product {self.name!r}>'

    def create(data):
        instance = Base.create(data, Product)
        return instance