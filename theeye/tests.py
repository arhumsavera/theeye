# Create your tests here.
from rest_framework.test import APITestCase


class EventAPITest(APITestCase):
    def test_events_endpoint(self):
        response = self.client.get("/api/v1/events/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    # TODO test with readme data, 201 created
