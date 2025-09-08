### Requirements
- Docker Engine 1.13.1+
- Docker Compose v2

# Containerized Development Environment

1. Simply run the following command to start containerized services, this will run both the database and django service for you:
    ```
    make run_dev
    ```

2. If the services are up and running in the first time, you may need to run the following in `pycontw` service in docker shell.

    To get into the docker shell for `pycontw`

    ```
    make shell_dev
    ```

    In the shell, you can run any commands as if you are in a local development environment. Here are some common Django commands:

    ```sh
    # make migrations
    python manage.py makemigrations

    # apply migrations
    python manage.py migrate

    # create a superuser
    python manage.py createsuperuser

    # pull out strings for translations
    python manage.py makemessages -l en_US -l zh_Hant

    # compile translations
    python manage.py compilemessages
    ```
