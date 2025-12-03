from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_beanie import BeanieUserDatabase

from app.config import settings
from app.models.user import User, UserProfile

SECRET = settings.secret_key


class UserManager(UUIDIDMixin, BaseUserManager[User, str]):
    """User manager for FastAPI Users"""

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"✅ User {user.username} has registered.")
        if not user.profile.avatar_url:
            user.profile = UserProfile(
                avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={user.username}"
            )
            await user.save()


async def get_user_db():
    yield BeanieUserDatabase(User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


# JWT Authentication
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=settings.jwt_lifetime_seconds)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI Users instance
fastapi_users = FastAPIUsers[User, str](
    get_user_manager,
    [auth_backend],
)

# Dependency for current active user
current_active_user = fastapi_users.current_user(active=True)
