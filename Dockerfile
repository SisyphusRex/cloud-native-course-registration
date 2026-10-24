FROM python:3.12-slim

# Install uv from its official image instead of using pip.
COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Install pinned dependencies from the lockfile first so this layer is cached
# across code changes.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --no-install-project

# Then install the registration_api package itself (non-editable).
COPY src ./src
RUN uv sync --frozen --no-dev --no-editable

# Entry point that gunicorn loads.
COPY wsgi.py ./

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

# Cloud Run injects PORT. A single worker keeps one in-memory registration list
# per container; threads handle concurrent requests.
# sh -c expands $PORT; exec makes gunicorn PID 1 so it receives SIGTERM.
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 wsgi:app"]
