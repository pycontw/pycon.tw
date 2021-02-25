### Requirements
- Docker Engine 1.13.1+
- Docker Compose 1.10.0+

# Containerized Development Environment

1. Edit the `DATABASE_URL` in `src/pycontw2016/settings/local.env`(Copy from [`local.sample.env`](../src/pycontw2016/settings/local.sample.env)). Use the Postgres username, password, database name, and port configured in [`./docker-compose-dev.yml`](../docker-compose-dev.yml).

    ```
    DATABASE_URL=postgres://postgres:secretpostgres@db:5432/pycontw2016
    ```

2. Simply run the following command to install all dependencies, activate a containerized Postgres server, and run the Django server (<code>ctrl+c</code> to stop).

    ```
    ./enter_dev_env.sh
    ```
