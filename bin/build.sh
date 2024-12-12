#!/bin/bash

echo "Starting Docker image build..."

# Build the Docker image and show logs
docker-compose -f ./docker/docker-compose.yml build --no-cache 2>&1 | tee build.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "Docker image built successfully."
else
    echo "Failed to build Docker image. Check build.log for details."
fi