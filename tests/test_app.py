import os
import threading
import unittest
from http.client import HTTPConnection
from http.server import HTTPServer
from unittest.mock import patch

from app.main import StudentHandler, application_text, app_settings, student_info


class ApplicationTests(unittest.TestCase):
    def test_default_student_information(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(student_info(), {
                "Name": "Eduard", "Surname": "Kim", "Group": "IT2-2313",
                "Student ID": "37324",
            })

    def test_environment_overrides(self):
        values = {"STUDENT_NAME": "Demo", "STUDENT_SURNAME": "Test",
                  "STUDENT_GROUP": "TEST-GROUP", "STUDENT_ID": "99999"}
        with patch.dict(os.environ, values, clear=True):
            text = application_text()
            for expected in ("Name: Demo", "Surname: Test", "Group: TEST-GROUP", "Student ID: 99999"):
                self.assertIn(expected, text)
            self.assertNotIn("37324", text)

    def test_project_configuration(self):
        self.assertEqual(app_settings().getint("app", "port"), 8000)
        self.assertIn("Course: DevOps", application_text())

    def test_http_response(self):
        with HTTPServer(("127.0.0.1", 0), StudentHandler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            connection = HTTPConnection("127.0.0.1", server.server_port, timeout=3)
            try:
                with patch.dict(os.environ, {}, clear=True):
                    connection.request("GET", "/")
                    response = connection.getresponse()
                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.read().decode(), application_text())
                connection.request("GET", "/missing")
                response = connection.getresponse()
                self.assertEqual(response.status, 404)
                response.read()
            finally:
                connection.close()
                server.shutdown()
                thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
