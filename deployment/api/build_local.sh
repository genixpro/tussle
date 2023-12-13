#!/bin/bash -e

export REVISION_ID=$(git rev-parse HEAD)
export ARTICULON_ENV=production
export DOCKER_BUILDKIT=1

# Build the docker image for API base
docker build -t api-base \
             -t us-central1-docker.pkg.dev/tussle/tussle-api/tussle-api-base:$REVISION_ID \
             -t us-central1-docker.pkg.dev/tussle/tussle-api/tussle-api-base:latest \
             -f api/base.Dockerfile \
             ..

docker push us-central1-docker.pkg.dev/tussle/tussle-api/tussle-api-base:$REVISION_ID &

# Build the docker image for API
docker build -t api \
             -t us-central1-docker.pkg.dev/tussle/tussle-api/tussle-api:$REVISION_ID \
             -t us-central1-docker.pkg.dev/tussle/tussle-api/tussle-api:latest \
             -f api/Dockerfile \
             --build-arg ARTICULON_ENV=$ARTICULON_ENV \
             --build-arg REVISION_ID=$REVISION_ID \
             ..

docker push us-central1-docker.pkg.dev/tussle/tussle-api/tussle-api:$REVISION_ID &

wait

docker push us-central1-docker.pkg.dev/tussle/tussle-api/tussle-api-base:latest
docker push us-central1-docker.pkg.dev/tussle/tussle-api/tussle-api:latest


