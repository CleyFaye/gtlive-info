#!/bin/bash

sudo su www-data -s /bin/bash -c "cd /srv/www/wsgi/gtlive.info/web && ../venv/bin/python ./manage.py $*"
