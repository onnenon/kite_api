import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from forum_api.resources import register_blueprints
from forum_api.settings import FORUM_ADMIN, LOGGER


app = Flask(__name__)
app.config.from_object("forum_api.settings")

register_blueprints(app)
from forum_api.models import db, User

db.init_app(app)


@app.before_first_request
def init_forum():

    db.create_all()

    if User.get_user(username=FORUM_ADMIN.get("username")) is None:
        hashed = bcrypt.hashpw(
            FORUM_ADMIN.get("password").encode("utf8"), bcrypt.gensalt()
        )
        admin = User(
            username=FORUM_ADMIN.get("username"),
            pw_hash=hashed,
            is_admin=True,
            is_mod=True,
        )
        admin.save()
