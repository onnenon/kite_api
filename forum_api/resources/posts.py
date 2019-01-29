"""API Endpoints relating to posts"""
from flask import Blueprint
from flask_restful import Api, request, Resource
from forum_api.settings import LOGGER


posts_bp = Blueprint("posts", __name__)
api = Api(posts_bp)
