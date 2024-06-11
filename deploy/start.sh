#!/bin/bash
echo "Waiting for postgres connection"

while ! nc -z db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

exec "$@"

python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --workers=4 analyst.wsgi:application --bind 0.0.0.0:8000 --timeout 150