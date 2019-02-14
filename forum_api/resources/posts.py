"""API Endpoints relating to posts"""
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, request
from forum_api.models import Post, Topic, User, db
from forum_api.settings import LOGGER
from forum_api.utils import validate_length, validate_uuid

post_parser = reqparse.RequestParser()
put_parser = reqparse.RequestParser()

post_parser.add_argument(
    "title",
    dest="title",
    location="json",
    required=True,
    help="Type: String. The post's title, required. Length: 5-30 characters",
    type=validate_length(30, 5, "title"),
)
post_parser.add_argument(
    "body",
    dest="body",
    location="json",
    required=True,
    help="Type: String. The post's body, required. Length: 10-250 characters",
    type=validate_length(250, 10, "body"),
)
post_parser.add_argument(
    "author",
    dest="author",
    location="json",
    required=True,
    help="Type: String. The post's Author, required.",
)
post_parser.add_argument(
    "topic",
    dest="topic_name",
    location="json",
    required=True,
    help="Type: String. The Topic the post belongs to, required. Length: 5-30 characters",
)

put_parser.add_argument(
    "title",
    dest="title",
    location="json",
    required=False,
    help="Type: String. The post's title.",
    type=validate_length(30, 5, "title"),
)
post_parser.add_argument(
    "body",
    dest="body",
    location="json",
    required=False,
    help="Type: String. The post's body.",
    type=validate_length(250, 10, "body"),
)


class PostUpdate(Resource):
    def get(self, post_id):
        """Get info on a specific post.

        Args:
            post_id: UUID of the post to lookup.
        """
        if not validate_uuid(post_id):
            return {"error": "invalid UUID"}, 400
        LOGGER.debug({"Requested Post": post_id})
        post = Post.query.filter_by(id=post_id).first()
        if post is not None:
            return {"post": post.to_json}, 200
        return {"error": "post not found"}, 404

    def put(self, post_id):
        """Update info for a specific post.

        Args:
            post_id: UUID of the post to update.
        """
        pass


class Posts(Resource):
    def get(self):
        """Get list of existing posts."""
        posts = Post.query
        posts_json = [post.to_json() for post in posts]
        return {"posts": posts_json}, 200

    def post(self):
        """Create a new post."""
        args = post_parser.parse_args(strict=True)
        LOGGER.info({"Args": args})

        if User.query.filter_by(username=args.author).first() is None:
            return {"error": f"author {args.author} does not exist"}, 400

        if Topic.query.filter_by(name=args.topic_name).first() is None:
            return {"error": f"topic {args.topic_name} does not exist"}, 400

        post = Post(
            title=args.title,
            body=args.body,
            author=args.author,
            topic_name=args.topic_name,
        )
        db.session.add(post)
        db.session.flush()
        post_uuid = post.id
        db.session.commit()

        return {"message": post_uuid}, 200


posts_bp = Blueprint("posts", __name__)
api = Api(posts_bp)
api.add_resource(PostUpdate, "/api/v2/posts/<uuid:post_id>")
api.add_resource(Posts, "/api/v2/posts")
