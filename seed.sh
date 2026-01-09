#!/bin/bash

# HireWave - Quick Database Seeding Script

echo "🌱 HireWave Database Seeding"
echo "=============================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create .env file from .env.example"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    exit 1
fi

# Run the seed script
echo "🚀 Starting database seeding..."
echo ""
python3 seed_data.py

# Check if seeding was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Database seeding completed successfully!"
    echo ""
    echo "📖 For detailed information about test data, see:"
    echo "   TEST_DATA_REFERENCE.md"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Start the app: ./run.sh"
    echo "   2. Start Celery: ./run_celery.sh"
    echo "   3. Visit: http://localhost:8000"
else
    echo ""
    echo "❌ Database seeding failed!"
    echo "Please check the error messages above."
    exit 1
fi
