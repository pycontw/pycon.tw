# -*- coding: utf-8 -*-

import os

from fabric.api import cd, run, sudo
from fabric.api import task
from fabric.api import env

env.forward_agent = True


PROJECT_DIR = os.environ.get('PROJECT_DIR', '')
PROJECT_NAME = os.environ.get('PROJECT_NAME', '')
DJANGO_DIR = PROJECT_DIR + '/' + PROJECT_NAME

VIRTUALENV_NAME = os.environ.get('VIRTUALENV_NAME', '')
SUPERVISOR_NAME = os.environ.get('SUPERVISOR_NAME', '')


def upgrade_system():
    sudo('apt-get update -y')


def install_requirements():
    with cd(PROJECT_DIR):
        run('~/.virtualenvs/{0}/bin/pip install -r requirements/production.txt'.format(VIRTUALENV_NAME))


def migrate_db():
    with cd(DJANGO_DIR):
        run('source {0}/env.sh && ~/.virtualenvs/{1}/bin/python manage.py migrate'.format(PROJECT_DIR, VIRTUALENV_NAME))


def pull_repo():
    with cd(PROJECT_DIR):
        run('git pull origin master')


def restart_services():
    sudo('supervisorctl restart {0}'.format(SUPERVISOR_NAME))
    sudo('service nginx restart')


def collectstatic():
    with cd(DJANGO_DIR):
        run('source {0}/env.sh && ~/.virtualenvs/{1}/bin/python manage.py collectstatic --noinput -c'.format(PROJECT_DIR, VIRTUALENV_NAME))


@task
def deploy():
    pull_repo()
    install_requirements()
    collectstatic()
    migrate_db()
    restart_services()
