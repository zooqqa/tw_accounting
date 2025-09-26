"""
API роуты для управления транзакциями
"""

from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.auth import current_active_user
from app.models.users import User
from app.models.transactions import (
    Transaction, TransactionEntry, TransactionCreate, TransactionRead,
    TransactionType
)
from app.models.accounts import Account
from app.services.transactions import TransactionService
from pydantic import BaseModel


# Схемы для специализированных операций
class IncomeTransactionCreate(BaseModel):
    """Схема для создания транзакции прихода"""
    amount: Decimal
    description: str
    income_account_id: int
    bank_account_id: int
    project_id: Optional[int] = None
    category_id: Optional[int] = None
    counterparty_id: Optional[int] = None
    date: Optional[datetime] = None


class ExpenseTransactionCreate(BaseModel):
    """Схема для создания транзакции расхода"""
    amount: Decimal
    description: str
    expense_account_id: int
    bank_account_id: int
    project_id: Optional[int] = None
    category_id: Optional[int] = None
    counterparty_id: Optional[int] = None
    date: Optional[datetime] = None


class TransferTransactionCreate(BaseModel):
    """Схема для создания транзакции перевода"""
    amount: Decimal
    description: str
    from_account_id: int
    to_account_id: int
    project_id: Optional[int] = None
    date: Optional[datetime] = None


class TransactionEntryCreate(BaseModel):
    """Схема для создания проводки"""
    account_id: int
    amount: Decimal
    direction: str  # 'DEBIT' или 'CREDIT'


class ComplexTransactionCreate(BaseModel):
    """Схема для создания сложной транзакции с множественными проводками"""
    description: str
    type: TransactionType
    amount: Decimal
    entries: List[TransactionEntryCreate]
    project_id: Optional[int] = None
    category_id: Optional[int] = None
    counterparty_id: Optional[int] = None
    date: Optional[datetime] = None


router = APIRouter()


@router.get("/", response_model=List[TransactionRead])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    type: Optional[TransactionType] = None,
    project_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение списка транзакций"""
    statement = select(Transaction)
    
    if type:
        statement = statement.where(Transaction.type == type)
    if project_id:
        statement = statement.where(Transaction.project_id == project_id)
    if category_id:
        statement = statement.where(Transaction.category_id == category_id)
    
    statement = statement.offset(skip).limit(limit).order_by(Transaction.date.desc())
    transactions = db.exec(statement).all()
    return transactions


@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение транзакции по ID"""
    service = TransactionService(db)
    transaction = service.get_transaction_with_entries(transaction_id)
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction


@router.get("/{transaction_id}/entries", response_model=List[dict])
def get_transaction_entries(
    transaction_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение проводок транзакции"""
    # Проверяем существование транзакции
    transaction = db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Получаем проводки
    statement = select(TransactionEntry).where(TransactionEntry.transaction_id == transaction_id)
    entries = db.exec(statement).all()
    
    # Возвращаем проводки с информацией о счетах
    result = []
    for entry in entries:
        account = db.get(Account, entry.account_id)
        result.append({
            "id": entry.id,
            "account_id": entry.account_id,
            "account_name": account.name if account else "Unknown",
            "amount": entry.amount,
            "direction": entry.direction,
            "description": entry.description
        })
    
    return result


@router.post("/income", response_model=TransactionRead)
def create_income_transaction(
    transaction_data: IncomeTransactionCreate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Создание транзакции прихода денег"""
    service = TransactionService(db)
    
    transaction = service.create_income_transaction(
        amount=transaction_data.amount,
        description=transaction_data.description,
        income_account_id=transaction_data.income_account_id,
        bank_account_id=transaction_data.bank_account_id,
        project_id=transaction_data.project_id,
        category_id=transaction_data.category_id,
        counterparty_id=transaction_data.counterparty_id,
        date=transaction_data.date
    )
    
    return transaction


@router.post("/expense", response_model=TransactionRead)
def create_expense_transaction(
    transaction_data: ExpenseTransactionCreate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Создание транзакции расхода денег"""
    service = TransactionService(db)
    
    transaction = service.create_expense_transaction(
        amount=transaction_data.amount,
        description=transaction_data.description,
        expense_account_id=transaction_data.expense_account_id,
        bank_account_id=transaction_data.bank_account_id,
        project_id=transaction_data.project_id,
        category_id=transaction_data.category_id,
        counterparty_id=transaction_data.counterparty_id,
        date=transaction_data.date
    )
    
    return transaction


@router.post("/transfer", response_model=TransactionRead)
def create_transfer_transaction(
    transaction_data: TransferTransactionCreate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Создание транзакции перевода между счетами"""
    service = TransactionService(db)
    
    transaction = service.create_transfer_transaction(
        amount=transaction_data.amount,
        description=transaction_data.description,
        from_account_id=transaction_data.from_account_id,
        to_account_id=transaction_data.to_account_id,
        project_id=transaction_data.project_id,
        date=transaction_data.date
    )
    
    return transaction


@router.post("/complex", response_model=TransactionRead)
def create_complex_transaction(
    transaction_data: ComplexTransactionCreate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Создание сложной транзакции с множественными проводками"""
    service = TransactionService(db)
    
    # Преобразуем проводки в нужный формат
    entries = [
        (entry.account_id, entry.amount, entry.direction)
        for entry in transaction_data.entries
    ]
    
    transaction_create = TransactionCreate(
        description=transaction_data.description,
        type=transaction_data.type,
        amount=transaction_data.amount,
        project_id=transaction_data.project_id,
        category_id=transaction_data.category_id,
        counterparty_id=transaction_data.counterparty_id,
        date=transaction_data.date
    )
    
    transaction = service.create_transaction(transaction_create, entries)
    return transaction


@router.get("/accounts/{account_id}/balance")
def get_account_balance(
    account_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение текущего баланса счета"""
    service = TransactionService(db)
    balance = service.get_account_balance(account_id)
    
    return {
        "account_id": account_id,
        "balance": balance
    }


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Удаление транзакции (только в статусе DRAFT)"""
    transaction = db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    if transaction.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft transactions can be deleted"
        )
    
    # Удаляем связанные проводки
    entries_statement = select(TransactionEntry).where(
        TransactionEntry.transaction_id == transaction_id
    )
    entries = db.exec(entries_statement).all()
    
    for entry in entries:
        db.delete(entry)
    
    db.delete(transaction)
    db.commit()
    
    return {"message": "Transaction deleted successfully"}
