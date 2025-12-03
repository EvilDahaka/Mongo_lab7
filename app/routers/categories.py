from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.category import Category

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("/", response_model=List[dict])
async def list_categories():
    cats = await Category.find_all().to_list()
    return [
        {"id": str(c.id), "name": c.name, "slug": c.slug, "posts_count": c.statistics.posts_count}
        for c in cats
    ]


@router.get("/{category_id}")
async def get_category(category_id: str):
    cat = await Category.get(category_id)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return {"id": str(cat.id), "name": cat.name, "slug": cat.slug, "description": cat.description}
