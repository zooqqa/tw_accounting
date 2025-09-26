"""
Модели для счетов
"""

from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel


class AccountType(str, Enum):
    """Типы счетов"""
    BANK = "bank"
    CRYPTO = "crypto"
    CASH = "cash"
    INVESTMENT = "investment"


class Account(BaseModel, table=True):
    """Модель счета"""
    
    __tablename__ = "accounts"
    
    name: str = Field(max_length=255, description="Название счета")
    type: AccountType = Field(description="Тип счета")
    currency: str = Field(max_length=10, default="USD", description="Валюта счета")
    balance: Decimal = Field(default=Decimal("0.00"), description="Текущий баланс")
    description: Optional[str] = Field(default=None, description="Описание счета")
    is_active: bool = Field(default=True, description="Активен ли счет")
    
    # Связи (временно отключены)
    # transaction_entries: List["TransactionEntry"] = Relationship(back_populates="account")


class AccountCreate(SQLModel):
    """Схема для создания счета"""
    name: str
    type: AccountType
    currency: str = "USD"
    description: Optional[str] = None


class AccountUpdate(SQLModel):
    """Схема для обновления счета"""
    name: Optional[str] = None
    type: Optional[AccountType] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class AccountRead(SQLModel):
    """Схема для чтения счета"""
    id: int
    name: str
    type: AccountType
    currency: str
    balance: Decimal
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
