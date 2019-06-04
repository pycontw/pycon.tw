FROM python:3.6

# NodeJS's version is not pinned becuase nodesource only serve the latest
# version.
ENV YARN_VERSION 1.15.2-1
ENV PYTHONUNBUFFERED 1
ENV BASE_DIR /usr/local
ENV APP_DIR $BASE_DIR/app

# Install Node and Yarn from upstream
RUN curl -sS https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - \
 && echo 'deb http://deb.nodesource.com/node_8.x stretch main' | tee /etc/apt/sources.list.d/nodesource.list \
 && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
 && echo 'deb http://dl.yarnpkg.com/debian/ stable main' | tee /etc/apt/sources.list.d/yarn.list \
 && apt-get update \
 && apt-get install -y nodejs yarn=$YARN_VERSION \
 && rm -rf /var/lib/apt/lists/*
RUN adduser --system --disabled-login docker \
 && mkdir -p "$BASE_DIR" "$APP_DIR" "$APP_DIR/src/assets" "$APP_DIR/src/media" \
 && chown -R docker:nogroup "$BASE_DIR" "$APP_DIR"

USER docker
WORKDIR $APP_DIR
# Add bin directory used by `pip install --user`
ENV PATH "/home/docker/.local/bin:${PATH}"

# Only copy and install requirements to improve caching between builds
# Install Python dependencies
COPY --chown=docker:nogroup ./requirements $APP_DIR/requirements
RUN pip3 install --user -r "$APP_DIR/requirements/production.txt" \
 && rm -rf $HOME/.cache/pip/*
# Install Javascript dependencies
COPY --chown=docker:nogroup ./package.json $APP_DIR/package.json
COPY --chown=docker:nogroup ./yarn.lock $APP_DIR/yarn.lock
RUN yarn install --dev --frozen-lockfile \
 && rm -rf $HOME/.cache/yarn/*
# Finally, copy all the project files along with source files
COPY --chown=docker:nogroup . $APP_DIR

WORKDIR $APP_DIR/src
VOLUME $APP_DIR/src/media
EXPOSE 8000
CMD ["uwsgi", "--http-socket", ":8000", "--master", \
     "--hook-master-start", "unix_signal:15 gracefully_kill_them_all", \
     "--static-map", "/static=assets", "--static-map", "/media=media", \
     "--mount", "/2019=pycontw2016/wsgi.py", "--manage-script-name", \
     "--offload-threads", "2"]
