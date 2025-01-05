## Local Environment Setup

### Requirements
- Docker Engine 1.13.1+
- Docker Compose v2
- nvm
- poetry

### 0 - Database - Docker (Optional)
Create and start the database for development:

    make run_db

This will create a postgres database with the following existed:
```
database_name=pycontw2016
username=postgres
password=secretpostgres
port=5432
```
And the database connection url will be `postgres://postgres:secretpostgres@localhost:5432/pycontw2016`

If you plan to serve your own database server, you will need to modify `DATABASE_URL` in the next section.

### 1- Set up Local Environment Variables

Settings are stored in environment variables via [django-environ](http://django-environ.readthedocs.org/en/latest/). The quickest way to start is to copy `local.sample.env` into `local.env`:

    cp src/pycontw2016/settings/local.sample.env src/pycontw2016/settings/local.env

Then edit the `SECRET_KEY` line in `local.env`, replacing `{{ secret_key }}` into any [Django Secret Key](http://www.miniwebtool.com/django-secret-key-generator/) value. An example:

    SECRET_KEY=twvg)o_=u&@6^*cbi9nfswwh=(&hd$bhxh9iq&h-kn-pff0&&3


#### 2 - Install environment (Python and Node Modules)
Init environment, including installing dependencies

    make init

Activate the python environment in your terminal

    poetry shell

### 3 - Get Ready for Development

`cd` into the `src` directory:

    cd src

#### 4 - Migrate the database:

    python manage.py migrate

#### 5 - Create Super User

    python manage.py createsuperuser

#### 6 - Compile localized translation

    python manage.py compilemessages

Now you’re all set!

#### 7 - Run the Development Server

    python manage.py runserver

## Subsequent Development

Step 1 ~ 6 are (mostly) one-time thing, in subsequent development, you may want to
speed up the process of running your application. Use

    make run_local

to quick launch your local server. Then develop your logic as it may.

If you missed out the steps in above section, just run `poetry shell` and `cd src` then execute those commands when needed.
