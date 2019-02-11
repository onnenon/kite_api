from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object("forum_api.settings")

db = SQLAlchemy(app)

from forum_api.resources import register_blueprints

register_blueprints(app)

