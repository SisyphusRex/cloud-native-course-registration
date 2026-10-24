"""Course registration endpoint."""

# Standard Library imports

# Third Party imports
from flask import Blueprint, jsonify, request
from flask.views import MethodView

# First party imports
from registration_api.blueprints.courses import COURSE_IDS

registration_bp = Blueprint(name="registration", import_name=__name__)

# Deliberately in-memory: lost on restart and not shared between instances.
# This is the "bad" stateful design discussed in Part D of the report.
# An alternative would be to save this information in a persistent database,
# but that is outside the scope of this assignment, I think.
registrations = []


# register api
class RegistrationAPI(MethodView):
    def post(self):
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

    # Stubs: not part of the API yet.
    def get(self):
        return jsonify(error="not implemented"), 501

    def put(self):
        return jsonify(error="not implemented"), 501

    def delete(self):
        return jsonify(error="not implemented"), 501


registration_bp.add_url_rule("", view_func=RegistrationAPI.as_view("register"))
