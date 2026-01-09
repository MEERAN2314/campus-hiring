# HireWave - Makefile

.PHONY: help setup install run celery docker-up docker-down clean test

help:
	@echo "HireWave - Available Commands"
	@echo "============================================"
	@echo "make setup       - Initial setup (create dirs, .env, install deps)"
	@echo "make install     - Install dependencies"
	@echo "make run         - Run the FastAPI application"
	@echo "make celery      - Run Celery worker"
	@echo "make docker-up   - Start with Docker Compose"
	@echo "make docker-down - Stop Docker containers"
	@echo "make clean       - Clean temporary files"
	@echo "make test        - Run tests"

setup:
	@echo "Setting up project..."
	@python3 setup.py

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

run:
	@echo "Starting FastAPI server..."
	@uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

celery:
	@echo "Starting Celery worker..."
	@celery -A app.celery_worker worker --loglevel=info

docker-up:
	@echo "Starting with Docker Compose..."
	@docker-compose up --build

docker-down:
	@echo "Stopping Docker containers..."
	@docker-compose down

clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.log" -delete
	@rm -rf .pytest_cache
	@rm -rf htmlcov
	@rm -rf .coverage
	@echo "✓ Cleaned"

test:
	@echo "Running tests..."
	@pytest tests/ -v
