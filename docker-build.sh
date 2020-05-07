#!/bin/bash
#
# Build the local dev images
#

docker build \
   --file Dockerfile \
   --tag hooks \
   .

docker build \
   --file consumer/Dockerfile \
   --tag consumer \
   consumer
