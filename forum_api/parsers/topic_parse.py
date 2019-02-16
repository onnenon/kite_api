from flask_restful import reqparse

put_parser = reqparse.RequestParser()
put_parser.add_argument(
    "description",
    dest="descript",
    location="json",
    required=False,
    help="Type: String. The Topic's updated description.",
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
    help="Type: String. The new Topic's description.",
)
