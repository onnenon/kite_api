from flask import Flask

from forum_api.resources import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object("forum_api.settings")
    register_blueprints(app)

    from forum_api.models import db, create_admin
    from forum_api.settings import FORUM_ADMIN

    db.init_app(app)

    create_admin(FORUM_ADMIN["username"], FORUM_ADMIN["password"])
