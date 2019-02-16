import json
import time

import bcrypt
import jwt
from flask import Blueprint
from flask_restful import Api, Resource, request

from forum_api.models import User
from forum_api.settings import LOGGER, SECRET_KEY


class Auth(Resource):
    def post(self):
        if request.authorization is None:
            return {"errors": {"detail": "Basic auth header missing"}}, 400

        username = request.authorization.get("username")
        password = request.authorization.get("password")
        LOGGER.debug({username: password})

        user = User.query.filter_by(username=username).first()
        if user is not None:
            try:
                if bcrypt.checkpw(password.encode("utf8"), user.pw_hash):
                    perm = get_permissions(user)
                    LOGGER.debug({"Permissions": perm})

                    payload = {"sub": username, "perm": perm, "iat": int(time.time())}
                    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
                    LOGGER.debug({"Token": token})
                    return {"data": {"access_token": token.decode("utf8")}}, 200
            except Exception as e:
                LOGGER.error({"Exception": e})
                return {"errors": {"detail": "server error"}}, 500
        return {"errors": {"detail": "Invalid Credentials"}}, 403


class Refresh(Resource):
    def post(self):
        pass


def get_permissions(user):
    if user.is_admin:
        return "admin"
    if user.is_mod:
        return "mod"
    return "user"


auth_bp = Blueprint("auth", __name__)
api = Api(auth_bp)
api.add_resource(Auth, "/api/auth/login")
api.add_resource(Refresh, "/api/auth/refresh")
