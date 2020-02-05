#!/bin/sh

rm -f db.sqlite3
rm -r todo/migrations
python manage.py makemigrations todo
python manage.py migrate
python manage.py createsuperuser