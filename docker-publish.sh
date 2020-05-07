#!/bin/bash
#
# Build and publish the release images to docker hub registry
# Requires docker login to the repo to push the image
#

docker build \
   --compress \
   --file Dockerfile \
   --force-rm \
   --no-cache \
   --rm \
   --tag hackorama/hooks \
   .

docker push hackorama/hooks

docker build \
   --compress \
   --file consumer/Dockerfile \
   --force-rm \
   --no-cache \
   --rm \
   --tag hackorama/consumer \
   consumer

docker push hackorama/consumer
