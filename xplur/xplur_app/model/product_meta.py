from sqlalchemy import Column, Integer, String, Text
from xplur.database import db
from .base import Base

class ProductMeta(Base):
    __tablename__ = 'product_meta'
    id = Column(Integer, primary_key=True)
    meta_key = Column(String(50))
    meta_value = Column(String(100))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    product = db.relationship('Product', backref=db.backref('products_meta', lazy=True))

    def __repr__(self):
        return f'<Product Meta {self.name!r}>'


    def create(data):
        instance = Base.create(data, ProductMeta)
        return instance
