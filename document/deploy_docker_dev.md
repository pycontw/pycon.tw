# Containerized Development Environment

1. Edit the `DATABASE_URL` in `src/pycontw2016/settings/local.env`(Copy from `local.sample.env`). Use the Postgres username, password, database name, and port in `./docker-compose-dev.yml`.

    ```
    DATABASE_URL=postgres://postgres:secretpostgres@db:5432/pycontw2016
    ```

2. Simply run the following command to install all dependencies, activate a containerized Postgres server, and run the Django server (<code>ctrl+c</code> to stop).

    ```
    ./enter_dev_env.sh
    ```
