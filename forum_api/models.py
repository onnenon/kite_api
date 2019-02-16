from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

from forum_api.settings import LOGGER
from forum_api.utils import get_uuid

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(30), nullable=False, primary_key=True)
    pw_hash = db.Column(db.Binary(60), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)
    is_mod = db.Column(db.Boolean(), nullable=False, default=False)
    post_count = db.Column(db.Integer(), nullable=False, default=0)
    bio = db.Column(db.String(50), default="")

    posts = db.relationship("Post", backref="auth", cascade="all")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_user(username):
        return User.query.filter_by(username=username).first()

    def to_json(self):
        return {
            "username": self.username,
            "is_admin": self.is_admin,
            "is_mod": self.is_mod,
            "post_count": self.post_count,
            "bio": self.bio,
        }


class Topic(db.Model):
    __tablename__ = "topics"

    name = db.Column(db.String(30), primary_key=True, nullable=False)
    descript = db.Column(db.String(150))

    posts = db.relationship("Post", backref="topic", cascade="all")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit

    @staticmethod
    def get_all():
        return Topic.query.all()

    @staticmethod
    def get_user(top_name):
        return Topic.query.filter_by(name=top_name).first()

    def to_json(self):
        return {"name": self.name, "descript": self.descript}


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(UUID, primary_key=True, default=get_uuid)
    title = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(30), db.ForeignKey("users.username"), nullable=False)
    topic_name = db.Column(db.String(30), db.ForeignKey("topics.name"), nullable=False)
    date_ = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    replies = db.relationship("Reply", backref="post", cascade="all")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit

    @staticmethod
    def get_all():
        return Post.query.all()

    @staticmethod
    def get_user(post_id):
        return Post.query.filter_by(id=post_id).first()

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "author": self.author,
            "topic_name": self.topic_name,
            "date": self.date_,
        }


class Reply(db.Model):
    __tablename__ = "replies"

    id = db.Column(UUID, primary_key=True, default=get_uuid)
    body = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(30), db.ForeignKey("users.username"), nullable=False)
    post_id = db.Column(UUID, db.ForeignKey("posts.id"), nullable=False)
    date_ = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit

    @staticmethod
    def get_all():
        return Reply.query.all()

    @staticmethod
    def get_user(rep_id):
        return Reply.query.filter_by(id=rep_id).first()

    def to_json(self):
        return {
            "id": self.id,
            "body": self.body,
            "author": self.author,
            "post_id": self.post_id,
            "date": self.date_,
        }
