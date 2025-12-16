from collections import Counter

from fastapi import APIRouter

from app.models.post import Comment, Post

router = APIRouter()


@router.get("/stats/top-authors")
async def get_top_authors(limit: int = 10):
    posts = await Post.find_all().to_list()
    author_counts = Counter(post.author_name for post in posts)

    return [
        {"author": author, "post_count": count}
        for author, count in author_counts.most_common(limit)
    ]


@router.get("/stats/popular-categories")
async def get_popular_categories():
    posts = await Post.find_all().to_list()
    category_counts = {}

    for post in posts:
        if post.category:
            category = await post.category.fetch()
            category_counts[category.name] = category_counts.get(category.name, 0) + 1

    return [
        {"category": name, "post_count": count}
        for name, count in sorted(
            category_counts.items(), key=lambda x: x[1], reverse=True
        )
    ]


@router.get("/stats/comments-stats")
async def get_comments_stats():
    posts = await Post.find_all().to_list()
    comments = await Comment.find_all().to_list()

    post_comment_counts = Counter(c.post_id for c in comments)

    return {
        "total_comments": len(comments),
        "total_posts": len(posts),
        "average_comments_per_post": len(comments) / len(posts) if posts else 0,
        "posts_with_most_comments": [
            {"post_id": post_id, "comment_count": count}
            for post_id, count in post_comment_counts.most_common(10)
        ],
    }


@router.get("/stats/tags-distribution")
async def get_tags_distribution():
    posts = await Post.find_all().to_list()
    tag_counts = Counter()

    for post in posts:
        tag_counts.update(post.tags)

    return [{"tag": tag, "count": count} for tag, count in tag_counts.most_common(20)]
