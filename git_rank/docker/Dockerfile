FROM python:3.11-slim AS base

# ------------- Build stage --------------------
FROM base AS builder
ENV PATH="$PATH:/runtime/bin" \
  POETRY_VERSION=1.3.0 \
  PMD_VERSION=7.11.0

# System dependencies
RUN apt-get update && \
  apt-get install -y build-essential unzip wget python-dev-is-python3 && \
  pip install "poetry==$POETRY_VERSION"

# PMD Java Linter
RUN wget https://github.com/pmd/pmd/releases/download/pmd_releases%2F${PMD_VERSION}/pmd-dist-${PMD_VERSION}-bin.zip && \
  unzip pmd-dist-${PMD_VERSION}-bin.zip -d /runtime && \
  mv /runtime/pmd-bin-${PMD_VERSION} /runtime/pmd-bin

WORKDIR /src

# Generate requirements and install *all* dependencies
COPY pyproject.toml poetry.lock /src/
RUN poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt && \
  pip install --prefix=/runtime --force-reinstall -r requirements.txt

COPY . /src

# ------------- Runtime stage --------------------
FROM base AS runtime
ENV JAVA_HOME=/usr/lib/jvm/default-java \
  PATH=$PATH:/usr/local/pmd-bin/bin:~/.dotnet/tools \
  ROSLYNATOR_VERSION=0.10.1

# Install Java runtime for PMD and git for GitPython
RUN apt-get update && \
  apt-get install -y default-jre-headless git wget && \
  apt-get clean

# Install dotnet runtime for Roslynator linter
RUN wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
  dpkg -i packages-microsoft-prod.deb && \ 
  rm packages-microsoft-prod.deb && \
  apt-get update && \
  apt-get install -y dotnet-sdk-9.0 && \
  apt-get clean && \
  dotnet tool install roslynator.dotnet.cli --version ${ROSLYNATOR_VERSION} --tool-path /usr/local/bin

# #Scripted install for dotnet
# #replaces apt-get install -y dotnet-sdk-9.0 in case of processor architecture issues (MacOS)
# #From https://learn.microsoft.com/en-us/dotnet/core/install/linux-scripted-manual#scripted-install
# RUN wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh \
# && chmod +x ./dotnet-install.sh \
# && ./dotnet-install.sh --channel 9.0 --version latest --install-dir /usr/local/dotnet \
# && rm ./dotnet-install.sh 
# ENV DOTNET_ROOT=/usr/local/dotnet
# ENV PATH=$PATH:$DOTNET_ROOT
# RUN dotnet tool install roslynator.dotnet.cli --version ${ROSLYNATOR_VERSION} --tool-path /usr/local/bin

COPY --from=builder /runtime /usr/local
COPY . /app
WORKDIR /app

RUN useradd -r -m git_rank_service && \
  chown -R git_rank_service /app
USER git_rank_service

ENTRYPOINT ["/app/entrypoint.sh"]