"""API Endpoints relating to users"""
import bcrypt
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, request

from forum_api.models import User, db
from forum_api.settings import FORUM_ADMIN, LOGGER

post_parser = reqparse.RequestParser()

post_parser.add_argument(
    "username",
    dest="username",
    location="json",
    required=True,
    help="Type: String. The new user's username, required.",
)

post_parser.add_argument(
    "bio",
    dest="bio",
    location="json",
    required=False,
    help="Type: String. The new user's bio.",
)

post_parser.add_argument(
    "password",
    dest="password",
    location="json",
    required=True,
    help="Type: String. The new user's password, required.",
)

put_parser = reqparse.RequestParser()

put_parser.add_argument(
    "is_admin",
    dest="is_admin",
    location="json",
    required=False,
    type=bool,
    help="Type: Boolean. Is user an admin.",
)
put_parser.add_argument(
    "is_mod",
    dest="is_mod",
    location="json",
    required=False,
    type=bool,
    help="Type: Boolean. Is user an moderator.",
)
put_parser.add_argument(
    "bio",
    dest="bio",
    location="json",
    required=False,
    help="Type: String. The user's updated bio.",
)
put_parser.add_argument(
    "password",
    dest="password",
    location="json",
    required=False,
    help="Type: String. The new user's password, required.",
)


class UserLookup(Resource):
    def get(self, username):
        """Get info on a user.

        Args:
            username: Username to lookup.
        """
        LOGGER.debug({"Requested user": username})
        user = User.query.filter_by(username=username).first()
        if user is not None:
            user_json = user.to_json()
            return {"user": user_json}, 200

        return {"message": "user not found"}, 404

    def put(self, username):
        """Update user info.

        Args:
            username: The user to be updated.
        """
        args = put_parser.parse_args(strict=True)
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if args.is_admin is not None:
                user.is_admin = args.is_admin
            if args.bio is not None:
                user.bio = args.bio
            if args.is_mod is not None:
                user.is_mod = args.is_mod
            if args.password is not None:
                user.pw_hash = bcrypt.hashpw(
                    args.password.encode("utf8"), bcrypt.gensalt()
                )
            db.session.commit()
            return {"message": f"{username} updated"}, 200

        return {"message": "user not found"}, 404

    def delete(self, username):
        """Delete a user.

        Args:
            username: The user to be deleted.
        """
        user = User.query.filter_by(username=username).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return {"message": f"{username} deleted"}, 204
        return {"message": "user not found"}, 404


class UserList(Resource):
    def post(self):
        """Create a new user."""

        args = post_parser.parse_args(strict=True)
        LOGGER.info({"Args": args})

        user = User.query.filter_by(username=args.username).first()

        if user is None:
            try:
                hashed = bcrypt.hashpw(args.password.encode("utf8"), bcrypt.gensalt())
                record = User(username=args.username, pw_hash=hashed, bio=args.bio)
                db.session.add(record)
                db.session.commit()
                return {"message": f"user {args.username} created"}, 201
            except Exception as e:
                LOGGER.error({"Exception": e})
                return {"message": e}, 500
        return {"message": f"user {args.username} exists"}, 400

    def get(self):
        """Get list of all users."""
        user_filter = {}
        users = User.query
        users_json = [res.to_json() for res in users]
        return {"users": users_json}, 200


users_bp = Blueprint("users", __name__)
api = Api(users_bp)
api.add_resource(UserLookup, "/api/user/<string:username>")
api.add_resource(UserList, "/api/user")
