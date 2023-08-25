#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py makemigrations authentication
python manage.py makemigrations deposits
python manage.py makemigrations plans
python manage.py makemigrations withdraw
python manage.py migrate