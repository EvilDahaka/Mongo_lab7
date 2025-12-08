from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth.user_manager import current_active_user
from app.models.post import Comment
from app.models.user import User
from app.schemas.pagination import PaginatedResponse
from app.schemas.post import (
    CommentCreate,
    CommentResponse,
    PostCreate,
    PostResponse,
    PostUpdate,
)
from app.services.post_service import PostService

router = APIRouter()


@router.get("/posts", response_model=PaginatedResponse[PostResponse])
async def list_posts(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):
    return await PostService.get_posts(page, size)


@router.get("/posts/search/", response_model=PaginatedResponse[PostResponse])
async def search_posts(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    return await PostService.search_posts(q, page, size)


@router.get(
    "/posts/category/{category_id}", response_model=PaginatedResponse[PostResponse]
)
async def get_posts_by_category(
    category_id: str, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)
):
    result = await PostService.get_posts_by_category(category_id, page, size)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return result


@router.get("/posts/tag/{tag}", response_model=PaginatedResponse[PostResponse])
async def get_posts_by_tag(
    tag: str, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)
):
    return await PostService.get_posts_by_tag(tag, page, size)


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    post = await PostService.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    category_name = None
    if post.category:
        await post.category.fetch()
        category_name = post.category.name

    return PostResponse(
        id=str(post.id),
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        author_name=post.author_name,
        category_name=category_name,
        tags=post.tags,
        published=post.published,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@router.post("/posts", response_model=PostResponse, status_code=201)
async def create_post(post: PostCreate, user: User = Depends(current_active_user)):
    new_post = await PostService.create_post(post, str(user.id), user.username)

    category_name = None
    if new_post.category:
        await new_post.category.fetch()
        category_name = new_post.category.name

    return PostResponse(
        id=str(new_post.id),
        title=new_post.title,
        content=new_post.content,
        author_id=new_post.author_id,
        author_name=new_post.author_name,
        category_name=category_name,
        tags=new_post.tags,
        published=new_post.published,
        created_at=new_post.created_at,
        updated_at=new_post.updated_at,
    )


@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str, post: PostUpdate, user: User = Depends(current_active_user)
):
    existing_post = await PostService.get_post(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if existing_post.author_id != str(user.id):
        raise HTTPException(status_code=403, detail="Not authorized")

    updated_post = await PostService.update_post(post_id, post)

    category_name = None
    if updated_post.category:
        await updated_post.category.fetch()
        category_name = updated_post.category.name

    return PostResponse(
        id=str(updated_post.id),
        title=updated_post.title,
        content=updated_post.content,
        author_id=updated_post.author_id,
        author_name=updated_post.author_name,
        category_name=category_name,
        tags=updated_post.tags,
        published=updated_post.published,
        created_at=updated_post.created_at,
        updated_at=updated_post.updated_at,
    )


@router.delete("/posts/{post_id}", status_code=204)
async def delete_post(post_id: str, user: User = Depends(current_active_user)):
    existing_post = await PostService.get_post(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if existing_post.author_id != str(user.id):
        raise HTTPException(status_code=403, detail="Not authorized")

    await PostService.delete_post(post_id)
    return None


@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_post_comments(post_id: str):
    comments = await Comment.find(Comment.post_id == post_id).to_list()
    return [
        CommentResponse(
            id=str(c.id), author=c.author, content=c.content, created_at=c.created_at
        )
        for c in comments
    ]


@router.post(
    "/posts/{post_id}/comments", response_model=CommentResponse, status_code=201
)
async def create_comment(post_id: str, comment: CommentCreate):
    post = await PostService.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        post_id=post_id, author=comment.author, content=comment.content
    )
    await new_comment.insert()

    return CommentResponse(
        id=str(new_comment.id),
        author=new_comment.author,
        content=new_comment.content,
        created_at=new_comment.created_at,
    )
