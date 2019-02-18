import re
import bcrypt
from unittest import TestCase
from forum_api import app
from forum_api.models import db, User
from forum_api.settings import LOGGER, FORUM_ADMIN


class ForumBaseTest(TestCase):

    logger = LOGGER

    @classmethod
    def setUp(self):
        self.app = app.test_client()
        app.config.from_object("forum_api.settings")

    def clean_data(self, data):
        data = data.decode("utf-8")
        data = re.sub("\n", " ", data)
        data = re.sub(" +", " ", data)
        return data

    @classmethod
    def tearDownClass(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            if User.get_user(username=FORUM_ADMIN.get("username")) is None:
                hashed = bcrypt.hashpw(
                    FORUM_ADMIN.get("password").encode("utf8"), bcrypt.gensalt()
                )
                admin = User(
                    username=FORUM_ADMIN.get("username"),
                    pw_hash=hashed,
                    is_admin=True,
                    is_mod=True,
                )
                admin.save()
