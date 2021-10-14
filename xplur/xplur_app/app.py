from flask import Blueprint
from .views.product import ProductView
from flask_restful_swagger import swagger
from flask_restful import Api

xplur_app = Blueprint('xplur_app', __name__)
xplur_app.add_url_rule('/product/', view_func=ProductView.as_view('products'))

api = swagger.docs(Api(xplur_app), apiVersion='0.1')
