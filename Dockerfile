# [Node Stage to get node_modolues and node dependencies]
FROM node:8.16.0-buster-slim as node_stage

COPY ./yarn.lock yarn.lock
COPY ./package.json package.json

RUN npm install -g yarn
RUN yarn install --dev --frozen-lockfile  \
 && rm -rf $HOME/.cache/yarn/*


# [Python Stage for Django web server]
FROM python:3.6-slim-buster as python_stage

COPY --from=node_stage /node_modules /usr/local/lib/node_modules
COPY --from=node_stage /usr/local/bin/node /usr/local/bin/node

ENV PYTHONUNBUFFERED 1
ENV BASE_DIR /usr/local
ENV APP_DIR $BASE_DIR/app

# make nodejs accessible and executable globally
ENV NODE_PATH /usr/local/lib/node_modules/
ENV PATH /usr/local/bin:$PATH

# Add bin directory used by `pip install --user`
ENV PATH /home/docker/.local/bin:$PATH

# Infrastructure tools
# gettext is used for django to compile .po to .mo files.
RUN apt-get update
RUN apt-get install gettext libpq-dev gcc -y

# APP directory setup
RUN adduser --system --disabled-login docker \
 && mkdir -p "$BASE_DIR" "$APP_DIR" "$APP_DIR/src/assets" "$APP_DIR/src/media" \
 && chown -R docker:nogroup "$BASE_DIR" "$APP_DIR"

USER docker

# Only copy and install requirements to improve caching between builds
# Install Python dependencies
COPY --chown=docker:nogroup ./requirements $APP_DIR/requirements
RUN pip3 install --user -r "$APP_DIR/requirements/production.txt" \
 && rm -rf $HOME/.cache/pip/*

# Finally, copy all the project files along with source files
COPY --chown=docker:nogroup ./ $APP_DIR

WORKDIR $APP_DIR/src
VOLUME $APP_DIR/src/media
EXPOSE 8000
CMD ["uwsgi", "--http-socket", ":8000", "--master", \
     "--hook-master-start", "unix_signal:15 gracefully_kill_them_all", \
     "--static-map", "/static=assets", "--static-map", "/media=media", \
     "--mount", "/2024=pycontw2016/wsgi.py", "--manage-script-name", \
     "--offload-threads", "2"]
