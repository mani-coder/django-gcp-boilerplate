#!/usr/bin/env bash

set -e
stars=$(printf '%*s' 50 '')

export DOCKER_BUILDKIT=1

echo "y" | docker image prune -a --filter "until=12h"
docker compose down
echo "${stars// /*}"
docker compose up -d --build
echo "${stars// /*}"

docker compose logs --no-color -f -t > logs/docker.log &
