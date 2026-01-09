#!/usr/bin/env python3
"""
Seed script to populate database with sample data for testing
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
        "created_at": utc_now(),
        "updated_at": utc_now()
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
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "recruiter_003",
        "email": "talent@cloudnine.com",
        "full_name": "Priya Sharma",
        "user_type": "recruiter",
        "phone": "+1234567897",
        "hashed_password": get_password_hash("password123"),
        "company_name": "CloudNine Technologies",
        "skills": [],
        "profile_complete": True,
        "is_active": True,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "recruiter_004",
        "email": "hiring@datastream.io",
        "full_name": "Robert Martinez",
        "user_type": "recruiter",
        "phone": "+1234567898",
        "hashed_password": get_password_hash("password123"),
        "company_name": "DataStream Analytics",
        "skills": [],
        "profile_complete": True,
        "is_active": True,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "recruiter_005",
        "email": "careers@fintech.com",
        "full_name": "Lisa Anderson",
        "user_type": "recruiter",
        "phone": "+1234567899",
        "hashed_password": get_password_hash("password123"),
        "company_name": "FinTech Innovations",
        "skills": [],
        "profile_complete": True,
        "is_active": True,
        "created_at": utc_now(),
        "updated_at": utc_now()
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
        "created_at": utc_now(),
        "updated_at": utc_now()
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
        "created_at": utc_now(),
        "updated_at": utc_now()
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
        "created_at": utc_now(),
        "updated_at": utc_now()
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
        "created_at": utc_now(),
        "updated_at": utc_now()
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
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "candidate_006",
        "email": "sophia.garcia@university.edu",
        "full_name": "Sophia Garcia",
        "user_type": "candidate",
        "phone": "+1234567900",
        "hashed_password": get_password_hash("password123"),
        "college_name": "Georgia Tech",
        "skills": ["Python", "Django", "PostgreSQL", "REST APIs", "Git"],
        "profile_complete": True,
        "is_active": True,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "candidate_007",
        "email": "ryan.patel@university.edu",
        "full_name": "Ryan Patel",
        "user_type": "candidate",
        "phone": "+1234567901",
        "hashed_password": get_password_hash("password123"),
        "college_name": "University of Michigan",
        "skills": ["JavaScript", "Vue.js", "Node.js", "Express", "MongoDB"],
        "profile_complete": True,
        "is_active": True,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "candidate_008",
        "email": "olivia.wilson@university.edu",
        "full_name": "Olivia Wilson",
        "user_type": "candidate",
        "phone": "+1234567902",
        "hashed_password": get_password_hash("password123"),
        "college_name": "Cornell University",
        "skills": ["Data Analysis", "Python", "Pandas", "SQL", "Tableau"],
        "profile_complete": True,
        "is_active": True,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "candidate_009",
        "email": "ethan.rodriguez@university.edu",
        "full_name": "Ethan Rodriguez",
        "user_type": "candidate",
        "phone": "+1234567903",
        "hashed_password": get_password_hash("password123"),
        "college_name": "University of Texas",
        "skills": ["Cybersecurity", "Network Security", "Ethical Hacking", "Linux"],
        "profile_complete": True,
        "is_active": True,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "candidate_010",
        "email": "ava.thompson@university.edu",
        "full_name": "Ava Thompson",
        "user_type": "candidate",
        "phone": "+1234567904",
        "hashed_password": get_password_hash("password123"),
        "college_name": "University of Washington",
        "skills": ["Mobile Development", "React Native", "iOS", "Android", "Flutter"],
        "profile_complete": True,
        "is_active": True,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "candidate_011",
        "email": "noah.jackson@university.edu",
        "full_name": "Noah Jackson",
        "user_type": "candidate",
        "phone": "+1234567905",
        "hashed_password": get_password_hash("password123"),
        "college_name": "Duke University",
        "skills": ["DevOps", "Kubernetes", "Docker", "CI/CD", "Jenkins"],
        "profile_complete": True,
        "is_active": True,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "candidate_012",
        "email": "mia.white@university.edu",
        "full_name": "Mia White",
        "user_type": "candidate",
        "phone": "+1234567906",
        "hashed_password": get_password_hash("password123"),
        "college_name": "Northwestern University",
        "skills": ["Product Management", "Agile", "Scrum", "JIRA", "Analytics"],
        "profile_complete": True,
        "is_active": True,
        "created_at": utc_now(),
        "updated_at": utc_now()
    }
]

SAMPLE_JOBS = [
    {
        "_id": "job_001",
        "company_id": "recruiter_001",
        "company_name": "TechCorp Solutions",
        "title": "Full Stack Developer",
        "description": "We are looking for a talented Full Stack Developer to join our team. You will work on building scalable web applications using modern technologies. Experience with React, Node.js, and MongoDB is essential. You'll collaborate with cross-functional teams to deliver high-quality software solutions.",
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
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_002",
        "company_id": "recruiter_002",
        "company_name": "InnovateAI Labs",
        "title": "Machine Learning Engineer",
        "description": "Join our AI team to build cutting-edge machine learning models. Work on real-world problems in computer vision and NLP. You'll develop and deploy ML models at scale, optimize algorithms, and collaborate with data scientists to bring AI solutions to production.",
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
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_003",
        "company_id": "recruiter_001",
        "company_name": "TechCorp Solutions",
        "title": "Frontend Developer",
        "description": "Create beautiful and responsive user interfaces. Work with React, TypeScript, and modern CSS frameworks. You'll be responsible for implementing pixel-perfect designs, ensuring cross-browser compatibility, and optimizing web performance.",
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
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_004",
        "company_id": "recruiter_002",
        "company_name": "InnovateAI Labs",
        "title": "Backend Developer",
        "description": "Build robust and scalable backend systems. Work with microservices, databases, and cloud infrastructure. You'll design RESTful APIs, implement business logic, and ensure system reliability and performance.",
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
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_005",
        "company_id": "recruiter_001",
        "company_name": "TechCorp Solutions",
        "title": "Product Manager",
        "description": "Lead product development from ideation to launch. Work with cross-functional teams to deliver exceptional products. You'll define product roadmaps, gather user feedback, and make data-driven decisions to drive product success.",
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
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_006",
        "company_id": "recruiter_003",
        "company_name": "CloudNine Technologies",
        "title": "DevOps Engineer",
        "description": "Automate infrastructure and streamline deployment processes. Work with Kubernetes, Docker, and CI/CD pipelines. You'll manage cloud infrastructure, implement monitoring solutions, and ensure high availability of services.",
        "job_type": "technical",
        "required_skills": ["DevOps", "Kubernetes", "Docker", "CI/CD", "AWS"],
        "experience_level": "Fresher",
        "location": "Austin, TX (Remote)",
        "salary_range": "$85,000 - $110,000",
        "vacancies": 2,
        "target_colleges": ["Georgia Tech", "University of Michigan", "Duke University"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_007",
        "company_id": "recruiter_004",
        "company_name": "DataStream Analytics",
        "title": "Data Analyst",
        "description": "Transform data into actionable insights. Work with SQL, Python, and visualization tools like Tableau. You'll analyze large datasets, create dashboards, and present findings to stakeholders to drive business decisions.",
        "job_type": "technical",
        "required_skills": ["Data Analysis", "Python", "SQL", "Tableau", "Excel"],
        "experience_level": "Fresher",
        "location": "Chicago, IL (Hybrid)",
        "salary_range": "$65,000 - $85,000",
        "vacancies": 3,
        "target_colleges": ["Cornell University", "Northwestern University", "University of Michigan"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_008",
        "company_id": "recruiter_003",
        "company_name": "CloudNine Technologies",
        "title": "Mobile App Developer",
        "description": "Build native and cross-platform mobile applications. Work with React Native, iOS, and Android. You'll create intuitive mobile experiences, integrate with backend APIs, and ensure app performance across devices.",
        "job_type": "technical",
        "required_skills": ["React Native", "iOS", "Android", "JavaScript", "Mobile Development"],
        "experience_level": "Fresher",
        "location": "Los Angeles, CA (Remote)",
        "salary_range": "$75,000 - $95,000",
        "vacancies": 2,
        "target_colleges": ["University of Washington", "UC Berkeley", "Stanford University"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_009",
        "company_id": "recruiter_005",
        "company_name": "FinTech Innovations",
        "title": "Cybersecurity Analyst",
        "description": "Protect our systems and data from security threats. Work with security tools, conduct vulnerability assessments, and implement security best practices. You'll monitor networks, respond to incidents, and ensure compliance with security standards.",
        "job_type": "technical",
        "required_skills": ["Cybersecurity", "Network Security", "Ethical Hacking", "Linux", "Security Tools"],
        "experience_level": "Fresher",
        "location": "New York, NY (Hybrid)",
        "salary_range": "$80,000 - $100,000",
        "vacancies": 2,
        "target_colleges": ["University of Texas", "Carnegie Mellon University", "MIT"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_010",
        "company_id": "recruiter_004",
        "company_name": "DataStream Analytics",
        "title": "Business Analyst",
        "description": "Bridge the gap between business and technology. Gather requirements, analyze processes, and recommend solutions. You'll work with stakeholders to understand business needs and translate them into technical specifications.",
        "job_type": "non_technical",
        "required_skills": ["Business Analysis", "Requirements Gathering", "Communication", "Problem Solving", "Documentation"],
        "experience_level": "Fresher",
        "location": "Denver, CO (Hybrid)",
        "salary_range": "$70,000 - $90,000",
        "vacancies": 2,
        "target_colleges": ["Northwestern University", "Duke University", "Harvard University"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_011",
        "company_id": "recruiter_005",
        "company_name": "FinTech Innovations",
        "title": "UI/UX Designer",
        "description": "Design beautiful and intuitive user experiences. Work with Figma, conduct user research, and create wireframes and prototypes. You'll collaborate with developers to bring designs to life and ensure excellent user experience.",
        "job_type": "non_technical",
        "required_skills": ["UI/UX Design", "Figma", "User Research", "Prototyping", "Design Thinking"],
        "experience_level": "Fresher",
        "location": "San Francisco, CA (Remote)",
        "salary_range": "$70,000 - $90,000",
        "vacancies": 1,
        "target_colleges": ["Stanford University", "Harvard University", "UC Berkeley"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": utc_now(),
        "updated_at": utc_now()
    },
    {
        "_id": "job_012",
        "company_id": "recruiter_003",
        "company_name": "CloudNine Technologies",
        "title": "Quality Assurance Engineer",
        "description": "Ensure software quality through comprehensive testing. Write automated tests, perform manual testing, and identify bugs. You'll work closely with developers to maintain high code quality and deliver bug-free software.",
        "job_type": "technical",
        "required_skills": ["QA Testing", "Selenium", "Test Automation", "Manual Testing", "Bug Tracking"],
        "experience_level": "Fresher",
        "location": "Remote",
        "salary_range": "$65,000 - $85,000",
        "vacancies": 2,
        "target_colleges": ["Georgia Tech", "University of Michigan", "Cornell University"],
        "status": "active",
        "assessment_id": None,
        "applications_count": 0,
        "created_at": utc_now(),
        "updated_at": utc_now()
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
    print("   - Email: recruiter@techcorp.com | Password: password123 | Company: TechCorp Solutions")
    print("   - Email: hr@innovateai.com | Password: password123 | Company: InnovateAI Labs")
    print("   - Email: talent@cloudnine.com | Password: password123 | Company: CloudNine Technologies")
    print("   - Email: hiring@datastream.io | Password: password123 | Company: DataStream Analytics")
    print("   - Email: careers@fintech.com | Password: password123 | Company: FinTech Innovations")
    
    print("\n   Candidate Accounts (All passwords: password123):")
    print("   - john.doe@university.edu - MIT - Full Stack Skills")
    print("   - jane.smith@university.edu - Stanford - Backend/Cloud Skills")
    print("   - alex.kumar@university.edu - UC Berkeley - ML/AI Skills")
    print("   - emily.brown@university.edu - Harvard - Frontend/Design Skills")
    print("   - david.lee@university.edu - Carnegie Mellon - Systems Skills")
    print("   - sophia.garcia@university.edu - Georgia Tech - Python/Django Skills")
    print("   - ryan.patel@university.edu - University of Michigan - JavaScript/Vue Skills")
    print("   - olivia.wilson@university.edu - Cornell - Data Analysis Skills")
    print("   - ethan.rodriguez@university.edu - University of Texas - Cybersecurity Skills")
    print("   - ava.thompson@university.edu - University of Washington - Mobile Dev Skills")
    print("   - noah.jackson@university.edu - Duke - DevOps Skills")
    print("   - mia.white@university.edu - Northwestern - Product Management Skills")
    
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
