"""API Endpoints relating to topics"""
from flask import Blueprint
from flask_restful import Api, request, Resource
from forum_api.settings import LOGGER
from forum_api.models import db, Topic

class TopicsLookup(Resource):
    def get(self, topicName):
        """Get info on a topic

         Args:
            topicName: Topic to lookup
        """

        LOGGER.debug({"Requested Topic": topicName})
        topic = Topic.query.filter_by(name=topicName).first()
        if topic is not None:
            topic_json = topic.to_json()
            return {"Topic": topic_json}, 200

        return {"message": "Topic not found"}, 404




















topics_bp = Blueprint("topics", __name__)
api = Api(topics_bp)
