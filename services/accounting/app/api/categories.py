"""
API роуты для управления категориями
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.auth import current_active_user
from app.models.users import User
from app.models.categories import Category, CategoryCreate, CategoryUpdate, CategoryRead

router = APIRouter()

@router.get("/", response_model=List[CategoryRead])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение списка категорий"""
    statement = select(Category).offset(skip).limit(limit)
    categories = db.exec(statement).all()
    return categories

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(
    category_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение категории по ID"""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.post("/", response_model=CategoryRead)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Создание новой категории"""
    category = Category(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Обновление категории"""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    for field, value in category_data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Удаление категории"""
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
