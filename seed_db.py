import asyncio

from beanie import init_beanie
from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users_db_beanie import BeanieUserDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from app.auth.user_manager import UserManager
from app.config import settings
from app.models.user import User
from app.schemas.user import UserCreate


async def seed_users():
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]

    await init_beanie(db, document_models=[User])

    # ❗ створюємо БД і менеджер ВРУЧНУ
    user_db = BeanieUserDatabase(User)
    user_manager = UserManager(user_db)

    try:
        await user_manager.create(
            UserCreate(
                email="admin@example.com",
                password="admin123",
                username="admin",
                is_superuser=True,
                is_verified=True,
            )
        )
        print("✅ Admin created")
    except UserAlreadyExists:
        print("ℹ️ Admin already exists")


import asyncio
from datetime import datetime

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models.category import Category
from app.models.post import Comment, Post
from app.models.user import User

CATEGORIES = [
    {
        "name": "Tech",
        "description": "Технології та програмування",
    },
    {
        "name": "Life",
        "description": "Життя і побут",
    },
    {
        "name": "Science",
        "description": "Наука",
    },
]

POSTS = [
    {
        "title": "Асинхронність у Python",
        "content": "Async/await без болю.",
        "category": "Tech",
        "tags": ["python", "async"],
        "published": True,
    },
    {
        "title": "FastAPI без магії",
        "content": "Як воно реально працює.",
        "category": "Tech",
        "tags": ["fastapi"],
        "published": True,
    },
    {
        "title": "Трохи про життя",
        "content": "Думки вголос.",
        "category": "Life",
        "tags": ["life"],
        "published": False,
    },
]

COMMENTS = [
    {
        "author": "system",
        "content": "Корисний пост",
    },
    {
        "author": "guest",
        "content": "Дякую за пояснення",
    },
    {
        "author": "bot",
        "content": "Автокоментар",
    },
]


async def seed_content():
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]

    await init_beanie(
        database=db,
        document_models=[User, Category, Post, Comment],
    )

    # ---------- USER ----------
    admin = await User.find_one(User.email == "admin@example.com")
    if not admin:
        raise RuntimeError("Admin user not found. Run seed_users first.")

    # ---------- CATEGORIES ----------
    category_map: dict[str, Category] = {}

    for data in CATEGORIES:
        category = await Category.find_one(Category.name == data["name"])
        if not category:
            category = Category(**data)
            await category.insert()
        category_map[data["name"]] = category

    # ---------- POSTS ----------
    posts: list[Post] = []

    for data in POSTS:
        exists = await Post.find_one(Post.title == data["title"])
        if exists:
            posts.append(exists)
            continue

        post = Post(
            title=data["title"],
            content=data["content"],
            author_id=str(admin.id),
            author_name=admin.username,
            category=category_map.get(data["category"]),
            tags=data.get("tags", []),
            published=data.get("published", False),
            created_at=datetime.utcnow(),
        )
        await post.insert()
        posts.append(post)

    # ---------- COMMENTS ----------
    for post in posts:
        for data in COMMENTS:
            exists = await Comment.find_one(
                Comment.post_id == str(post.id),
                Comment.author == data["author"],
                Comment.content == data["content"],
            )
            if exists:
                continue

            await Comment(
                post_id=str(post.id),
                author=data["author"],
                content=data["content"],
            ).insert()

    print("✅ Mass content seed completed")


if __name__ == "__main__":
    asyncio.run(seed_users())
    asyncio.run(seed_content())
