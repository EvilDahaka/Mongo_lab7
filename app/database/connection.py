from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models.category import Category
from app.models.post import Comment, Post
from app.models.user import User

client = None


async def init_db():
    global client
    client = AsyncIOMotorClient(settings.mongodb_url)

    await init_beanie(
        database=client[settings.database_name],
        document_models=[User, Post, Comment, Category],
    )


async def close_db():
    global client
    if client:
        client.close()
