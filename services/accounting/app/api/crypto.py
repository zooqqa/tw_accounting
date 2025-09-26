"""
API роуты для работы с криптовалютами
"""

from decimal import Decimal
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel

from app.core.database import get_session
from app.core.auth import current_active_user
from app.models.users import User
from app.models.transactions import TransactionRead, CryptoTransactionDetail
from app.services.crypto import CryptoService


# Схемы для криптовалютных операций
class CryptoIncomeCreate(BaseModel):
    """Схема для создания криптовалютной транзакции прихода"""
    amount_crypto: Decimal
    currency: str  # "TRX" или "USDT"
    description: str
    crypto_account_id: int
    usd_account_id: int
    tx_hash: Optional[str] = None
    wallet_from: Optional[str] = None
    wallet_to: Optional[str] = None
    project_id: Optional[int] = None
    category_id: Optional[int] = None
    counterparty_id: Optional[int] = None


class CryptoExpenseCreate(BaseModel):
    """Схема для создания криптовалютной транзакции расхода"""
    amount_crypto: Decimal
    currency: str  # "TRX" или "USDT"
    description: str
    crypto_account_id: int
    usd_account_id: int
    tx_hash: Optional[str] = None
    wallet_from: Optional[str] = None
    wallet_to: Optional[str] = None
    fee_crypto: Optional[Decimal] = None
    project_id: Optional[int] = None
    category_id: Optional[int] = None
    counterparty_id: Optional[int] = None


class TronTransactionValidation(BaseModel):
    """Схема для валидации TRON транзакции"""
    tx_hash: str


router = APIRouter()


@router.post("/income", response_model=TransactionRead)
async def create_crypto_income(
    transaction_data: CryptoIncomeCreate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Создание транзакции прихода криптовалюты"""
    service = CryptoService(db)
    
    transaction = await service.create_crypto_income_transaction(
        amount_crypto=transaction_data.amount_crypto,
        currency=transaction_data.currency,
        description=transaction_data.description,
        crypto_account_id=transaction_data.crypto_account_id,
        usd_account_id=transaction_data.usd_account_id,
        tx_hash=transaction_data.tx_hash,
        wallet_from=transaction_data.wallet_from,
        wallet_to=transaction_data.wallet_to,
        project_id=transaction_data.project_id,
        category_id=transaction_data.category_id,
        counterparty_id=transaction_data.counterparty_id
    )
    
    return transaction


@router.post("/expense", response_model=TransactionRead)
async def create_crypto_expense(
    transaction_data: CryptoExpenseCreate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Создание транзакции расхода криптовалюты"""
    service = CryptoService(db)
    
    transaction = await service.create_crypto_expense_transaction(
        amount_crypto=transaction_data.amount_crypto,
        currency=transaction_data.currency,
        description=transaction_data.description,
        crypto_account_id=transaction_data.crypto_account_id,
        usd_account_id=transaction_data.usd_account_id,
        tx_hash=transaction_data.tx_hash,
        wallet_from=transaction_data.wallet_from,
        wallet_to=transaction_data.wallet_to,
        fee_crypto=transaction_data.fee_crypto,
        project_id=transaction_data.project_id,
        category_id=transaction_data.category_id,
        counterparty_id=transaction_data.counterparty_id
    )
    
    return transaction


@router.get("/rates")
async def get_crypto_rates(
    user: User = Depends(current_active_user)
):
    """Получение текущих курсов криптовалют"""
    # Создаем временную сессию для получения курсов
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        service = CryptoService(db)
        rates = await service.update_crypto_rates()
        return {
            "rates": rates,
            "base_currency": "USD",
            "updated_at": "2025-09-26T17:20:00Z"  # В реальности - текущее время
        }
    finally:
        db.close()


@router.post("/validate-tron")
async def validate_tron_transaction(
    validation_data: TronTransactionValidation,
    user: User = Depends(current_active_user)
):
    """Валидация TRON транзакции"""
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        service = CryptoService(db)
        result = await service.validate_tron_transaction(validation_data.tx_hash)
        
        if result:
            return {
                "valid": True,
                "transaction_info": result
            }
        else:
            return {
                "valid": False,
                "error": "Transaction not found or not confirmed"
            }
    finally:
        db.close()


@router.get("/transactions/{transaction_id}/details")
def get_crypto_transaction_details(
    transaction_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение деталей криптовалютной транзакции"""
    service = CryptoService(db)
    details = service.get_crypto_transaction_details(transaction_id)
    
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crypto transaction details not found"
        )
    
    return {
        "transaction_id": details.transaction_id,
        "currency": details.currency,
        "amount_crypto": details.amount_crypto,
        "rate_to_usd": details.rate_to_usd,
        "tx_hash": details.tx_hash,
        "wallet_from": details.wallet_from,
        "wallet_to": details.wallet_to,
        "fee": details.fee,
        "block_number": details.block_number,
        "confirmation_count": details.confirmation_count
    }


@router.get("/accounts/{account_id}/summary")
def get_crypto_account_summary(
    account_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение сводки по криптовалютному счету"""
    service = CryptoService(db)
    summary = service.get_crypto_balance_summary(account_id)
    return summary


@router.get("/supported-currencies")
def get_supported_currencies(user: User = Depends(current_active_user)):
    """Получение списка поддерживаемых криптовалют"""
    return {
        "currencies": [
            {
                "code": "TRX",
                "name": "TRON",
                "network": "TRON",
                "decimals": 6,
                "type": "native"
            },
            {
                "code": "USDT",
                "name": "Tether USD",
                "network": "TRON (TRC20)",
                "decimals": 6,
                "type": "token",
                "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
            }
        ]
    }


@router.get("/wallet-validation/{address}")
async def validate_wallet_address(
    address: str,
    network: str = "tron",
    user: User = Depends(current_active_user)
):
    """Валидация адреса криптовалютного кошелька"""
    # Простая валидация TRON адреса (начинается с T, длина 34 символа)
    if network.lower() == "tron":
        if len(address) == 34 and address.startswith('T'):
            return {
                "valid": True,
                "address": address,
                "network": "TRON",
                "format": "base58"
            }
        else:
            return {
                "valid": False,
                "error": "Invalid TRON address format"
            }
    
    return {
        "valid": False,
        "error": f"Network {network} not supported"
    }
