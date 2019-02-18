import json

from tests import ForumBaseTest


class PostTest(ForumBaseTest):
    def setUp(self):
        super(PostTest, self).setUp()
        self.app.post("/api/v2/users", json={"username": "foo", "password": "testpass"})
        self.app.post("/api/v2/users", json={"username": "bar", "password": "testpass"})
        self.app.post(
            "/api/v2/topics", json={"name": "Cars", "description": "Things about cars."}
        )

    def test_001_create_post(self):
        resp = self.app.post(
            "/api/v2/posts",
            json={
                "topic": "Cars",
                "author": "foo",
                "title": "I Like Cars",
                "body": "I like them",
            },
        )
        data = json.loads(resp.data)
        self.logger.debug({"Resp Data": data})
        self.assertEquals(resp.status_code, 201)
