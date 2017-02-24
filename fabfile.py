# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys

from fabric.api import cd, run, sudo, lcd, local
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
        run('~/.virtualenvs/{0}/bin/pip install -r '
            'requirements/production.txt'.format(VIRTUALENV_NAME))


def migrate_db():
    with cd(DJANGO_DIR):
        run('source {0}/env.sh && ~/.virtualenvs/{1}/bin/python '
            'manage.py migrate'.format(PROJECT_DIR, VIRTUALENV_NAME))


def pull_repo():
    with cd(PROJECT_DIR):
        run('git pull origin master')


def restart_services():
    sudo('supervisorctl restart {0}'.format(SUPERVISOR_NAME))
    sudo('service nginx restart')


def collectstatic():
    with cd(DJANGO_DIR):
        run('source {0}/env.sh && ~/.virtualenvs/{1}/bin/python '
            'manage.py collectstatic --noinput -c'.format(
                PROJECT_DIR, VIRTUALENV_NAME,
            ))


def compile_translations():
    with cd(DJANGO_DIR):
        # run('~/.virtualenvs/{0}/bin/tx pull'.format(VIRTUALENV_NAME))
        run('~/.virtualenvs/{0}/bin/python manage.py compilemessages'.format(
            VIRTUALENV_NAME,
        ))


def clean_local_untracked_translation():
    # Fix local git changes when only .po files are committed
    # but .mo files are not.
    with cd(PROJECT_DIR):
        run('git checkout -- src/locale/')


@task
def deploy():
    clean_local_untracked_translation()
    pull_repo()
    install_requirements()
    collectstatic()
    migrate_db()
    compile_translations()
    restart_services()


def write_transifex_config():
    """Used to setup Travis for Transifex push.
    """
    transifexrc_path = os.path.expanduser('~/.transifexrc')
    if os.path.exists(transifexrc_path):
        return
    with open(transifexrc_path, 'w') as f:
        f.write((
            '[https://www.transifex.com]\n'
            'hostname = https://www.transifex.com\n'
            'password = {password}\n'
            'token = \n'
            'username = pycontw\n'
        ).format(password=os.environ['TRANSIFEX_PASSWORD']))


@task
def pull_tx():
    with lcd('src'):
        local("ls locale/*/LC_MESSAGES/django.* | "
              "grep '^locale/[^_]' | "
              "xargs rm")
        local('tx pull -a')
        local('python manage.py compilemessages -x _src')


@task
def push_tx():
    with lcd('src'):
        local('python manage.py makemessages -a')
        local('tx push -s')


@task
def travis_push_transifex():
    if os.getenv('TRAVIS_PULL_REQUEST') != 'false':
        print('Build triggered by a pull request. Transifex push skipped.',
              file=sys.stderr)
        return
    current_branch = os.getenv('TRAVIS_BRANCH')
    target_branch = 'master'
    if current_branch != target_branch:
        print('Branch {cur} is not {target}. Transifex push skipped.'.format(
            cur=current_branch, target=target_branch,
        ), file=sys.stderr)
        return
    write_transifex_config()
    push_tx()
