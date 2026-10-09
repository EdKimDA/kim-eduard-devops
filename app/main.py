import configparser
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


def app_settings():
    config = configparser.ConfigParser()
    config.read(Path(__file__).resolve().parents[1] / "config" / "app.conf")
    return config


def student_info():
    return {
        "Name": os.getenv("STUDENT_NAME", "Eduard"),
        "Surname": os.getenv("STUDENT_SURNAME", "Kim"),
        "Group": os.getenv("STUDENT_GROUP", "IT2-2313"),
        "Student ID": os.getenv("STUDENT_ID", "37324"),
    }


def application_text():
    lines = ["================================", "DevOps Student Application",
             "================================", ""]
    lines.extend(f"{key}: {value}" for key, value in student_info().items())
    lines.append("Course: " + app_settings().get("app", "course", fallback="DevOps"))
    lines.extend(["", "Application is running successfully!"])
    return "\n".join(lines) + "\n"


class StudentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        body = application_text().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    config = app_settings()
    port = int(os.getenv("APP_PORT", config.get("app", "port", fallback="8000")))
    print(application_text(), flush=True)
    print(f"Listening on port {port}", flush=True)
    with HTTPServer(("0.0.0.0", port), StudentHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
