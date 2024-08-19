#!/bin/sh

echo "Waiting for PostgreSQL to be available..."
while ! pg_isready -h "db" -p 5432 -U "postgres"; do
  sleep 1
done
echo "PostgreSQL is up!"

echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate
python manage.py update_status
python manage.py shell -c "from myaccount import __init__"

# Start the Django application
exec "$@"
