"""Course Registration API for CS6030 Assignment 2."""

import os
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)

# Random per-process ID so responses show which instance handled a request.
INSTANCE_ID = uuid.uuid4().hex[:8]

# WMU graduate Computer Science courses (source: docs/courses.txt).
COURSES = [
    {"id": "CS5110", "title": "Big Data"},
    {"id": "CS5115", "title": "Programming Prep for Graduate Studies"},
    {"id": "CS5260", "title": "Parallel Computations"},
    {"id": "CS5270", "title": "Computer Graphics"},
    {"id": "CS5300", "title": "Artificial Neural Systems"},
    {"id": "CS5310", "title": "Algorithms"},
    {"id": "CS5410", "title": "Game Programming"},
    {"id": "CS5430", "title": "Database Systems"},
    {"id": "CS5541", "title": "Computer Systems"},
    {"id": "CS5550", "title": "Computer Networks and Distributed Systems"},
    {"id": "CS5560", "title": "Network Programming"},
    {"id": "CS5610", "title": "Advanced R Programming for Data Science"},
    {"id": "CS5700", "title": "Computer Security and Information Assurance"},
    {"id": "CS5750", "title": "Secure Software Development"},
    {"id": "CS5800", "title": "Theory Foundations"},
    {"id": "CS5810", "title": "Compiler Design and Implementation"},
    {"id": "CS5820", "title": "Artificial Intelligence"},
    {"id": "CS5821", "title": "Machine Learning"},
    {"id": "CS5822", "title": "Natural Language Processing"},
    {"id": "CS5823", "title": "Autonomous Vehicles for CS Majors"},
    {"id": "CS5950", "title": "Advanced Topics in Computer and Information Science"},
    {"id": "CS5990", "title": "Independent Study in Computer Science"},
    {"id": "CS6030", "title": "Cloud Computing"},
    {"id": "CS6100", "title": "Advanced Storage, Retrieval and Processing of Big Data"},
    {"id": "CS6110", "title": "Data Science Foundations"},
    {"id": "CS6250", "title": "Advanced Computer Architecture"},
    {"id": "CS6260", "title": "Advanced Parallel Computations"},
    {"id": "CS6310", "title": "Advanced Design and Analysis of Algorithms"},
    {"id": "CS6430", "title": "Database Management System Implementation"},
    {"id": "CS6530", "title": "Data Mining"},
    {"id": "CS6550", "title": "Advanced Operating Systems"},
    {"id": "CS6560", "title": "Advanced Computer Networks: Anatomy of the Internet"},
    {"id": "CS6570", "title": "Wireless Networks"},
    {"id": "CS6580", "title": "Pervasive Computing"},
    {"id": "CS6600", "title": "Software Engineering"},
    {"id": "CS6610", "title": "Software Testing"},
    {"id": "CS6700", "title": "Advanced Computer and Information Security"},
    {"id": "CS6720", "title": "Pattern Recognition"},
    {"id": "CS6800", "title": "Advanced Theory of Computation"},
    {"id": "CS6810", "title": "Compiler Optimization"},
    {"id": "CS6820", "title": "Advanced Artificial Intelligence"},
    {"id": "CS6821", "title": "Information Retrieval"},
    {"id": "CS6910", "title": "Seminar in Computer Science"},
    {"id": "CS6970", "title": "Master's Project"},
    {"id": "CS7000", "title": "Master's Thesis"},
    {"id": "CS7100", "title": "Independent Research"},
    {"id": "CS7120", "title": "Professional Field Experience"},
    {"id": "CS7250", "title": "Doctoral Research Seminar"},
    {"id": "CS7300", "title": "Doctoral Dissertation"},
    {"id": "CS7350", "title": "Graduate Research"},
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
