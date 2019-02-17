import json

import pytest

from forum_api.settings import FORUM_ADMIN, LOGGER
from tests import ForumBaseTest


class UserTest(ForumBaseTest):
    def test_load_admin(self):
        resp = self.app.get("/api/user")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(
            data.get("users")[0].get("username"), FORUM_ADMIN.get("username")
        )
        self.assertEquals(data.get("users")[0].get("is_mod"), True)
        self.assertEquals(data.get("users")[0].get("is_mod"), True)

    def test_user_post_success(self):
        resp = self.app.post(
            "/api/user",
            json={"username": "foo", "password": "testpass", "bio": "Test Bio"},
        )
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEqual(resp.status_code, 200)
