#!/bin/bash

set -e

chown -R www-data:www-data /app/

cd /usr/src/

./manage.py collectstatic --no-input
./manage.py migrate --no-input

>&2 echo "Running site with uwsgi"
exec uwsgi --chdir /usr/src/ \
    --socket :8000 \
    --socket-timeout 1800 \
    --uid 33 \
    --gid 33 \
    --threads 5 \
    --processes 5 \
    --module app.wsgi:application \
    --harakiri 1800 \
    --master \
    --max-requests 5000 \
    --vacuum \
    --limit-post 0 \
    --post-buffering 16384 \
    --thunder-lock \
    --logto '/app/log/uwsgi.log' \
    --ignore-sigpipe \
    --ignore-write-errors \
    --disable-write-exception
