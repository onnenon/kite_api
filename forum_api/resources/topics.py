"""API Endpoints relating to topics"""
from flask import Blueprint
from flask_restful import Api, request, Resource
from forum_api.settings import LOGGER


topics_bp = Blueprint("topics", __name__)
api = Api(topics_bp)
