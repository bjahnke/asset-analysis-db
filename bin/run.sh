#!/bin/bash

docker-compose -f docker/docker-compose.yml down -v
# Run the Docker container and show logs
docker-compose -f docker/docker-compose.yml up -d --force-recreate 2>&1 | tee run.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "Docker container started successfully."
else
    echo "Failed to start Docker container. Check run.log for details."
fi