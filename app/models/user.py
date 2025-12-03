from datetime import datetime
from enum import Enum
from typing import Optional

from beanie import Document, Indexed
from fastapi_users.db import BeanieBaseUser
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """Ролі користувачів"""

    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"


class UserProfile(BaseModel):
    """Профіль користувача"""

    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = (
        "https://api.dicebear.com/7.x/avataaars/svg?seed=default"
    )
    website: Optional[str] = None


class UserStatistics(BaseModel):
    """Статистика користувача"""

    posts_count: int = 0
    comments_count: int = 0


class User(BeanieBaseUser, Document):
    """ODM модель користувача з FastAPI Users"""

    # FastAPI Users вимагає ці поля (вже є в BeanieBaseUser):
    # - email: EmailStr
    # - hashed_password: str
    # - is_active: bool
    # - is_superuser: bool
    # - is_verified: bool

    # Додаткові поля
    username: Indexed(str, unique=True) = Field(..., min_length=3, max_length=30)
    role: UserRole = UserRole.READER

    # Вбудовані дані
    profile: UserProfile = Field(default_factory=UserProfile)
    statistics: UserStatistics = Field(default_factory=UserStatistics)

    # Дати
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Settings:
        name = "users"
        # Email collation for fastapi_users_db_beanie compatibility
        email_collation = {"locale": "simple"}
