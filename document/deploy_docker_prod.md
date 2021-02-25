# Setup the Production Server

The following describes how to run the server in production using Docker
Compose.

## Requirements

- Git 1.8+
- Docker 17.09+ (since we use `--chown` flag in the COPY directive)
- Docker Compose


## Gather Container Environment Variables

There are four configurations that must be set when running the container.

 * `SECRET_KEY` is used to provide cryptographic signing, refer to
   src/pycontw2016/settings/local.sample.env on how to generate secret key
 * `MEDIA_ROOT` specifies where media files (user-uploaded assets) are stored
   in the host. This will be mounted into the container.
 * `DATABASE_URL` specifies how to connect to the database (in the URL form
   e.g. `postgres://username:password@host_or_ip:5432/database_name`)
 * `EMAIL_URL` specifies how to connect to the mail server
   (e.g. `smtp+tls://username:password@host_or_ip:25`)
 * `DSN_URL` specify how to connect to Sentry error reporting service
   (e.g. `https://key@sentry.io/project`), please refer to
   [Sentry's documentation on how to obtain Data Source Name](https://docs.sentry.io/error-reporting/quickstart/?platform=python)
 * (optional) `GTM_TRACK_ID`
 * (optional) `SLACK_WEBHOOK_URL`

Write them in a [`.env` file](https://docs.docker.com/compose/env-file/) at the same directory that contains
`docker-compose.yml`.

## Deploying Associated Services

To deploy the website, we also need the following two service (at least):

  * [Nginx service for PyCon Taiwan website](https://github.com/pycontw/pycontw-nginx)
  * [PostgreSQL service for PyCon Taiwan website](https://github.com/pycontw/pycontw-postgresql)

Firstly, fetch the `docker-compose.yaml` files from the above links of the Nginx and PostgreSQL service respectively, and then deploy the PostgresSQL service by

```
# cd pycontw-postgresql
docker-compose up --build -d
```

and then deploy the Nginx service by

```
# cd pycontw-nginx
docker-compose up --build -d
```

If your docker processes are up correctly by checking `docker container ls`, you are ready to deploy the website like

```
docker-compose stop ; docker-compose rm -f ; docker-compose pull ; docker-compose up --build -d
```

You may skip the part of `docker-compose stop`, `docker-compose rm -f`, and `docker-compose pull` if you are build from scratch so there is no pre-existing pycontw website containers.

# Run the Production Server

Run the production server container:

    docker-compose start
