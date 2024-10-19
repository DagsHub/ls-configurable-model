# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12
ARG USE_PIP_CACHE=true

FROM python:${PYTHON_VERSION}-slim AS python-base
ARG TEST_ENV

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_CACHE_DIR=/root/.cache/uv \
    WORKERS=1 \
    THREADS=2

# Update the base OS
RUN --mount=type=cache,target="/var/cache/apt",sharing=locked \
    --mount=type=cache,target="/var/lib/apt/lists",sharing=locked \
    set -eux; \
    apt-get update; \
    apt-get upgrade -y; \
    apt install --no-install-recommends -y  \
        git build-essential gcc zlib1g-dev libjpeg-dev libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx; \ 
    apt-get autoremove -y

RUN pip install uv; uv venv

# install base requirements
COPY requirements-base.txt .
RUN if [ "$USE_PIP_CACHE" = "true" ]; then \
      uv pip install -r requirements-base.txt --cache-dir ${PIP_CACHE_DIR}; \
    else \
      uv pip install -r requirements-base.txt; \
    fi

# install custom requirements
COPY requirements.txt .
RUN if [ "$USE_PIP_CACHE" = "true" ]; then \
      uv pip install -r requirements.txt --cache-dir ${PIP_CACHE_DIR}; \
    else \
      uv pip install -r requirements.txt; \
    fi

# install test requirements if needed
COPY requirements-test.txt .
# build only when TEST_ENV="true"
RUN if [ "$TEST_ENV" = "true" ]; then \
    if [ "$USE_PIP_CACHE" = "true" ]; then \
        uv pip install -r requirements-test.txt --cache-dir ${PIP_CACHE_DIR}; \
    else \
        uv pip install -r requirements-test.txt; \
    fi; \
    fi

COPY . .
RUN uv pip install -e label-studio-ml-backend/

EXPOSE 9090

ENV VIRTUAL_ENV=/app/.venv/
ENV PATH=/app/.venv/bin:$PATH

# uncomment for better debugging
# CMD label-studio-ml start .
CMD gunicorn --preload --bind :9090 --workers $WORKERS --threads $THREADS --timeout 0 _wsgi:app
