## Getting Started

### Requirements

- Git 1.8+
- Python 3.6.x
- Yarn 1.0+
- Node.js 8.0+

### Set up a Virtual Environment

#### Database - Docker (Optional)

Write database password in .env:

    POSTGRES_PASSWORD=somepassword

Define .env location in docker-compose-db.yml under the corresponding database service:

    services:
      db:
        image: postgres:11-alpine
        env_file:
          - .env

Create and start the database for development:

    docker-compose -f docker-compose-db.yml up

#### Python - Built-in `venv`

Create your virtual environment:

    python3 -m venv venv

And enable it:

    . venv/bin/activate

#### Python - [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org)

You need to specify your python path when creating the virtual environment:

    mkvirtualenv --python=$(which python3) pycontw2016

#### Node.js - [nvm](https://github.com/creationix/nvm)

Switch to version specified in `.nvmrc`:

    nvm use

### Install Dependencies

Use pip to install Python depedencies:

    pip install -r requirements.txt

Use Yarn to install Node dependencies:

    yarn install --dev

### Set up Local Environment Variables for Database

Settings are stored in environment variables via [django-environ](http://django-environ.readthedocs.org/en/latest/). The quickest way to start is to copy `local.sample.env` into `local.env`:

    cp src/pycontw2016/settings/local.sample.env src/pycontw2016/settings/local.env

Default is sqlite3, you can change to connect `postgres`. Copy `local.sample.env` and change its parameters to your personal setting.
Then edit the `SECRET_KEY` line in `local.env`, replacing `{{ secret_key }}` into any [Django Secret Key](http://www.miniwebtool.com/django-secret-key-generator/) value. An example:

    SECRET_KEY=twvg)o_=u&@6^*cbi9nfswwh=(&hd$bhxh9iq&h-kn-pff0&&3

If you’re using a database for the first time, create a database named `pycontw2016` owned by the database user specified in the env file:

> Enter pycontw_db_1 container
```cmd
docker exec -it pycontw_db_1 psql -U postgres
```

```sql
# Replace "postgres" with your specified role.
CREATE DATABASE pycontw2016 with owner = postgres;
```

After that, just run the migration.

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
