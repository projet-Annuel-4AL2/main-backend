#!/usr/bin/env sh
until python manage.py migrate; do
echo "Migrations failed, retrying in 3 seconds..."
sleep 3
done
daphne -b 0.0.0.0 -p 8000 bytebelt.asgi:application