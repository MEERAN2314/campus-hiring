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

# Ask which mode
echo "Choose seeding mode:"
echo "1) Interactive (asks for confirmation)"
echo "2) Force (clears all data immediately)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "2" ]; then
    echo ""
    echo "🚀 Running FORCE seed (will clear ALL data)..."
    echo ""
    python3 seed_force.py
else
    echo ""
    echo "🚀 Running interactive seed..."
    echo ""
    python3 seed_data.py
fi

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
