#!/bin/bash -xe
CONTAINER="pycontw"
COMPOSE_FILE="./docker-compose-dev.yml"

# test if the container is running
HASH=`docker ps -q -f name=$CONTAINER`

# test if the container is stopped
HASH_STOPPED=`docker ps -qa -f name=$CONTAINER`

if [[ $(uname -m) == 'arm64' ]]; then
  export DOCKER_DEFAULT_PLATFORM=linux/amd64
fi

if [ -n "$HASH" ];then
    echo "found existing running container $CONTAINER, proceeding to exec another shell"
    docker-compose -f $COMPOSE_FILE exec -i $CONTAINER bash -c "SHELL=bash source /app/.venv/bin/activate && bash"
elif [ -n "$HASH_STOPPED" ];then
    echo "found existing stopped container $CONTAINER, starting"
    (docker-compose -f $COMPOSE_FILE restart && docker start $HASH_STOPPED) >/dev/null 2>&1
    docker-compose -f $COMPOSE_FILE exec -i $CONTAINER bash -c "SHELL=bash source /app/.venv/bin/activate && bash"
else
    echo "existing container not found, creating a new one, named $CONTAINER"
    docker-compose -f $COMPOSE_FILE up --build --remove-orphans -d
    docker-compose -f $COMPOSE_FILE exec -i $CONTAINER bash -c "SHELL=bash source /app/.venv/bin/activate && bash"
fi
echo "see you, use 'docker rm $CONTAINER' to kill the dev container or 'docker-compose -f $COMPOSE_FILE down' to kill both the postgres and the dev container if you want a fresh env next time"
