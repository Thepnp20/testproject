from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models import Task, User, TaskLog


async def init_db():
    """Initialize database connection and Beanie models"""
    # Create motor client
    client = AsyncIOMotorClient(settings.mongodb_url)
    
    # Initialize Beanie with the Product document class
    await init_beanie(
        database=client[settings.database_name],
        document_models=[Task, User, TaskLog]
    )


async def close_db():
    """Close database connection"""
    # Motor client will be closed automatically when the application shuts down
    pass 