#!/bin/bash

# Campus Hiring Platform - Celery Worker Script

echo "Starting Celery Worker..."
echo "Make sure Redis is running: redis-server"

# Run Celery worker
celery -A app.celery_worker worker --loglevel=info
