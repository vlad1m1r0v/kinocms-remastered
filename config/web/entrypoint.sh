#!/bin/bash
# entrypoint.sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Apply database migrations
python src/manage.py migrate

# Seed data
make seed

# Collect static files
python src/manage.py collectstatic --noinput

exec "$@"
