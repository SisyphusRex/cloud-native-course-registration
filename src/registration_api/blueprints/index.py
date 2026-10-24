"""Service info endpoint."""

# Standard Library imports
import os
import uuid

# Third Party imports
from flask import Blueprint, jsonify
from flask.views import MethodView

# First party imports

index_bp = Blueprint(name="index", import_name=__name__)

# Random per-process ID so responses show which instance handled a request.
INSTANCE_ID = uuid.uuid4().hex[:8]


# main page
class IndexAPI(MethodView):
    def get(self):
        return jsonify(
            service="registration-api",
            instance=INSTANCE_ID,
            revision=os.environ.get("K_REVISION", "local"),
        )

    # Stubs: not part of the API yet.
    def post(self):
        return jsonify(error="not implemented"), 501

    def put(self):
        return jsonify(error="not implemented"), 501

    def delete(self):
        return jsonify(error="not implemented"), 501


index_bp.add_url_rule("", view_func=IndexAPI.as_view("index"))
