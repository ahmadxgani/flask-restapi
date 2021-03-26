from flask import Flask, request, abort, jsonify, render_template, make_response
from app.plugins import pinterest
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

p_scraper = pinterest.PinterestImageScraper()

from app.controller import routes
from app.model import user, plugin