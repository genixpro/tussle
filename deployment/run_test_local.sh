#!/bin/bash -e

export REVISION_ID=$(git rev-parse HEAD)
export TUSSLE_ENV=testing
export DOCKER_BUILDKIT=1

# First locally build the testing containers.
./testing/build_local.sh

GCP_APPLICATION_TOKEN=`cat ~/.config/gcloud/application_default_credentials.json`

echo "The GCP Token is $GCP_APPLICATION_TOKEN"

# Now set the GOOGLE_APPLICATION_CREDENTIALS env var to the key.json file
docker run --env GOOGLE_APPLICATION_CREDENTIALS="/tussle/key.json"  \
        --env TUSSLE_ENV="testing" \
        --env GCP_APPLICATION_TOKEN="$GCP_APPLICATION_TOKEN" \
        --env GOOGLE_CLOUD_PROJECT="tussle" \
        --env REVISION_ID="$REVISION_ID" \
         us-central1-docker.pkg.dev/tussle/tussle-testing/tussle-testing:$REVISION_ID

