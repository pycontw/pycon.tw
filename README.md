# PyCon TW 2016

This repository serves the website of PyCon TW 2016. This project is open source and the license can be found in LICENSE.

## Getting Started

### Requirements

- Git 1.8+
- Python 2.7+

### Setting up virtualenv

At first, you should make sure you have [virtualenv](http://www.virtualenv.org/) installed.

then, create your virtualenv:

    virtualenv venv

Second, you need to enable the virtualenv by

    source venv/bin/activate

Install all dependencies:

    pip install -r requirements.txt

### Setting up local environment variables

Settings are stored in environment variables via [django-environ](http://django-environ.readthedocs.org/en/latest/). The quickiest way to start is to rename `local.sample.env` into `local.env`:

    mv src/pycontw2016/settings/local.sample.env src/pycontw2016/settings/local.env

Then edit the SECRET_KEY in local.env file, replace `{{ secret_key }}` into any [Django Secret Key](http://www.miniwebtool.com/django-secret-key-generator/), for example:

    SECRET_KEY=twvg)o_=u&@6^*cbi9nfswwh=(&hd$bhxh9iq&h-kn-pff0&&3

### Run web server

After that, just cd to `src` folder:

    cd src

And run migrate and http server:

    python manage.py migrate
    python manage.py runserver

### Run tests

Tests are managed with [pytest-django](http://pytest-django.readthedocs.org/en/latest/tutorial.html). To run the tests:

    py.test

## How to contribute

Follow the [Github Flow](https://guides.github.com/introduction/flow/), please **DON'T push the commits into master directly**, always create branch by the feature you want to update.
