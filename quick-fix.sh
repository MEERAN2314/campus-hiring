#!/bin/bash

echo "🔧 Fixing HireWave bcrypt issue..."

# Stop containers
echo "📦 Stopping containers..."
docker-compose down

# Rebuild with no cache
echo "🏗️  Rebuilding containers..."
docker-compose build --no-cache

# Start containers
echo "🚀 Starting containers..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check status
echo "✅ Checking status..."
docker-compose ps

echo ""
echo "🎉 Done! Check the status above."
echo "📝 View logs with: docker-compose logs -f web"
echo "🌐 Access app at: http://localhost:8000"
