[![codecov.io](https://codecov.io/github/pycontw/pycon.tw/coverage.svg?branch=master)](https://codecov.io/github/pycontw/pycon.tw?branch=master)
[![travis-ci status](https://api.travis-ci.org/pycontw/pycon.tw.svg?branch-master)](https://travis-ci.org/pycontw/pycon.tw)

# PyCon TW

This repository serves the website of PyCon TW, Python Conference Taiwan. This project is open source and the license can be found in LICENSE.

## Getting Started

### Requirements

- Git 1.8+
- Python 3.6.x
- Yarn 1.0+
- Node.js 8.0+

### Set up a Development Environment & Run Server

#### Method 1 : `Quick start in 5 minutes`
* [ deploy with .sh and docker ](/document/deploy_docker_dev.md)
#### Method 2 : `Step by step`
* [ deploy in local environment ](/document/deploy_local_env_dev.md)


## Run Tests

Tests are managed with [pytest-django](http://pytest-django.readthedocs.org/en/latest/tutorial.html). You have two options to run tests, either with the local environment, or in an isolated one via [Tox](http://tox.readthedocs.org/en/latest/).


### Testing in the Local Environment

Run the following command inside `src`:

    pytest

To run tests with coverage report:

    pytest --cov=.


### Testing with Tox

Run the following inside the top-level directory (the one with `tox.ini`):

    tox


## How to Contribute

Follow the [GitHub Flow](https://guides.github.com/introduction/flow/), please **DO NOT push the commits into master directly**. Always create branch by the feature you want to update. You are encouraged to submit a pull request for reviewing before merging things into master.

We strongly recommend you configure your editor to match our coding styles. You can do this manually, or use an [EditorConfig plugin](http://editorconfig.org/#download) if your editor supports it. An `.editorconfig` file has already been attached to the repository.


## Deployment

For site administrators, please refer to [document/deploy_docker_prod.md](/document/deploy_docker_prod.md).
