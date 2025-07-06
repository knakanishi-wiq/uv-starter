# Dockerfile for building a Docker image to deploy a Python application using UV for dependency management.
# This Dockerfile sets up a multi-stage build process. It installs UV to manage Python dependencies and sets up the application environment.
# Python version to use for the base image.
ARG PYTHON_VERSION=3.11

FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS base

# Prevents Python bytecode files from being written to disk
# Ensures that python putputs are sent straight to terminal without buffering.
# Enables the python fault handler
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# Install any image specific requirements, such as curl and the ssh client
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl && \
    apt-get install -y git openssh-client

# Set working directory and expose port.
WORKDIR /app
EXPOSE 8000
# Copy application code to the container.
COPY . /app

# Set up SSH - Add GitHub to known hosts
RUN mkdir -p ~/.ssh && \
    ssh-keyscan github.com >> ~/.ssh/known_hosts

# Install dependencies with UV
RUN --mount=type=ssh uv sync --dev

CMD [ "uv", "run", "python", "backend.app"]
