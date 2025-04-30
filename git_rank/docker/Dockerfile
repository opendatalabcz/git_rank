FROM python:3.11-slim AS base

FROM base AS builder

ENV PATH="$PATH:/runtime/bin" \
  POETRY_VERSION=1.3.0 \
  PMD_VERSION=7.11.0

# System deps:
RUN apt-get update && \
  apt-get install -y build-essential unzip wget python-dev-is-python3 && \
  pip install "poetry==$POETRY_VERSION"

RUN wget https://github.com/pmd/pmd/releases/download/pmd_releases%2F${PMD_VERSION}/pmd-dist-${PMD_VERSION}-bin.zip && \
  unzip pmd-dist-${PMD_VERSION}-bin.zip -d /runtime && \
  mv /runtime/pmd-bin-${PMD_VERSION} /runtime/pmd-bin

WORKDIR /src

# Generate requirements and install *all* dependencies.
COPY pyproject.toml poetry.lock /src/
RUN poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt && \
  pip install --prefix=/runtime --force-reinstall -r requirements.txt

COPY . /src

FROM base AS runtime
RUN apt-get update && \
  apt-get install -y default-jre-headless git && \
  apt-get clean

COPY --from=builder /runtime /usr/local
COPY . /app
WORKDIR /app

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:/usr/local/pmd-bin/bin

ENTRYPOINT ["/app/entrypoint.sh"]