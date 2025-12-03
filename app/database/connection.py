from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# Import models so Beanie can register them
from app.models.user import User
from app.models.post import Post
from app.models.category import Category

async def init_db():
    """Initialize Beanie with motor client and register document models."""
    client = AsyncIOMotorClient(settings.mongodb_url)
    database = client[settings.mongodb_db_name]

    await init_beanie(
        database=database,
        document_models=[
            User,
            Post,
            Category
        ]
    )

    print("✅ Beanie initialized successfully")

    # Create indexes if models declare them
    try:
        await create_indexes()
    except Exception:
        # Non-fatal: indexes might be created automatically or require permissions
        pass


async def create_indexes():
    """Create indexes defined in models (best-effort)."""
    # The Beanie API for indexes varies; using model-level helpers when available.
    # Best-effort index creation; if models declare `Settings.indexes`, Beanie will handle them on init.
    try:
        await User.get_motor_collection().create_indexes([])
    except Exception:
        pass
    try:
        await Post.get_motor_collection().create_indexes([])
    except Exception:
        pass
    try:
        await Category.get_motor_collection().create_indexes([])
    except Exception:
        pass

    print("✅ Index setup attempted")
