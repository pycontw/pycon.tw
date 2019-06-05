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
 * (optional) `SLACK_WEBHOOK_URL`

Write them in a [`.env` file](https://docs.docker.com/compose/env-file/) at the same directory that contains
`docker-compose.yml`.

# Run the Production Server

Run the production server container:

    docker-compose start
