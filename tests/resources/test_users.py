import json

from forum_api.settings import FORUM_ADMIN, LOGGER
from tests import ForumBaseTest


class UserTest(ForumBaseTest):
    def test_001_load_admin(self):
        resp = self.app.get("/api/v2/users")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(
            data.get("data").get("users")[0].get("username"),
            FORUM_ADMIN.get("username"),
        )
        self.assertEquals(data.get("data").get("users")[0].get("is_mod"), True)
        self.assertEquals(data.get("data").get("users")[0].get("is_mod"), True)

    def test_002_user_post_success(self):
        resp = self.app.post(
            "/api/v2/users",
            json={"username": "foo", "password": "testpass", "bio": "Test Bio"},
        )
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(data.get("data").get("message"), "user foo created")
        self.assertEquals(resp.status_code, 201)

    def test_003_user_post_fail(self):
        resp = self.app.post(
            "api/v2/users", json={"username": "foo", "password": "test"}
        )
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 400)

    def test_004_user_record_get_success(self):
        resp = self.app.get("/api/v2/users/foo")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(data.get("status"), "success")
        self.assertEquals(data.get("data").get("username"), "foo")

    def test_005_user_record_get_failure(self):
        resp = self.app.get("/api/v2/users/bar")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(data.get("status"), "fail")
        self.assertEquals(data.get("data").get("title"), "user bar not found")

    def test_006_user_record_put_success(self):
        resp = self.app.put(
            "/api/v2/users/foo", json={"bio": "New Bio", "is_admin": True}
        )
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(data.get("status"), "success")
        self.assertEquals(data.get("data").get("message"), "foo updated")

    def test_007_user_record_put_success_002(self):
        resp = self.app.put(
            "/api/v2/users/foo", json={"password": "longpass", "is_mod": True}
        )
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(data.get("status"), "success")
        self.assertEquals(data.get("data").get("message"), "foo updated")

    def test_008_user_record_put_failure(self):
        resp = self.app.put("/api/v2/users/bar", json={"bio": "something"})
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(data.get("status"), "fail")
        self.assertEquals(data.get("data").get("title"), "user bar does not exist")

    def test_009_user_attributes_updated(self):
        resp = self.app.get("/api/v2/users/foo")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 200)
        self.assertTrue(data.get("data").get("is_admin"))
        self.assertTrue(data.get("data").get("is_mod"))
        self.assertEquals(data.get("data").get("bio"), "New Bio")

    def test_010_use_record_delete_success(self):
        resp = self.app.delete("/api/v2/users/foo")
        self.assertEquals(resp.status_code, 204)

    def test_011_user_record_delete_failure(self):
        resp = self.app.delete("/api/v2/users/foo")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(data.get("status"), "fail")
        self.assertEquals(data.get("data").get("title"), "user foo does not exist")
