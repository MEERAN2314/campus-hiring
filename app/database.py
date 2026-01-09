from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None
    db = None


db = Database()


async def connect_to_mongo():
    """Connect to MongoDB"""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.db = db.client[settings.MONGODB_DB_NAME]
        
        # Test connection
        await db.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        # Create indexes
        await create_indexes()
        
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        db.client.close()
        logger.info("Closed MongoDB connection")


async def create_indexes():
    """Create database indexes for better performance"""
    try:
        # Users collection
        await db.db.users.create_index("email", unique=True)
        await db.db.users.create_index("user_type")
        
        # Jobs collection
        await db.db.jobs.create_index("company_id")
        await db.db.jobs.create_index("status")
        await db.db.jobs.create_index("created_at")
        
        # Assessments collection
        await db.db.assessments.create_index("job_id")
        
        # Applications collection
        await db.db.applications.create_index([("job_id", 1), ("candidate_id", 1)], unique=True)
        await db.db.applications.create_index("candidate_id")
        await db.db.applications.create_index("status")
        
        # Submissions collection
        await db.db.submissions.create_index("application_id")
        await db.db.submissions.create_index("candidate_id")
        
        # Results collection
        await db.db.results.create_index("submission_id", unique=True)
        await db.db.results.create_index("application_id")
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.warning(f"Error creating indexes: {e}")


def get_database():
    """Get database instance"""
    return db.db
