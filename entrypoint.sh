#!/bin/bash

echo
echo "Hooks - Webhooks manager"
echo

cd /server

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py loaddata sample-data

nohup python -u manage.py run_huey > huey.log &

echo
echo "Huey task queue worker started with logs at /server/hey.log"
echo

echo "Starting Hooks Django server at http://localhost:8090/ ..."
echo

python -u manage.py runserver 0.0.0.0:8000 2>&1

exec "$@"
