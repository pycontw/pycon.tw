[![codecov.io](https://codecov.io/github/pycontw/pycontw2016/coverage.svg?branch=master)](https://codecov.io/github/pycontw/pycontw2016?branch=master)
[![travis-ci status](https://api.travis-ci.org/pycontw/pycontw2016.svg?branch-master)](https://travis-ci.org/pycontw/pycontw2016)

# PyCon TW 2016

[![Join the chat at https://gitter.im/pycontw/pycontw2016](https://badges.gitter.im/pycontw/pycontw2016.svg)](https://gitter.im/pycontw/pycontw2016?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

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
