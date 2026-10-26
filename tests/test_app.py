import os
import tempfile
import unittest

# Use an isolated database for test runs.
_test_dir = tempfile.TemporaryDirectory()
os.environ["DATABASE_PATH"] = os.path.join(_test_dir.name, "test.db")

from app import app  # noqa: E402


class ContactManagerTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        from app import get_db
        with get_db() as connection:
            connection.execute("DELETE FROM contacts")

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Contacts", response.data)

    def test_add_contact(self):
        response = self.client.post("/add", data={
            "name": "Test Contact",
            "phone": "1234567890",
            "email": "test@example.com",
            "address": "Test Street",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Contact", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "healthy")


if __name__ == "__main__":
    unittest.main()
