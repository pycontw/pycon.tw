## Getting Started
### Set up a Virtual Environment

#### Database - Docker (Optional)
Create and start the database for development:

    docker-compose -f docker-compose-dev.yml db up -d

This will create a postgres database with the following existed:
```
database_name=pycontw2016
username=postgres
password=secretpostgres
port=5432
```
And the database connection url will be `postgres://postgres:secretpostgres@localhost:5432/pycontw2016`

#### Install environment using Makefile (Python and Node Modules)
Init environment, including installing dependencies

    make init

Activate the python environment in your terminal

    poetry shell

### Set up Local Environment Variables for Database

Settings are stored in environment variables via [django-environ](http://django-environ.readthedocs.org/en/latest/). The quickest way to start is to copy `local.sample.env` into `local.env`:

    cp src/pycontw2016/settings/local.sample.env src/pycontw2016/settings/local.env

Default is sqlite3, you can change to connect `postgres`. Copy `local.sample.env` and change its parameters to your personal setting.
Then edit the `SECRET_KEY` line in `local.env`, replacing `{{ secret_key }}` into any [Django Secret Key](http://www.miniwebtool.com/django-secret-key-generator/) value. An example:

    SECRET_KEY=twvg)o_=u&@6^*cbi9nfswwh=(&hd$bhxh9iq&h-kn-pff0&&3

### Get Ready for Development

`cd` into the `src` directory:

    cd src

#### Migrate the database:

    python manage.py migrate

#### Create Super User

    python manage.py createsuperuser

#### Compile localized translation

    python manage.py compilemessages

Now you’re all set!

## Run the Development Server

    python manage.py runserver
