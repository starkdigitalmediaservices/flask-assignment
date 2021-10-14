from xplur_app.views.product import ProductView
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .database import db
from xplur_app.models import *
from flask_sqlalchemy import SQLAlchemy
from xplur_app.app import xplur_app
import os
# from flask_io import FlaskIO
from dotenv import load_dotenv
from flasgger import Swagger

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI') 

app.register_blueprint(xplur_app, url_prefix='/api/v1/')
swagger = Swagger(app)

db.init_app(app)
migrate = Migrate(app, db)