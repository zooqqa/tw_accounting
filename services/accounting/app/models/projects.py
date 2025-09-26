"""
Модели для проектов
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel


class ProjectStatus(str, Enum):
    """Статусы проектов"""
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class Project(BaseModel, table=True):
    """Модель проекта"""
    
    __tablename__ = "projects"
    
    name: str = Field(max_length=255, description="Название проекта")
    description: Optional[str] = Field(default=None, description="Описание проекта")
    status: ProjectStatus = Field(default=ProjectStatus.ACTIVE, description="Статус проекта")
    currency: str = Field(max_length=10, default="USD", description="Валюта проекта")
    start_date: Optional[datetime] = Field(default=None, description="Дата начала")
    end_date: Optional[datetime] = Field(default=None, description="Дата окончания")
    budget: Optional[float] = Field(default=None, description="Бюджет проекта")
    
    # Связи
    transactions: List["Transaction"] = Relationship(back_populates="project")


class ProjectCreate(SQLModel):
    """Схема для создания проекта"""
    name: str
    description: Optional[str] = None
    currency: str = "USD"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None


class ProjectUpdate(SQLModel):
    """Схема для обновления проекта"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    currency: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None


class ProjectRead(SQLModel):
    """Схема для чтения проекта"""
    id: int
    name: str
    description: Optional[str]
    status: ProjectStatus
    currency: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    budget: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]
