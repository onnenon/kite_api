"""API Endpoints relating to users"""
import bcrypt

from flask import Blueprint
from flask_restful import Api, request, Resource, reqparse

from forum_api.models import db, User
from forum_api.settings import LOGGER, FORUM_ADMIN

u_post_parse = reqparse.RequestParser()

u_post_parse.add_argument(
    "username",
    dest="username",
    location="json",
    required=True,
    help="Type: String. The new user's username.",
)

u_post_parse.add_argument(
    "password",
    dest="password",
    location="json",
    required=True,
    help="Type: String. The new user's password.",
)
u_post_parse.add_argument(
    "bio",
    dest="bio",
    location="json",
    required=False,
    help="Type: String. The new user's bio.",
)


class UserLookup(Resource):
    def get(self, username):
        """Get info on a user.

        Args:
            username: Username to lookup.
        """
        LOGGER.debug({"Requested user": username})
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {"message": "user not found"}, 404

        # Logic to create json return object
        return {"message": f"{username} datas ..."}, 200

    def put(self, username):
        """Update user info.

        Args:
            username: The user to be updated.
        """
        return {"message": f"{username} updated"}, 200

    def delete(self, username):
        """Delete a user.

        Args:
            username: The user to be deleted.
        """
        return {"message": f"{username} deleted"}, 200


class UserList(Resource):
    def post(self):
        """Create a new user."""

        args = u_post_parse.parse_args(strict=True)
        LOGGER.info({"Args": args})

        user = User.query.filter_by(username=args.username).first()

        if user is None:
            try:
                hashed = bcrypt.hashpw(args.password.encode("utf8"), bcrypt.gensalt())
                record = User(username=args.username, pw_hash=hashed, bio=args.bio)
                db.session.add(record)
                db.session.commit()
                return {"message": "Created"}, 200
            except Exception as e:
                LOGGER.error({"Exception": e})
                return {"message": e}, 500
        return {"message": "User exists"}, 400

        return {"message": "User created"}, 200

    def get(self):
        """Get list of all users."""
        user_filter = {}

        users = User.query

        users_json = [res.to_json() for res in users]
        return {"users": users_json}, 200


users_bp = Blueprint("users", __name__)
api = Api(users_bp)
api.add_resource(UserLookup, "/api/users/<string:username>")
api.add_resource(UserList, "/api/users")
