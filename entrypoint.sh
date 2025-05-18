#!/bin/sh

echo "Applying migrations..."
python manage.py migrate --noinput

# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Check the command passed to the container
if [ "$1" = "celery" ]; then
    echo "Starting Celery worker..."
    exec celery -A data_process.celery worker --loglevel=info --concurrency=2
elif [ "$1" = "web" ]; then
    echo "Starting Django development server..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Invalid command. Use 'celery' or 'web'"
    exit 1
fi
