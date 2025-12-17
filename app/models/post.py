from datetime import datetime
from typing import List, Optional

from beanie import Document, Indexed, Link
from pydantic import Field

from .category import Category


class Comment(Document):
    post_id: str
    author: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "comments"


class Post(Document):
    title: str = Indexed()
    content: str
    author_id: str
    author_name: str
    category: Optional[Link[Category]] = None
    tags: List[str] = Field(default_factory=list)
    published: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "posts"
