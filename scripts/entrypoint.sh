#!/bin/sh

set -e

# Tail the cron log file
cron && tail -f /var/log/cron.log

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py seed

python3 manage.py runserver 0.0.0.0:8000

