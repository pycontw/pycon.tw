# Setup the Production Server

The following describes how to run the server in production using Docker.

It assumes that:

1. A database has already been properly setup
2. A reverse proxy is configured to forward requests to the server
(strictly speaking the server will work without a reverse proxy, but performance
will be awful)

How to fulfill the above prerequisite is beyond the scope of this document.


## Requirements

- Git 1.8+
- Docker 17.09+ (since we use `--chown` flag in the COPY directive)


## Build the Container Image

After cloning this repository, and checking-out the correct branch, `cd` into
the directory and run

    docker build -f Dockerfile -t pycontw-2019 .


## Gather Container Environment Variables

There are four configurations that must be set when running the container.

 * `SECRET_KEY` is used to provide cryptographic signing, refer to
   src/pycontw2016/settings/local.sample.env on how to generate secret key
 * `DATABASE_URL` specifies how to connect to the database (in the URL form
   e.g. `postgres://username:password@host_or_ip:5432/database_name`)
 * `EMAIL_URL` specifies how to connect to the mail server
   (e.g. `smtp+tls://username:password@host_or_ip:25`)
 * `DSN_URL` specify how to connect to Sentry error reporting service
   (e.g. `https://key@sentry.io/project`), please refer to
   [Sentry's documentation on how to obtain Data Source Name](https://docs.sentry.io/error-reporting/quickstart/?platform=python)
 * (optional) `GA_TRACK_ID` specify the Google Analytics ID for the website
 * (optional) `GTM_TRACK_ID` specify the Google Google Tag Manager ID for the
   website
 * (optional) `SLACK_WEBHOOK_URL`

For demonstration purpose, we'll use dummy values for the above container
environment variables from here on, **please change them to according to your environment**.


## Get Ready for Production

Migrate the database to the latest schema

    docker run --rm \
      -e DJANGO_SETTINGS_MODULE='pycontw2016.settings.production.pycontw2019' \
      -e SECRET_KEY='not_really_a_secret' \
      -e DATABASE_URL='postgres://username:password@host_or_ip:5432/database_name' \
      -e EMAIL_URL='smtp+tls://username:password@host_or_ip:25' \
      -e DSN_URL='https://key@sentry.io/project' \
      pycontw-2019 \
      python3 manage.py migrate

Generate the static assets (e.g. javascript, CSS)

    docker run --rm \
      -e DJANGO_SETTINGS_MODULE='pycontw2016.settings.production.pycontw2019' \
      -e SECRET_KEY='not_really_a_secret' \
      -e DATABASE_URL='postgres://username:password@host_or_ip:5432/database_name' \
      -e EMAIL_URL='smtp+tls://username:password@host_or_ip:25' \
      -e DSN_URL='https://key@sentry.io/project' \
      --mount type=volume,src=pycontw-2019-static,dst=/usr/local/app/src/assets \
      pycontw-2019 \
      python3 manage.py collectstatic --no-input


# Run the Production Server

Run the production server container with automatic restart across failures and reboots

    docker run \
      --name=pycontw-2019 \
      --detach \
      --restart=always \
      -e DJANGO_SETTINGS_MODULE='pycontw2016.settings.production.pycontw2019' \
      -e SECRET_KEY='not_really_a_secret' \
      -e DATABASE_URL='postgres://username:password@host_or_ip:5432/database_name' \
      -e EMAIL_URL='smtp+tls://username:password@host_or_ip:25' \
      -e DSN_URL='https://key@sentry.io/project' \
      --mount type=volume,src=pycontw-2019-media,dst=/usr/local/app/src/media \
      --mount type=volume,src=pycontw-2019-static,dst=/usr/local/app/src/assets \
      pycontw-2019

