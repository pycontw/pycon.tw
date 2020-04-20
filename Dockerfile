FROM python:3.6-buster

ENV PYTHONUNBUFFERED 1
ENV BASE_DIR /usr/local
ENV APP_DIR $BASE_DIR/app

ENV NVM_INSTALLER_URL https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh
ENV NVM_DIR $BASE_DIR/nvm
ENV YARN_VERSION 1.15.2-1
ENV NODE_VERSION 8.16.0

# make nodejs and yarn accessible and executable globally
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
# Add bin directory used by `pip install --user`
ENV PATH "/home/docker/.local/bin:${PATH}"

# Infrastructure tools
# gettext is used for django to compile .po to .mo files.
RUN apt-get update
RUN apt-get install apt-utils -y
RUN apt-get update
RUN apt-get install gettext python3-pip -y

# Install Node and Yarn from upstream
RUN curl -o- $NVM_INSTALLER_URL | bash \
 && . $NVM_DIR/nvm.sh \
 && nvm install $NODE_VERSION \
 && nvm alias default $NODE_VERSION \
 && nvm use default \
 && nvm --version \
 && npm install -g yarn \
 && yarn --version

# APP directory setup
RUN adduser --system --disabled-login docker \
 && mkdir -p "$BASE_DIR" "$APP_DIR" "$APP_DIR/src/assets" "$APP_DIR/src/media" \
 && chown -R docker:nogroup "$BASE_DIR" "$APP_DIR"

USER docker
WORKDIR $APP_DIR

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
     "--mount", "/2020=pycontw2016/wsgi.py", "--manage-script-name", \
     "--offload-threads", "2"]
