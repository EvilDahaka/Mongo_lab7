# users/schemas.py (Оновлений файл)
from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, EmailStr, Field  # ⬅️ Додаємо ConfigDict

from app.models.user import UserProfile, UserRole


class UserRead(schemas.BaseUser[str]):
    """Schema for reading user"""

    username: str
    role: UserRole
    profile: UserProfile
    created_at: datetime

    # ❗️ ВИПРАВЛЕННЯ ДЛЯ BEANIE
    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate):
    """Schema for registration"""

    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.READER
    full_name: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating profile"""

    username: Optional[str] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None

    # ❗️ ВИПРАВЛЕННЯ ДЛЯ BEANIE
    model_config = ConfigDict(from_attributes=True)
