import re
from datetime import datetime
from typing import List, Optional

from app.models.category import Category
from app.models.post import AuthorEmbedded, CategoryEmbedded, Post, PostStatus
from app.models.user import User
from app.schemas.pagination import PaginatedResponse, PaginationParams
from app.schemas.post import PostCreateRequest

TRANSLIT_MAP = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "h",
    "ґ": "g",
    "д": "d",
    "е": "e",
    "є": "ie",
    "ж": "zh",
    "з": "z",
    "и": "y",
    "і": "i",
    "ї": "i",
    "й": "i",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ь": "",
    "ю": "iu",
    "я": "ia",
}


class PostService:
    """Service for post business logic."""

    @staticmethod
    def generate_slug(title: str) -> str:
        """Generate URL-friendly slug with Ukrainian transliteration."""
        slug = title.lower()
        for uk, en in TRANSLIT_MAP.items():
            slug = slug.replace(uk, en)
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug[:100]

    @staticmethod
    async def create_post(data: PostCreateRequest, author: User) -> Post:
        """Create a new post. Author must be provided (authenticated user)."""
        if not author:
            raise ValueError("Author not provided")

        category = await Category.get(data.category_id)
        if not category:
            raise ValueError("Category not found")

        post = Post(
            title=data.title,
            slug=PostService.generate_slug(data.title),
            content=data.content,
            excerpt=data.excerpt,
            author=AuthorEmbedded(
                user_id=str(author.id),
                username=author.username,
                avatar_url=author.profile.avatar_url,
            ),
            category=CategoryEmbedded(category_id=str(category.id), name=category.name),
            tags=data.tags,
            featured_image=data.featured_image,
            status=PostStatus.PUBLISHED,
            published_at=datetime.utcnow(),
        )

        await post.insert()

        author.statistics.posts_count += 1
        await author.save()

        category.statistics.posts_count += 1
        await category.save()

        return post

    @staticmethod
    async def get_all_published(params: PaginationParams) -> PaginatedResponse[Post]:
        """Return published posts with pagination."""
        total = await Post.find(Post.status == PostStatus.PUBLISHED).count()
        posts = (
            await Post.find(Post.status == PostStatus.PUBLISHED)
            .sort(-Post.created_at)
            .skip(params.skip)
            .limit(params.limit)
            .to_list()
        )
        return PaginatedResponse.create(items=posts, total=total, params=params)

    @staticmethod
    async def get_by_id(post_id: str) -> Optional[Post]:
        post = await Post.get(post_id)
        if post:
            post.increment_views()
            await post.save()
        return post

    @staticmethod
    async def search_by_text(
        query: str, params: PaginationParams
    ) -> PaginatedResponse[Post]:
        search_filter = {"$text": {"$search": query}, "status": PostStatus.PUBLISHED}
        total = await Post.find(search_filter).count()
        posts = (
            await Post.find(search_filter)
            .skip(params.skip)
            .limit(params.limit)
            .to_list()
        )
        return PaginatedResponse.create(items=posts, total=total, params=params)

    @staticmethod
    async def get_by_category(category_id: str) -> List[Post]:
        return await Post.find(
            Post.category.category_id == category_id,
            Post.status == PostStatus.PUBLISHED,
        ).to_list()

    @staticmethod
    async def get_by_tag(tag: str) -> List[Post]:
        return await Post.find(
            Post.tags == tag, Post.status == PostStatus.PUBLISHED
        ).to_list()
