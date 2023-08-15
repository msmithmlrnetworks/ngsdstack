#!/bin/bash

# Feedback to the user
echo "Starting your_service_name from docker-compose-first-start.yml..."

# Start a specific service from the first docker-compose file
docker-compose -f docker-compose-first-start.yml up -d checkmk

# Feedback to the user
echo "Waiting for 60 seconds..."
sleep 60

# Stop the specific service
echo "Stopping checkMk..."
docker-compose -f docker-compose-first-start.yml down

# Start services using the second docker-compose file
echo "Starting all services from docker-compose.yml..."
docker-compose -f docker-compose.yml up -d

# Final feedback and exit
echo "All services started. Exiting script."
exit 0
