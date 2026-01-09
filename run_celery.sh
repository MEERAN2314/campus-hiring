#!/bin/bash

# Campus Hiring Platform - Celery Worker Script

echo "Starting Celery Worker..."

# Activate virtual environment
source venv/bin/activate

# Run Celery worker
celery -A app.celery_worker worker --loglevel=info
