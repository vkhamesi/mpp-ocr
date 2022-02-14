#!/bin/sh

nginx

python3.7 -m pipenv run uwsgi --ini app-docker.ini
