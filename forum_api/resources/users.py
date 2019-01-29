"""API Endpoints relating to users"""
from flask import Blueprint
from flask_restful import Api, request, Resource

from forum_api.settings import LOGGER
from forum_api.models import User


class UserLookup(Resource):
    def get(self, username):
        """Get info on a user.

        Args:
            username: Username to lookup.
        """
        LOGGER.debug({"Requested user": username})
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {"message": "user not fount"}, 404
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
        return {"message": "User created"}, 200

    def get(self):
        """Get list of all users."""
        return {"message": "all users"}, 200


users_bp = Blueprint("users", __name__)
api = Api(users_bp)
api.add_resource(UserLookup, "/api/users/<string:username>")
api.add_resource(UserList, "/api/users")
