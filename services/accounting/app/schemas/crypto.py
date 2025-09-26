"""
Схемы для валидации криптовалютных данных
"""

from decimal import Decimal
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


class CryptoTransactionDetailRead(BaseModel):
    """Схема для чтения деталей криптовалютной транзакции"""
    transaction_id: int
    currency: str
    amount_crypto: Decimal
    rate_to_usd: Decimal
    tx_hash: Optional[str] = None
    wallet_from: Optional[str] = None
    wallet_to: Optional[str] = None
    fee: Optional[Decimal] = None
    block_number: Optional[int] = None
    confirmation_count: Optional[int] = None


class CryptoRatesResponse(BaseModel):
    """Схема для ответа с курсами криптовалют"""
    rates: dict[str, Decimal]
    base_currency: str
    updated_at: datetime


class TronTransactionInfo(BaseModel):
    """Информация о TRON транзакции"""
    hash: str
    success: bool
    block_number: Optional[int] = None
    timestamp: Optional[int] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    amount: Optional[int] = None
    fee: Optional[int] = None
    confirmations: Optional[bool] = None


class CryptoCurrencyInfo(BaseModel):
    """Информация о поддерживаемой криптовалюте"""
    code: str
    name: str
    network: str
    decimals: int
    type: str  # "native" или "token"
    contract_address: Optional[str] = None
    
    @validator('code')
    def validate_code(cls, v):
        if v not in ['TRX', 'USDT']:
            raise ValueError('Only TRX and USDT are supported')
        return v.upper()


class WalletValidationResponse(BaseModel):
    """Ответ валидации адреса кошелька"""
    valid: bool
    address: Optional[str] = None
    network: Optional[str] = None
    format: Optional[str] = None
    error: Optional[str] = None


class CryptoAccountSummary(BaseModel):
    """Сводка по криптовалютному счету"""
    account_name: str
    usd_balance: Decimal
    currencies: dict[str, dict]


class CryptoTransactionValidationResult(BaseModel):
    """Результат валидации криптовалютной транзакции"""
    valid: bool
    transaction_info: Optional[TronTransactionInfo] = None
    error: Optional[str] = None
