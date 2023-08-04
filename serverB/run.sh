#!/usr/bin/env bash

gunicorn --workers 4 --bind 0.0.0.0:8889 -m 007 --log-level=debug wsgi:app
