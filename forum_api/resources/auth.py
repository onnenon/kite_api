from flask import Blueprint
from flask_restful import Api, Resource


class Auth(Resource):
    def post(self):
        pass


auth_bp = Blueprint("auth", __name__)
api = Api(auth_bp)
api.add_resource(Auth, "/api/auth", endpoint="api-auth")
