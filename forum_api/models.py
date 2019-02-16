from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from forum_api.settings import LOGGER
from forum_api.utils import get_uuid
from sqlalchemy.dialects.postgresql import UUID

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
        """Addes the non-existing user to the DB."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes the user from the DB."""
        db.session.delete(self)
        db.session.commit

    @staticmethod
    def get_all():
        """Returns a list of all User objects in the Users table"""
        return User.query.all()

    @staticmethod
    def get_user(username):
       """Returns a user Object for a specific user, if it exists.

        Args:
            username: username to search for
        """
        return User.query.filter_by(username=username).first()

    def to_json(self):
        """Returns a JSON representation of the user."""
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
        """Addes the non-existing topic to the DB."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes the topic from the DB."""
        db.session.delete(self)
        db.session.commit

    @staticmethod
    def get_all():
        """Returns a list of all User objects in the Users table"""
        return Topic.query.all()

    @staticmethod
    def get_user(top_name):
        """Returns a user Object for a specific user, if it exists.

        Args:
            username: username to search for
        """
        return Topic.query.filter_by(name=top_name).first()

    def to_json(self):
        """Returns a JSON representation of the topic."""
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
        """Saves the post to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes the post from the database."""
        db.session.delete(self)
        db.session.commit

    @staticmethod
    def get_all():
        """Returns a list of all post objects in the database."""
        return Post.query.all()

    @staticmethod
    def get_user(post_id):
        """Returns a post object for a specific post.

        Args:
            post_id: The ID of the post to search for.
        """
        return Post.query.filter_by(id=post_id).first()

    def to_json(self):
        """Returns a JSON representation of the post."""
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
