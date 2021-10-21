# Create your tests here.
from rest_framework.test import APITestCase


class EventAPITest(APITestCase):
    def setUp(self):
        self.test_data = [
            {
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "pageview",
                "data": {"host": "www.consumeraffairs.com", "path": "/"},
                "timestamp": "2021-01-01 09:15:27.243860",
            },
            {
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "cta click",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/",
                    "element": "chat bubble",
                },
                "timestamp": "2021-01-01 09:15:27.243860",
            },
            {
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "form interaction",
                "name": "submit",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/",
                    "form": {"first_name": "John", "last_name": "Doe"},
                },
                "timestamp": "2021-01-01 09:15:27.243860",
            },
        ]

    def test_events_endpoint(self):
        response = self.client.get("/api/v1/events/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_post_event(self):
        for i, event in enumerate(self.test_data):
            response = self.client.post("/api/v1/events/", event, format="json")
            self.assertEqual(response.status_code, 201)
