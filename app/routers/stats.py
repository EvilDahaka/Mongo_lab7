from fastapi import APIRouter
from app.models.post import Post
from typing import List, Dict

router = APIRouter(prefix="/api/stats", tags=["Statistics"])


@router.get("/top-authors")
async def get_top_authors(limit: int = 10) -> List[Dict]:
    pipeline = [
        {"$match": {"status": "published"}},
        {"$group": {
            "_id": "$author.user_id",
            "username": {"$first": "$author.username"},
            "posts_count": {"$sum": 1},
            "total_views": {"$sum": "$statistics.views"},
            "total_likes": {"$sum": "$statistics.likes"}
        }},
        {"$sort": {"posts_count": -1}},
        {"$limit": limit}
    ]
    result = await Post.aggregate(pipeline).to_list()
    return result


@router.get("/popular-categories")
async def get_popular_categories() -> List[Dict]:
    pipeline = [
        {"$match": {"status": "published"}},
        {"$group": {
            "_id": "$category.category_id",
            "category_name": {"$first": "$category.name"},
            "posts_count": {"$sum": 1},
            "total_views": {"$sum": "$statistics.views"},
            "avg_likes": {"$avg": "$statistics.likes"}
        }},
        {"$sort": {"posts_count": -1}}
    ]
    result = await Post.aggregate(pipeline).to_list()
    return result


@router.get("/comments-stats")
async def get_comments_stats() -> Dict:
    pipeline = [
        {"$match": {"status": "published"}},
        {"$group": {
            "_id": None,
            "total_posts": {"$sum": 1},
            "total_comments": {"$sum": "$statistics.comments_count"},
            "avg_comments_per_post": {"$avg": "$statistics.comments_count"},
            "max_comments": {"$max": "$statistics.comments_count"}
        }}
    ]
    result = await Post.aggregate(pipeline).to_list()
    return result[0] if result else {}


@router.get("/tags-distribution")
async def get_tags_distribution(limit: int = 10) -> List[Dict]:
    pipeline = [
        {"$match": {"status": "published"}},
        {"$unwind": "$tags"},
        {"$group": {
            "_id": "$tags",
            "count": {"$sum": 1},
            "avg_views": {"$avg": "$statistics.views"}
        }},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    result = await Post.aggregate(pipeline).to_list()
    return result
