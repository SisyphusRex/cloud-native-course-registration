"""Course Registration API for CS6030 Assignment 2."""

# Standard Library imports

# Third Party imports
from flask import Flask

# First party imports
from registration_api.blueprints.courses import courses_bp
from registration_api.blueprints.index import index_bp
from registration_api.blueprints.registration import registration_bp

app = Flask(__name__)

# Here, we are registering the API endpoints and the
# url prefix that points to them.
app.register_blueprint(index_bp, url_prefix="/")
app.register_blueprint(courses_bp, url_prefix="/courses")
app.register_blueprint(registration_bp, url_prefix="/register")
