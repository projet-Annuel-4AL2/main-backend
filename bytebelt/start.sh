#!/usr/bin/env sh
#until python manage.py migrate; do 
#echo "Migrations failed, retrying in 3 seconds..."
#sleep 3
#done
#python manage.py loaddata dump_data.json 
daphne -b 0.0.0.0 -p 80 bytebelt.asgi:application
#python manage.py dumpdata  --exclude auth.permission --exclude contenttypes > dump_data.json
#python manage.py dumpdata --natural-primary --natural-foreign > dump_data.json
