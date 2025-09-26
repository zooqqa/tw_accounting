"""
Модели для пользователей и аутентификации
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from app.models.base import BaseModel


class User(BaseModel, table=True):
    """Простая модель пользователя"""
    
    __tablename__ = "users"
    
    # Основные поля пользователя
    email: str = Field(unique=True, index=True, max_length=255, description="Email")
    hashed_password: str = Field(max_length=255, description="Хешированный пароль")
    is_active: bool = Field(default=True, description="Активен ли пользователь")
    is_superuser: bool = Field(default=False, description="Суперпользователь")
    is_verified: bool = Field(default=False, description="Подтвержден ли email")
    
    # Дополнительные поля пользователя
    first_name: Optional[str] = Field(default=None, max_length=255, description="Имя")
    last_name: Optional[str] = Field(default=None, max_length=255, description="Фамилия") 
    phone: Optional[str] = Field(default=None, max_length=50, description="Телефон")


class UserRead(SQLModel):
    """Схема для чтения пользователя"""
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    is_active: bool
    is_superuser: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]


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


class UserLogin(SQLModel):
    """Схема для входа пользователя"""
    email: str
    password: str


class Token(SQLModel):
    """Схема токена"""
    access_token: str
    token_type: str


class TokenData(SQLModel):
    """Данные токена"""
    email: Optional[str] = None
