#!/bin/sh
echo 'Run migration'
python3 /app/src/manage.py migrate
echo 'Create super user'
python3 /app/src/manage.py createsuperuser --noinput || echo "Super user already created"
echo 'Compile localized translation'
python3 /app/src/manage.py compilemessages
exec "$@"
