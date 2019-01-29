from flask import Blueprint
from flask_restful import Api, request, Resource
from forum_api.settings import LOGGER

USERS = {"test": "password"}


class Auth(Resource):
    def post(self):
        username = request.authorization.get("username")
        LOGGER.debug({"username": username})
        password = request.authorization.get("password")
        LOGGER.debug({"password": password})

        if username in USERS and password == USERS[username]:
            return {"message": "Authenticated"}, 200
        return {"message": "Invalid Credentials"}, 403


class Refresh(Resource):
    def post(self):
        pass


auth_bp = Blueprint("auth", __name__)
api = Api(auth_bp)
api.add_resource(Auth, "/api/auth/login")
api.add_resource(Refresh, "/api/auth/refresh")
