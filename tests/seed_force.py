#!/usr/bin/env python3
"""
Force seed script - Clears ALL data and seeds without confirmation
USE WITH CAUTION!
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.utils.auth import get_password_hash
from datetime import datetime, timezone
import sys

# Helper function for timezone-aware datetime
def utc_now():
    """Get current UTC time as timezone-aware datetime"""
    return datetime.now(timezone.utc)

# Import sample data from seed_data
from seed_data import SAMPLE_RECRUITERS, SAMPLE_CANDIDATES, SAMPLE_JOBS


async def force_seed_database():
    """Force seed the database - NO CONFIRMATION"""
    
    print("=" * 60)
    print("HireWave - FORCE Database Seeding")
    print("=" * 60)
    print("\n⚠️  FORCE MODE: Clearing ALL data without confirmation!")
    
    # Connect to MongoDB
    print("\n📡 Connecting to MongoDB...")
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.MONGODB_DB_NAME]
        
        # Test connection
        await client.admin.command('ping')
        print("✓ Connected to MongoDB successfully")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        sys.exit(1)
    
    # Clear ALL existing data
    print("\n🗑️  Clearing ALL existing data...")
    try:
        collections_to_clear = ['users', 'jobs', 'assessments', 'applications', 'submissions', 'results']
        for collection in collections_to_clear:
            result = await db[collection].delete_many({})
            print(f"   ✓ Cleared {result.deleted_count} documents from {collection}")
        print("✓ All existing data cleared")
    except Exception as e:
        print(f"⚠️  Warning: {e}")
    
    # Insert recruiters
    print("\n👔 Inserting sample recruiters...")
    try:
        await db.users.insert_many(SAMPLE_RECRUITERS)
        print(f"✓ Inserted {len(SAMPLE_RECRUITERS)} recruiters")
    except Exception as e:
        print(f"✗ Failed to insert recruiters: {e}")
    
    # Insert candidates
    print("\n🎓 Inserting sample candidates...")
    try:
        await db.users.insert_many(SAMPLE_CANDIDATES)
        print(f"✓ Inserted {len(SAMPLE_CANDIDATES)} candidates")
    except Exception as e:
        print(f"✗ Failed to insert candidates: {e}")
    
    # Insert jobs
    print("\n💼 Inserting sample jobs...")
    try:
        await db.jobs.insert_many(SAMPLE_JOBS)
        print(f"✓ Inserted {len(SAMPLE_JOBS)} jobs")
    except Exception as e:
        print(f"✗ Failed to insert jobs: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Force seeding completed!")
    print("=" * 60)
    
    print("\n📊 Summary:")
    print(f"   Recruiters: {len(SAMPLE_RECRUITERS)}")
    print(f"   Candidates: {len(SAMPLE_CANDIDATES)}")
    print(f"   Jobs: {len(SAMPLE_JOBS)}")
    
    print("\n🔐 Test Credentials:")
    print("   All passwords: password123")
    print("\n   Recruiter: recruiter@techcorp.com")
    print("   Candidate: john.doe@university.edu")
    
    print("\n" + "=" * 60)
    
    # Close connection
    client.close()


if __name__ == "__main__":
    print("\n⚠️  WARNING: This will DELETE ALL DATA without asking!")
    print("Press Ctrl+C within 3 seconds to cancel...")
    
    import time
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🚀 Starting force seed...\n")
    asyncio.run(force_seed_database())
