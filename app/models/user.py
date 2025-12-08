from typing import Optional

from beanie import Document
from fastapi_users.db import BeanieBaseUser
from pydantic import EmailStr


class User(BeanieBaseUser, Document):
    email: EmailStr
    username: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Settings:
        name = "users"
        email_collation = {"locale": "en", "strength": 2}
