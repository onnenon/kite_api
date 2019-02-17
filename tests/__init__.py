import re
from unittest import TestCase
from forum_api import app
from forum_api.settings import LOGGER


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
