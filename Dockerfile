# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim AS python-base
ARG TEST_ENV

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_CACHE_DIR=/.cache \
    WORKERS=1 \
    THREADS=2

# Update the base OS
RUN --mount=type=cache,target="/var/cache/apt",sharing=locked \
    --mount=type=cache,target="/var/lib/apt/lists",sharing=locked \
    set -eux; \
    apt-get update; \
    apt-get upgrade -y; \
    apt install --no-install-recommends -y  \
        git build-essential gcc zlib1g-dev libjpeg-dev; \
    apt-get autoremove -y

RUN pip install uv; uv venv

# install base requirements
COPY requirements-base.txt .
RUN --mount=type=cache,target=${PIP_CACHE_DIR},sharing=locked \
    uv pip install -r requirements-base.txt

# install custom requirements
COPY requirements.txt .
RUN --mount=type=cache,target=${PIP_CACHE_DIR},sharing=locked \
    uv pip install -r requirements.txt

# install test requirements if needed
COPY requirements-test.txt .
# build only when TEST_ENV="true"
RUN --mount=type=cache,target=${PIP_CACHE_DIR},sharing=locked \
    if [ "$TEST_ENV" = "true" ]; then \
      uv pip install -r requirements-test.txt; \
    fi
RUN apt update; apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx

COPY . .
RUN uv pip install -e label-studio-ml-backend/

EXPOSE 9090

ENV VIRTUAL_ENV=/app/.venv/
ENV PATH=/app/.venv/bin:$PATH

# uncomment for better debugging
# CMD label-studio-ml start .
CMD gunicorn --preload --bind :9090 --workers $WORKERS --threads $THREADS --timeout 0 _wsgi:app
