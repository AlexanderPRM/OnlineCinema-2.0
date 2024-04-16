#!/bin/bash

echo "Waiting Main Database..."

while ! nc -z $db_host $db_port; do
    sleep 0.1
done

echo "Main Database started"

echo "Waiting Cache database..."

while ! nc -z $db_host $db_port; do
    sleep 0.1
done

echo "Cache database started"

cd app
gunicorn src.api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
