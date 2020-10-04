FROM python:3.6-slim-buster

ENV PYTHONUNBUFFERED 1
WORKDIR /app

ENV BASE_DIR /usr/local

ENV NVM_INSTALLER_URL https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh
ENV NVM_DIR $BASE_DIR/nvm
ENV YARN_VERSION 1.15.2-1
ENV NODE_VERSION 8.16.0

# make nodejs and yarn accessible and executable globally
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Infrastructure tools
# gettext is used for django to compile .po to .mo files.
RUN apt-get update
RUN apt-get install apt-utils -y
RUN apt-get update
RUN apt-get install gettext python3-pip -y
RUN apt-get install postgresql-client -y

# Install Node and Yarn from upstream
RUN curl -o- $NVM_INSTALLER_URL | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default \
    && nvm --version \
    && npm install -g yarn \
    && yarn --version

# Install Python dependencies
COPY ./requirements ./requirements
RUN pip3 install -r ./requirements/dev.txt

# Install Javascript dependencies
COPY ./package.json ./package.json
COPY ./yarn.lock ./yarn.lock
RUN yarn install --dev --frozen-lockfile

# prepare db testing data
COPY ./contrib/db-testing-data.json /db-testing-data.json

# for entry point
COPY ./contrib/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
