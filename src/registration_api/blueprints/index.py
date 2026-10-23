"""Service info endpoint."""

# Standard Library imports
import os
import uuid

# Third Party imports
from flask import Blueprint, jsonify

# First party imports

index_bp = Blueprint("index", __name__)

# Random per-process ID so responses show which instance handled a request.
INSTANCE_ID = uuid.uuid4().hex[:8]


# main page
@index_bp.get("/")
def index():
    return jsonify(
        service="registration-api",
        instance=INSTANCE_ID,
        revision=os.environ.get("K_REVISION", "local"),
    )
