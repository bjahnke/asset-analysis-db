#!/bin/bash

echo "Starting Docker container..."

# Run the Docker container and show logs
docker run -p 4000:80 asset-analysis-db 2>&1 | tee run.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "Docker container started successfully."
else
    echo "Failed to start Docker container. Check run.log for details."
fi