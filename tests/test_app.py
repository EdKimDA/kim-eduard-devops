import os
import threading
import unittest
from http.server import HTTPServer
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen

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

    def test_http_response(self):
        with HTTPServer(("127.0.0.1", 0), StudentHandler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                with patch.dict(os.environ, {}, clear=True):
                    with urlopen(f"http://127.0.0.1:{server.server_port}/", timeout=3) as response:
                        self.assertEqual(response.status, 200)
                        self.assertEqual(response.read().decode(), application_text())
                with self.assertRaises(HTTPError) as error:
                    urlopen(f"http://127.0.0.1:{server.server_port}/missing", timeout=3)
                self.assertEqual(error.exception.code, 404)
            finally:
                server.shutdown()
                thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
