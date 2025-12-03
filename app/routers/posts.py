from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth.user_manager import current_active_user
from app.models.post import Post
from app.models.user import User
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.schemas.post import PostCreateRequest, PostResponse
from app.services.post_service import PostService

router = APIRouter(prefix="/api/posts", tags=["Posts"])


@router.get("/", response_model=PaginatedResponse[PostResponse])
async def get_all_posts(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
):
    params = PaginationParams(page=page, page_size=page_size)
    result = await PostService.get_all_published(params)
    items = [PostResponse.from_document(post) for post in result.items]
    return PaginatedResponse(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        total_pages=result.total_pages,
    )


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    post = await PostService.get_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return PostResponse.from_document(post)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    data: PostCreateRequest, current_user: User = Depends(current_active_user)
):
    try:
        post = await PostService.create_post(data, current_user)
        return PostResponse.from_document(post)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/search/", response_model=PaginatedResponse[PostResponse])
async def search_posts(
    q: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    params = PaginationParams(page=page, page_size=page_size)
    result = await PostService.search_by_text(q, params)
    items = [PostResponse.from_document(post) for post in result.items]
    return PaginatedResponse(
        items=items,
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        total_pages=result.total_pages,
    )


@router.get("/category/{category_id}", response_model=List[PostResponse])
async def get_posts_by_category(category_id: str):
    posts = await PostService.get_by_category(category_id)
    return [PostResponse.from_document(post) for post in posts]


@router.get("/tag/{tag}", response_model=List[PostResponse])
async def get_posts_by_tag(tag: str):
    posts = await PostService.get_by_tag(tag)
    return [PostResponse.from_document(post) for post in posts]
