FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV BASE_DIR /usr/local
ENV APP_DIR $BASE_DIR/app
ENV VENV_DIR $BASE_DIR/venv

RUN apt-get update \
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
 && "$VENV_DIR/bin/python3" -m compileall "$VENV_DIR/lib" -x 'dbfpy/dbfnew\.py'

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
CMD ["uwsgi", "--http-socket", ":8000", "--master", "--hook-master-start", \
     "unix_signal:15 gracefully_kill_them_all", "--static-map", \
     "/static=assets", "--static-map", "/media=media", "--mount", \
     "/2017=pycontw2016/wsgi.py", "--manage-script-name", "--offload-threads", \
     "2"]
