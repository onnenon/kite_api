from datetime import datetime

import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

from forum_api import db
from forum_api.settings import LOGGER
from forum_api.utils import get_uuid


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(30), nullable=False, primary_key=True)
    pw_hash = db.Column(db.Binary(60), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    is_mod = db.Column(db.Boolean(), nullable=False, default=False)
    post_count = db.Column(db.Integer(), nullable=False, default=0)

    posts = db.relationship("Post", backref="auth", cascade="all")


class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(UUID, primary_key=True, default=get_uuid)
    title = db.Column(db.String(30), unique=True, nullable=False)
    descript = db.Column(db.String(150))

    posts = db.relationship("Post", backref="topic", cascade="all")


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(UUID, primary_key=True, default=get_uuid)
    title = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(30), db.ForeignKey("users.username"), nullable=False)
    topic_id = db.Column(UUID, db.ForeignKey("topics.id"), nullable=False)
    date_ = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    replies = db.relationship("Reply", backref="post", cascade="all")


class Reply(db.Model):
    __tablename__ = "replies"

    id = db.Column(UUID, primary_key=True, default=get_uuid)
    body = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(30), db.ForeignKey("users.username"), nullable=False)
    post_id = db.Column(UUID, db.ForeignKey("posts.id"), nullable=False)
    date_ = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )


def create_admin(username, password):
    admin = User.query.filter_by(username=username).first()
    if not admin:
        hashed = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        LOGGER.debug({"Hash": hashed})
        LOGGER.debug({"username": username})
        LOGGER.debug({"password": password})
        admin = User(username=username, pw_hash=hashed, is_admin=True)
        db.session.add(admin)
        db.session.commit()
