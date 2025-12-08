from bson import ObjectId
from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[str]):
    username: str
    email: EmailStr

    @classmethod
    def model_validate(cls, obj):
        if hasattr(obj, "id") and isinstance(obj.id, ObjectId):
            obj.id = str(obj.id)
        return super().model_validate(obj)


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
