#!/bin/bash

echo "Waiting Database..."

while ! nc -z $db_host $db_port; do
    sleep 0.1
done

echo "Database started"

echo "Waiting Cache database..."

while ! nc -z $db_host $db_port; do
    sleep 0.1
done

echo "Cache database started"

cd app
gunicorn src.api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
