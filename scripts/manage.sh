#!/bin/bash

sudo su www-data -s /bin/bash -c "cd /srv/gtlive/gtlive && ../venv/bin/python ./manage.py $*"
