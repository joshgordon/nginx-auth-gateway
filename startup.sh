#!/bin/sh

./manage.py collectstatic
./manage.py migrate

gunicorn auth_gateway.wsgi -b 0.0.0.0:8000
