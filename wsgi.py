"""WSGI Entry Point."""

# Standard Library imports
import os

# Third Party imports

# First party imports
from registration_api.app import app

if __name__ == "__main__":
    # Flask development server, for local use only. In the container, gunicorn
    # imports `app` from this module instead and this block does not run.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
