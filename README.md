[![codecov.io](https://codecov.io/github/pycontw/pycontw2016/coverage.svg?branch=master)](https://codecov.io/github/pycontw/pycontw2016?branch=master)
[![travis-ci status](https://api.travis-ci.org/pycontw/pycontw2016.svg?branch-master)](https://travis-ci.org/pycontw/pycontw2016)

# PyCon TW 2016

This repository serves the website of PyCon TW 2016. This project is open source and the license can be found in LICENSE.

## Getting Started

### Requirements

- Git 1.8+
- Python 3.4+

### Set up a Virtual Environment

#### Built-in `venv`

Create your virtual environment:

    python3 -m venv venv

And enable it:

    . venv/bin/activate

#### [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org)

You need to specify your python path when creating the virtual environment:

    mkvirtualenv --python=$(which python3) pycontw2016

### Install Dependencies

Just use pip:

    pip install -r requirements.txt

### Set up Local Environment Variables and Database

Settings are stored in environment variables via [django-environ](http://django-environ.readthedocs.org/en/latest/). The quickiest way to start is to copy `local.sample.env` into `local.env`:

    cp src/pycontw2016/settings/local.sample.env src/pycontw2016/settings/local.env

Then edit the `SECRET_KEY` line in `local.env`, replacing `{{ secret_key }}` into any [Django Secret Key](http://www.miniwebtool.com/django-secret-key-generator/) value. An example:

    SECRET_KEY=twvg)o_=u&@6^*cbi9nfswwh=(&hd$bhxh9iq&h-kn-pff0&&3

After that, just run the migration

### Get Ready for Development

`cd` into the `src` directory:

    cd src

And migrate the database:

    python manage.py migrate

Now you’re all set!

## Run the Development Server

    python manage.py runserver

## Run Tests

Tests are managed with [pytest-django](http://pytest-django.readthedocs.org/en/latest/tutorial.html). You have two options to run tests, either with the local environment, or in an isolated one via [Tox](http://tox.readthedocs.org/en/latest/).


### Testing in the Local Environment

Run the following command inside `src`:

    py.test

To run tests with coverage report:

    py.test --cov=.


### Testing with Tox

Run the following inside the top-level directory (the one with `tox.ini`):

    tox


## Setup the Production Server

The following describes how to run the server in production using Docker.

It assumes that:

1. A database has already been properly setup
2. A reverse proxy is configured to forward requests to the server
(strictly speaking the server will work without a reverse proxy, but performance will be awful)

How to fulfill the above prerequisite is beyond the scope of this document.


### Requirements

- Git 1.8+
- Docker 17.09+ (since we use `--chown` flag in the COPY directive)


### Build the Container Image

After cloning this repository, and checking-out the correct branch, `cd` into the directory and run

    docker build -f Dockerfile -t pycontw-2016 .


### Gather Container Environment Variables

There are four configurations that must be set when running the container.

 * `SECRET_KEY` is used to provide cryptographic signing, refer to src/pycontw2016/settings/local.sample.env on how to generate
 * `DATABASE_URL` specifies how to connect to the database (in the URL form e.g. `postgres://username:password@host_or_ip:5432/database_name`)
 * `EMAIL_URL` specifies how to connect to the mail server (e.g. `smtp+tls://username:password@host_or_ip:25`)
 * `DSN_URL` specify how to connect to Sentry error reporting service (e.g. `https://key@sentry.io/project`), please refer to [Sentry's documentation on how to obtain Data Source Name](https://docs.sentry.io/error-reporting/quickstart/?platform=python)

For demonstration purpose, we'll use dummy values for the above container environment variables from here on, **please change them to according to your environment**.


### Get Ready for Production

Generate the static assets (e.g. javascript, CSS)

    docker run --rm \
      -e DJANGO_SETTINGS_MODULE='pycontw2016.settings.production' \
      -e SECRET_KEY='not_really_a_secret' \
      -e DATABASE_URL='postgres://username:password@host_or_ip:5432/database_name' \
      -e EMAIL_URL='smtp+tls://username:password@host_or_ip:25' \
      -e DSN_URL='https://key@sentry.io/project' \
      --mount type=volume,src=pycontw-2016-media,dst=/usr/local/app/src/media \
      --mount type=volume,src=pycontw-2016-static,dst=/usr/local/app/src/assets \
      pycontw-2016 \
      python3 manage.py collectstatic --no-input

Migrate the database to the latest schema

    docker run --rm \
      -e DJANGO_SETTINGS_MODULE='pycontw2016.settings.production' \
      -e SECRET_KEY='not_really_a_secret' \
      -e DATABASE_URL='postgres://username:password@host_or_ip:5432/database_name' \
      -e EMAIL_URL='smtp+tls://username:password@host_or_ip:25' \
      -e DSN_URL='https://key@sentry.io/project' \
      --mount type=volume,src=pycontw-2016-media,dst=/usr/local/app/src/media \
      --mount type=volume,src=pycontw-2016-static,dst=/usr/local/app/src/assets \
      pycontw-2016 \
      python3 manage.py migrate


## Run the Production Server

Run the production server container with automatic restart across failures and reboots

    docker run \
      --name=pycontw-2016 \
      --detach \
      --restart=always \
      -e DJANGO_SETTINGS_MODULE='pycontw2016.settings.production' \
      -e SECRET_KEY='not_really_a_secret' \
      -e DATABASE_URL='postgres://username:password@host_or_ip:5432/database_name' \
      -e EMAIL_URL='smtp+tls://username:password@host_or_ip:25' \
      -e DSN_URL='https://key@sentry.io/project' \
      --mount type=volume,src=pycontw-2016-media,dst=/usr/local/app/src/media \
      --mount type=volume,src=pycontw-2016-static,dst=/usr/local/app/src/assets \
      pycontw-2016


## How to Contribute

Follow the [GitHub Flow](https://guides.github.com/introduction/flow/), please **DO NOT push the commits into master directly**. Always create branch by the feature you want to update. You are encouraged to submit a pull request for reviewing before merging things into master.

We strongly recommend you configure your editor to match our conding styles. You can do this manually, or use an [EditorConfig plugin](http://editorconfig.org/#download) if your editor supports it. An `.editorconfig` file has already been attached to the repository.


## Internationalisation

Translations are hosted on [Transifex](https://www.transifex.com/pycon-taiwan/pycon-tw-2016/). When new commits are added into master branch, Travis CI will automatically push new translation strings to Transifex, so simply fix or edit the translation online.

### Update translation

Translation updates into code base are done **manually** under `src/`. You need to [configure the Transifex client](http://docs.transifex.com/client/config/) first by adding the file `~/.transifexrc`.

Old translation files will stop `tx pull` updating if they have later modified time, which they generally have when they are pulled from the remote repo. So old translation files should be removed first:

    rm locale/zh_Hant/LC_MESSAGES/django.*

Run `tx pull` to get newer translation and recompile the PO files:

    tx pull -l zh-Hant
    python manage.py compilemessages -l zh_Hant
