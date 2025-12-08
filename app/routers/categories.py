from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.auth.user_manager import current_active_user
from app.models.category import Category
from app.models.user import User
from app.schemas.post import CategoryCreate, CategoryResponse

router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
async def list_categories():
    categories = await Category.find_all().to_list()
    return [
        CategoryResponse(id=str(c.id), name=c.name, description=c.description)
        for c in categories
    ]


@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: str):
    category = await Category.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return CategoryResponse(
        id=str(category.id), name=category.name, description=category.description
    )


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    category: CategoryCreate, user: User = Depends(current_active_user)
):
    # Check if category already exists
    existing = await Category.find_one(Category.name == category.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(name=category.name, description=category.description)
    await new_category.insert()

    return CategoryResponse(
        id=str(new_category.id),
        name=new_category.name,
        description=new_category.description,
    )
