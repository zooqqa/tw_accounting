# Database models

from sqlmodel import SQLModel
from app.models.base import BaseModel, TimestampMixin
from app.models.users import User, UserCreate, UserUpdate, UserRead
from app.models.accounts import Account, AccountType, AccountCreate, AccountUpdate, AccountRead
from app.models.projects import Project, ProjectStatus, ProjectCreate, ProjectUpdate, ProjectRead
from app.models.categories import Category, CategoryType, CategoryCreate, CategoryUpdate, CategoryRead
from app.models.counterparties import Counterparty, CounterpartyType, CounterpartyCreate, CounterpartyUpdate, CounterpartyRead
from app.models.transactions import (
    Transaction, TransactionEntry, CryptoTransactionDetail,
    TransactionType, TransactionStatus,
    TransactionCreate, TransactionUpdate, TransactionRead
)

# Создание базовой таблицы для всех моделей
Base = SQLModel.metadata
