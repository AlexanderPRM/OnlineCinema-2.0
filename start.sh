#!/bin/bash

NETWORK_NAME="online-cinema"

format=$(getopt -n "$0" -o "" -l "type:" -- "$@")

if [[ $? -ne 0 ]]; then
    exit 2
fi

if [ $# -lt 1 ]; then
   echo "Not correct number of args."
   exit 2
fi


eval set -- "$format"

while [ $# -gt 0 ]
do
     case "$1" in
          --type) type="$2"; shift;;
     esac
     shift;
done


echo $type
if [ $type != "develop" ] && [ $type != "production" ]; then
    echo "Argument type must be develop or production"
    exit 2
fi

network_exists=$(docker network ls | grep $NETWORK_NAME | wc -l)

if [ $network_exists  -eq 0 ]; then
    echo "Creating Docker network: $NETWORK_NAME"
    docker network create $NETWORK_NAME
fi

if [ $type == "develop" ]; then
    run="NETWORK_NAME=$NETWORK_NAME docker-compose up --build -d"
else
    run="NETWORK_NAME=$NETWORK_NAME docker-compose -f docker.compose.prod.yaml --env-file .env.prod up --build -d"
fi

echo "Starting Auth Microservice"
cd auth && eval $run && cd ..
echo "Auth microservice started"

echo "Nginx starting..."
if [ $(docker ps -a -q -f name=online-cinema-develop-nginx) ]; then
    docker stop online-cinema-develop-nginx > /dev/null
    docker rm online-cinema-develop-nginx > /dev/null
fi

docker build -t online-cinema-develop-nginx .
docker run -p 80:80 --name online-cinema-develop-nginx --network $NETWORK_NAME -d online-cinema-develop-nginx
echo "Nginx started on port 80"
