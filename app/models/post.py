from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
from bson import ObjectId


class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class AuthorEmbedded(BaseModel):
    user_id: str
    username: str
    avatar_url: Optional[str] = None


class CategoryEmbedded(BaseModel):
    category_id: str
    name: str


class CommentEmbedded(BaseModel):
    comment_id: str = Field(default_factory=lambda: str(ObjectId()))
    author: AuthorEmbedded
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "approved"
    likes: int = 0


class PostStatistics(BaseModel):
    views: int = 0
    likes: int = 0
    comments_count: int = 0


class Post(Document):
    title: str = Field(..., min_length=3, max_length=200)
    slug: Indexed(str, unique=True)
    content: str = Field(..., min_length=100)
    excerpt: str

    author: AuthorEmbedded
    category: CategoryEmbedded

    tags: List[str] = Field(default_factory=list)
    featured_image: Optional[str] = None

    status: PostStatus = PostStatus.PUBLISHED
    comments: List[CommentEmbedded] = Field(default_factory=list)
    statistics: PostStatistics = Field(default_factory=PostStatistics)

    created_at: Indexed(datetime) = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None

    class Settings:
        name = "posts"
        indexes = [
            "slug",
            "author.user_id",
            "category.category_id",
            [("status", 1), ("created_at", -1)],
            [("title", "text"), ("content", "text")]
        ]

    def add_comment(self, author: AuthorEmbedded, text: str) -> None:
        comment = CommentEmbedded(author=author, text=text)
        self.comments.append(comment)
        self.statistics.comments_count += 1

    def increment_views(self) -> None:
        self.statistics.views += 1

    def increment_likes(self) -> None:
        self.statistics.likes += 1
