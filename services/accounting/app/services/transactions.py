"""
Сервис для работы с транзакциями
"""

from decimal import Decimal
from datetime import datetime
from typing import List, Optional, Tuple
from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.models.transactions import (
    Transaction, TransactionEntry, TransactionType, TransactionStatus,
    TransactionCreate, CryptoTransactionDetail
)
from app.models.accounts import Account
from app.models.projects import Project
from app.models.categories import Category
from app.models.counterparties import Counterparty


class TransactionService:
    """Сервис для работы с транзакциями и двойной записью"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_transaction(
        self, 
        transaction_data: TransactionCreate,
        entries: List[Tuple[int, Decimal, str]]  # (account_id, amount, direction)
    ) -> Transaction:
        """
        Создание транзакции с проводками
        
        Args:
            transaction_data: Данные транзакции
            entries: Список проводок (account_id, amount, direction)
                    direction: 'DEBIT' или 'CREDIT'
        
        Returns:
            Созданная транзакция
        """
        # Проверяем принцип двойной записи
        self._validate_double_entry(entries)
        
        # Проверяем существование связанных объектов
        self._validate_related_objects(transaction_data)
        
        # Создаем транзакцию
        transaction = Transaction(
            description=transaction_data.description,
            type=transaction_data.type,
            status=TransactionStatus.PENDING,
            amount=transaction_data.amount,
            date=transaction_data.date or datetime.utcnow(),
            project_id=transaction_data.project_id,
            category_id=transaction_data.category_id,
            counterparty_id=transaction_data.counterparty_id
        )
        
        self.db.add(transaction)
        self.db.flush()  # Получаем ID транзакции
        
        # Создаем проводки
        total_debit = Decimal('0')
        total_credit = Decimal('0')
        
        for account_id, amount, direction in entries:
            # Проверяем существование счета
            account = self.db.get(Account, account_id)
            if not account:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Account {account_id} not found"
                )
            
            # Создаем проводку
            entry = TransactionEntry(
                transaction_id=transaction.id,
                account_id=account_id,
                amount=amount,
                direction=direction,
                description=f"{direction} - {transaction.description}"
            )
            
            self.db.add(entry)
            
            # Подсчитываем итоги
            if direction == 'DEBIT':
                total_debit += amount
            else:
                total_credit += amount
        
        # Финальная проверка баланса
        if total_debit != total_credit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transaction not balanced: debit {total_debit} != credit {total_credit}"
            )
        
        # Обновляем статус транзакции
        transaction.status = TransactionStatus.COMPLETED
        
        # Обновляем балансы счетов
        self._update_account_balances(entries)
        
        self.db.commit()
        self.db.refresh(transaction)
        
        return transaction
    
    def create_income_transaction(
        self,
        amount: Decimal,
        description: str,
        income_account_id: int,
        bank_account_id: int,
        project_id: Optional[int] = None,
        category_id: Optional[int] = None,
        counterparty_id: Optional[int] = None,
        date: Optional[datetime] = None
    ) -> Transaction:
        """Создание транзакции прихода денег"""
        
        transaction_data = TransactionCreate(
            description=description,
            type=TransactionType.INCOME,
            amount=amount,
            date=date,
            project_id=project_id,
            category_id=category_id,
            counterparty_id=counterparty_id
        )
        
        # Проводки: Дебет банковского счета, Кредит счета доходов
        entries = [
            (bank_account_id, amount, 'DEBIT'),    # Увеличиваем денежный счет
            (income_account_id, amount, 'CREDIT')  # Увеличиваем доходы
        ]
        
        return self.create_transaction(transaction_data, entries)
    
    def create_expense_transaction(
        self,
        amount: Decimal,
        description: str,
        expense_account_id: int,
        bank_account_id: int,
        project_id: Optional[int] = None,
        category_id: Optional[int] = None,
        counterparty_id: Optional[int] = None,
        date: Optional[datetime] = None
    ) -> Transaction:
        """Создание транзакции расхода денег"""
        
        transaction_data = TransactionCreate(
            description=description,
            type=TransactionType.EXPENSE,
            amount=amount,
            date=date,
            project_id=project_id,
            category_id=category_id,
            counterparty_id=counterparty_id
        )
        
        # Проводки: Дебет счета расходов, Кредит банковского счета
        entries = [
            (expense_account_id, amount, 'DEBIT'),  # Увеличиваем расходы
            (bank_account_id, amount, 'CREDIT')     # Уменьшаем денежный счет
        ]
        
        return self.create_transaction(transaction_data, entries)
    
    def create_transfer_transaction(
        self,
        amount: Decimal,
        description: str,
        from_account_id: int,
        to_account_id: int,
        project_id: Optional[int] = None,
        date: Optional[datetime] = None
    ) -> Transaction:
        """Создание транзакции перевода между счетами"""
        
        transaction_data = TransactionCreate(
            description=description,
            type=TransactionType.TRANSFER,
            amount=amount,
            date=date,
            project_id=project_id
        )
        
        # Проводки: Дебет счета-получателя, Кредит счета-отправителя
        entries = [
            (to_account_id, amount, 'DEBIT'),    # Увеличиваем счет-получатель
            (from_account_id, amount, 'CREDIT')  # Уменьшаем счет-отправитель
        ]
        
        return self.create_transaction(transaction_data, entries)
    
    def get_transaction_with_entries(self, transaction_id: int) -> Optional[Transaction]:
        """Получение транзакции с проводками"""
        statement = select(Transaction).where(Transaction.id == transaction_id)
        transaction = self.db.exec(statement).first()
        
        if transaction:
            # Получаем проводки
            entries_statement = select(TransactionEntry).where(
                TransactionEntry.transaction_id == transaction_id
            )
            entries = self.db.exec(entries_statement).all()
            # Добавляем проводки к транзакции (временно для возврата)
            transaction.entries_list = entries
        
        return transaction
    
    def get_account_balance(self, account_id: int) -> Decimal:
        """Получение текущего баланса счета"""
        account = self.db.get(Account, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Account {account_id} not found"
            )
        return account.balance
    
    def _validate_double_entry(self, entries: List[Tuple[int, Decimal, str]]):
        """Проверка принципа двойной записи"""
        if len(entries) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transaction must have at least 2 entries"
            )
        
        total_debit = sum(amount for _, amount, direction in entries if direction == 'DEBIT')
        total_credit = sum(amount for _, amount, direction in entries if direction == 'CREDIT')
        
        if total_debit != total_credit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Transaction not balanced: debit {total_debit} != credit {total_credit}"
            )
    
    def _validate_related_objects(self, transaction_data: TransactionCreate):
        """Проверка существования связанных объектов"""
        if transaction_data.project_id:
            project = self.db.get(Project, transaction_data.project_id)
            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Project {transaction_data.project_id} not found"
                )
        
        if transaction_data.category_id:
            category = self.db.get(Category, transaction_data.category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category {transaction_data.category_id} not found"
                )
        
        if transaction_data.counterparty_id:
            counterparty = self.db.get(Counterparty, transaction_data.counterparty_id)
            if not counterparty:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Counterparty {transaction_data.counterparty_id} not found"
                )
    
    def _update_account_balances(self, entries: List[Tuple[int, Decimal, str]]):
        """Обновление балансов счетов"""
        for account_id, amount, direction in entries:
            account = self.db.get(Account, account_id)
            if account:
                if direction == 'DEBIT':
                    account.balance += amount
                else:  # CREDIT
                    account.balance -= amount
                
                self.db.add(account)
