#!/bin/bash
#
# Docker entrypoint script
#
# Launches Huey task queue worker process in background and launches Django server after configuring database
# and seeding sample test data.
#
# TODO: Use rsupervisord for launching task queue background process or move the task queue to a separate image
#

echo
echo "Hooks - Webhooks manager"
echo

cd /server

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
python manage.py loaddata sample-data-docker

nohup python -u manage.py run_huey > huey.log &

echo
echo "Huey task queue worker started with logs at /server/hey.log"
echo

echo "Starting Hooks Django server at http://localhost:8000/ ..."
echo

python -u manage.py runserver 0.0.0.0:8000 2>&1

exec "$@"
