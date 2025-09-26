"""
Модели для категорий доходов/расходов
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel


class CategoryType(str, Enum):
    """Типы категорий"""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class Category(BaseModel, table=True):
    """Модель категории"""
    
    __tablename__ = "categories"
    
    name: str = Field(max_length=255, description="Название категории")
    type: CategoryType = Field(description="Тип категории")
    description: Optional[str] = Field(default=None, description="Описание категории")
    parent_id: Optional[int] = Field(default=None, foreign_key="categories.id", description="Родительская категория")
    is_active: bool = Field(default=True, description="Активна ли категория")
    color: Optional[str] = Field(default=None, max_length=7, description="Цвет категории (hex)")
    icon: Optional[str] = Field(default=None, max_length=50, description="Иконка категории")
    
    # Связи
    parent: Optional["Category"] = Relationship(back_populates="children", sa_relationship_kwargs={"remote_side": "Category.id"})
    children: List["Category"] = Relationship(back_populates="parent")
    transactions: List["Transaction"] = Relationship(back_populates="category")


class CategoryCreate(SQLModel):
    """Схема для создания категории"""
    name: str
    type: CategoryType
    description: Optional[str] = None
    parent_id: Optional[int] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class CategoryUpdate(SQLModel):
    """Схема для обновления категории"""
    name: Optional[str] = None
    type: Optional[CategoryType] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class CategoryRead(SQLModel):
    """Схема для чтения категории"""
    id: int
    name: str
    type: CategoryType
    description: Optional[str]
    parent_id: Optional[int]
    is_active: bool
    color: Optional[str]
    icon: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
