from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str
    content: str
    category_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    published: bool = False


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[str] = None
    tags: Optional[List[str]] = None
    published: Optional[bool] = None


class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    author_name: str
    category_name: Optional[str] = None
    tags: List[str]
    published: bool
    created_at: datetime
    updated_at: datetime


class CategoryCreate(BaseModel):
    name: str
    description: str


class CategoryResponse(BaseModel):
    id: str
    name: str
    description: str


class CommentCreate(BaseModel):
    author: str
    content: str


class CommentResponse(BaseModel):
    id: str
    author: str
    content: str
    created_at: datetime
