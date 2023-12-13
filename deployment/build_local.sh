#!/bin/bash -e

export REVISION_ID=$(git rev-parse HEAD)
export ARTICULON_ENV=production
export DOCKER_BUILDKIT=1

./api/build_local.sh &
./frontend/build_local.sh &
wait
