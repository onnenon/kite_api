"""API Endpoints relating to topics"""
from flask import Blueprint
from flask_restful import Api, request, Resource, reqparse
from forum_api.settings import LOGGER
from forum_api.models import db, Topic


put_parser = reqparse.RequestParser()
put_parser.add_argument(
    "description",
    dest="descript",
    location="json",
    required=False,
    help="Type: String. The Topic's updated description."
)

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    "name",
    dest="name",
    location="json",
    required=True,
    help="Type: String. The new Topic's name, required.",
)
post_parser.add_argument(
    "description",
    dest="descript",
    location="json",
    required=False,
    help="Type: String. The new Topic's description."
)


class TopicLookup(Resource):
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




    def put(self, topicName):
        """Update topic info
        Args:
            This topic will be updated
        """
        args = put_parser.parse_args(strict=True)
        topic = Topic.query.filter_by(name=topicName).first()
        if topic is not None:
            if args.description is not None:
                topic.descript = args.description
            db.session.commit()
            return {"message": f"{topicName} updated"}, 200

        return {"message": "topic not found"}, 404

    def delete(self,topicName):
        """

        :param topicName:
        :return:
        """
        topic = Topic.query.filter_by(name=topicName).first()
        if topic is not None:
            db.session.delete(topic)
            db.session.commit()
            return {"message": f"{topicName} deleted"}, 200
        return {"message": "user not found"}, 404


class TopicList(Resource):

    #this one needs work
    def post(self):
        """Create a new Topic."""

        args = post_parser.parse_args(strict=True)
        LOGGER.info({"Args": args})

        topic = Topic.query.filter_by(name=args.name).first()

        if topic is None:
            try:
                record = Topic(name=args.name, descript=args.description)
                db.session.add(record)
                db.session.commit()
                return {"message": f"topic {args.name} created"}, 200
            except Exception as e:
                LOGGER.error({"Exception": e})
                return {"message": e}, 500
        return {"message": f"topic {args.name} exists"}, 400

    def get(self):
        """Get list of all topics."""
        topic_filter = {}
        topics = Topic.query
        topics_json = [res.to_json() for res in topics]
        return {"users": topics_json}, 200




topics_bp = Blueprint("topics", __name__)
api = Api(topics_bp)
api.add_resource(TopicLookup, "/api/topics/<string:name>")
api.add_resource(TopicList, "/api/topics")