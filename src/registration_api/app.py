"""Course Registration API for CS6030 Assignment 2."""

import os
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)

# Random per-process ID so responses show which instance handled a request.
INSTANCE_ID = uuid.uuid4().hex[:8]

COURSES = [
    {"id": "CS6030", "title": "Cloud Computing"},
    {"id": "CS5200", "title": "Database Management Systems"},
    {"id": "CS5550", "title": "Computer Networks"},
    {"id": "CS6260", "title": "Machine Learning"},
]
COURSE_IDS = {course["id"] for course in COURSES}

# Deliberately in-memory: lost on restart and not shared between instances.
# This is the "bad" stateful design discussed in Part D of the report.
registrations = []


@app.get("/")
def index():
    return jsonify(
        service="registration-api",
        instance=INSTANCE_ID,
        revision=os.environ.get("K_REVISION", "local"),
    )


@app.get("/courses")
def list_courses():
    return jsonify(COURSES)


@app.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    student = data.get("student")
    course = data.get("course")

    if not isinstance(student, str) or not student.strip():
        return jsonify(error="'student' is required"), 400
    if not isinstance(course, str) or not course.strip():
        return jsonify(error="'course' is required"), 400
    if course not in COURSE_IDS:
        return jsonify(error=f"unknown course '{course}'"), 404

    registrations.append({"student": student.strip(), "course": course})
    return jsonify(status="registered"), 201


def main():
    """Run the Flask development server (use gunicorn in production)."""
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


if __name__ == "__main__":
    main()
