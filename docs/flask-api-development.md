# REST API Development with Flask: Reference Summary

> **Source:** Matthias Döring, ["REST API Development with Flask"](https://www.datascienceblog.net/post/programming/flask-api-development/), *Data Science Blog*, July 24, 2020.
> Example code: [github.com/matdoering/minimal-flask-example](https://github.com/matdoering/minimal-flask-example)
>
> This is a summary written for this project, not a copy of the article. See the original for full code listings and screenshots.

## Overview

The article argues that Flask is a good fit when you want a lightweight application or freedom to choose your own libraries, compared with Django's batteries-included approach ([comparison](https://testdriven.io/blog/django-vs-flask/)). It walks through four things:

1. How to structure a RESTful Flask project.
2. How to run and manually test it.
3. How to make it production-ready (automated tests, an application server).
4. How to document it with Swagger / OpenAPI.

## 1. Project Structure

```
flask_app/
│   requirements.txt
│   app.ini
│   wsgi.py
│
└───src/
│   │   app.py
│   │   api_spec.py
│   │
│   └───blueprints/
│       │   blueprint_x.py
│       │   blueprint_y.py
│       │   swagger.py
│
└───test/
    │   conftest.py
    │   test_endpoints.py
```

| File | Role |
|---|---|
| `requirements.txt` | Lists the project's dependencies |
| `app.ini` | Configuration for the uWSGI application server |
| `wsgi.py` | Entry point the application server loads |
| `src/app.py` | Creates the Flask app and registers the blueprints |
| `src/api_spec.py` | Builds the OpenAPI specification |
| `src/blueprints/` | One module per functional area of the API; `swagger.py` serves the docs UI |
| `test/conftest.py` | Shared pytest fixtures and command-line options |
| `test/test_endpoints.py` | Endpoint tests |

## 2. A Minimal Application

- **`app.py`** creates the `Flask` object and calls `app.register_blueprint(...)` once per blueprint. Each blueprint gets a **versioned URL prefix** (under `/api/v1/`), so the API can evolve without breaking existing clients.
- **A blueprint module** creates a `Blueprint` and attaches routes to it. The example has a GET endpoint that returns a simple message, and a POST endpoint that reads JSON with `request.get_json()` and returns a computed result.
- **`wsgi.py`** imports the app. Only under `if __name__ == "__main__"` does it start Flask's development server with debug enabled, so debug mode never runs when a production server imports the module.

## 3. Running and Manual Testing

- The development server can be started with the Flask CLI (`flask run`) or by running `python wsgi.py`.
- **cURL** is used for quick manual checks. The important options are:
  - `-X` sets the HTTP method.
  - `-H` adds a header, e.g. `Content-Type: application/json`.
  - `-d` sends the request body.
- For more thorough manual testing, the author suggests GUI clients such as [Postman](https://www.postman.com/) or [Insomnia](https://insomnia.rest/).

## 4. Getting Ready for Production

### Automated tests with pytest

- The tests send real HTTP requests to a running server using the `requests` library.
- `conftest.py` adds a custom `--host` command-line option through the `pytest_addoption` hook. Session-scoped fixtures provide the host and the `/api/v1` base URL.
- Because the host is configurable, the same suite runs against the dev server or the production server, e.g. `pytest --host=http://localhost:<port>`.
- The tests assert on status codes and response bodies.

### Application server (uWSGI)

- Flask's built-in server is for development only. The article uses **uWSGI** in production.
- `app.ini` settings:
  - `module = wsgi:app` points uWSGI at the entry point.
  - `master` and `processes = 5` run a master process with five workers.
  - `http-socket` serves HTTP for local testing, and `socket` exposes a Unix socket for a reverse proxy.
  - `chmod-socket`, `vacuum` and `die-on-term` handle socket permissions, cleanup and shutdown.
- Start it with `uwsgi --ini app.ini --need-app`.

### Further steps

Put **nginx** in front of uWSGI as a reverse proxy. The article links to a DigitalOcean tutorial on serving Flask with uWSGI and nginx.

## 5. Documentation with Swagger / OpenAPI

The argument is that an API is only usable if people can understand it and experiment with it. Swagger provides both.

### Generating the OpenAPI JSON

1. **`api_spec.py`** creates an `APISpec` with the Flask and Marshmallow plugins (`apispec`, `apispec_webframeworks`, `marshmallow`). It defines request and response **schemas** and registers **tags** to group endpoints.
2. **`app.py`** registers each view function with the spec inside `app.test_request_context()` and serves the result at `/api/swagger.json`.
3. **Endpoint docstrings** contain a YAML block that describes each method's request body, responses and tags. apispec reads these blocks to build the spec.
4. **A pytest test** validates the generated spec with `openapi_spec_validator`. The [Swagger Editor](https://editor.swagger.io/) helps track down errors.

### Serving the Swagger UI

- `swagger.py` builds a blueprint with `get_swaggerui_blueprint` from `flask_swagger_ui`, pointing it at the docs path (`/api/docs`) and the JSON URL.
- `app.py` registers the UI blueprint, and the interactive docs then appear at `/api/docs`.

## Key Takeaways

- Group endpoints by functionality using **blueprints**.
- Keep dependencies in **`requirements.txt`**.
- Test endpoints with **pytest**, and make the target host configurable.
- Run a real **application server** in production, not Flask's dev server, and tune its configuration.
- Document the API with **Swagger / OpenAPI**.

## Libraries and Tools Mentioned

| Purpose | Tools |
|---|---|
| Framework | Flask (Django for comparison) |
| Testing | pytest, requests, cURL, Postman, Insomnia |
| Serving | uWSGI, nginx |
| API docs | apispec, apispec_webframeworks, marshmallow, flask_swagger_ui, openapi_spec_validator, Swagger Editor |

## How This Project Compares

| Article | This project |
|---|---|
| `wsgi.py` entry point at the root | Same: [wsgi.py](../wsgi.py) |
| `src/app.py` registers blueprints | Same idea: [src/registration_api/app.py](../src/registration_api/app.py) |
| `src/blueprints/` | `src/registration_api/blueprints/` (`index`, `courses`, `registration`) |
| Versioned prefixes (`/api/v1/...`) | Not used. The assignment specifies `/courses` and `/register` exactly |
| uWSGI with 5 processes | gunicorn with 1 worker and 8 threads, so each container holds one in-memory registration list |
| nginx reverse proxy | Not needed. Cloud Run terminates HTTPS and routes traffic to the container |
| pytest + `requests` against a live server | pytest with Flask's `test_client()`, which runs in-process with no server needed |
| `requirements.txt` maintained by hand | `pyproject.toml` + `uv.lock`, with `requirements.txt` generated by `uv export` |
| Swagger UI | Not implemented (possible extra) |
