import json

from tests import ForumBaseTest

class TopicTest(ForumBaseTest):
    def setUp(self):
        super(TopicTest, self).setUp()
        self.app.post("/api/v2/users", json={"username1": "foo", "password": "testpass"})
        self.app.post("/api/v2/users", json={"username2": "bar", "password": "testpass"})

    """200 and not 201"""
    def test_001_create_topic(self):
        resp = self.app.post(
            "/api/v2/topics",
            json={
                "name": "Basketball",
                "description": "Everything related to Basketball",
            },
        )
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 201)
        self.assertEquals(data.get("data").get("message"), "topic Basketball created")

    def test_002_post_topic_fail(self):
        resp = self.app.post(
            "/api/v2/topics",
            json={
                "name": "Basketball",
                "description": "Basketball stuff",
            },
        )
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 400)

    def test_003_get_topics(self):
        resp = self.app.get("/api/v2/topics")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 200)

    def test_004_get_topic_info(self):
        self.app.post(
            "/api/v2/topics",
            json={
                "name": "Basketball",
                "description": "Basketball stuff",
            },
        )
        resp = self.app.get(f"/api/v2/topics/Basketball")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(data.get("data").get("topic").get("name"), "Basketball")

    def test_005_delete_success(self):
        resp = self.app.post(
            "/api/v2/topics",
            json={
                "name": "Basketball",
                "description": "Everything related to Basketball",
            },
        )
        resp = self.app.delete(f"/api/v2/topics/Basketball")
        self.assertEquals(resp.status_code, 204)


    def test_006_delete_doesnt_exist(self):
        name = "notThere"
        resp = self.app.delete(f"/api/v2/topics/{name}")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(data.get("data").get("title"), f"topic {name} not found")


    def test_007_topic_not_found(self):
        name = "saiuhsdfiuhiusiyfeu23982893s"
        resp = self.app.get(f"/api/v2/topics/{name}")
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(
            data.get("data").get("title"), f"topic {name} not found"
        )

