FROM python:3.11-slim AS base

FROM base AS builder

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  PATH="$PATH:/runtime/bin" \
  POETRY_VERSION=1.3.0

# System deps:
RUN apt-get update && \
  apt-get install -y build-essential unzip wget python-dev-is-python3 git && \
  pip install "poetry==$POETRY_VERSION"

WORKDIR /src

# Generate requirements and install *all* dependencies.
COPY pyproject.toml poetry.lock /src/
RUN poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt && \
  pip install --prefix=/runtime --force-reinstall -r requirements.txt

COPY . /src

FROM base AS runtime
COPY --from=builder /runtime /usr/local
COPY . /app
WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
