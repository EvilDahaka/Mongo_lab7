from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryStatistics(BaseModel):
    posts_count: int = 0


class Category(Document):
    name: Indexed(str, unique=True) = Field(..., min_length=2, max_length=50)
    slug: Indexed(str, unique=True)
    description: Optional[str] = None

    parent_id: Optional[str] = None

    statistics: CategoryStatistics = Field(default_factory=CategoryStatistics)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "categories"
