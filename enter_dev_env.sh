#!/bin/bash -xe
CONTAINER="app-dev"
PROJECT_NAME="pycontw_backend_dev"
COMPOSE_FILE="./docker-compose-dev.yml"
COMPOSE_CMD="docker compose -f $COMPOSE_FILE -p ${PROJECT_NAME}"

# test if the container is running
HASH=`docker ps -q -f name="${PROJECT_NAME}-${CONTAINER}-1"`

# test if the container is stopped
HASH_STOPPED=`docker ps -qa -f name="${PROJECT_NAME}-${CONTAINER}-1"`

if [[ $(uname -m) == 'arm64' ]]; then
  export DOCKER_DEFAULT_PLATFORM=linux/amd64
fi

if [ -n "$HASH" ];then
    echo "found existing running container $CONTAINER, proceeding to exec another shell"
    $COMPOSE_CMD exec -i $CONTAINER bash -c "SHELL=bash source /app/.venv/bin/activate && bash"
elif [ -n "$HASH_STOPPED" ];then
    echo "found existing stopped container $CONTAINER, starting"
    ($COMPOSE_CMD restart && docker start $HASH_STOPPED) >/dev/null 2>&1
    $COMPOSE_CMD exec -i $CONTAINER bash -c "SHELL=bash source /app/.venv/bin/activate && bash"
else
    echo "existing container not found, creating a new one, named $CONTAINER"
    $COMPOSE_CMD up --build --remove-orphans -d
    $COMPOSE_CMD exec -i $CONTAINER bash -c "SHELL=bash source /app/.venv/bin/activate && bash"
fi
echo "see you, use '$COMPOSE_CMD down' to kill both the postgres and the dev container if you want a fresh env next time"
