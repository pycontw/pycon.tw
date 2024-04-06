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

ENV PYTHONUNBUFFERED 1

# Infrastructure tools
# gettext is used for django to compile .po to .mo files.
RUN apt-get update
RUN apt-get install -y \
    libpq-dev \
    gcc \
    zlib1g-dev \
    libjpeg62-turbo-dev \
    gettext

# Only copy and install requirements to improve caching between builds
# Install Python dependencies
COPY ./requirements ./requirements
RUN pip3 install -r ./requirements/dev.txt

COPY --from=node_stage /node_modules ./node_modules
COPY --from=node_stage /usr/local/bin/node /usr/local/bin/node

# for entry point
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
