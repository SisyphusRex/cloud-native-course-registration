"""Course Registration API for CS6030 Assignment 2."""

# Standard Library imports

# Third Party imports
from flask import Flask

# First party imports
from registration_api.blueprints.courses import courses_bp
from registration_api.blueprints.index import index_bp
from registration_api.blueprints.registration import registration_bp

app = Flask(__name__)

app.register_blueprint(index_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(registration_bp)
