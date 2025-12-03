from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.post import Post


class PostCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=100)
    excerpt: str
    author_id: str
    category_id: str
    tags: List[str] = []
    featured_image: Optional[str] = None


class PostResponse(BaseModel):
    id: str
    title: str
    slug: str
    excerpt: str
    author_username: str
    category_name: str
    tags: List[str]
    featured_image: Optional[str]
    views: int
    likes: int
    comments_count: int
    created_at: datetime

    @classmethod
    def from_document(cls, post: "Post") -> "PostResponse":
        return cls(
            id=str(post.id),
            title=post.title,
            slug=post.slug,
            excerpt=post.excerpt,
            author_username=post.author.username,
            category_name=post.category.name,
            tags=post.tags,
            featured_image=post.featured_image,
            views=post.statistics.views,
            likes=post.statistics.likes,
            comments_count=post.statistics.comments_count,
            created_at=post.created_at,
        )
