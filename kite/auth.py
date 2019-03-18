import time
from functools import wraps

import bcrypt
import jwt
from flask import Blueprint
from flask_restful import Api, Resource, request

from kite.models import User
from kite.settings import LOGGER, SECRET_KEY


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
                    payload = {
                        "sub": username,
                        "is_admin": user.is_admin,
                        "is_mod": user.is_mod,
                        "iat": int(time.time()),
                    }
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


def token_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.authorization.get("token")
        LOGGER.debug({"Token": token})
        return f(*args, **kwargs)


auth_bp = Blueprint("auth", __name__)
api = Api(auth_bp)
api.add_resource(Auth, "/api/auth/login")
api.add_resource(Refresh, "/api/auth/refresh")
