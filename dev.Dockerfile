# [Node Stage to get node_modolues and node dependencies]
FROM node:8.16.0-buster-slim as node_stage

COPY ./yarn.lock yarn.lock
COPY ./package.json package.json

RUN apt-get update
RUN apt-get install python-pip -y

RUN npm install -g yarn
RUN yarn install --dev --frozen-lockfile

# [Python Stage for Django web server]
FROM python:3.10.14-slim-bullseye as python_stage

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Infrastructure tools
# gettext is used for django to compile .po to .mo files.
RUN apt-get update
RUN apt-get install -y \
    libpq-dev \
    gcc \
    zlib1g-dev \
    libjpeg62-turbo-dev \
    mime-support \
    gettext \
    libxml2-dev \
    libxslt-dev

# Install Poetry
RUN pip install --no-cache-dir pip==23.3.2 && \
    pip install --no-cache-dir poetry==1.8.2

# Install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root && \
    yes | poetry cache clear --all pypi

# Add poetry bin directory to PATH
ENV PATH="${WORKDIR}/.venv/bin:$PATH"

COPY --from=node_stage /node_modules ./node_modules
COPY --from=node_stage /usr/local/bin/node /usr/local/bin/node
