from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from forum_api.resources import register_blueprints

app = Flask(__name__)
app.config.from_object("forum_api.settings")

db = SQLAlchemy(app)

register_blueprints(app)
