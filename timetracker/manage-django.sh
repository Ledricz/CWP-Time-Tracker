#!./bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py test employees
python manage.py loaddata default_users default_projects default_entries
python manage.py runserver 0.0.0.0:8000