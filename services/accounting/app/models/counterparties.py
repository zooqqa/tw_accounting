"""
Модели для контрагентов
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel


class CounterpartyType(str, Enum):
    """Типы контрагентов"""
    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    PARTNER = "partner"
    EMPLOYEE = "employee"
    OTHER = "other"


class Counterparty(BaseModel, table=True):
    """Модель контрагента"""
    
    __tablename__ = "counterparties"
    
    name: str = Field(max_length=255, description="Название контрагента")
    type: CounterpartyType = Field(description="Тип контрагента")
    email: Optional[str] = Field(default=None, max_length=255, description="Email")
    phone: Optional[str] = Field(default=None, max_length=50, description="Телефон")
    address: Optional[str] = Field(default=None, description="Адрес")
    tax_id: Optional[str] = Field(default=None, max_length=50, description="Налоговый номер")
    description: Optional[str] = Field(default=None, description="Описание")
    is_active: bool = Field(default=True, description="Активен ли контрагент")
    
    # Связи
    transactions: List["Transaction"] = Relationship(back_populates="counterparty")
    invoices: List["Invoice"] = Relationship(back_populates="counterparty")


class CounterpartyCreate(SQLModel):
    """Схема для создания контрагента"""
    name: str
    type: CounterpartyType
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    description: Optional[str] = None


class CounterpartyUpdate(SQLModel):
    """Схема для обновления контрагента"""
    name: Optional[str] = None
    type: Optional[CounterpartyType] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CounterpartyRead(SQLModel):
    """Схема для чтения контрагента"""
    id: int
    name: str
    type: CounterpartyType
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    tax_id: Optional[str]
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
