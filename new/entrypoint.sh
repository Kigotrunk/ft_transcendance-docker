#!/bin/sh

# Wait for PostgreSQL to be available
echo "Waiting for PostgreSQL to be available..."
while ! pg_isready -h "db" -p 5432 -U "postgres"; do
  sleep 1
done
echo "PostgreSQL is up!"

# Run Django migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate
python manage.py update_status
python manage.py shell -c "from myaccount import __init__"

echo "Creating Django superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('Tournoi info', 'tournoi@tournoi.com', 'tournoi')" | python manage.py shell

echo "Superuser created!"


# Start the Django application
exec "$@"
