from flask_restful import reqparse

post_parser = reqparse.RequestParser()

post_parser.add_argument(
    "username",
    dest="username",
    location="json",
    required=True,
    help="Type: String. The new user's username, required.",
)
post_parser.add_argument(
    "bio",
    dest="bio",
    location="json",
    required=False,
    help="Type: String. The new user's bio.",
)
post_parser.add_argument(
    "password",
    dest="password",
    location="json",
    required=True,
    help="Type: String. The new user's password, required.",
)

put_parser = reqparse.RequestParser()

put_parser.add_argument(
    "is_admin",
    dest="is_admin",
    location="json",
    required=False,
    type=bool,
    help="Type: Boolean. Is user an admin.",
)
put_parser.add_argument(
    "is_mod",
    dest="is_mod",
    location="json",
    required=False,
    type=bool,
    help="Type: Boolean. Is user an moderator.",
)
put_parser.add_argument(
    "bio",
    dest="bio",
    location="json",
    required=False,
    help="Type: String. The user's updated bio.",
)
put_parser.add_argument(
    "password",
    dest="password",
    location="json",
    required=False,
    help="Type: String. The new user's password, required.",
)
