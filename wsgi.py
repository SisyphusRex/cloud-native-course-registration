"""WSGI Entry Point."""

# Standard Library imports

# Third Party imports

# First party imports
from registration_api.app import app

if __name__ == "__main__":
    # Flask development server, for local use only. In the container, gunicorn
    # imports `app` from this module instead and this block does not run.
    app.run(debug=True, host="127.0.0.1", port=8080)
