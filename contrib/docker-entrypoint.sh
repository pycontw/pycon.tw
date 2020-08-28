#!/bin/sh
echo 'Run migration'
python3 /app/src/manage.py migrate
echo 'Create super user'
python3 /app/src/manage.py createsuperuser --noinput || echo "Super user already created"
echo 'Inject DB testing data'
python3 /app/src/manage.py loaddata /db-testing-data.json --exclude=users.user
echo 'Compile localized translation'
python3 /app/src/manage.py compilemessages
exec "$@"
