"""
Модели для пользователей и аутентификации
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel


class User(BaseModel, table=True):
    """Модель пользователя"""
    
    __tablename__ = "users"
    
    # Основные поля пользователя
    email: str = Field(unique=True, index=True, max_length=255, description="Email")
    hashed_password: str = Field(max_length=255, description="Хешированный пароль")
    is_active: bool = Field(default=True, description="Активен ли пользователь")
    is_superuser: bool = Field(default=False, description="Суперпользователь")
    
    # Дополнительные поля пользователя
    first_name: Optional[str] = Field(default=None, max_length=255, description="Имя")
    last_name: Optional[str] = Field(default=None, max_length=255, description="Фамилия")
    phone: Optional[str] = Field(default=None, max_length=50, description="Телефон")
    is_verified: bool = Field(default=False, description="Подтвержден ли email")
    
    # Связи
    # transactions: List["Transaction"] = Relationship(back_populates="user")


class UserCreate(SQLModel):
    """Схема для создания пользователя"""
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserUpdate(SQLModel):
    """Схема для обновления пользователя"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserRead(SQLModel):
    """Схема для чтения пользователя"""
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    is_verified: bool
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]
