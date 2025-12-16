import logging
from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from beanie.operators import In
from bson import ObjectId

from app.models.category import Category
from app.models.post import Post
from app.schemas.pagination import PaginatedResponse
from app.schemas.post import PostCreate, PostResponse, PostUpdate


class PostService:

    @staticmethod
    async def _post_to_response(post: Post) -> PostResponse:
        category_name = None
        if post.category:
            try:
                category = await post.category.fetch()
                category_name = category.name
            except AttributeError:
                pass

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

    @staticmethod
    async def _paginate_query(
        query, page: int = 1, size: int = 10
    ) -> PaginatedResponse[PostResponse]:
        skip = (page - 1) * size
        posts = await query.skip(skip).limit(size).to_list()
        total = await query.count()
        items: List[PostResponse] = [
            await PostService._post_to_response(post) for post in posts
        ]
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size,
        )

    @staticmethod
    async def get_posts(
        page: int = 1, size: int = 10
    ) -> PaginatedResponse[PostResponse]:
        query = Post.find(Post.published == True)
        return await PostService._paginate_query(query, page, size)

    @staticmethod
    async def get_posts_by_category(
        category_id: str, page: int = 1, size: int = 10
    ) -> PaginatedResponse[PostResponse]:
        query = Post.find(
            Post.published == True, Post.category.id == ObjectId(category_id)
        )

        return await PostService._paginate_query(query, page, size)

    @staticmethod
    async def get_posts_by_tag(
        tag: str, page: int = 1, size: int = 10
    ) -> PaginatedResponse[PostResponse]:
        query = Post.find(Post.published == True, In(Post.tags, [tag]))
        return await PostService._paginate_query(query, page, size)

    @staticmethod
    async def search_posts(
        query_str: str, page: int = 1, size: int = 10
    ) -> PaginatedResponse[PostResponse]:
        query = Post.find(
            Post.published == True,
            {
                "$or": [
                    {"title": {"$regex": query_str, "$options": "i"}},
                    {"content": {"$regex": query_str, "$options": "i"}},
                ]
            },
        )
        return await PostService._paginate_query(query, page, size)

    @staticmethod
    async def get_post(post_id: str) -> Optional[PostResponse]:
        post = await Post.get(post_id)
        if not post:
            return None
        return await PostService._post_to_response(post)

    @staticmethod
    async def delete_post(post_id: str) -> bool:
        post = await Post.get(post_id)
        if not post:
            return False
        await post.delete()
        return True

    @staticmethod
    async def update_post(
        post_id: str, post_data: PostUpdate
    ) -> Optional[PostResponse]:
        post = await Post.get(post_id)
        if not post:
            return None

        update_dict = post_data.model_dump(exclude_unset=True)
        category_id = update_dict.pop("category_id", None)
        if category_id:
            category = await Category.get(category_id)
            if category:
                post.category = category

        for key, value in update_dict.items():
            setattr(post, key, value)

        post.updated_at = datetime.utcnow()
        await post.save()

        return await PostService._post_to_response(post)

    @staticmethod
    async def create_post(
        post_data: PostCreate, author_id: str, author_name: str
    ) -> PostResponse:
        post_dict = post_data.model_dump()
        category_id = post_dict.pop("category_id", None)
        post = Post(**post_dict, author_id=author_id, author_name=author_name)

        if category_id:
            category = await Category.get(category_id)
            if category:
                post.category = category

        await post.insert()
        return await PostService._post_to_response(post)
