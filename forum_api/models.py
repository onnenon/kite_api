from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from forum_api import db
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
    date = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    replies = db.relationship("Reply", backref="post", cascade="all")


class Reply(db.Model):
    __tablename__ = "replies"

    id = db.Column(UUID, primary_key=True, default=get_uuid)
    body = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(30), db.ForeignKey("users.username"), nullable=False)
    post_id = db.Column(UUID, db.ForeignKey("posts.id"), nullable=False)
    date = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
