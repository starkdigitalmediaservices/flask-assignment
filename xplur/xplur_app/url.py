from .views.product import ProductView
from .app import xplur_app

xplur_app.add_url_rule('/product/', view_func=ProductView.as_view('products'))
