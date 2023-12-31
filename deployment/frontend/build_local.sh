#!/bin/bash -e

export REVISION_ID=$(git rev-parse HEAD)
export TUSSLE_ENV=production
export DOCKER_BUILDKIT=1


# Build the docker image for frontend
docker build -t frontend \
             -t us-central1-docker.pkg.dev/notional-clover-408014/tussle-frontend/tussle-frontend-base:$REVISION_ID \
             -t us-central1-docker.pkg.dev/notional-clover-408014/tussle-frontend/tussle-frontend-base:latest \
             -f frontend/base.Dockerfile \
             ..

docker push us-central1-docker.pkg.dev/notional-clover-408014/tussle-frontend/tussle-frontend-base:$REVISION_ID &

# Build the docker image for frontend
docker build -t frontend \
             -t us-central1-docker.pkg.dev/notional-clover-408014/tussle-frontend/tussle-frontend:$REVISION_ID \
             -t us-central1-docker.pkg.dev/notional-clover-408014/tussle-frontend/tussle-frontend:latest \
             -f frontend/Dockerfile \
             --build-arg TUSSLE_ENV=$TUSSLE_ENV \
             --build-arg REVISION_ID=$REVISION_ID \
             ..

docker push us-central1-docker.pkg.dev/notional-clover-408014/tussle-frontend/tussle-frontend:$REVISION_ID &

wait

docker push us-central1-docker.pkg.dev/notional-clover-408014/tussle-frontend/tussle-frontend-base:latest
docker push us-central1-docker.pkg.dev/notional-clover-408014/tussle-frontend/tussle-frontend:latest

