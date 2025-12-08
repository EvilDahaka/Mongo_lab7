from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from beanie.operators import In, RegEx

from app.models.category import Category
from app.models.post import Post
from app.schemas.pagination import PaginatedResponse
from app.schemas.post import PostCreate, PostResponse, PostUpdate


class PostService:
    @staticmethod
    async def create_post(
        post_data: PostCreate, author_id: str, author_name: str
    ) -> Post:
        post_dict = post_data.model_dump()
        category_id = post_dict.pop("category_id", None)

        post = Post(**post_dict, author_id=author_id, author_name=author_name)

        if category_id:
            category = await Category.get(category_id)
            if category:
                post.category = category

        await post.insert()
        return post

    @staticmethod
    async def get_posts(
        page: int = 1, size: int = 10
    ) -> PaginatedResponse[PostResponse]:
        skip = (page - 1) * size
        posts = await Post.find(Post.published == True).skip(skip).limit(size).to_list()
        total = await Post.find(Post.published == True).count()

        items = []
        for post in posts:
            category_name = None
            if post.category:
                await post.category.fetch()
                category_name = post.category.name

            items.append(
                PostResponse(
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
            )

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size,
        )

    @staticmethod
    async def get_post(post_id: str) -> Optional[Post]:
        return await Post.get(post_id)

    @staticmethod
    async def update_post(post_id: str, post_data: PostUpdate) -> Optional[Post]:
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
        return post

    @staticmethod
    async def delete_post(post_id: str) -> bool:
        post = await Post.get(post_id)
        if not post:
            return False
        await post.delete()
        return True

    @staticmethod
    async def search_posts(
        query: str, page: int = 1, size: int = 10
    ) -> PaginatedResponse[PostResponse]:
        skip = (page - 1) * size
        posts = (
            await Post.find(Post.published == True, RegEx(Post.title, query, "i"))
            .skip(skip)
            .limit(size)
            .to_list()
        )

        total = await Post.find(
            Post.published == True, RegEx(Post.title, query, "i")
        ).count()

        items = []
        for post in posts:
            category_name = None
            if post.category:
                await post.category.fetch()
                category_name = post.category.name

            items.append(
                PostResponse(
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
            )

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size,
        )

    @staticmethod
    async def get_posts_by_category(category_id: str, page: int = 1, size: int = 10):
        category = await Category.get(category_id)
        if not category:
            return None

        skip = (page - 1) * size
        posts = (
            await Post.find(
                Post.published == True,
                Post.category.id == PydanticObjectId(category_id),
            )
            .skip(skip)
            .limit(size)
            .to_list()
        )

        total = await Post.find(
            Post.published == True, Post.category.id == PydanticObjectId(category_id)
        ).count()

        items = []
        for post in posts:
            items.append(
                PostResponse(
                    id=str(post.id),
                    title=post.title,
                    content=post.content,
                    author_id=post.author_id,
                    author_name=post.author_name,
                    category_name=category.name,
                    tags=post.tags,
                    published=post.published,
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                )
            )

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size,
        )

    @staticmethod
    async def get_posts_by_tag(tag: str, page: int = 1, size: int = 10):
        skip = (page - 1) * size
        posts = (
            await Post.find(Post.published == True, In(tag, Post.tags))
            .skip(skip)
            .limit(size)
            .to_list()
        )

        total = await Post.find(Post.published == True, In(tag, Post.tags)).count()

        items = []
        for post in posts:
            category_name = None
            if post.category:
                await post.category.fetch()
                category_name = post.category.name

            items.append(
                PostResponse(
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
            )

        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size,
        )
