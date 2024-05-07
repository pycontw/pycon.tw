# [Node Stage to get node_modolues and node dependencies]
FROM node:8.16.0-buster-slim as node_base
# [Python Stage for Django web server]
FROM python:3.10.14-slim-bullseye as python_base

FROM node_base as node_dependencies
COPY ./yarn.lock yarn.lock
COPY ./package.json package.json

RUN apt-get update
RUN apt-get install python-pip -y

RUN npm install -g yarn
RUN yarn install --dev --frozen-lockfile && yarn cache clean

FROM python_base as python_dependencies

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV BASE_DIR /usr/local
ENV APP_DIR $BASE_DIR/app


# Infrastructure tools
# gettext is used for django to compile .po to .mo files.
RUN apt-get update
RUN apt-get upgrade -y 
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
RUN poetry install --no-root --only main && \
    yes | poetry cache clear --all pypi

# Add poetry bin directory to PATH
ENV PATH="${WORKDIR}/.venv/bin:$PATH"

COPY --from=node_dependencies /node_modules $APP_DIR/node_modules
COPY --from=node_dependencies /usr/local/bin/node /usr/local/bin/node

# Make nodejs accessible and executable globally
ENV NODE_PATH $APP_DIR/node_modules/

FROM python_dependencies as dev
RUN poetry install --no-root --only dev


FROM python_dependencies as prod
# APP directory setup
RUN adduser --system --disabled-login docker \
 && mkdir -p "$BASE_DIR" "$APP_DIR" "$APP_DIR/src/assets" "$APP_DIR/src/media" \
 && chown -R docker:nogroup "$BASE_DIR" "$APP_DIR"

# Finally, copy all the project files along with source files
COPY --chown=docker:nogroup ./ $APP_DIR

USER docker

WORKDIR $APP_DIR/src
VOLUME $APP_DIR/src/media
EXPOSE 8000
CMD ["uwsgi", "--http-socket", ":8000", "--master", \
     "--hook-master-start", "unix_signal:15 gracefully_kill_them_all", \
     "--static-map", "/static=assets", "--static-map", "/media=media", \
     "--mount", "/2024=pycontw2016/wsgi.py", "--manage-script-name", \
     "--offload-threads", "2"]
