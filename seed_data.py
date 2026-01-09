#!/usr/bin/env python3
"""
Seed script to populate database with sample data for testing
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.utils.auth import get_password_hash
from datetime import datetime
import sys

# Sample data
SAMPLE_RECRUITERS = [
    {
        "_id": "recruiter_001",
        "email": "recruiter@techcorp.com",
        "full_name": "Sarah Johnson",
        "user_type": "recruiter",
        "phone": "+1234567890",
        "hashed_password": get_password_hash("password123"),
        "company_name": "TechCorp Solutions",
        "skills": [],
        "profile_complete": True,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": "recruiter_002",
        "email": "hr@innovateai.com",
        "full_name": "Michael Chen",
        "user_type": "recruiter",
        "phone": "+1234567891",
        "hashed_password": get_password_hash("password123"),
        "company_name": "InnovateAI Labs",
        "skills": [],
        "profile_complete": True,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

SAMPLE_CANDIDATES = [
    {
        "_id": "candidate_001",
        "email": "john.doe@university.edu",
        "full_name": "John Doe",
        "user_type": "candidate",
        "phone": "+1234567892",
        "hashed_password": get_password_hash("password123"),
        "college_name": "MIT",
        "skills": ["Python", "JavaScript", "React", "Node.js", "MongoDB"],
        "profile_complete": True,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": "candidate_002",
        "email": "jane.smith@university.edu",
        "full_name": "Jane Smith",
        "user_type": "candidate",
        "phone": "+1234567893",
        "hashed_password": get_password_hash("password123"),
        "college_name": "Stanford University",
        "skills": ["Java", "Spring Boot", "MySQL", "AWS", "Docker"],
        "profile_complete": True,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": "candidate_003",
        "email": "alex.kumar@university.edu",
        "full_name": "Alex Kumar",
        "user_type": "candidate",
        "phone": "+1234567894",
        "hashed_password": get_password_hash("password123"),
        "college_name": "UC Berkeley",
        "skills": ["Python", "Machine Learning", "TensorFlow", "Data Science"],
        "profile_complete": True,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": "candidate_004",
        "email": "emily.brown@university.edu",
        "full_name": "Emily Brown",
        "user_type": "candidate",
        "phone": "+1234567895",
        "hashed_password": get_password_hash("password123"),
        "college_name": "Harvard University",
        "skills": ["React", "TypeScript", "GraphQL", "UI/UX Design"],
        "profile_complete": True,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": "candidate_005",
        "email": "david.lee@university.edu",
        "full_name": "David Lee",
        "user_type": "candidate",
        "phone": "+1234567896",
        "hashed_password": get_password_hash("password123"),
        "college_name": "Carnegie Mellon University",
        "skills": ["C++", "System Design", "Algorithms", "Distributed Systems"],
        "profile_complete": True,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

SAMPLE_JOBS = [
    {
        "_id": "job_001",
        "company_id": "recruiter_001",
        "company_name": "TechCorp Solutions",
        "title": "Full Stack Developer",
        "description": "We are looking for a talented Full Stack Developer to join our team. You will work on building scalable web applications using modern technologies.",
        "job_type": "technical",
        "required_skills": ["Python", "JavaScript", "React", "Node.js", "MongoDB"],
        "experience_level": "Fresher",
        "location": "San Francisco, CA (Remote)",
        "salary_range": "$80,000 - $100,000",
        "vacancies": 3,
        "target_colleges": ["MIT", "Stanford University", "UC Berkeley"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": "job_002",
        "company_id": "recruiter_002",
        "company_name": "InnovateAI Labs",
        "title": "Machine Learning Engineer",
        "description": "Join our AI team to build cutting-edge machine learning models. Work on real-world problems in computer vision and NLP.",
        "job_type": "technical",
        "required_skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "Data Science"],
        "experience_level": "Fresher",
        "location": "Boston, MA (Hybrid)",
        "salary_range": "$90,000 - $120,000",
        "vacancies": 2,
        "target_colleges": ["MIT", "Carnegie Mellon University", "Stanford University"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": "job_003",
        "company_id": "recruiter_001",
        "company_name": "TechCorp Solutions",
        "title": "Frontend Developer",
        "description": "Create beautiful and responsive user interfaces. Work with React, TypeScript, and modern CSS frameworks.",
        "job_type": "technical",
        "required_skills": ["React", "TypeScript", "JavaScript", "CSS", "HTML"],
        "experience_level": "Fresher",
        "location": "Remote",
        "salary_range": "$70,000 - $90,000",
        "vacancies": 2,
        "target_colleges": ["Harvard University", "UC Berkeley", "Stanford University"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": "job_004",
        "company_id": "recruiter_002",
        "company_name": "InnovateAI Labs",
        "title": "Backend Developer",
        "description": "Build robust and scalable backend systems. Work with microservices, databases, and cloud infrastructure.",
        "job_type": "technical",
        "required_skills": ["Java", "Spring Boot", "MySQL", "AWS", "Docker"],
        "experience_level": "Fresher",
        "location": "Seattle, WA (Remote)",
        "salary_range": "$85,000 - $105,000",
        "vacancies": 2,
        "target_colleges": ["MIT", "Carnegie Mellon University", "UC Berkeley"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "_id": "job_005",
        "company_id": "recruiter_001",
        "company_name": "TechCorp Solutions",
        "title": "Product Manager",
        "description": "Lead product development from ideation to launch. Work with cross-functional teams to deliver exceptional products.",
        "job_type": "non_technical",
        "required_skills": ["Product Management", "Agile", "Communication", "Strategy", "Analytics"],
        "experience_level": "Fresher",
        "location": "New York, NY (Hybrid)",
        "salary_range": "$75,000 - $95,000",
        "vacancies": 1,
        "target_colleges": ["Harvard University", "Stanford University", "MIT"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]


async def seed_database():
    """Seed the database with sample data"""
    
    print("=" * 60)
    print("HireWave - Database Seeding")
    print("=" * 60)
    
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
        print("\n⚠️  Make sure:")
        print("   1. MongoDB Atlas connection string is correct in .env")
        print("   2. Your IP is whitelisted in MongoDB Atlas")
        print("   3. Database user has proper permissions")
        sys.exit(1)
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    print("\n🗑️  Clearing existing sample data...")
    try:
        await db.users.delete_many({"_id": {"$regex": "^(recruiter_|candidate_)"}})
        await db.jobs.delete_many({"_id": {"$regex": "^job_"}})
        print("✓ Cleared existing sample data")
    except Exception as e:
        print(f"⚠️  Warning: {e}")
    
    # Insert recruiters
    print("\n👔 Inserting sample recruiters...")
    try:
        await db.users.insert_many(SAMPLE_RECRUITERS)
        print(f"✓ Inserted {len(SAMPLE_RECRUITERS)} recruiters")
        for recruiter in SAMPLE_RECRUITERS:
            print(f"   - {recruiter['full_name']} ({recruiter['email']}) - {recruiter['company_name']}")
    except Exception as e:
        print(f"✗ Failed to insert recruiters: {e}")
    
    # Insert candidates
    print("\n🎓 Inserting sample candidates...")
    try:
        await db.users.insert_many(SAMPLE_CANDIDATES)
        print(f"✓ Inserted {len(SAMPLE_CANDIDATES)} candidates")
        for candidate in SAMPLE_CANDIDATES:
            print(f"   - {candidate['full_name']} ({candidate['email']}) - {candidate['college_name']}")
    except Exception as e:
        print(f"✗ Failed to insert candidates: {e}")
    
    # Insert jobs
    print("\n💼 Inserting sample jobs...")
    try:
        await db.jobs.insert_many(SAMPLE_JOBS)
        print(f"✓ Inserted {len(SAMPLE_JOBS)} jobs")
        for job in SAMPLE_JOBS:
            print(f"   - {job['title']} at {job['company_name']} ({job['location']})")
    except Exception as e:
        print(f"✗ Failed to insert jobs: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Database seeding completed successfully!")
    print("=" * 60)
    
    print("\n📊 Summary:")
    print(f"   Recruiters: {len(SAMPLE_RECRUITERS)}")
    print(f"   Candidates: {len(SAMPLE_CANDIDATES)}")
    print(f"   Jobs: {len(SAMPLE_JOBS)}")
    
    print("\n🔐 Test Credentials:")
    print("\n   Recruiter Accounts:")
    print("   - Email: recruiter@techcorp.com")
    print("     Password: password123")
    print("     Company: TechCorp Solutions")
    print()
    print("   - Email: hr@innovateai.com")
    print("     Password: password123")
    print("     Company: InnovateAI Labs")
    
    print("\n   Candidate Accounts:")
    print("   - Email: john.doe@university.edu")
    print("     Password: password123")
    print("     College: MIT")
    print()
    print("   - Email: jane.smith@university.edu")
    print("     Password: password123")
    print("     College: Stanford University")
    print()
    print("   - Email: alex.kumar@university.edu")
    print("     Password: password123")
    print("     College: UC Berkeley")
    print()
    print("   - Email: emily.brown@university.edu")
    print("     Password: password123")
    print("     College: Harvard University")
    print()
    print("   - Email: david.lee@university.edu")
    print("     Password: password123")
    print("     College: Carnegie Mellon University")
    
    print("\n🚀 Next Steps:")
    print("   1. Start the application: ./run.sh")
    print("   2. Start Celery worker: ./run_celery.sh")
    print("   3. Visit: http://localhost:8000")
    print("   4. Login with any of the test accounts above")
    print("   5. Recruiters can create assessments for jobs")
    print("   6. Candidates can apply and take assessments")
    
    print("\n" + "=" * 60)
    
    # Close connection
    client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
