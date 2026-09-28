# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.2
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install dependencies from pyproject.toml (this project has no requirements.txt).
# Copy only packaging metadata + source first so dependency layers cache well.
COPY pyproject.toml .
COPY src/ ./src/
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install .

# Switch to the non-privileged user to run the application.
USER appuser

# Expose the port that the application listens on.
EXPOSE 8083

# Package is installed as communicator_client (src layout), not src.communicator_client.
CMD ["uvicorn", "communicator_client.local_api.app:app", "--host=0.0.0.0", "--port=8080"]
