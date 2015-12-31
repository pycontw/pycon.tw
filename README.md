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

Tests are managed with [pytest-django](http://pytest-django.readthedocs.org/en/latest/tutorial.html). To run tests:

    py.test

To run tests with coverage report:

    py.test --cov=.


## How to Contribute

Follow the [GitHub Flow](https://guides.github.com/introduction/flow/), please **DO NOT push the commits into master directly**. Always create branch by the feature you want to update. You are encouraged to submit a pull request for reviewing before merging things into master.

We strongly recommend you configure your editor to match our conding styles. You can do this manually, or use an [EditorConfig plugin](http://editorconfig.org/#download) if your editor supports it. An `.editorconfig` file has already been attached to the repository.

## Internationalisation

Translations are hosted on [Transifex](https://www.transifex.com/pycon-taiwan/pycon-tw-2016/).
