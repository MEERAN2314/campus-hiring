#!/bin/bash

# HireWave - Run Script

echo "Starting HireWave..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration:"
    echo "   - GOOGLE_API_KEY (Gemini API key)"
    echo "   - MONGODB_URL (MongoDB Atlas connection string)"
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
mkdir -p uploads static/css static/js templates

# Run the application
echo "Starting FastAPI server..."
echo "Access at: http://localhost:8000"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
