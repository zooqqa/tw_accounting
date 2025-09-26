"""
Модели для транзакций
"""

from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import BaseModel


class TransactionType(str, Enum):
    """Типы транзакций"""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class TransactionStatus(str, Enum):
    """Статусы транзакций"""
    DRAFT = "draft"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Transaction(BaseModel, table=True):
    """Модель транзакции"""
    
    __tablename__ = "transactions"
    
    description: str = Field(max_length=500, description="Описание транзакции")
    type: TransactionType = Field(description="Тип транзакции")
    status: TransactionStatus = Field(default=TransactionStatus.COMPLETED, description="Статус транзакции")
    amount: Decimal = Field(description="Сумма транзакции")
    date: datetime = Field(description="Дата транзакции")
    
    # Внешние ключи
    project_id: Optional[int] = Field(default=None, foreign_key="projects.id", description="ID проекта")
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id", description="ID категории")
    counterparty_id: Optional[int] = Field(default=None, foreign_key="counterparties.id", description="ID контрагента")
    
    # Связи (временно отключены)
    # project: Optional["Project"] = Relationship(back_populates="transactions")
    # category: Optional["Category"] = Relationship(back_populates="transactions")
    # counterparty: Optional["Counterparty"] = Relationship(back_populates="transactions")
    # entries: List["TransactionEntry"] = Relationship(back_populates="transaction")
    # crypto_details: Optional["CryptoTransactionDetail"] = Relationship(back_populates="transaction")


class TransactionEntry(BaseModel, table=True):
    """Модель проводки (двойная запись)"""
    
    __tablename__ = "transaction_entries"
    
    transaction_id: int = Field(foreign_key="transactions.id", description="ID транзакции")
    account_id: int = Field(foreign_key="accounts.id", description="ID счета")
    amount: Decimal = Field(description="Сумма проводки")
    direction: str = Field(max_length=10, description="Направление (DEBIT/CREDIT)")
    description: Optional[str] = Field(default=None, description="Описание проводки")
    
    # Связи (временно отключены)
    # transaction: Transaction = Relationship(back_populates="entries")
    # account: "Account" = Relationship(back_populates="transaction_entries")


class CryptoTransactionDetail(BaseModel, table=True):
    """Детали криптовалютной транзакции"""
    
    __tablename__ = "crypto_transaction_details"
    
    transaction_id: int = Field(foreign_key="transactions.id", description="ID транзакции")
    tx_hash: str = Field(max_length=255, description="Хеш транзакции")
    network: str = Field(max_length=50, description="Сеть (TRON, ETH, BTC)")
    wallet_from: Optional[str] = Field(default=None, max_length=255, description="Кошелек отправителя")
    wallet_to: Optional[str] = Field(default=None, max_length=255, description="Кошелек получателя")
    fee: Optional[Decimal] = Field(default=None, description="Комиссия")
    block_number: Optional[int] = Field(default=None, description="Номер блока")
    confirmation_count: Optional[int] = Field(default=None, description="Количество подтверждений")
    
    # Связи (временно отключены)
    # transaction: Transaction = Relationship(back_populates="crypto_details")


# Схемы для API
class TransactionCreate(SQLModel):
    """Схема для создания транзакции"""
    description: str
    type: TransactionType
    amount: Decimal
    date: datetime
    project_id: Optional[int] = None
    category_id: Optional[int] = None
    counterparty_id: Optional[int] = None


class TransactionUpdate(SQLModel):
    """Схема для обновления транзакции"""
    description: Optional[str] = None
    type: Optional[TransactionType] = None
    status: Optional[TransactionStatus] = None
    amount: Optional[Decimal] = None
    date: Optional[datetime] = None
    project_id: Optional[int] = None
    category_id: Optional[int] = None
    counterparty_id: Optional[int] = None


class TransactionRead(SQLModel):
    """Схема для чтения транзакции"""
    id: int
    description: str
    type: TransactionType
    status: TransactionStatus
    amount: Decimal
    date: datetime
    project_id: Optional[int]
    category_id: Optional[int]
    counterparty_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
