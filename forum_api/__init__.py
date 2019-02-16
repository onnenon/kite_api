import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from forum_api.resources import register_blueprints
from forum_api.models import db, User
from forum_api.settings import FORUM_ADMIN


def create_app():
    app = Flask(__name__)
    app.config.from_object("forum_api.settings")
    db.init_app(app)

    register_blueprints(app)
    with app.app_context():
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
    return app

