import json

from mock import MagicMock, patch
from tests import API_VERSION, ForumBaseTest

from kite.api.response import Fail, Success

MOCK_REPLY = MagicMock()

MOCK_REPLY().to_json.return_value = {"mock": "data"}


class ReplyTest(ForumBaseTest):
    valid_uuid = "e98ffad9-9381-4f56-a91a-1a67b830e9ee"
    invalid_uuid = "lmao"

    @patch("kite.api.v2.replies.Reply.get_all", side_effect=MOCK_REPLY)
    def test_001_get_replies_success(self, mock):
        resp = self.app.get("/api/v2/replies")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 200)

    @patch("kite.api.v2.replies.Reply.get_reply", side_effect=MOCK_REPLY)
    def test_002_get_reply_success(self, mock):
        resp = self.app.get(f"/api/v2/replies/{self.valid_uuid}")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 200)

    @patch("kite.api.v2.replies.Reply.get_reply", return_value=None)
    def test_003_get_reply_failure_does_not_exist(self, mock):
        resp = self.app.get(f"/api/v2/replies/{self.valid_uuid}")
        data = json.loads(resp.data)
        self.assertEquals(resp.status_code, 404)

    def test_004_get_reply_failure_invalid_uuid(self):
        resp = self.app.get(f"/api/v2/replies/{self.invalid_uuid}")
        self.assertEquals(resp.status_code, 400)
