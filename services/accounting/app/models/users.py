"""
Модели для пользователей и аутентификации
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from fastapi_users.db import SQLModelBaseUser
from app.models.base import BaseModel


class User(SQLModelBaseUser, table=True):
    """Модель пользователя"""
    
    __tablename__ = "users"
    
    # Дополнительные поля пользователя
    first_name: Optional[str] = Field(default=None, max_length=255, description="Имя")
    last_name: Optional[str] = Field(default=None, max_length=255, description="Фамилия")
    phone: Optional[str] = Field(default=None, max_length=50, description="Телефон")
    is_verified: bool = Field(default=False, description="Подтвержден ли email")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
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
