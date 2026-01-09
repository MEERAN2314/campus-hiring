#!/usr/bin/env python3
"""
Setup script for Campus Hiring Platform
"""

import os
import sys
import subprocess

def create_directories():
    """Create necessary directories"""
    directories = [
        'uploads',
        'static/css',
        'static/js',
        'templates',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✓ Created .env file from .env.example")
            print("⚠️  Please update .env with your configuration (especially GOOGLE_API_KEY)")
        else:
            print("✗ .env.example not found")
    else:
        print("✓ .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        sys.exit(1)

def main():
    """Main setup function"""
    print("=" * 50)
    print("Campus Hiring Platform - Setup")
    print("=" * 50)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Setting up environment file...")
    create_env_file()
    
    print("\n3. Installing dependencies...")
    install_dependencies()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Update .env with your configuration")
    print("2. Start MongoDB: mongod")
    print("3. Start Redis: redis-server")
    print("4. Run the app: ./run.sh")
    print("5. Run Celery worker (in another terminal): ./run_celery.sh")
    print("\nOr use Docker: docker-compose up --build")

if __name__ == '__main__':
    main()
