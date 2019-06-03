FROM python:3.5

ENV TINI_VERSION=v0.18.0
ENV PYTHONUNBUFFERED 1
ENV BASE_DIR /usr/local
ENV APP_DIR $BASE_DIR/app
ENV VENV_DIR $BASE_DIR/venv

RUN wget -O /tini "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-amd64" \
 && chmod +x /tini \
 && apt-get update \
 && apt-get install -y wait-for-it \
 && adduser --system --disabled-login docker \
 && mkdir -p "$BASE_DIR" "$APP_DIR" "$APP_DIR/src/assets" "$APP_DIR/src/media" "$VENV_DIR" \
 && chown -R docker:nogroup "$BASE_DIR" "$APP_DIR" "$VENV_DIR"

USER docker

# Only copy and install requirements to improve caching between builds
COPY --chown=docker:nogroup ./requirements $APP_DIR/requirements
RUN python3 -m venv $VENV_DIR \
 && "$VENV_DIR/bin/pip3" install -r "$APP_DIR/requirements/production.txt" \
 && "$VENV_DIR/bin/python3" -m compileall \
 && "$VENV_DIR/bin/python3" -m compileall "$VENV_DIR/lib"

# Enable the virtual environment manually
ENV VIRTUAL_ENV "$VENV_DIR"
ENV PATH "$VENV_DIR/bin:$PATH"

# Pre-compile .py files in project to improve start-up speed
COPY --chown=docker:nogroup ./src $APP_DIR/src
RUN "$VENV_DIR/bin/python3" -m compileall "$APP_DIR/src"

# Finally, copy all the project files
COPY --chown=docker:nogroup . $APP_DIR

WORKDIR $APP_DIR/src
VOLUME $APP_DIR/src/media
EXPOSE 8000
ENTRYPOINT "$VENV_DIR/bin/python3"

