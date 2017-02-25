#!/bin/bash -ex
chown -R cutepaste:cutepaste /data
python manage.py migrate
exec uwsgi --ini uwsgi.ini
